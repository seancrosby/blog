import os
import frontmatter
import markdown
import re
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, date
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

class SiteGenerator:
    def __init__(self, content_dir=CONTENT_DIR, template_dir=TEMPLATE_DIR, output_dir=OUTPUT_DIR, assets_dir=ASSETS_DIR):
        self.content_dir = content_dir
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.assets_dir = assets_dir
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def get_date_str(self, post, filepath):
        date_val = post.get('date')
        if isinstance(date_val, (datetime, date)):
            return date_val.strftime('%Y-%m-%d')
        elif isinstance(date_val, str):
            return date_val
        else:
            return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

    def get_title(self, post, filename):
        title = post.get('title')
        if not title:
            for line in post.content.split('\n'):
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    break
            if not title:
                title = filename.replace('.md', '').replace('-', ' ').title()
        return title

    def get_tags(self, post):
        tags = post.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        return tags

    def process_post(self, filename):
        filepath = os.path.join(self.content_dir, filename)
        post = frontmatter.load(filepath)
        
        date_str = self.get_date_str(post, filepath)
        title = self.get_title(post, filename)
        tags = self.get_tags(post)
        
        content = handle_custom_tags(post.content)
        content_html = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        
        slug = filename.replace('.md', '.html')

        return {
            'title': title,
            'date': date_str,
            'slug': slug,
            'content': content_html,
            'tags': tags
        }

    def generate(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        post_template = self.env.get_template('post.html')
        index_template = self.env.get_template('index.html')
        tags_template = self.env.get_template('tags.html')

        posts = []
        tags_map = defaultdict(list)

        for filename in os.listdir(self.content_dir):
            if filename.endswith('.md'):
                post_data = self.process_post(filename)
                posts.append(post_data)

                for tag in post_data['tags']:
                    tags_map[tag].append(post_data)

                output_path = os.path.join(self.output_dir, post_data['slug'])
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(post_template.render(
                        title=post_data['title'],
                        date=post_data['date'],
                        content=post_data['content'],
                        tags=post_data['tags']
                    ))

        posts.sort(key=lambda x: x['date'], reverse=True)
        
        sorted_tags = sorted(tags_map.items())
        for tag, tag_posts in sorted_tags:
            tag_posts.sort(key=lambda x: x['date'], reverse=True)

        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as out_f:
            out_f.write(index_template.render(posts=posts))

        with open(os.path.join(self.output_dir, 'tags.html'), 'w', encoding='utf-8') as out_f:
            out_f.write(tags_template.render(tags=sorted_tags))

        # Copy assets to output directory if they exist and source != destination
        if os.path.exists(self.assets_dir):
            # Resolve absolute paths to compare
            src_assets = os.path.abspath(self.assets_dir)
            dest_assets = os.path.abspath(os.path.join(self.output_dir, os.path.basename(self.assets_dir)))
            
            if src_assets != dest_assets:
                if os.path.exists(dest_assets):
                    shutil.rmtree(dest_assets)
                shutil.copytree(src_assets, dest_assets)

        print(f"Successfully generated {len(posts)} posts and {len(sorted_tags)} tags.")
        return posts, sorted_tags

def generate_site():
    generator = SiteGenerator()
    generator.generate()

if __name__ == "__main__":
    generate_site()
