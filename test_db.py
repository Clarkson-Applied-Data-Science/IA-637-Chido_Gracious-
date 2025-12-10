import pymysql
import yaml
from pathlib import Path

config = yaml.safe_load(Path("config.yml").read_text())
conn = pymysql.connect(
    host=config["db"]["host"],
    port=3306,
    user=config["db"]["user"],
    password=config["db"]["pw"],
    db=config["db"]["db"],
    cursorclass=pymysql.cursors.Cursor,
)
with conn.cursor() as cur:
    cur.execute("SELECT DATABASE()")
    row = cur.fetchone()
    print("Current database:", row[0])
    cur.execute("SHOW TABLES")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
conn.close()
