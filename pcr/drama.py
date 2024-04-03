# 角色生日特别演出、小活动的脚本，文本从db中提取
import sqlite3
from config import db_name, db_name_jp

write_file = "drama.txt"

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


def nop():
    # 大家一起办年节菜派对
    sql = """
        select b.drama_id, u.unit_name, b.param_01, b.param_02
        from nop_drama_script b join unit_data u 
        on substr(b.param_01,1,4) = substr(u.unit_id,1,4)
        where command_type=11
        order by command_id asc"""

    cursor.execute(sql)
    all_data = cursor.fetchall()
    last = None
    for data in all_data:
        if last is None or last != data[0]:
            last = data[0]
            f.write("===%s===\n" % data[1])
        f.write("{{对话|" + data[2] + "|" + data[1] + "|" + data[3].replace("\\\\n", "<br>") + "}}\n")

def wac():
    # 2024年3月31日开始的公会成员庆祝生日演出
    sql = """select date_id, unlock_time from wac_data order by date_id; """
    cursor.execute(sql)
    wac_data = cursor.fetchall()
    for wac in wac_data:
        sql = """select u.unit_name, w.param_01, w.param_02 
        from wac_birthday_drama_script w join unit_data u 
        on substr(w.param_01,1,4) = substr(u.unit_id,1,4) 
        where w.drama_id=""" + str(wac[0]) + """4 and command_type=11 
        order by command_id;"""
        sql2 = """select u.unit_name, w.param_01, w.param_02 
        from wac_drama_script w join unit_data u 
        on substr(w.param_01,1,4) = substr(u.unit_id,1,4)
        where w.drama_id=""" + str(wac[0]) + """2 and command_type=11 
        order by command_id;"""
        cursor.execute(sql)
        all_data = cursor.fetchall()
        f.write("%s\n==角色生日公会庆祝==\n" % wac[1])
        for data in all_data:
            f.write("{{对话|%s|%s|%s}}\n" % (data[1], data[0], data[2].replace("\\\\n", "<br>")))
        cursor.execute(sql2)
        all_data = cursor.fetchall()
        f.write("[[file:wac_.png|center]]\n")
        for data in all_data:
            f.write("{{对话|%s|%s|%s}}\n" % (data[1], data[0], data[2].replace("\\\\n", "<br>")))


def dragon():
    # 龙与探险者
    sql = "select * from srt_panel order by reading_id"

    cursor.execute(sql)
    # [(1000100, '苹果', 1, 10001, '红色，酸酸甜甜的水果。', 'ing', 'o')]
    data = cursor.fetchall()
    type_map = {1: "普通", 2: "隐藏", 3: "公主连结"}
    st, ed = 0, 0
    for i, d in enumerate(data):
        if i == 0:
            continue
        if d[3] == data[ed][3]:
            ed = i
            continue
        ed = i
        f.write("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>\n")
        for j in range(st, ed):
            f.write("| " + data[j][1] + 
                " || " + data[j][6] + 
                " || " + data[j][7] + 
                " || " + type_map[data[j][2]] + 
                " || " + data[j][4] + 
                " || " + str(data[j][5]) + "\n")
            f.write("|-\n")
        st = ed
    ed = ed + 1
    f.write("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>\n")
    for j in range(st, ed):
        f.write("| " + data[j][1] + 
            " || " + data[j][6] + 
            " || " + data[j][7] + 
            " || " + type_map[data[j][2]] + 
            " || " + data[j][4] +
            " || " + str(data[j][5]) + "\n")
        f.write("|-\n")

if __name__ == "__main__":
    # role()
    # psy()
    # nop()
    wac()
    f.close()
    conn.close()