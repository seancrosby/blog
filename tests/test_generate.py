import os
import pytest
import shutil
from scripts.generate import handle_custom_tags, SiteGenerator
from datetime import datetime, date
import frontmatter

def test_handle_custom_tags():
    text = "Check out this video: [youtube:dQw4w9WgXcQ]"
    expected = 'Check out this video: <div class="video-container"><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
    assert handle_custom_tags(text) == expected

def test_get_date_str_from_metadata_datetime():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", date=datetime(2023, 10, 27))
    assert gen.get_date_str(post, "dummy.md") == "2023-10-27"

def test_get_date_str_from_metadata_date():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", date=date(2023, 10, 27))
    assert gen.get_date_str(post, "dummy.md") == "2023-10-27"

def test_get_date_str_from_metadata_string():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", date="2023-10-27")
    assert gen.get_date_str(post, "dummy.md") == "2023-10-27"

def test_get_date_str_from_filesystem(mocker):
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("")
    # Use a UTC timestamp that avoids date shift across timezones for simplicity
    # 1698364800 is 2023-10-27 00:00:00 UTC
    # To be safe, we'll just check if it matches whatever strftime returns for that timestamp
    ts = 1698364800
    expected_date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    mock_mtime = mocker.patch('os.path.getmtime', return_value=ts)
    assert gen.get_date_str(post, "dummy.md") == expected_date

def test_get_title_from_metadata():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", title="Custom Title")
    assert gen.get_title(post, "dummy.md") == "Custom Title"

def test_get_title_from_content():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("# Header Title\nContent")
    assert gen.get_title(post, "dummy.md") == "Header Title"

def test_get_title_from_filename():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("Just content")
    assert gen.get_title(post, "hello-world.md") == "Hello World"

def test_get_tags_list():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", tags=["tag1", "tag2"])
    assert gen.get_tags(post) == ["tag1", "tag2"]

def test_get_tags_string():
    gen = SiteGenerator(template_dir='templates')
    post = frontmatter.Post("", tags="tag1, tag2")
    assert gen.get_tags(post) == ["tag1", "tag2"]

def test_process_post(tmp_path, mocker):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    post_file = content_dir / "test-post.md"
    post_file.write_text('---\ntitle: Test Post\ndate: 2023-10-27\ntags: test\n---\n# Hello\n[youtube:123]', encoding='utf-8')
    
    gen = SiteGenerator(content_dir=str(content_dir), template_dir='templates')
    post_data = gen.process_post("test-post.md")
    
    assert post_data['title'] == "Test Post"
    assert post_data['date'] == "2023-10-27"
    assert post_data['slug'] == "test-post.html"
    assert "<h1>Hello</h1>" in post_data['content']
    assert "iframe" in post_data['content']
    assert post_data['tags'] == ["test"]

def test_full_generate(tmp_path):
    # Setup mock content, templates, and assets
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "post1.md").write_text('---\ntitle: Post 1\ndate: 2023-10-01\ntags: news\n---\nContent 1', encoding='utf-8')
    (content_dir / "post2.md").write_text('---\ntitle: Post 2\ndate: 2023-10-02\ntags: tech, news\n---\nContent 2', encoding='utf-8')
    
    # We'll use the real templates but point to them
    template_dir = 'templates'
    output_dir = tmp_path / "public"
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    (assets_dir / "test.css").write_text("body { color: red; }")
    
    gen = SiteGenerator(
        content_dir=str(content_dir),
        template_dir=template_dir,
        output_dir=str(output_dir),
        assets_dir=str(assets_dir)
    )
    
    posts, sorted_tags = gen.generate()
    
    # Verify outputs
    assert len(posts) == 2
    assert posts[0]['title'] == "Post 2" # Sorted newest first
    
    assert (output_dir / "post1.html").exists()
    assert (output_dir / "post2.html").exists()
    assert (output_dir / "index.html").exists()
    assert (output_dir / "tags.html").exists()
    assert (output_dir / "assets" / "test.css").exists()
    
    # Check tags
    tags_dict = dict(sorted_tags)
    assert "news" in tags_dict
    assert "tech" in tags_dict
    assert len(tags_dict["news"]) == 2
    assert len(tags_dict["tech"]) == 1
