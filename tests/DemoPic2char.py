import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'tesseract'
#text = pytesseract.image_to_string(Image.open("./33.png"), lang='chi_sim')
text = pytesseract.image_to_string(Image.open("./33.png"))
print(text)
