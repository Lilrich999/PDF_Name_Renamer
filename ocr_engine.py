"""
ocr_engine.py
-------------
Handles turning a PDF's pages into images (pdf2image) and turning
images into text (pytesseract). Everything Tesseract-related is
isolated here so config.py is the only place you need to touch to
point at a different Tesseract/poppler install.
"""

from typing import List
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

import config
from logger import get_logger

logger = get_logger(__name__)

Image.MAX_IMAGE_PIXELS = None  # trust our own scans; disable Pillow's decompression-bomb limit

if config.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD


def pdf_to_images(pdf_path: str) -> List[Image.Image]:
    """Convert the first PAGES_TO_SCAN pages of a PDF into PIL images."""
    try:
        kwargs = {
            "dpi": config.PDF_TO_IMAGE_DPI,
            "first_page": 1,
            "last_page": config.PAGES_TO_SCAN,
        }
        if config.POPPLER_PATH:
            kwargs["poppler_path"] = config.POPPLER_PATH

        images = convert_from_path(pdf_path, **kwargs)
        return images
    except Exception as exc:
        logger.error(f"Failed to convert '{pdf_path}' to images: {exc}")
        return []


def extract_text(image: Image.Image) -> str:
    """Run OCR on a single (already-preprocessed) image."""
    try:
        text = pytesseract.image_to_string(
            image, lang=config.OCR_LANGUAGE, config=config.OCR_CONFIG
        )
        return text
    except Exception as exc:
        logger.error(f"OCR failed on an image: {exc}")
        return ""


def extract_text_from_pdf(pdf_path: str) -> str:
    """Convenience wrapper: PDF path -> preprocessed images -> combined text."""
    from image_processing import preprocess_image  # local import avoids a cycle

    images = pdf_to_images(pdf_path)
    combined_text = []

    for page_num, image in enumerate(images, start=1):
        cleaned = preprocess_image(image)
        text = extract_text(cleaned)
        logger.debug(f"OCR text from page {page_num} of '{pdf_path}':\n{text}")
        combined_text.append(text)

    return "\n".join(combined_text)