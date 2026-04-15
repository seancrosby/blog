import os
import pytest
from PIL import Image
from scripts.resize_images import resize_image

def test_resize_image_large(tmp_path):
    # Create a large image
    image_path = tmp_path / "test_large.jpg"
    with Image.new("RGB", (2000, 1000)) as img:
        img.save(image_path)
    
    # Resize it
    max_size = 1200
    resized = resize_image(str(image_path), max_size)
    
    assert resized is True
    with Image.open(image_path) as img:
        width, height = img.size
        assert width == 1200
        assert height == 600

def test_resize_image_small(tmp_path):
    # Create a small image
    image_path = tmp_path / "test_small.jpg"
    with Image.new("RGB", (800, 600)) as img:
        img.save(image_path)
    
    # Attempt to resize it
    max_size = 1200
    resized = resize_image(str(image_path), max_size)
    
    assert resized is False
    with Image.open(image_path) as img:
        width, height = img.size
        assert width == 800
        assert height == 600

def test_resize_image_square(tmp_path):
    # Create a large square image
    image_path = tmp_path / "test_square.jpg"
    with Image.new("RGB", (2000, 2000)) as img:
        img.save(image_path)
    
    # Resize it
    max_size = 1200
    resized = resize_image(str(image_path), max_size)
    
    assert resized is True
    with Image.open(image_path) as img:
        width, height = img.size
        assert width == 1200
        assert height == 1200
