# 🤖 AI Comment Generator — LLM Fine-Tuning Pipeline

This repository showcases my **end-to-end AI engineering workflow** in building a **domain-specific Large Language Model (LLM)** for generating **natural, contextual social media comments**.

The focus of this project is **model development**, covering:
- Data engineering (scraping & synthetic data generation)
- Prompt & instruction design
- LLM fine-tuning using **QLoRA**
- Model evaluation & deployment to Hugging Face

> 🔗 **Looking for the web application implementation?**  
> 👉 See: https://github.com/aismaanly/flask-comment-generator

---

## 🎯 Project Objective

To build a **custom fine-tuned LLM** that can generate **human-like, relevant social media comments** based on post descriptions optimized for real-world usage and lightweight deployment.

This project was developed as part of my **AI Engineer internship (MBKM)** and reflects **industry-oriented AI practices**, not just API usage.

---

## 🧠 AI Engineering Scope

### 1️⃣ Data Collection
- **Real-world data**: Instagram comment scraping using `Instaloader`
- **Synthetic data**: Instruction–Input–Output generation using **LLaMA**
- Final dataset size:
  - 3,385 real comments
  - 1,157 synthetic samples

### 2️⃣ Data Processing & EDA
- Text cleaning & normalization
- Duplicate & irrelevant data removal
- Character length analysis (instruction / input / output)
- WordCloud & distribution analysis

### 3️⃣ Model Fine-Tuning
- Base Model: **LLaMA 3.x**
- Fine-tuning method: **QLoRA (via Unsloth)**
- Training strategy:
  - Parameter-efficient tuning
  - Overfitting control (learning rate, epochs)
  - Training & validation loss monitoring

### 4️⃣ Model Deployment
- Fine-tuned adapters pushed to **Hugging Face**
- Models ready for downstream integration

🔗 **Published Models**
- https://huggingface.co/aismaanly/ai_comment  
- https://huggingface.co/aismaanly/ai_synthetic

---

## 🛠 Tech Stack

- **Language**: Python
- **LLM**: LLaMA 3.x
- **Fine-Tuning**: Unsloth, LoRA, QLoRA
- **Data**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, WordCloud
- **Platform**: Google Colab, Hugging Face

---


## 🚀 Next Step

To see how this fine-tuned model is **integrated into a real web application** using Flask & SQLite:

👉 **Web Integration Repository**  
https://github.com/aismaanly/flask-comment-generator
