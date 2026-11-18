import glob
import re
import os
import json

with open("blog/data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"Total posts in posts.json: {len(posts)}")
for p in posts:
    slug = p["slug"]
    src_file = os.path.join("blog/posts-src", f"{slug}.html")
    has_src = os.path.exists(src_file)
    first_img = None
    if has_src:
        with open(src_file, "r", encoding="utf-8") as sf:
            content = sf.read()
        m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        if m:
            first_img = m.group(1)
    
    # Check assets
    png_asset = os.path.join("blog/assets", f"{slug}.png")
    jpg_asset = os.path.join("blog/assets", f"{slug}.jpg")
    asset_status = "NONE"
    if os.path.exists(png_asset):
        asset_status = f"{slug}.png"
    elif os.path.exists(jpg_asset):
        asset_status = f"{slug}.jpg"
    elif slug == "openclaw-desarrollo-agntico-en-el-workspace-local" and os.path.exists("blog/assets/openclaw-infografia.jpg"):
        asset_status = "openclaw-infografia.jpg"
        
    print(f"[{slug}]")
    print(f"  First img in post content: {first_img}")
    print(f"  Asset on disk: {asset_status}")
