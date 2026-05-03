from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from pipeline.base import ImagePipeline, filter_step


class ImageFilters(ImagePipeline):
    """
    Collection of image filters, each registered automatically
    by the PipelineMeta metaclass via the @filter_step decorator.
    """

    @filter_step("grayscale")
    def grayscale(self, image: Image.Image) -> Image.Image:
        """Convert image to grayscale."""
        return image.convert("L").convert("RGB")

    @filter_step("blur")
    def blur(self, image: Image.Image) -> Image.Image:
        """Apply Gaussian blur to the image."""
        return image.filter(ImageFilter.GaussianBlur(radius=2))

    @filter_step("sharpen")
    def sharpen(self, image: Image.Image) -> Image.Image:
        """Sharpen the image."""
        return image.filter(ImageFilter.SHARPEN)

    @filter_step("edge_detection")
    def edge_detection(self, image: Image.Image) -> Image.Image:
        """Detect edges in the image."""
        return image.filter(ImageFilter.FIND_EDGES)

    @filter_step("brighten")
    def brighten(self, image: Image.Image) -> Image.Image:
        """Increase image brightness by 50%."""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.5)

    @filter_step("darken")
    def darken(self, image: Image.Image) -> Image.Image:
        """Decrease image brightness by 50%."""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(0.5)

    @filter_step("increase_contrast")
    def increase_contrast(self, image: Image.Image) -> Image.Image:
        """Increase image contrast."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)

    @filter_step("invert")
    def invert(self, image: Image.Image) -> Image.Image:
        """Invert all pixel colors using NumPy."""
        img_array = np.array(image)
        inverted = 255 - img_array
        return Image.fromarray(inverted.astype(np.uint8))

    @filter_step("flip_horizontal")
    def flip_horizontal(self, image: Image.Image) -> Image.Image:
        """Flip the image horizontally using NumPy."""
        img_array = np.array(image)
        flipped = np.fliplr(img_array)
        return Image.fromarray(flipped.astype(np.uint8))

    @filter_step("flip_vertical")
    def flip_vertical(self, image: Image.Image) -> Image.Image:
        """Flip the image vertically using NumPy."""
        img_array = np.array(image)
        flipped = np.flipud(img_array)
        return Image.fromarray(flipped.astype(np.uint8))