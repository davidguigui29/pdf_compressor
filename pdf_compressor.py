import fitz  # PyMuPDF
from PIL import Image
import os

def compress_scanned_pdf(input_pdf_path, output_pdf_path, quality=50, dpi=100):
    pdf_document = fitz.open(input_pdf_path)
    new_doc = fitz.open()
    temp_image_paths = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72), colorspace=fitz.csRGB)
        img_path = f"temp_page_{page_num}.jpg"
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.save(img_path, "JPEG", quality=quality)
        temp_image_paths.append(img_path)

        rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = new_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(rect, filename=img_path)

    new_doc.save(output_pdf_path, deflate=True)
    new_doc.close()
    pdf_document.close()

    for img_path in temp_image_paths:
        os.remove(img_path)
