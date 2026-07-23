"""
config.py
---------
All project-wide settings live here so nothing is hard-coded
in the other modules. Change paths, DPI, or OCR options in
one place.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input_pdfs")
OUTPUT_DIR = os.path.join(BASE_DIR, "renamed_pdfs")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")

# ---------------------------------------------------------------------------
# PDF -> Image conversion
# ---------------------------------------------------------------------------
# Only the first N pages are scanned for a name (most ID/bio-data pages
# have the name on page 1). Increase if names appear later in your docs.
PAGES_TO_SCAN = 1

# Higher DPI = better OCR accuracy but slower conversion.
PDF_TO_IMAGE_DPI = 150

# Path to the poppler "bin" folder if it's not on your system PATH.
# Leave as None if `pdftoppm`/`pdfinfo` already work from a terminal.
POPPLER_PATH = r"C:\Users\Pc\Desktop\poppler-26.02.0\Library\bin"

# ---------------------------------------------------------------------------
# Tesseract OCR
# ---------------------------------------------------------------------------
# Leave as None if `tesseract` is already on your system PATH.
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OCR_LANGUAGE = "eng"

# Tesseract page segmentation mode. 3 = fully automatic (default),
# 6 = assume a single uniform block of text (often better for forms).
OCR_CONFIG = "--psm 6"

# ---------------------------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------------------------
GRAYSCALE = True
DENOISE = False
THRESHOLD = True          # binarize (black/white) the image before OCR
CONTRAST_FACTOR = 1.5     # >1 boosts contrast, 1.0 = unchanged
UPSCALE_FACTOR = 1         # enlarge small/low-res scans before OCR

# ---------------------------------------------------------------------------
# Name detection
# ---------------------------------------------------------------------------
# Labels commonly found on Ghanaian bio-data / ID forms. Detection is
# case-insensitive and tries these in order.
SURNAME_LABELS = ["surname", "last name", "family name"]
OTHER_NAMES_LABELS = ["other names", "other name", "first name", "given name", "given names"]

# Max number of words allowed in a detected name (guards against grabbing
# a whole misread sentence as a "name").
MAX_NAME_WORDS = 4

# ---------------------------------------------------------------------------
# File naming
# ---------------------------------------------------------------------------
OUTPUT_EXTENSION = ".pdf"
# If a name is already used, files are suffixed _2, _3, ... automatically.

# ---------------------------------------------------------------------------
# Fallback random names (used when OCR/name detection fails)
# ---------------------------------------------------------------------------
RANDOM_NAME_PREFIX = "Unknown"