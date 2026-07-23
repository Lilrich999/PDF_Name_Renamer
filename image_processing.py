"""
image_processing.py
--------------------
Cleans and enhances a page image before it goes to OCR. Cleaner
input almost always means more accurate text extraction, so this
runs on every page.
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import config


def preprocess_image(image: Image.Image) -> Image.Image:
    """Run the full cleanup pipeline based on config.py settings."""
    if config.UPSCALE_FACTOR and config.UPSCALE_FACTOR != 1:
        image = _upscale(image, config.UPSCALE_FACTOR)

    if config.GRAYSCALE:
        image = _to_grayscale(image)

    if config.DENOISE:
        image = _denoise(image)

    if config.CONTRAST_FACTOR and config.CONTRAST_FACTOR != 1.0:
        image = _boost_contrast(image, config.CONTRAST_FACTOR)

    if config.THRESHOLD:
        image = _binarize(image)

    return image


def _upscale(image: Image.Image, factor: float) -> Image.Image:
    new_size = (int(image.width * factor), int(image.height * factor))
    return image.resize(new_size, Image.LANCZOS)


def _to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")


def _denoise(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.MedianFilter(size=3))


def _boost_contrast(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def _binarize(image: Image.Image, threshold: int = 150) -> Image.Image:
    """Simple global threshold -> pure black/white image."""
    grayscale = image.convert("L")
    array = np.array(grayscale)
    array = np.where(array > threshold, 255, 0).astype(np.uint8)
    return Image.fromarray(array)
