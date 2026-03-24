import os
import sys
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

def summarize_markdown(file_path, model="llama3", force=False):
    """
    Uses Ollama to generate a summary for a markdown blog post and updates its front matter.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        post = frontmatter.load(file_path)
        
        # Skip if summary already exists and not forcing regeneration
        if 'summary' in post.metadata and not force:
            print(f"Skipping '{file_path}': Summary already exists.")
            return

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

def summarize_all(model="llama3", force=False):
    """
    Iterates through all markdown files in the content directory and generates summaries.
    """
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(CONTENT_DIR, filename)
            summarize_markdown(filepath, model, force)

if __name__ == "__main__":
    force_update = "--force" in sys.argv
    model_name = "llama3"
    
    # Check if a model name was provided (excluding the --force flag)
    args = [a for a in sys.argv[1:] if a != "--force"]
    if args:
        model_name = args[0]
        
    summarize_all(model_name, force_update)
