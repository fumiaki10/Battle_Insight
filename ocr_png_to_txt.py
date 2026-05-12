from PIL import Image, ImageOps, ImageFilter #PILのImageを使う　画像処理ようのライブラリ
import pytesseract #ocr機能を使う　


#tesseractの位置を指定
pytesseract.pytesseract.tesseract_cmd = (
  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

#imageに画像データとして、メモリに変換した相対パスのtest.pngを格納
image = Image.open("test.png")

#左、上、右、下　この位置から内側を切り抜き
cropped = image.crop((0, 200, 1200, 900))

#グレースケール化
gray = cropped.convert("L")

# 横、縦幅2倍にする
big = gray.resize((gray.width * 2, gray.height * 2))

#中間色を消す　白黒をはっきりさせる
bw = big.point(lambda x: 0 if x < 160 else 255)

bw.save("processed.png")


#imageをstring型、日本語にしてocrにする
text = pytesseract.image_to_string(image, lang="jpn")

print(text)