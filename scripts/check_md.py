import os
import argparse
import tempfile
import subprocess
import shutil
import ollama

def generate_correction(content, model="llama3"):
    """
    Calls Ollama to get corrected markdown content.
    """
    prompt = (
        "You are an expert editor. Please spell and grammar check the following markdown content. "
        "Return the full corrected content. Maintain all markdown formatting, including frontmatter. "
        "Do not provide any preamble or commentary, just the corrected markdown text.\n\n"
        f"Content:\n{content}"
    )
    response = ollama.generate(model=model, prompt=prompt)
    return response['response'].strip()

def launch_editor(file_path, temp_file_path):
    """
    Launches vimdiff or vim -d to compare the original and corrected files.
    """
    try:
        # Try vimdiff first
        subprocess.run(['vimdiff', '-c', 'windo set wrap', file_path, temp_file_path], check=True)
        return True
    except FileNotFoundError:
        # Fallback to vim -d if vimdiff command is not directly available
        try:
            subprocess.run(['vim', '-d', file_path, temp_file_path], check=True)
            return True
        except Exception as e:
            print(f"Error: Could not start vim in diff mode. {e}")
            return False
    except subprocess.CalledProcessError:
        print("Vim closed with an error.")
        return False

def check_markdown(file_path, model="llama3"):
    """
    Spell and grammar checks a markdown file using Ollama and opens suggestions in Vim side-by-side.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Read the original content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Analyzing '{file_path}' with {model} via Ollama...")

    try:
        corrected_content = generate_correction(content, model)
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return

    # Create a temporary file for the corrected suggestions
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

    editor_success = launch_editor(file_path, temp_file_path)

    if editor_success:
        print("\nReview complete.")
        choice = input(f"Would you like to overwrite '{file_path}' with the suggestions? (y/N): ").strip().lower()
        if choice == 'y':
            shutil.copy2(temp_file_path, file_path)
            print(f"Success: '{file_path}' has been updated with suggestions.")
        else:
            print("No changes applied to the original file.")

    # Clean up the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"\nTemporary suggestions file removed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spell and grammar check a markdown file using AI and review via Vim.")
    parser.add_argument("file", help="The markdown file to check.")
    parser.add_argument("model", nargs="?", default="llama3", help="The Ollama model to use (default: llama3).")
    
    args = parser.parse_args()
    check_markdown(args.file, args.model)
