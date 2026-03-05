import os
import frontmatter
import markdown
import re
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from collections import defaultdict

# Configuration
CONTENT_DIR = 'content'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'public'
ASSETS_DIR = 'assets'

def handle_custom_tags(text):
    # Support [youtube:VIDEO_ID]
    youtube_pattern = r'\[youtube:([\w-]+)\]'
    youtube_replacement = r'<div class="video-container"><iframe src="https://www.youtube.com/embed/\1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
    return re.sub(youtube_pattern, youtube_replacement, text)

def generate_site():
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    post_template = env.get_template('post.html')
    index_template = env.get_template('index.html')
    tags_template = env.get_template('tags.html')

    posts = []
    tags_map = defaultdict(list)

    # Process Markdown files
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(CONTENT_DIR, filename)
            post = frontmatter.load(filepath)
            
            # Extract metadata
            date_val = post.get('date')
            from datetime import date
            if isinstance(date_val, (datetime, date)):
                date_str = date_val.strftime('%Y-%m-%d')
            elif isinstance(date_val, str):
                date_str = date_val
            else:
                date_str = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

            title = post.get('title')
            
            # Process custom tags like [youtube:ID]
            content = handle_custom_tags(post.content)
            content_html = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
            
            if not title:
                for line in post.content.split('\n'):
                    if line.startswith('# '):
                        title = line.replace('# ', '').strip()
                        break
                if not title:
                    title = filename.replace('.md', '').replace('-', ' ').title()

            # Handle Tags
            tags = post.get('tags', [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(',')]

            slug = filename.replace('.md', '.html')

            post_data = {
                'title': title,
                'date': date_str,
                'slug': slug,
                'content': content_html,
                'tags': tags
            }
            posts.append(post_data)

            # Map tags to posts
            for tag in tags:
                tags_map[tag].append(post_data)

            # Render individual post
            output_path = os.path.join(OUTPUT_DIR, slug)
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(post_template.render(title=title, date=date_str, content=content_html, tags=tags))

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Sort tags alphabetically and their posts by date
    sorted_tags = sorted(tags_map.items())
    for tag, tag_posts in sorted_tags:
        tag_posts.sort(key=lambda x: x['date'], reverse=True)

    # Render index page
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as out_f:
        out_f.write(index_template.render(posts=posts))

    # Render tags page
    with open(os.path.join(OUTPUT_DIR, 'tags.html'), 'w', encoding='utf-8') as out_f:
        out_f.write(tags_template.render(tags=sorted_tags))

    # Copy assets to output directory
    import shutil
    if os.path.exists(ASSETS_DIR):
        dest_assets = os.path.join(OUTPUT_DIR, ASSETS_DIR)
        if os.path.exists(dest_assets):
            shutil.rmtree(dest_assets)
        shutil.copytree(ASSETS_DIR, dest_assets)

    print(f"Successfully generated {len(posts)} posts and {len(sorted_tags)} tags.")

if __name__ == "__main__":
    generate_site()
