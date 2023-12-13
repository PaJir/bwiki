import sqlite3

write_file = "room_unit_comments.txt"

def roomUnitComments(db_name, minid, append=True):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    """公会之家交互语音文字
    公会语音	角色ID	触发	类型	羁绊	时间区间	描述
    """
    sql = "SELECT id, unit_id, trigger, voice_id, beloved_step, time, description " + \
        "FROM room_unit_comments " + \
        "WHERE substr(unit_id, -2, 2) == '01' ORDER BY id"
    cursor.execute(sql)
    data = cursor.fetchall()
    wf = open(write_file, "a+" if append else "w+", encoding="utf-8")
    for d in data:
        if d[0] < minid:
            continue
        d = [str(_) for _ in d]
        # d[0] = "Room:" + d[0]
        d[1] = d[1][:4]
        # d = "\t".join(d)
        d = "<!--" + d[0] + "-->{" + "{公会语音2|角色ID=" + d[1] + "|触发=" + d[2] + "|类型=" + d[3] + "|羁绊=" + d[4] + "|时间区间=" + d[5] + "|描述=" + d[6] + "}" + "}"
        d = d.replace("\\\\n", "<br>").replace("\\u3000", "　")
        wf.write(d + "\n")
    wf.close()
    conn.close()
