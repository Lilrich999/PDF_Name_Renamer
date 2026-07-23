# PDF Name Renamer

Scans each PDF in `input_pdfs/`, OCRs the first page, tries to detect a
person's name on it, and copies the file into `renamed_pdfs/` under that
name (e.g. `Adjei_Kwame.pdf`). If no name can be detected, it falls back
to a random placeholder name so nothing is skipped.

## 1. Set up the virtual environment

```bash
cd PDF_Name_Renamer
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## 2. Install system dependencies

This project needs two system tools outside of pip:

- **Tesseract OCR** (reads text from images)
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: `brew install tesseract`
  - Linux: `sudo apt install tesseract-ocr`
- **Poppler** (converts PDF pages to images)
  - Windows: https://github.com/oschwartz10612/poppler-windows/releases
  - macOS: `brew install poppler`
  - Linux: `sudo apt install poppler-utils`

If either tool isn't on your system PATH, point to it directly in
`config.py`:

```python
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler-24.02.0\Library\bin"
```

## 3. Add your PDFs

Drop your scanned PDFs into `input_pdfs/`.

## 4. Run it

```bash
python main.py
```

Renamed copies land in `renamed_pdfs/`. Nothing in `input_pdfs/` is
ever changed or deleted -- files are always copied, not moved.
A full run log is written to `log.txt`.

## How name detection works

`name_detector.py` first looks for labeled fields like `Surname:` and
`Other Names:`, which is how most Ghanaian bio-data/ID forms are laid
out (edit the label lists in `config.py` if your documents use
different wording). If no labels are found, it falls back to
grabbing the first line that looks like a plausible name (2-4
capitalized words, no digits).

## Tuning

Everything adjustable lives in `config.py`: OCR language and page
segmentation mode, image preprocessing (contrast, upscaling,
denoising, thresholding), how many pages to scan per PDF, and the
label words used for name detection. If OCR accuracy is poor on your
scans, start by raising `PDF_TO_IMAGE_DPI` and tweaking
`CONTRAST_FACTOR`.

## Project layout

```
PDF_Name_Renamer/
├── main.py              # Entry point -- run this
├── config.py            # All settings
├── image_processing.py  # Cleans/enhances page images
├── ocr_engine.py         # PDF -> image -> text (Tesseract)
├── name_detector.py      # Finds a name inside OCR text
├── file_manager.py       # Copies/renames PDFs safely
├── random_names.py       # Fallback names when detection fails
├── logger.py             # Shared logging setup
├── requirements.txt
├── log.txt               # Created automatically on first run
├── input_pdfs/           # Put your PDFs here
└── renamed_pdfs/         # Renamed copies appear here
```
