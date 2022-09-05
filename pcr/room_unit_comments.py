import sqlite3
from config import db_name

write_file = "room_unit_comments.txt"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def roomUnitComments():
    """公会之家交互语音文字"""
    sql = "SELECT id, unit_id, trigger, voice_id, beloved_step, time, description " + \
        "FROM room_unit_comments " + \
        "WHERE substr(unit_id, -2, 2) == '01' ORDER BY id"
    cursor.execute(sql)
    data = cursor.fetchall()
    wf = open(write_file, "w+", encoding="utf-8")
    for d in data:
        d = [str(_) for _ in d]
        d[0] = "Room:" + d[0]
        d[1] = d[1][:4]
        d = "\t".join(d)
        d = d.replace("\\\\n", "<br>")
        wf.write(d + "\n")
    wf.close()

roomUnitComments()