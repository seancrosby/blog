import os
import pytest
import frontmatter
from scripts.summarize_md import generate_summary, summarize_markdown, summarize_all

def test_generate_summary(mocker):
    # Mock ollama.generate
    mock_ollama = mocker.patch('ollama.generate')
    mock_ollama.return_value = {'response': ' This is a summary. '}
    
    result = generate_summary("Blog content", model="test-model")
    
    assert result == "This is a summary."
    mock_ollama.assert_called_once()
    args, kwargs = mock_ollama.call_args
    assert kwargs['model'] == "test-model"
    assert "Blog content" in kwargs['prompt']

def test_summarize_markdown_skips_existing(tmp_path, mocker):
    # Setup file with existing summary
    file_path = tmp_path / "test.md"
    content = "---\ntitle: Test Post\nsummary: Existing summary\n---\nBlog content"
    file_path.write_text(content, encoding='utf-8')
    
    # Mock generate_summary (should not be called)
    mock_gen = mocker.patch('scripts.summarize_md.generate_summary')
    
    summarize_markdown(str(file_path), overwrite=False)
    
    mock_gen.assert_not_called()
    
    # Verify file content remains unchanged
    post = frontmatter.load(str(file_path))
    assert post.metadata['summary'] == "Existing summary"

def test_summarize_markdown_overwrites_with_force(tmp_path, mocker):
    # Setup file with existing summary
    file_path = tmp_path / "test.md"
    content = "---\ntitle: Test Post\nsummary: Existing summary\n---\nBlog content"
    file_path.write_text(content, encoding='utf-8')
    
    # Mock generate_summary to return new summary
    mock_gen = mocker.patch('scripts.summarize_md.generate_summary', return_value="New summary")
    
    # Use overwrite=True
    summarize_markdown(str(file_path), overwrite=True)
    
    mock_gen.assert_called_once()
    
    # Verify file content is updated
    post = frontmatter.load(str(file_path))
    assert post.metadata['summary'] == "New summary"

def test_summarize_all(tmp_path, mocker):
    # Setup content directory
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    
    file1 = content_dir / "post1.md"
    file1.write_text("---\ntitle: Post 1\n---\nContent 1", encoding='utf-8')
    
    file2 = content_dir / "post2.md"
    file2.write_text("---\ntitle: Post 2\nsummary: Existing\n---\nContent 2", encoding='utf-8')
    
    # Mock CONTENT_DIR in scripts.summarize_md
    mocker.patch('scripts.summarize_md.CONTENT_DIR', str(content_dir))
    
    # Mock generate_summary
    mock_gen = mocker.patch('scripts.summarize_md.generate_summary', return_value="New summary")
    
    # Run summarize_all without overwrite
    summarize_all(overwrite=False)
    
    # Only post1 should be summarized
    assert mock_gen.call_count == 1
    
    # Run summarize_all with overwrite
    mock_gen.reset_mock()
    summarize_all(overwrite=True)
    
    # Both posts should be summarized
    assert mock_gen.call_count == 2
