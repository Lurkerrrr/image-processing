import os
from PIL import Image


def load_images(input_dir: str) -> list[tuple[str, Image.Image]]:
    """Load all images from the input directory."""
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    images = []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            filepath = os.path.join(input_dir, filename)
            img = Image.open(filepath).convert("RGB")
            images.append((filename, img))
            print(f"Loaded: {filename}")

    return images


def save_image(image: Image.Image, filename: str, output_dir: str) -> None:
    """Save a single processed image to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)
    print(f"Saved: {filename}")