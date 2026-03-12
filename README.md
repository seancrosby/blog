# Sean Crosby's Blog

A bespoke static blog engine that transforms Markdown content into a clean, modern website hosted on GitHub Pages.

## Core Goals
1. Share insights that build faith in Christ.
2. Serve as a model for student online portfolios.

---

## 🛠 Prerequisites & Installation

### 1. Python Environment
This project requires Python 3.x and several libraries.
```bash
# Clone the repository
git clone https://github.com/seancrosby/blog.git
cd blog

# Install dependencies
pip install -r requirements.txt
```

### 2. AI Spell & Grammar Checking (Optional)
To use the AI-assisted editing features, you'll need [Ollama](https://ollama.com/) installed and running locally with the `llama3` model.
```bash
# Pull the default model
ollama pull llama3
```

---

## 📝 Creating Content

### 1. Create a New Post
Add a new `.md` file to the `content/` directory. Each file should include frontmatter for metadata:

```markdown
---
title: My New Blog Post
date: 2026-03-06
tags: reflection, tech
---

# Your Content Here
This is a standard markdown post.
```

### 2. Custom Syntax
- **YouTube Embeds:** Use `[youtube:VIDEO_ID]` (e.g., `[youtube:dQw4w9WgXcQ]`).
- **Images:** Place images in `assets/images/` and reference them: `![Description](../assets/images/your-image.jpg)`.

### 3. AI Spellcheck & Grammar Review
Run the AI editor to review your post before publishing:
```bash
python scripts/check_md.py content/my-post.md
```
This script uses Ollama to generate suggestions and opens them in a `vimdiff` view for your review.

### 4. AI Content Advice
To get AI-powered feedback on your post's content and structure:
```bash
python scripts/advise_md.py content/my-post.md
```
This script uses Ollama to provide advice on what else to include and how to make the post more satisfying for readers.

---

## 🚀 Generating & Previewing

To generate the static HTML files in the `public/` directory:
```bash
python scripts/generate.py
```

To preview the site locally, you can use Python's built-in server:
```bash
cd public
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

---

## 🧪 Testing

We use `pytest` for unit and integration tests.
```bash
# Run all tests
PYTHONPATH=. pytest
```

---

## 🤖 GitHub Actions & Deployment

The blog is automatically built and deployed via GitHub Actions whenever changes are pushed to the `main` branch.

**Workflow Path:** `.github/workflows/deploy.yml`
1. **Build Job:** Installs dependencies, runs tests, and generates the `public/` folder.
2. **Deploy Job:** Uploads the `public/` artifact and deploys it to GitHub Pages.

---

## ✅ TODO
- [ ] Add AI-generated summaries for each post.
- [ ] Implement Dark Mode.
- [ ] Create an image optimization/resizing script.
- [ ] Add featured images and thumbnails to the homepage.
