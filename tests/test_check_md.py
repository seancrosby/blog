import os
import pytest
from scripts.check_md import generate_correction, launch_editor, check_markdown
import subprocess

def test_generate_correction(mocker):
    mock_ollama = mocker.patch('ollama.generate')
    mock_ollama.return_value = {'response': 'Corrected Content'}
    
    result = generate_correction("Original Content", model="test-model")
    
    assert result == "Corrected Content"
    mock_ollama.assert_called_once()
    args, kwargs = mock_ollama.call_args
    assert kwargs['model'] == "test-model"
    assert "Original Content" in kwargs['prompt']

def test_launch_editor_vimdiff_success(mocker):
    mock_run = mocker.patch('subprocess.run')
    result = launch_editor("file.md", "temp.md")
    
    assert result is True
    mock_run.assert_called_with(['vimdiff', '-c', 'windo set wrap', 'file.md', 'temp.md'], check=True)

def test_launch_editor_vimdiff_not_found_fallback_success(mocker):
    # Mock subprocess.run to fail on first call and succeed on second
    mock_run = mocker.patch('subprocess.run')
    mock_run.side_effect = [FileNotFoundError, None]
    
    result = launch_editor("file.md", "temp.md")
    
    assert result is True
    assert mock_run.call_count == 2
    mock_run.assert_any_call(['vimdiff', '-c', 'windo set wrap', 'file.md', 'temp.md'], check=True)
    mock_run.assert_any_call(['vim', '-d', 'file.md', 'temp.md'], check=True)

def test_check_markdown_flow(tmp_path, mocker):
    # Setup files
    file_path = tmp_path / "test.md"
    file_path.write_text("Original content", encoding='utf-8')
    
    # Mock dependencies
    mocker.patch('scripts.check_md.generate_correction', return_value="Corrected content")
    mocker.patch('scripts.check_md.launch_editor', return_value=True)
    mock_input = mocker.patch('builtins.input', side_effect=["", "y"]) # Enter for vimdiff, 'y' for overwrite
    mock_shutil_copy = mocker.patch('shutil.copy2')
    
    check_markdown(str(file_path))
    
    # Verify
    mock_shutil_copy.assert_called_once()
    assert mock_input.call_count == 2

def test_check_markdown_no_overwrite(tmp_path, mocker):
    # Setup files
    file_path = tmp_path / "test.md"
    file_path.write_text("Original content", encoding='utf-8')
    
    # Mock dependencies
    mocker.patch('scripts.check_md.generate_correction', return_value="Corrected content")
    mocker.patch('scripts.check_md.launch_editor', return_value=True)
    mock_input = mocker.patch('builtins.input', side_effect=["", "n"]) # Enter for vimdiff, 'n' for no overwrite
    mock_shutil_copy = mocker.patch('shutil.copy2')
    
    check_markdown(str(file_path))
    
    # Verify
    mock_shutil_copy.assert_not_called()
