import csv #csvを扱うための記述 エクセルの保存形式としてよく使われる。読んだり書きこんだり行ごとに取り出したり表形式データを扱える
# 名前,ダメージ,K/D
# ローブ,6443,2/0 こんな感じで,ごとに区切ってあるやつがcsv
# csv.reader(file)fileに入ってる名前、点数、田中、80みたいなのを⇒["名前","点数","田中","80"]みたいなリストに変換してくれる
import re #文字列の検索や特定パターンの抜出を行える  ダメージ 6443 K/D 2/D　⇒　というデータ
# text = "ダメージ6443" 
# result = re.findall(r"\d+", text) r⇒その中のバックスラッシュを単なる文字として扱える \d⇒数字一文字　+　⇒1回以上続く　　数字が一回以上連続している部分を探せ
# print(result)                        ⇒　['6443']
import os
import glob
import shutil


INPUT_FILES = "data/raw/*.txt"
OUTPUT_FILE = "data/results/my_result.csv"
MY_NAME = "ローブ"
PROCESSED_DIR = "data/processed"


# プレイヤーかどうかを判定する
def is_player_start(line):
  if line in ["MVP","ダメージ","K/D","支援","味方を撃破","被ロック時間"]:
    # line in ⇒ lineに含まれているか？の意味　見出しならプレイヤーじゃない
    # lineがこれらの内容ならFalseを返す
    return False
  
  if re.fullmatch(r"\d+", line):
    # 数字だけならプレイヤー名ではない　数字だけならfalseを返す
    return False
  
  if re.fullmatch(r"\d+/\d+", line):
    # \d / \d 数字/数字の組み合わせかどうか
    return False
  
  if re.fullmatch(r"\d+%", line):
    # 被ロック判定　63%　みたいなやつ
    return False
  
  # この辺が引っかからないならおそらくプレイヤー名ということでTrue
  return True

# 名前をきれいにする、余計な文字を取り除く
def clean_name(line):
  return line.replace("▶","").replace("MVP","").strip()

players = []

# INPUT_FILEの中身*txtを全部探してinput_txtにいれる
input_files = glob.glob(INPUT_FILES)
for input_file in input_files:
   

  with open(input_file, "r", encoding="utf-8")as f:
          # line.strip()したものを⇒forで回す⇒if line.strip()を満たしていたら追加
          lines = [line.strip() for line in f if line.strip()]

# enumerate使うと番号も振れる　i=1 name=ローブみたいに取り出したものに番号が振れる
  for i, line in enumerate(lines):
  #  ▶もMVPも描いてない名前を上で作っているのでそれを持ってきて
    name = clean_name(line)

    if i + 6 < len(lines):
        # 振られた番号をもとに次の行を見れるようにする
        # ocrの結果が縦に行で並んでいるから
        # ローブ
        # 6443みたいになっているので順番で取っている
        damage = lines[i + 1]
        kd = lines[i + 2]
        support = lines[i + 3]
        ally_kill = lines[i + 4]
        lock_time = lines[i + 5]
        burst_kill = lines[i + 6]

        if(
          is_player_start(line)
          and re.fullmatch(r"\d+", damage)
          and re.fullmatch(r"\d+/\d+", kd)
          and re.fullmatch(r"\d+", support)
          and re.fullmatch(r"\d+", ally_kill)
          and re.fullmatch(r"\d+%", lock_time)
          and re.fullmatch(r"\d+", burst_kill)
        ):
          if name == MY_NAME:
              
            players.append({
              "プレイヤー名": name,
              "ダメージ": damage,
              "K/D": kd,
              "支援": support,
              "味方撃破": ally_kill,
              "被ロック": lock_time,
              "バースト撃破": burst_kill,
          })


fieldnames=["プレイヤー名", "ダメージ", "K/D", "支援", "味方撃破", "被ロック", "バースト撃破"]

expected_header = ",".join(fieldnames)

header_exists = False

if os.path.exists(OUTPUT_FILE):
   with open(OUTPUT_FILE, "r", encoding="utf-8-sig")as f:
      first_line = f.readline().strip()

      if first_line == expected_header:
         header_exists = True

with open(OUTPUT_FILE, "a", encoding="utf-8-sig", newline="") as f:
   writer = csv.DictWriter(
      f,
      fieldnames=fieldnames
   )

   if not header_exists:
    writer.writeheader()
   writer.writerows(players)

os.makedirs(PROCESSED_DIR, exist_ok=True)

for input_file in input_files:
   shutil.move(input_file, PROCESSED_DIR)

print(f"{len(players)}人分を抽出しました")
print(f"{OUTPUT_FILE}に保存しました")