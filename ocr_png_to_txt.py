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

#ダメージ列を取る
damage_area = image.crop((650,250,950,920))

damage_area.save("damage_test.png")

#グレースケール化
gray = cropped.convert("L")

# 横、縦幅2倍にする
big = gray.resize((gray.width * 2, gray.height * 2))

#中間色を消す　白黒をはっきりさせる
bw = big.point(lambda x: 0 if x < 160 else 255)

bw.save("processed.png")

#imageをstring型、日本語にしてocrにする
text = pytesseract.image_to_string(
  damage_area,
  lang="jpn",
  config="--psm 6 -c tessedit_char_whitelist=0123456789"
)

#k/dを取りに行く
kd_area = image.crop((950,250,1150,920))
kd_gray = kd_area.convert("L")
kd_big = kd_gray.resize((kd_gray.width * 3, kd_gray.height * 3))
kd_bw = kd_big.point(lambda x: 0 if x < 180 else 255)

kd_bw.save("kd_test.png")

kd_text = pytesseract.image_to_string(
  kd_bw,
  lang="eng",
  config="--psm 6 -c tessedit_char_whitelist=0123456789/"
)

print(kd_text)