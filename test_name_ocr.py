from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image = Image.open("data/raw_images/test.png")

name_area = image.crop((460,250,650,900))

name_gray = name_area.convert("L")
name_big = name_gray.resize((name_gray.width * 3,name_gray.height * 3))
name_bw = name_big.point(lambda x: 0 if x < 180 else 255)

name_bw.save("name_test.png")

name_text = pytesseract.image_to_string(
  name_bw,
  lang="jpn+eng",
  config="--psm 6"
)
print(name_text)