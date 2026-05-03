import multiprocessing
from PIL import Image
from pipeline.filters import ImageFilters
from utils.loader import save_image


def process_single_image(args: tuple) -> str:
    """
    Process a single image by running it through the pipeline.
    This function runs in a separate worker process.

    :param args: Tuple of (filename, image, steps, output_dir)
    :return: Filename of the processed image
    """
    filename, image, steps, output_dir = args
    pipeline = ImageFilters()
    processed_image = pipeline.run(image, steps)
    save_image(processed_image, filename, output_dir)
    return filename


def process_images_concurrently(
    images: list[tuple[str, Image.Image]],
    steps: list[str],
    output_dir: str,
    num_workers: int = None
) -> list[str]:
    """
    Process multiple images concurrently using a multiprocessing pool.

    :param images: List of (filename, image) tuples
    :param steps: List of filter names to apply
    :param output_dir: Directory to save processed images
    :param num_workers: Number of worker processes (defaults to CPU count)
    :return: List of processed filenames
    """
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    print(f"\n[Worker] Starting processing with {num_workers} worker processes")
    print(f"[Worker] Filters to apply: {steps}")
    print(f"[Worker] Images to process: {len(images)}\n")

    args_list = [
        (filename, image, steps, output_dir)
        for filename, image in images
    ]

    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(process_single_image, args_list)

    print(f"\n[Worker] Processing complete! {len(results)} images processed.")
    return results