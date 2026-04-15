import argparse
import os
from PIL import Image

def resize_image(image_path, max_size):
    """
    Resize an image to fit within max_size x max_size while maintaining aspect ratio.
    If the image is already smaller than max_size in both dimensions, skip resizing.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width <= max_size and height <= max_size:
                print(f"Skipping {image_path} (size: {width}x{height} is within {max_size}px)")
                return False

            # Calculate new dimensions
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))

            print(f"Resizing {image_path} from {width}x{height} to {new_width}x{new_height}")
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save the image back, overwriting the original
            img.save(image_path, optimize=True)
            return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Resize images for web display.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Resize all images in the assets/images directory.")
    group.add_argument("--file", type=str, help="Resize a specific image file.")
    parser.add_argument("--max-size", type=int, default=1200, help="Maximum width or height for the resized image (default: 1200).")
    parser.add_argument("--img-dir", type=str, default="assets/images", help="Directory containing images (default: assets/images).")

    args = parser.parse_args()

    supported_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    if args.all:
        if not os.path.isdir(args.img_dir):
            print(f"Error: Directory {args.img_dir} does not exist.")
            return

        resized_count = 0
        for filename in os.listdir(args.img_dir):
            if filename.lower().endswith(supported_extensions):
                image_path = os.path.join(args.img_dir, filename)
                if resize_image(image_path, args.max_size):
                    resized_count += 1
        print(f"Finished. Resized {resized_count} images.")
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File {args.file} does not exist.")
            return
        
        if not args.file.lower().endswith(supported_extensions):
            print(f"Error: File extension of {args.file} is not supported.")
            return

        if resize_image(args.file, args.max_size):
            print("Successfully resized image.")
        else:
            print("Image was not resized.")

if __name__ == "__main__":
    main()
