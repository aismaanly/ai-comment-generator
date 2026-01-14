from rich import print
import os
from openai import OpenAI
from datasets import Dataset, DatasetDict, load_dataset
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)
MODEL = "meta/llama-3.1-405b-instruct"

# 1. Subtopics Generation
n_subtopics = 3

TOPIC_GENERATION_PROMPT_TEMPLATE = """\
Saya ingin membuat dataset sintetis berupa instruksi dalam bahasa alami (Natural Language Instruction) dan respons berupa komentar media sosial. 
Berdasarkan konteks ini, berikan saya {n_subtopics} subtopik untuk mencakup berbagai jenis komentar yang bisa dibuat di media sosial.

List subtopik harus tanpa angka, dan tanpa deskripsi subtopik. Subtopik harus dipisahkan oleh koma. Tidak boleh ada teks lain selain daftar subtopik.
"""

def generate_subtopics(client, n_subtopics):
    prompt = TOPIC_GENERATION_PROMPT_TEMPLATE.format(n_subtopics=n_subtopics)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user",
             "content": prompt}
        ],
        temperature=0.2,
        top_p=0.7,
    )
    return response

responses = generate_subtopics(client, n_subtopics=n_subtopics)
print(responses.choices[0].message.content)


# 2. Instruction Generation
n_instructions = 400

INSTRUCTION_PROMPT_TEMPLATE = """\
Tujuan kita adalah membuat dataset instruksi dari pengguna dalam bahasa sehari-hari (natural language instruction) yang nantinya akan direspons oleh AI pembuat komentar media sosial.
Berdasarkan topik yang diberikan, hasilkan {n_instructions} instruksi singkat yang mungkin diberikan kepada asisten AI untuk membuat komentar. Instruksi ini harus menyertakan jenis postingan yang akan dikomentari.

Beberapa instruksi harus ditulis seolah-olah diberikan diberikan oleh seseorang dengan pengetahuan terbatas tentang media sosial atau cara berkomentar, seperti pengguna pemula atau awam. 

Topiknya adalah: {sub_topic}
List instruksi harus tanpa nomor. Setiap instruksi harus dipisahkan oleh karakter baris baru. Tidak boleh ada teks lain selain list instruksi tersebut.
"""
subtopic_list = responses.choices[0].message.content.split(",")
def generate_instructions(client, sub_topic, n_instructions):
    print(f"Generating Instructions for {sub_topic}.")
    prompt = INSTRUCTION_PROMPT_TEMPLATE.format(sub_topic=sub_topic, n_instructions=n_instructions)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user",
             "content": prompt}
        ],
        temperature=0.2,
        top_p=0.7,
    )
    return response.choices[0].message.content


def instructions_generator(client, subtopic_list, n_instructions):
    instruction_list = [generate_instructions(client, subtopic, n_instructions) for subtopic in subtopic_list]
    return instruction_list

instruction_list = instructions_generator(client, subtopic_list, n_instructions)

instruction_list_formatted = []
for instruction_set in instruction_list:
    instruction_list_formatted.extend([instruction.strip() for instruction in instruction_set.split("\n") if instruction])
print(instruction_list_formatted)

# 3. Input Generation
INPUT_PROMPT_TEMPLATE = """\
Diberikan sebuah instruksi dari pengguna mengenai jenis komentar media sosial yang diinginkan, buatlah sebuah deskripsi tentang postingan media sosial yang relevan. Deskripsi ini akan berfungsi sebagai 'input' untuk AI pembuat komentar.
Fokus pada topik utama, suasana, atau kejadian yang ada di postingan, seolah-olah sedang menulis caption singkat atau ringkasan konten postingan tersebut. Pastikan deskripsi realistis, beragam, dan bisa memicu komentar sesuai instruksi.

Instruksi: {instruction} 
Hasilkan hanya deskripsi itu sendiri. Tanpa teks pengantar, penutup, atau karakter tambahan di awal atau akhir deskripsi postingan.
"""

def generate_inputs(client, instruction, retries=5, delay=5):
    print(f"Generate Deskripsi Postingan untuk Instruksi: [bold yellow]{instruction}[/bold yellow]")
    prompt = INPUT_PROMPT_TEMPLATE.format(instruction=instruction)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user",
             "content": prompt}
        ],
            temperature=0.7, 
            top_p=0.9,       
            max_tokens=256,  
    )
    return response.choices[0].message.content.strip()

def input_generator(client, instruction_list):
    input_list = []
    for instruction in instruction_list:
        input_list.append(generate_inputs(client, instruction))
    return input_list

input_description_list = input_generator(client, instruction_list_formatted)
input_description_pair_list = []
for instruction, post_description in zip(instruction_list_formatted, input_description_list):
    input_description_pair_list.append(
        {
            "instruction": instruction,
            "input": post_description,
        }
    )

print(input_description_pair_list)


# 4. Output Generation
OUTPUT_PROMPT_TEMPLATE = """\
Anda adalah AI pembuat komentar media sosial yang ahli dalam menulis komentar yang relevan, natural, dan sesuai konteks.
Diberikan sebuah instruksi dari pengguna dan deskripsi postingan media sosial, buatlah sebuah komentar yang realistis dan alami seolah-olah ditulis oleh manusia.

Gunakan bahasa sehari-hari atau bahasa gaul yang umum di media sosial (sesuai konteks instruksi). Komentar harus singkat, tidak terlalu formal, dan bisa mencakup emoji atau singkatan yang wajar jika sesuai. Hindari pengulangan dan pastikan komentar tidak terdengar seperti robot.

Instruksi: {instruction}
Deskripsi Postingan: {input_description}

Hasilkan hanya komentar itu sendiri, tanpa teks pengantar, penutup, atau karakter tambahan di awal atau akhir komentar.
"""

def generate_outputs(client, instruction, input_description, retries=5, delay=5):
    print(f"Generate Komentar untuk Instruksi: [bold yellow]{instruction}[/bold yellow] dan Postingan: [bold cyan]{input_description[:50]}...[/bold cyan]")
    prompt = OUTPUT_PROMPT_TEMPLATE.format(instruction=instruction, input_description=input_description)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user",
             "content": prompt}
        ],
            temperature=0.8, 
            top_p=0.95,      
            max_tokens=100,  
    )
    return response.choices[0].message.content.strip() 

def output_generator(client, instruction_input_list):
    generated_outputs = [] 
    for item in instruction_input_list:
        comment = generate_outputs(client, item['instruction'], item['input'])
        generated_outputs.append(
            {
                "instruction": item['instruction'],
                "input": item['input'],
                "output": comment
            }
        )
    return generated_outputs 

# Panggil fungsi output_generator dan simpan hasilnya ke output_list
output_list = output_generator(client, input_description_pair_list)

print(output_list)

# Saving the Dataset
output_filename = 'alpaca_comment_dataset.jsonl'
with open(output_filename, 'w', encoding='utf-8') as f:
    for item in output_list:
        f.write(json.dumps(item))
        f.write('\n')
print(f"\nDataset berhasil disimpan ke: [bold magenta]{output_filename}[/bold magenta]")