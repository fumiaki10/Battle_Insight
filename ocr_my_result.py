from PIL import Image
import pytesseract
import os
import glob

pytesseract.pytesseract.tesseract_cmd = (
  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

INPUT_IMAGES = "data/raw_images/*.png"
OUTPUT_DIR = "data/raw/ローブ"
TARGET_NAME = "ローブ"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def to_list(text):
  return [line.strip() for line in text.splitlines() if line.strip()]

def clean_name_line(line):
  return (
    line
    .replace("MVP", "")
    .replace("“", "")
    .replace('"', "")
    .replace("▶", "")
    .strip()
  )

image_files = glob.glob(INPUT_IMAGES)

for image_file in image_files:
  image = Image.open(image_file)

  base_name = os.path.splitext(os.path.basename(image_file))[0]
  output_path = os.path.join(OUTPUT_DIR, base_name + ".txt")

  # 名前を取りに行く
  name_area = image.crop((460, 250, 650, 900))
  name_gray = name_area.convert("L")
  name_big = name_gray.resize((name_gray.width * 3, name_gray.height * 3))
  name_bw = name_big.point(lambda x: 0 if x < 180 else 255)

  name_bw.save("name_test.png")

  name_text = pytesseract.image_to_string(
    name_bw,
    lang="jpn+eng",
    config="--psm 6"
  )

  name_list = [clean_name_line(line) for line in to_list(name_text)]
  name_list = [name for name in name_list if name]

  # ダメージ列を取る
  damage_area = image.crop((730, 250, 950, 920))
  damage_text = pytesseract.image_to_string(
    damage_area,
    lang="jpn",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  # K/Dを取る
  kd_area = image.crop((950, 250, 1150, 920))
  kd_gray = kd_area.convert("L")
  kd_big = kd_gray.resize((kd_gray.width * 3, kd_gray.height * 3))
  kd_bw = kd_big.point(lambda x: 0 if x < 180 else 255)

  kd_text = pytesseract.image_to_string(
    kd_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789/"
  )

  # 支援を取る
  support_area = image.crop((1070, 250, 1280, 950))
  support_gray = support_area.convert("L")
  support_big = support_gray.resize((support_gray.width * 3, support_gray.height * 3))
  support_bw = support_big.point(lambda x: 0 if x < 180 else 255)

  support_text = pytesseract.image_to_string(
    support_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  # 味方撃破を取る
  ally_kill_area = image.crop((1250, 250, 1400, 920))
  ally_kill_gray = ally_kill_area.convert("L")
  ally_kill_big = ally_kill_gray.resize((ally_kill_gray.width * 3, ally_kill_gray.height * 3))
  ally_kill_bw = ally_kill_big.point(lambda x: 0 if x < 180 else 255)

  ally_kill_text = pytesseract.image_to_string(
    ally_kill_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  # 被ロック時間を取る
  lock_time_area = image.crop((1370, 250, 1630, 920))
  lock_time_gray = lock_time_area.convert("L")
  lock_time_big = lock_time_gray.resize((lock_time_gray.width * 3, lock_time_gray.height * 3))
  lock_time_bw = lock_time_big.point(lambda x: 0 if x < 180 else 255)

  lock_time_text = pytesseract.image_to_string(
    lock_time_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789%"
  )

  # バースト中の撃破を取る
  burst_kill_area = image.crop((1620, 250, 1750, 920))
  burst_kill_gray = burst_kill_area.convert("L")
  burst_kill_big = burst_kill_gray.resize((burst_kill_gray.width * 3, burst_kill_gray.height * 3))
  burst_kill_bw = burst_kill_big.point(lambda x: 0 if x < 180 else 255)

  burst_kill_text = pytesseract.image_to_string(
    burst_kill_bw,
    lang="eng",
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
  )

  damage_list = to_list(damage_text)
  kd_list = to_list(kd_text)
  support_list = to_list(support_text)
  ally_kill_list = to_list(ally_kill_text)
  lock_time_list = to_list(lock_time_text)
  burst_kill_list = to_list(burst_kill_text)

  # ローブがいないリザルトは保存しない
  if TARGET_NAME not in name_list:
    print(f"{base_name}: {TARGET_NAME}が見つからないのでスキップ")
    print(name_list)
    continue

  my_index = name_list.index(TARGET_NAME)
  print("name_list:", name_list)
  print("my_index:", my_index)
  print("damage_list:", damage_list)
  print("kd_list:", kd_list)
  print("support_list:", support_list)
  print("ally_kill_list:", ally_kill_list)
  print("lock_time_list:", lock_time_list)
  print("burst_kill_list:", burst_kill_list)

  # 各リストにその行が存在するか確認
  if my_index >= min(
    len(damage_list),
    len(kd_list),
    len(support_list),
    len(ally_kill_list),
    len(lock_time_list),
    len(burst_kill_list)
  ):
    print(f"{base_name}: データ数が足りないのでスキップ")
    continue

  output_lines = [
    TARGET_NAME,
    damage_list[my_index],
    kd_list[my_index],
    support_list[my_index],
    ally_kill_list[my_index],
    lock_time_list[my_index],
    burst_kill_list[my_index]
  ]

  with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

  print(f"{output_path}を作成しました")