import json

# 元ファイル名
INPUT = "auth_backup.json"
# 出力ファイル名
OUTPUT = "auth_backup.json"

# 1. バイナリで読んで UTF-8 としてデコード（BOM 付きにも対応）
with open(INPUT, "rb") as f:
    raw = f.read()
# UTF-8 BOM（0xEF,0xBB,0xBF）を自動的に取り除いてデコード
text = raw.decode("utf-8-sig")

# 2. JSON パース
data = json.loads(text)

# 3. 改めて UTF-8（BOMなし）で整形保存
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Cleaned fixture saved to {OUTPUT}")
