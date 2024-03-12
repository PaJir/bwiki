# 角色生日特别演出
import sqlite3
from config import db_name, db_name_jp
from skill import attackPattern

write_file = "birthday_drama.txt"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)

f = open(write_file, "w+", encoding="UTF-8")

def role():
    sql = """
        select u.unit_name, b.param_01, b.param_02
        from birthday_login_bonus_drama_script b join unit_data u 
        on substr(b.param_01,1,4) = substr(u.unit_id,1,4)
        where command_type=11
        order by command_id asc"""

    cursor.execute(sql)
    all_data = cursor.fetchall()
    last = None
    for data in all_data:
        if last is None or last != data[0]:
            last = data[0]
            f.write("==角色生日特别演出==\n")
            f.write("[[file:Blb cake " + data[0] + ".png|center]]\n")
        f.write("{{对话|" + data[1] + "|" + data[0] + "|" + data[2].replace("\\\\n", "<br>") + "}}\n")

def psy():
    sql = """
        select u.unit_name, p.param_01, p.param_02, p.drama_id, t.title
        from psy_drama_script p left join unit_data u
        on substr(p.param_01,1,4) = substr(u.unit_id,1,4)
        join psy_drama t on p.drama_id=t.drama_id
        where command_type=11
        order by command_id asc"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    last = ""
    for data in all_data:
        if last != data[3]:
            f.write("==" + data[4] + "==\n")
            last = data[3]
        f.write("{{对话|" + data[1] + "|" + (data[0] if data[0] is not None else "") + "|" + data[2].replace("\\\\n", "<br>") + "}}\n")

if __name__ == "__main__":
    # role()
    psy()
    f.close()
    conn.close()