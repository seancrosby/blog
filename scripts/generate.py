import os
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Configuration
CONTENT_DIR = 'content'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'public'
ASSETS_DIR = 'assets'

def generate_site():
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    post_template = env.get_template('post.html')
    index_template = env.get_template('index.html')

    posts = []

    # Process Markdown files
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(CONTENT_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
                # Simple frontmatter/content split (optional, but good for metadata)
                # For now, we'll just use the first line as the title if it starts with #
                html_content = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
                
                # Derive metadata
                title = filename.replace('.md', '').replace('-', ' ').title()
                date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')
                slug = filename.replace('.md', '.html')

                posts.append({
                    'title': title,
                    'date': date,
                    'slug': slug,
                    'content': html_content
                })

                # Render individual post
                output_path = os.path.join(OUTPUT_DIR, slug)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(post_template.render(title=title, date=date, content=html_content))

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)

    # Render index page
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as out_f:
        out_f.write(index_template.render(posts=posts))

    print(f"Successfully generated {len(posts)} posts.")

if __name__ == "__main__":
    generate_site()
