import os
import sys
import tempfile
import subprocess
import ollama

def check_markdown(file_path, model="llama3"):
    """
    Spell and grammar checks a markdown file using Ollama and opens suggestions in Vim side-by-side.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Read the original content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Analyzing '{file_path}' with {model} via Ollama...")

    # Construct the prompt for Ollama
    prompt = (
        "You are an expert editor. Please spell and grammar check the following markdown content. "
        "Return the full corrected content. Maintain all markdown formatting, including frontmatter. "
        "Do not provide any preamble or commentary, just the corrected markdown text.\n\n"
        f"Content:\n{content}"
    )

    try:
        # Call Ollama
        response = ollama.generate(model=model, prompt=prompt)
        corrected_content = response['response'].strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return

    # Create a temporary file for the corrected suggestions
    # delete=False because we need it to persist until Vim closes
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode='w', encoding='utf-8') as temp_f:
        temp_f.write(corrected_content)
        temp_file_path = temp_f.name

    print("Opening side-by-side diff view in Vim...")
    print(f"Left (Original): {file_path}")
    print(f"Right (Suggestions): {temp_file_path}")
    print("\nInstructions:")
    print("1. Changes are highlighted. Use Ctrl+W, L to move right, Ctrl+W, H to move left.")
    print("2. Use ']c' to jump to next change, '[c' to jump to previous change.")
    print("3. Edit your original file as needed.")
    print("4. Save your original file (:w) and exit both windows (:qa).")

    input("\nPress Enter to open vimdiff...")

    try:
        # Open both files in Vim diff mode for highlighting
        subprocess.run(['vimdiff', '-c', 'windo set wrap', file_path, temp_file_path], check=True)
    except subprocess.CalledProcessError:
        print("Vim closed with an error.")
    except FileNotFoundError:
        # Fallback to vim -d if vimdiff command is not directly available
        try:
            subprocess.run(['vim', '-d', file_path, temp_file_path], check=True)
        except Exception as e:
            print(f"Error: Could not start vim in diff mode. {e}")
    finally:
        # Clean up the temporary file immediately after Vim exits
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"\nTemporary suggestions file removed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/check_md.py <file.md> [model_name]")
        print("Default model is 'llama3'.")
        sys.exit(1)

    input_file = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "llama3"
    
    check_markdown(input_file, model_name)
