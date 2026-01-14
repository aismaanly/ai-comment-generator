import instaloader
import json

# Load instaloader
L = instaloader.Instaloader()

post_urls = [
    "https://www.instagram.com/p/DGuzvovyJEL",
    "https://www.instagram.com/p/DFhN0oBSRvr",
    "https://www.instagram.com/p/DF2u7pDSNZT",
    "https://www.instagram.com/p/DGVOFQly1A2",
    "https://www.instagram.com/p/DFaKI_GSr4U",
    "https://www.instagram.com/p/Czah0HoSkyK",
    "https://www.instagram.com/p/DCJ1cKWJcpx",
    "https://www.instagram.com/p/DE1fZTCTzkE",
    "https://www.instagram.com/p/DFmLymNTZt5",
    "https://www.instagram.com/p/DGxW4gkP26O",
    "https://www.instagram.com/p/DGZq6tjyD5R",
    "https://www.instagram.com/p/DGcp9navpvk",
    "https://www.instagram.com/p/DGctSuOPT7G",
    "https://www.instagram.com/p/DGkZEIWpwic",
    "https://www.instagram.com/p/DFj8U1dJ-h5",
    "https://www.instagram.com/p/DGSyIWjpLnt",
]

def extract_shortcode(url):
    return url.strip("/").split("/")[-1]

def extract_data_from_post(post):
    caption = post.caption or ""
    comments_data = []

    try:
        for comment in post.get_comments():
            comments_data.append({
                "comment_id": comment.id,
                "text": comment.text,
                "username": comment.owner.username
            })
    except Exception as e:
        print(f"❌ Error extracting comments for {post.shortcode}: {e}")
    
    return {
        "input_url": f"https://www.instagram.com/p/{post.shortcode}/",
        "post_id": post.mediaid,
        "owner_username": post.owner_username,
        "timestamp": post.date_utc.strftime("%Y-%m-%d"),
        "type": "video" if post.is_video else "image",
        "likes": post.likes,
        "caption": caption,
        "comments_count": post.comments,
        "comments": comments_data
    }

all_data = []

for url in post_urls:
    shortcode = extract_shortcode(url)
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        post_data = extract_data_from_post(post)
        all_data.append(post_data)
        print(f"✅ Extracted: {shortcode}")
    except Exception as e:
        print(f"❌ Error with {shortcode}: {e}")

# Save as JSON
with open("instagram_post.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
