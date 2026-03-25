import os
import argparse
import ollama
import frontmatter

CONTENT_DIR = 'content'

def generate_summary(content, author="Sean", model="llama3"):
    """
    Calls Ollama to generate a concise summary of the blog post content.
    """
    prompt = (
        f"You are an expert blog editor. I will provide you with the content of a blog post written by {author}. "
        f"Please provide a concise, interesting, and engaging summary of the post in 2-3 sentences. "
        f"The summary MUST be written in the third person, referring to the author as '{author}'. "
        "The tone should be professional and informative, avoiding excessive hype or 'peppy' language. "
        "The summary should be suitable for a blog homepage to entice readers to click through. "
        "IMPORTANT: Return ONLY the summary text itself. Do not include any introductory phrases (like 'Here is a summary'), "
        "do not use quotes to wrap the entire summary, and do not include any other conversational filler.\n\n"
        f"Blog Post Content:\n{content}"
    )
    response = ollama.generate(model=model, prompt=prompt)
    summary = response['response'].strip()
    
    # Post-processing to remove common AI artifacts
    # Remove leading/trailing quotes (both single and double)
    if (summary.startswith('"') and summary.endswith('"')) or (summary.startswith("'") and summary.endswith("'")):
        summary = summary[1:-1].strip()
        
    # Remove common AI headers if they still appear
    headers_to_remove = [
        "Here is a concise and engaging summary of the blog post:",
        "Here is a concise, interesting, and engaging summary of the post:",
        "Here is a concise, interesting, and engaging summary of the blog post:",
        "Here is a summary of the blog post:",
        "Here is a summary of the post:",
        "Summary:",
        "Here's a summary:",
    ]
    for header in headers_to_remove:
        if summary.lower().startswith(header.lower()):
            summary = summary[len(header):].strip()
            # If after stripping the header there are quotes, strip them too
            if (summary.startswith('"') and summary.endswith('"')) or (summary.startswith("'") and summary.endswith("'")):
                summary = summary[1:-1].strip()
            
    return summary

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

        author = post.metadata.get('author', 'Sean')
        print(f"Summarizing '{file_path}' (Author: {author}) with {model}...")
        summary = generate_summary(post.content, author, model)
        
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
