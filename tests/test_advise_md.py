import os
import pytest
from scripts.advise_md import generate_advice, advise_markdown

def test_generate_advice(mocker):
    mock_ollama = mocker.patch('ollama.generate')
    mock_ollama.return_value = {'response': 'Actionable advice.'}
    
    result = generate_advice("Blog content", model="test-model")
    
    assert result == "Actionable advice."
    mock_ollama.assert_called_once()
    args, kwargs = mock_ollama.call_args
    assert kwargs['model'] == "test-model"
    assert "Blog content" in kwargs['prompt']

def test_advise_markdown_flow(tmp_path, mocker):
    # Setup files
    file_path = tmp_path / "test.md"
    file_path.write_text("---\ntitle: Test Post\n---\nBlog content", encoding='utf-8')
    
    # Mock dependencies
    mock_gen = mocker.patch('scripts.advise_md.generate_advice', return_value="Great post!")
    
    # Capture stdout to verify output if needed, but here we just check if it runs
    advise_markdown(str(file_path))
    
    mock_gen.assert_called_once_with("Blog content", "llama3")

def test_advise_markdown_no_frontmatter(tmp_path, mocker):
    # Setup files
    file_path = tmp_path / "test.md"
    file_path.write_text("Just content without frontmatter", encoding='utf-8')
    
    # Mock dependencies
    mock_gen = mocker.patch('scripts.advise_md.generate_advice', return_value="Great post!")
    
    advise_markdown(str(file_path))
    
    mock_gen.assert_called_once_with("Just content without frontmatter", "llama3")
