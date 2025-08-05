from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
import subprocess
import re

# Markdown Generation Function
def generate_markdown(title, body, published_date):
    try:
        date_obj = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            date_obj = datetime.fromisoformat(published_date.split("T")[0])
        except ValueError:
            print(f"[!] Failed to parse date: {published_date}")
            date_obj = datetime.now()

    year = str(date_obj.year)
    month = f"{date_obj.month:02d}"
    filename = title.lower().replace(" ", "-").replace("/", "-") + ".md"

    # Paths
    hugo_root = "D:/balasubrahmanya/slm/my-hugo-site/content/posts"
    dated_folder = os.path.join(hugo_root, year, month)
    os.makedirs(dated_folder, exist_ok=True)
    final_path = os.path.join(dated_folder, filename)

    log_dir = "output"
    os.makedirs(log_dir, exist_ok=True)
    output_path = os.path.join(log_dir, filename)

    # Final markdown content
    markdown_content = f"""---
title: "{title}"
date: {date_obj.isoformat()}
draft: false
tags: ["News", "AI", "Tech", "TechNews", "Intellex"]
categories: ["{year}", "{year}-{month}"]
---

{body}
"""

    # Write to Hugo content directory
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # Write to output log directory
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"[✓] Article written to: {final_path}")
    print(f"[✓] Backup saved to: {output_path}")


# Rewrite Article using SLM
def rewrite_article(summary, title):
    prompt = f"""
You are an expert AI news writer.

Rewrite the following tech news summary into a clean, human-like article in Markdown format. The article should:
- Be professional and engaging
- Avoid placeholder text like [insert date]
- Use correct grammar and formatting
- Not include emojis
- Use H1 title, paragraphs, and bullet points if relevant

Title: {title}

Summary: {summary}

Write the article now:
"""
    result = subprocess.run(
        ['ollama', 'run', 'phi3'],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    raw_output = result.stdout.decode()
    return clean_article(raw_output)


# Cleanup Markdown Output
def clean_article(markdown):
    markdown = re.sub(r"\[.*?\]", "", markdown)  # Remove [insert date]
    markdown = re.sub(r"[^\x00-\x7F]+", "", markdown)  # Remove emojis / non-ASCII
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)  # Collapse excess newlines

    # Ensure H1 title
    lines = markdown.strip().splitlines()
    if lines and not lines[0].startswith("#"):
        lines[0] = f"# {lines[0]}"
    return "\n".join(lines)



# from jinja2 import Environment, FileSystemLoader
# from datetime import datetime
# import os
# import subprocess
# import re


# # def generate_markdown(title, body, published):
# #     env = Environment(loader=FileSystemLoader("templates"))
# #     template = env.get_template("article_template.md.j2")
# #     content = template.render(title=title, body=body, published=published)

# #     filename = title.lower().replace(" ", "_")[:40]
# #     filepath = f"output/{filename}.md"
# #     with open(filepath, "w") as f:
# #         f.write(content)
# #     print(f"Saved article: {filepath}")

# # def generate_markdown(title, body, published_date):
# #     # Convert title to safe filename
# #     filename = title.lower().replace(" ", "-").replace("/", "-") + ".md"

# #     # Output directory (for backup or logs)
# #     output_dir = "output"
# #     os.makedirs(output_dir, exist_ok=True)
# #     output_path = os.path.join(output_dir, filename)

# #     # Sirivarthe Hugo site posts directory
# #     hugo_post_dir = "D:/balasubrahmanya/slm/my-hugo-site/content/posts"
# #     os.makedirs(hugo_post_dir, exist_ok=True)
# #     hugo_post_path = os.path.join(hugo_post_dir, filename)

# #     # Markdown article structure
# #     markdown_content = f"""---
# # title: "{title}"
# # date: {published_date}
# # draft: false
# # tags: ["auto-generated", "tech", "AI"]
# # ---

# # {body}
# # """



# def generate_markdown(title, body, published_date):
#     # Convert date to folder path: /2025/07/
#     try:
#         date_obj = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %z")
#     except ValueError:
#         # If published_date is already in ISO format or something else
#         date_obj = datetime.fromisoformat(published_date.split("T")[0])

#     year = str(date_obj.year)
#     month = f"{date_obj.month:02d}"

#     # Convert title to safe filename
#     filename = title.lower().replace(" ", "-").replace("/", "-") + ".md"

#     # Destination: Hugo content/posts/2025/07/
#     hugo_root = "D:/balasubrahmanya/slm/my-hugo-site/content/posts"
#     dated_folder = os.path.join(hugo_root, year, month)
#     os.makedirs(dated_folder, exist_ok=True)
#     final_path = os.path.join(dated_folder, filename)

#     # Save a log version in output/ too
#     log_dir = "output"
#     os.makedirs(log_dir, exist_ok=True)
#     output_path = os.path.join(log_dir, filename)

#     # Markdown content
#     markdown_content = f"""---
# title: "{title}"
# date: {date_obj.isoformat()}
# draft: false
# tags: ["News", "AI", "Tech", "TechNews", "Intellex"]
# categories: ["{year}", "{year}-{month}"]
# ---

# {body}
# """

#     with open(final_path, "w", encoding="utf-8") as f:
#         f.write(markdown)

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(markdown)

#     print(f"[✓] Article written to: {final_path}")


#     # # Save in output/ for logging
#     # with open(output_path, "w", encoding="utf-8") as f:
#     #     f.write(markdown_content)

#     # # Also save directly into Hugo site
#     # with open(hugo_post_path, "w", encoding="utf-8") as f:
#     #     f.write(markdown_content)

#     # print(f"[✓] Article saved to: {hugo_post_path}")



# def rewrite_article(summary, title):
#     prompt = f"""
# You are an expert AI news writer.

# Rewrite the following tech news summary into a clean, human-like article in Markdown format. The article should:
# - Be professional and engaging
# - Avoid placeholder text like [insert date]
# - Use correct grammar and formatting
# - Not include emojis
# - Use H1 title, paragraphs, and bullet points if relevant

# Title: {title}

# Summary: {summary}

# Write the article now:
# """
#     result = subprocess.run(
#         ['ollama', 'run', 'phi3'],
#         input=prompt.encode(),
#         stdout=subprocess.PIPE
#     )

#     raw_output = result.stdout.decode()
#     return clean_article(raw_output)

# def clean_article(markdown):
#     # Remove any placeholders like [insert date]
#     markdown = re.sub(r"\[.*?\]", "", markdown)

#     # Remove emojis / non-ASCII
#     markdown = re.sub(r"[^\x00-\x7F]+", "", markdown)

#     # Collapse extra newlines
#     markdown = re.sub(r"\n{3,}", "\n\n", markdown)

#     # Ensure the first line is a title
#     lines = markdown.strip().splitlines()
#     if lines and not lines[0].startswith("#"):
#         lines[0] = f"# {lines[0]}"
#     return "\n".join(lines)
