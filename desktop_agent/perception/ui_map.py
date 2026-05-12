import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_ui_elements(image_path):

    image = Image.open(image_path)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    elements = []

    for i, text in enumerate(data["text"]):

        text = text.strip()

        if not text:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        elements.append({
            "text": text,
            "x": x,
            "y": y,
            "width": w,
            "height": h
        })

    return elements