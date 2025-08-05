# import shutil
# import os

# HUGO_SITE_PATH = "D:/balasubrahmanya/slm/my-hugo-site"
# HUGO_CONTENT_DIR = os.path.join(HUGO_SITE_PATH, "content/posts")
# GENERATED_ARTICLES_DIR = "output"

# def publish_to_hugo():
#     if not os.path.exists(HUGO_CONTENT_DIR):
#         print("❌ Hugo content directory does not exist!")
#         return

#     for filename in os.listdir(GENERATED_ARTICLES_DIR):
#         if filename.endswith(".md"):
#             src = os.path.join(GENERATED_ARTICLES_DIR, filename)
#             dst = os.path.join(HUGO_CONTENT_DIR, filename)
#             shutil.copy(src, dst)
#             print(f"✅ Copied {filename} to Hugo content folder.")

import shutil
import os

HUGO_SITE_PATH = "D:/balasubrahmanya/slm/my-hugo-site"
HUGO_CONTENT_DIR = os.path.join(HUGO_SITE_PATH, "content/posts")
GENERATED_ARTICLES_DIR = "output"

def publish_to_hugo():
    if not os.path.exists(HUGO_CONTENT_DIR):
        print("❌ Hugo content directory does not exist!")
        return

    for filename in os.listdir(GENERATED_ARTICLES_DIR):
        if filename.endswith(".md"):
            src = os.path.join(GENERATED_ARTICLES_DIR, filename)
            dst = os.path.join(HUGO_CONTENT_DIR, filename)
            shutil.copy(src, dst)
            print(f"✅ Copied {filename} to Hugo content folder.")
