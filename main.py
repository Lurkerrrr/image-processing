import multiprocessing
from utils.loader import load_images
from processing.worker import process_images_concurrently


def main():
    INPUT_DIR = "inputs"
    OUTPUT_DIR = "outputs"

    STEPS = [
        "grayscale",
        "blur",
        "sharpen",
    ]

    NUM_WORKERS = None

    print("=" * 50)
    print("   Image Processing Pipeline")
    print("=" * 50)

    print(f"\n[Main] Loading images from '{INPUT_DIR}'...")
    images = load_images(INPUT_DIR)

    if not images:
        print(f"[Main] No images found in '{INPUT_DIR}' folder.")
        print(f"[Main] Please add some images and try again.")
        return

    print(f"[Main] Found {len(images)} image(s) to process.")

    print(f"\n[Main] Starting concurrent processing...")
    results = process_images_concurrently(
        images=images,
        steps=STEPS,
        output_dir=OUTPUT_DIR,
        num_workers=NUM_WORKERS
    )

    print("\n" + "=" * 50)
    print(f"   Done! {len(results)} image(s) processed successfully.")
    print(f"   Check the '{OUTPUT_DIR}' folder for results.")
    print("=" * 50)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()