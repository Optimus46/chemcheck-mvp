import io
from typing import Union

import cv2
import numpy as np
import pytesseract
from PIL import Image


# NOTE FOR REPORT / ARCHITECTURE DIAGRAM:
#
# This module is the dedicated **OCR component** in the ChemCheck pipeline.
# It is responsible for:
#   1. Accepting a raw uploaded image (from the UI)
#   2. Pre‑processing the image to reduce noise (grayscale + thresholding)
#   3. Running Tesseract OCR to obtain machine‑readable text
#
# In your system diagram, this can appear as a single block:
#   "OCR Engine (pre‑processing + Tesseract)".


def _load_image(image_file: Union[bytes, "io.BufferedReader"]) -> np.ndarray:
    """
    Load the uploaded image into an OpenCV (NumPy) array.

    Streamlit's uploader returns a file‑like object; PIL can open it,
    and we then convert it to an array that OpenCV can process.
    """
    pil_img = Image.open(image_file).convert("RGB")
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def _preprocess_for_ocr(image_bgr: np.ndarray) -> np.ndarray:
    """
    Apply simple, robust pre‑processing steps to improve OCR quality.

    The goal is not deep image enhancement, but a lightweight pipeline
    that is easy to explain:
      - Convert to grayscale
      - Apply adaptive thresholding to handle uneven lighting / noise
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding is more robust to varying illumination than a single
    # global threshold, which is why it is commonly used in OCR pre‑processing.
    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,   # block size
        10,   # constant subtracted from mean
    )
    return processed


def extract_text(image_file) -> str:
    """
    High‑level OCR function used by the rest of the system.

    Parameters
    ----------
    image_file :
        File‑like object from the UI (e.g. Streamlit's file_uploader).

    Returns
    -------
    str
        Raw text extracted from the label image.

    Explanation for report / viva
    -----------------------------
    - This function calls the internal helpers to:
        1) load the raw image,
        2) pre‑process it to reduce noise,
        3) run Tesseract OCR.
    - This separation of concerns makes the OCR pipeline easy to show in
      an architecture diagram and to upgrade later (e.g. different filters
      or a different OCR engine) without changing the rest of the system.
    """
    image_bgr = _load_image(image_file)
    processed = _preprocess_for_ocr(image_bgr)
    text = pytesseract.image_to_string(processed)
    return text
