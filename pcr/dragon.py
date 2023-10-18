import sqlite3
from config import db_name

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

sql = "select * from srt_panel order by reading_id"

cursor.execute(sql)
wf = open("dragon.txt", "w+", encoding="utf-8")
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
    wf.write("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>\n")
    for j in range(st, ed):
        wf.write("| " + data[j][1] + 
              " || " + data[j][6] + 
              " || " + data[j][7] + 
              " || " + type_map[data[j][2]] + 
              " || " + data[j][4] + 
              " || " + str(data[j][5]) + "\n")
        wf.write("|-\n")
    st = ed
ed = ed + 1
wf.write("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>\n")
for j in range(st, ed):
    wf.write("| " + data[j][1] + 
          " || " + data[j][6] + 
          " || " + data[j][7] + 
          " || " + type_map[data[j][2]] + 
          " || " + data[j][4] +
          " || " + str(data[j][5]) + "\n")
    wf.write("|-\n")