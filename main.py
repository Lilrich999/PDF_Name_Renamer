"""
main.py
--------
Entry point. Run this file to process every PDF in input_pdfs/:

    1. Convert each PDF's first page(s) to an image.
    2. Clean up the image for OCR.
    3. Extract text with Tesseract.
    4. Try to detect a name in that text.
    5. Copy the PDF into renamed_pdfs/ under that name
       (or a random fallback name if detection fails).

Usage:
    python main.py
"""

import os

import config
import file_manager
import ocr_engine
import name_detector
import random_names
from logger import get_logger

logger = get_logger(__name__)


def process_pdf(pdf_path: str) -> None:
    filename = os.path.basename(pdf_path)
    logger.info(f"Processing '{filename}'...")

    ocr_text = ocr_engine.extract_text_from_pdf(pdf_path)
    detected_name = name_detector.detect_name(ocr_text)

    if detected_name:
        logger.info(f"Detected name for '{filename}': {detected_name}")
        base_name = detected_name
    else:
        base_name = random_names.generate_random_name()
        logger.warning(
            f"No name detected for '{filename}'. Using fallback name: {base_name}"
        )

    file_manager.copy_and_rename(pdf_path, base_name)


def main() -> None:
    file_manager.ensure_directories()

    pdfs = file_manager.list_input_pdfs()
    if not pdfs:
        logger.warning(f"No PDFs found in '{config.INPUT_DIR}'. Nothing to do.")
        return

    logger.info(f"Found {len(pdfs)} PDF(s) to process.")

    success_count = 0
    for pdf_path in pdfs:
        try:
            process_pdf(pdf_path)
            success_count += 1
        except Exception as exc:
            logger.error(f"Unexpected error processing '{pdf_path}': {exc}")

    logger.info(f"Done. {success_count}/{len(pdfs)} PDF(s) processed successfully.")
    logger.info(f"Renamed PDFs are in: {config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
