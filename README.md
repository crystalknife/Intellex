# Intellex
AI-powered platform that fetches, rewrites, and publishes news in markdown for static sites.
# AutoJourno-AI 📰

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Custom-lightgrey.svg)](LICENSE)
[![Hugo](https://img.shields.io/badge/Hugo-Powered-blueviolet.svg)](https://gohugo.io/)

AutoJourno-AI is an intelligent, autonomous news article generation engine that fetches real-time news from global sources, rewrites them in a human-like markdown format, and organizes them neatly for static publishing via Hugo. This system is designed for developers, journalists, media startups, and digital publication platforms.

---

### ✨ Key Features

* **Automated News Fetching:** Gathers the latest news using APIs based on keywords, categories, or regions.
* **AI-Powered Rewriting:** Leverages a Small Language Model (SLM) to transform headlines and summaries into unique, well-structured articles.
* **Template-Based Formatting:** Uses Jinja2 templates to ensure all articles have consistent markdown structure and Hugo front matter.
* **Seamless Hugo Integration:** Automatically pushes generated articles into a Hugo project's content directory for instant deployment.

### ⚙️ How It Works

The system follows a simple, four-step pipeline to automate content creation:

`[Fetch News (news_fetcher.py)]` → `[Rewrite with SLM (slm_writer.py)]` → `[Generate Article (generate_article.py)]` → `[Publish to Hugo (hugo_publisher.py)]`

### 🧠 Project Structure

```bash
autojourno-ai/
├── main.py                        # Entry point for running the full pipeline
├── requirements.txt              # Python dependencies
├── config.ini                    # Configuration file for API keys and settings
├── data/                         # (Optional) Placeholder for storing input or fetched data
├── layouts/page/                 # Hugo-specific layout overrides (if used)
├── models/
│   └── slm_writer.py             # SLM (Small Language Model) for rewriting fetched news
├── output/
│   └── *.md                      # Generated markdown articles
├── templates/
│   └── article_template.md.j2    # Jinja2 template for formatting news content
├── utils/
│   ├── generate_article.py       # Converts fetched news to formatted articles
│   ├── hugo_publisher.py         # Pushes articles into Hugo’s content folder
│   └── news_fetcher.py           # News scraping using APIs (e.g., NewsAPI)
├── venv/                         # Local Python virtual environment
└── hugo.zip                      # Static Hugo site template (can be extracted for deployment)
```

---

### 🚀 Getting Started

#### Prerequisites

* Python 3.10+
* `pip` and `venv`
* [Hugo](https://gohugo.io/getting-started/installing/) (for static site generation)
* A News API Key (e.g., from [NewsAPI.org](https://newsapi.org/))

#### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/autojourno-ai.git](https://github.com/yourusername/autojourno-ai.git)
    cd autojourno-ai
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the system:**
    * Rename `config.ini.example` to `config.ini` (or create it).
    * Add your API key and other settings:
    ```ini
    [news_api]
    api_key = YOUR_NEWS_API_KEY_HERE
    keywords = AI, technology, SpaceX, startups
    
    [hugo]
    content_path = my-hugo-site/content/news/
    ```

---

### 🛠️ Usage

#### Run the Full Pipeline

Execute the main script to run all modules in sequence:
```bash
python main.py
```

#### Run Individual Modules

You can also run each step of the process independently.

1.  **Fetch news from the API:**
    ```bash
    python utils/news_fetcher.py
    ```

2.  **Generate markdown articles from fetched data:**
    ```bash
    python utils/generate_article.py
    ```

3.  **Publish generated articles to your Hugo site:**
    ```bash
    python utils/hugo_publisher.py
    ```

### 🧪 Example Output

Generated articles will appear in the `output/` directory with URL-friendly filenames:

```
output/
├── elon-musks-spacex-might-invest-2-billion-in-musks-xai.md
├── study-warns-of-significant-risks-in-using-ai-therapy-chatbots.md
└── meta-acquires-voice-startup-play-ai.md
```
Each `.md` file is formatted and ready to be placed in your Hugo site’s `content/news/` folder.

---

### 📂 Deployment

To deploy your news site with the generated content:

1.  **Unzip the Hugo template:**
    ```bash
    unzip hugo.zip -d my-hugo-site
    cd my-hugo-site
    ```

2.  **Ensure articles are in place:**
    The `hugo_publisher.py` script will have already moved the articles into `my-hugo-site/content/news/`.

3.  **Serve or build the site with Hugo:**
    ```bash
    # Serve locally for testing
    hugo server

    # Build the static site for deployment
    hugo
    ```
    The final site will be in the `public/` directory, ready to be deployed to Netlify, Vercel, GitHub Pages, or any static host.

---

### 💡 Use Cases

* **News Aggregator Sites:** Automate content creation from top headlines.
* **Tech Newsletters:** Generate markdown-ready content to plug into email platforms.
* **Personal AI Blog:** Auto-blog on specific topics or industries.
* **SEO Optimization:** Generate trending content quickly to improve site ranking.

---

### 📜 License

This project is released under a **Custom License**. Please see the `LICENSE` file for more details.

---

### 👨‍💻 Author

**Balasubrahmanya A G**
* Computer Science & Engineering Student
* Tech Enthusiast
* 📧 Email: [subrahmanyaprasad23balu@gmail.com](mailto:subrahmanyaprasad23balu@gmail.com)
* 🔗 LinkedIn: [https://www.linkedin.com/in/balasubrahmanya-a-g-77965628b/](https://www.linkedin.com/in/balasubrahmanya-a-g-77965628b/)
