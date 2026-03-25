import os
import argparse
import ollama
import frontmatter

CONTENT_DIR = 'content'

def generate_summary(content, model="llama3"):
    """
    Calls Ollama to generate a concise summary of the blog post content.
    """
    prompt = (
        "You are an expert blog editor. I will provide you with the content of my blog post. "
        "Please provide a concise, engaging summary of the post in 2-3 sentences, written in the first person (using 'I', 'me', 'my'). "
        "The summary should be suitable for a blog homepage to entice readers to click through. "
        "Return ONLY the summary text, nothing else.\n\n"
        f"Blog Post Content:\n{content}"
    )
    response = ollama.generate(model=model, prompt=prompt)
    return response['response'].strip()

def summarize_markdown(file_path, model="llama3", overwrite=False):
    """
    Uses Ollama to generate a summary for a markdown blog post and updates its front matter.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        post = frontmatter.load(file_path)
        
        # Check if summary already exists
        if 'summary' in post.metadata:
            if not overwrite:
                print(f"Skipping '{file_path}': Summary already exists.")
                return
            else:
                print(f"Overwriting summary for '{file_path}'...")
                # Explicitly delete the current summary as requested
                del post.metadata['summary']

        print(f"Summarizing '{file_path}' with {model}...")
        summary = generate_summary(post.content, model)
        
        # Update front matter
        post.metadata['summary'] = summary
        
        # Write back to file
        with open(file_path, 'wb') as f:
            frontmatter.dump(post, f)
            
        print(f"Updated '{file_path}' with summary.")
        
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")

def summarize_all(model="llama3", overwrite=False):
    """
    Iterates through all markdown files in the content directory and generates summaries.
    """
    if not os.path.exists(CONTENT_DIR):
        print(f"Error: Content directory '{CONTENT_DIR}' not found.")
        return

    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(CONTENT_DIR, filename)
            summarize_markdown(filepath, model, overwrite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AI summaries for blog posts.")
    parser.add_argument("model", nargs="?", default="llama3", help="The Ollama model to use (default: llama3).")
    parser.add_argument("--overwrite", "-f", "--force", action="store_true", help="Overwrite existing summaries. Deletes the current summary before generating a new one.")
    
    args = parser.parse_args()
    summarize_all(args.model, args.overwrite)
