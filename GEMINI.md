# Project: Sean Crosby's Blog

## Context & Goals
This is a custom static blog hosted on GitHub Pages. Instead of using a standard SSG (like Jekyll or Hugo), this project uses bespoke Python scripts to transform Markdown content into a functional, aesthetic website.

## Tech Stack
- **Content:** Markdown (`.md`) files.
- **Engine:** Python 3.x scripts for HTML generation.
- **Hosting:** GitHub Pages.
- **Styling:** Vanilla CSS (aim for a clean, modern, "paper-like" aesthetic).

## Directory Structure
- `content/`: Source `.md` files for blog entries.
- `scripts/`: Python scripts for site generation.
- `templates/`: HTML templates for the homepage and post layouts.
- `public/`: The generated static site (output directory).
- `assets/`: CSS, images, and other static files.

## Mandates & Constraints
- **Generation:** All HTML in `public/` must be reproducible via the Python scripts in `scripts/`.
- **Markdown Processing:** Use standard Python libraries (like `markdown` or `mistune`) for conversion.
- **Homepage:** Must dynamically list all blog entries from the `content/` directory, sorted by date (newest first).
- **GitHub Pages:** Ensure the root or `docs/` folder (depending on configuration) is compatible with GitHub's hosting requirements.
- **Workflow:** Before finishing any task involving new content, always run the generation script to ensure the `public/` folder is up to date.
