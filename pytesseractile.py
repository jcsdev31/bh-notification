import pytesseract
from PIL import Image

img_file = "images/cropped_raw.png"
img = Image.open(img_file)

ocr_result = pytesseract.image_to_string(img, config="--psm 6")
print(ocr_result)