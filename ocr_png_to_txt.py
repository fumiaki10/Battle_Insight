from PIL import Image, ImageOps, ImageFilter #PILのImageを使う　画像処理ようのライブラリ
import pytesseract #ocr機能を使う　
import os 
import glob

#tesseractの位置を指定
pytesseract.pytesseract.tesseract_cmd = (
  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


#imageに画像データとして、メモリに変換した相対パスのtest.pngを格納
INPUT_IMAGES = "data/raw_images/*.png"
OUTPUT_DIR = "data/raw/ローブ"

os.makedirs(OUTPUT_DIR, exist_ok=True)

image_files = glob.glob(INPUT_IMAGES)

for image_file in image_files:
  image = Image.open(image_file)

  base_name = os.path.splitext(os.path.basename(image_file))[0]
  output_path = os.path.join(OUTPUT_DIR, base_name + ".txt")
  

  #左、上、右、下　この位置から内側を切り抜き
  cropped = image.crop((0, 200, 1200, 900))

  #ダメージ列を取る
  damage_area = image.crop((650,250,950,920))

  damage_area.save("damage_test.png")

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

  #支援を取りに行く
  support_area = image.crop((1100,250,1250,920))

  support_gray = support_area.convert("L")
  support_big = support_gray.resize((support_gray.width * 3, support_gray.height * 3))
  support_bw = support_big.point(lambda x: 0 if x < 180 else 255)

  support_bw.save("support_test.png")

  support_text = pytesseract.image_to_string(
    support_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  #味方撃破を取りに行く
  ally_kill_area = image.crop((1250,250,1400,920))

  ally_kill_gray = ally_kill_area.convert("L")
  ally_kill_big = ally_kill_gray.resize((ally_kill_gray.width * 3, ally_kill_gray.height * 3))
  ally_kill_bw = ally_kill_big.point(lambda x: 0 if x < 180 else 255)

  ally_kill_bw.save("ally_kill_test.png")

  ally_kill_text = pytesseract.image_to_string(
    ally_kill_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  #被ロック時間を取りに行く
  lock_time_area = image.crop((1370,250,1630,920))

  lock_time_gray = lock_time_area.convert("L")
  lock_time_big = lock_time_gray.resize((lock_time_gray.width * 3, lock_time_gray.height * 3))
  lock_time_bw = lock_time_big.point(lambda x: 0 if x < 180 else 255)

  lock_time_bw.save("lock_time_test.png")

  lock_time_text = pytesseract.image_to_string(
    lock_time_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789%"
  )


  #バースト中の撃破を取りに行く
  burst_kill_area = image.crop((1620,250,1750,920))

  burst_kill_gray = burst_kill_area.convert("L")
  burst_kill_big = burst_kill_gray.resize((burst_kill_gray.width * 3, burst_kill_gray.height * 3))
  burst_kill_bw = burst_kill_big.point(lambda x: 0 if x < 180 else 255)

  burst_kill_bw.save("burst_kill_test.png")

  burst_kill_text = pytesseract.image_to_string(
    burst_kill_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  #上記で切り取った部分を格納⇒整理する
  def to_list(text):
    return[line.strip() for line in text.splitlines() if line.strip()]

  damage_list = to_list(text)
  kd_list = to_list(kd_text)
  support_list = to_list(support_text)
  ally_kill_list = to_list(ally_kill_text)
  lock_time_list = to_list(lock_time_text)
  burst_kill_list = to_list(burst_kill_text)

  # 上手くとれていないので手打ち
  name = ["ローブ","player2","player3","player4"]

  output_lines = []

  player_count = min(
    len(damage_list),
    len(kd_list),
    len(support_list),
    len(ally_kill_list),
    len(lock_time_list),
    len(burst_kill_list)
  )

  for i in range(player_count):

  # for i in range(4):
    output_lines.append(name[i])
    output_lines.append(damage_list[i])
    output_lines.append(kd_list[i])
    output_lines.append(support_list[i])
    output_lines.append(ally_kill_list[i])
    output_lines.append(lock_time_list[i])
    output_lines.append(burst_kill_list[i])

  with open(output_path, "w", encoding="utf-8")as f:
    f.write("\n".join(output_lines))

  print(f"{output_path}を作成しました")