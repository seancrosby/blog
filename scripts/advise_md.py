import os
import sys
import ollama
import frontmatter

def advise_markdown(file_path, model="llama3"):
    """
    Uses Ollama to provide advice on a markdown blog post's content.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Load the post using frontmatter to separate metadata from content
    try:
        post = frontmatter.load(file_path)
        content = post.content
        title = post.get('title', os.path.basename(file_path))
    except Exception as e:
        print(f"Error reading file: {e}")
        # Fallback to reading the whole file if frontmatter fails
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title = os.path.basename(file_path)
        except Exception as e2:
            print(f"Critical error reading file: {e2}")
            return

    print(f"Analyzing '{title}' with {model} via Ollama...")

    # Construct the prompt for Ollama
    prompt = (
        "You are an expert blog editor and writing coach. I will provide you with the content of a blog post. "
        "Please analyze it and provide constructive feedback on the following:\n"
        "1. What else should be included to make the post more comprehensive or engaging?\n"
        "2. Does the post feel complete? Are there any logical gaps or unanswered questions?\n"
        "3. Would this post be satisfying or effective for a blog reader? Consider the tone, structure, and value provided.\n\n"
        "Please be specific and provide actionable advice. Keep your response concise but thorough.\n\n"
        f"Blog Post Content:\n{content}"
    )

    try:
        # Call Ollama
        response = ollama.generate(model=model, prompt=prompt)
        advice = response['response'].strip()
        
        print("\n" + "="*40)
        print(f"ADVICE FOR: {title}")
        print("="*40 + "\n")
        print(advice)
        print("\n" + "="*40)
        
    except Exception as e:
        print(f"Error calling Ollama: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/advise_md.py <file.md> [model_name]")
        print("Default model is 'llama3'.")
        sys.exit(1)

    input_file = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "llama3"
    
    advise_markdown(input_file, model_name)
