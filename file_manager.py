"""
file_manager.py
-----------------
Everything to do with the filesystem: listing input PDFs, building
safe/unique output filenames, and copying files into renamed_pdfs/.
Nothing in here ever deletes or moves the original -- files are
always copied, so input_pdfs/ is left untouched.
"""

import os
import re
import shutil
from typing import List

import config
from logger import get_logger

logger = get_logger(__name__)


def ensure_directories() -> None:
    os.makedirs(config.INPUT_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)


def list_input_pdfs() -> List[str]:
    """Return full paths of every .pdf file in input_pdfs/."""
    if not os.path.isdir(config.INPUT_DIR):
        return []

    pdfs = [
        os.path.join(config.INPUT_DIR, f)
        for f in sorted(os.listdir(config.INPUT_DIR))
        if f.lower().endswith(".pdf")
    ]
    return pdfs


def sanitize_filename(name: str) -> str:
    """Strip characters that aren't safe in filenames, replace spaces with underscores."""
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_\-]", "", name)
    return name or "Unnamed"


def make_unique_path(base_name: str) -> str:
    """
    Turn 'Adjei_Kwame' into a full output path, adding _2, _3, ...
    if that name is already taken in renamed_pdfs/.
    """
    candidate = f"{base_name}{config.OUTPUT_EXTENSION}"
    full_path = os.path.join(config.OUTPUT_DIR, candidate)

    counter = 2
    while os.path.exists(full_path):
        candidate = f"{base_name}_{counter}{config.OUTPUT_EXTENSION}"
        full_path = os.path.join(config.OUTPUT_DIR, candidate)
        counter += 1

    return full_path


def copy_and_rename(source_path: str, new_base_name: str) -> str:
    """Copy source_path into renamed_pdfs/ under a safe, unique name. Returns the new path."""
    safe_name = sanitize_filename(new_base_name)
    destination = make_unique_path(safe_name)

    shutil.copy2(source_path, destination)
    logger.info(f"'{os.path.basename(source_path)}' -> '{os.path.basename(destination)}'")

    return destination
