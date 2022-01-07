import sqlite3
from config import db_name

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

sql = "select * from srt_panel order by reading_id"

cursor.execute(sql)

# [(1000100, '苹果', 1, 10001, '红色，酸酸甜甜的水果。', 'ing', 'o')]
data = cursor.fetchall()
type_map = {1: "普通读法", 2: "隐藏读法", 3: "公主连结读法"}
st, ed = 0, 0
for i, d in enumerate(data):
    if i == 0:
        continue
    if d[3] == data[ed][3]:
        ed = i
        continue
    ed = i
    print("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>")
    for j in range(st, ed):
        print("| " + data[j][1] + " || " + data[j][5] + " || " + data[j][6] + " || " + type_map[data[j][2]] + " || " + data[j][4])
        print("|-")
    st = ed
ed = ed + 1
print("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>")
for j in range(st, ed):
    print("| " + data[j][1] + " || " + data[j][5] + " || " + data[j][6] + " || " + type_map[data[j][2]] + " || " + data[j][4])
    print("|-")