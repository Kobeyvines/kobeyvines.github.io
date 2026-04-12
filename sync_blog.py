import os
import re
import shutil
import math
import frontmatter
from pathlib import Path

# --- CONFIGURATION ---
VAULT_ROOT = Path("/home/kobey/Documents/Obsidian Vault")
OBSIDIAN_POSTS_DIR = VAULT_ROOT / "01_Portfolio_Drafts"
OBSIDIAN_ATTACHMENTS_DIR = OBSIDIAN_POSTS_DIR / "Attachments" 

ASTRO_CONTENT_DIR = Path("src/content/blog")
ASTRO_ASSETS_DIR = Path("public/images/blog")

def calculate_reading_time(content):
    # 1. Strip out code blocks (already doing this)
    clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # 2. NEW: Strip out Markdown tables (| cell | cell |)
    # These are high-density data that shouldn't count as narrative words
    clean_content = re.sub(r'\|.*?\|', '', clean_content)
    
    # 3. NEW: Strip out long lists of numbers/data (common in your price analysis)
    # This removes strings of digits that aren't narrative words
    clean_content = re.sub(r'\b\d+[\d.,]*\b', '', clean_content)

    # Count actual words
    words = re.findall(r'\w+', clean_content)
    word_count = len(words)
    
    # 4. Technical WPM: Pros read faster, and we want to align with Medium
    # Let's use 275 WPM + a small floor for images
    minutes = math.ceil(word_count / 275)
    
    # Add 12 seconds per image (Medium's logic)
    image_count = len(re.findall(r'!\[\[.*?\]\]|!\[.*?\]\(.*?\)', content))
    minutes += math.ceil((image_count * 12) / 60)
    
    # Ensure a minimum of 1
    minutes = max(1, minutes)
    
    return f"{minutes} min read"

def sync():
    print(f"🚀 Starting Sync...")
    
    if not OBSIDIAN_ATTACHMENTS_DIR.exists():
        print(f"❌ ERROR: Attachments folder not found at {OBSIDIAN_ATTACHMENTS_DIR}")
        return

    ASTRO_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    ASTRO_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for md_file in OBSIDIAN_POSTS_DIR.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            if post.get('status') == 'published':
                print(f"📝 Processing Post: {md_file.name}")
                content = post.content
                
                # FIX 1: Explicitly cast to string and assign to metadata
                reading_time_value = calculate_reading_time(content)
                post.metadata['readingTime'] = str(reading_time_value)
                
                image_matches = re.findall(r'!\[\[(.*?)\]\]|!\[[^\]]*\]\(([^)]+)\)', content)
                
                for wiki_img, std_img in image_matches:
                    img_name = wiki_img if wiki_img else std_img
                    
                    if img_name.startswith('http'):
                        continue

                    clean_name = os.path.basename(img_name)
                    name_only = os.path.splitext(clean_name)[0].lower()
                    
                    found_file = None
                    for file in OBSIDIAN_ATTACHMENTS_DIR.iterdir():
                        if file.stem.lower() == name_only:
                            found_file = file
                            break
                            
                    if found_file:
                        dest_path = ASTRO_ASSETS_DIR / found_file.name
                        shutil.copy2(found_file, dest_path)
                        web_path = f"/images/blog/{found_file.name}"
                        
                        if wiki_img:
                            old_syntax = f"![[{wiki_img}]]"
                            new_syntax = f"![image]({web_path})"
                            content = content.replace(old_syntax, new_syntax)
                        else:
                            content = content.replace(img_name, web_path)
                        
                        print(f"   ✅ Transformed & Copied: {found_file.name}")
                    else:
                        print(f"   ❌ Still could not find: {img_name}")

                # Save the updated post
                post.content = content
                with open(ASTRO_CONTENT_DIR / md_file.name, 'wb') as fout:
                    # FIX 2: frontmatter.dump will now serialize the metadata correctly
                    frontmatter.dump(post, fout)
                
                print(f"   ⏱️  Reading time set: {post.metadata['readingTime']}")

if __name__ == "__main__":
    sync()