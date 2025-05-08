import sqlite3

db_path = r"C:\Users\kitazawa\OneDrive - NRIセキュアテクノロジーズ株式会社\アプリ\ClientPortal\clientPortal\db.sqlite3"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# check_sheetアプリに関連する全テーブルを取得してDROP
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'check_sheet_%';")
tables = cur.fetchall()
for (table_name,) in tables:
    cur.execute(f"DROP TABLE IF EXISTS {table_name};")

conn.commit()
conn.close()
print("check_sheetアプリの全テーブル削除完了")