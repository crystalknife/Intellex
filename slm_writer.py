import subprocess

def rewrite_article(content, title):
    prompt = f"""Act as a professional news writer.
Rewrite the following content as a formal news article. Ensure it is original, clear, and SEO-optimized.

Title: {title}

Content:
{content}

--- End ---
"""
    result = subprocess.run(
        ['ollama', 'run', 'phi3'],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()
