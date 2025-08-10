# 角色生日特别演出、小活动的脚本，文本从db中提取
import sqlite3
from config import db_name, db_name_jp

write_file = "drama.txt"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)
cursor_jp = conn_jp.cursor()

f = None

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
    sql_cn = """select substr(u.unit_id,1,4) || '11', u.unit_name from unit_data u;"""
    cursor.execute(sql_cn)
    id_name = cursor.fetchall()
    id_name_map = {}
    for x in id_name:
        id_name_map[x[0]] = x[1]
    sql = """select date_id, unlock_time from wac_data order by date_id; """
    cursor_jp.execute(sql)
    wac_data = cursor_jp.fetchall()
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
        cursor_jp.execute(sql)
        all_data = cursor_jp.fetchall()
        if len(all_data) > 0:
            f.write("==%s==\n%s\n" % (id_name_map.get(all_data[0][1], all_data[0][0]), wac[1].split(" ")[0]))
        else:
            f.write("====\n%s\n" % wac[1].split(" ")[0])
        for data in all_data:
            f.write("{{对话|%s|%s|%s}}\n" % (data[1], id_name_map.get(data[1], data[0]), data[2].replace("\\\\n", "<br>")))
        cursor_jp.execute(sql2)
        all_data = cursor_jp.fetchall()
        if len(all_data) > 0:
            f.write("[[file:wac_%s.png|center]]\n" % id_name_map.get(all_data[0][1], all_data[0][0]))
        else:
            f.write("[[file:wac_.png|center]]\n")
        for data in all_data:
            f.write("{{对话|%s|%s|%s}}\n" % (data[1], id_name_map.get(data[1], data[0]), data[2].replace("\\\\n", "<br>")))


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
                " || " + data[j][-2] + 
                " || " + data[j][-1] + 
                " || " + type_map[data[j][2]] + 
                " || " + data[j][4] + 
                " || " + str(data[j][5]) + "\n")
            f.write("|-\n")
        st = ed
    ed = ed + 1
    f.write("| rowspan=" + str(ed-st) + " | <div class=\"dragon-game-item\" data-icon-id=\"" + str(data[st][3]) + "\"></div>\n")
    for j in range(st, ed):
        f.write("| " + data[j][1] + 
            " || " + data[j][-2] + 
            " || " + data[j][-1] + 
            " || " + type_map[data[j][2]] + 
            " || " + data[j][4] +
            " || " + str(data[j][5]) + "\n")
        f.write("|-\n")

def dragonFilter():
    # 龙与探险者
    sql = "select * from srt_panel order by reading_id"

    cursor.execute(sql)
    # [(1000100, '苹果', 1, 10001, '红色，酸酸甜甜的水果。', 1, 'ing', 'o')]
    data = cursor.fetchall()
    for d in data:
        f.write('<div class="trcard" data-param1="%s" data-param2="%s"><div class="dragon-game-item%s" data-icon-id="%d"></div><div class="black-white-text">%s</div></div>\n' %
                 (d[6], d[7], "" if d[5] == 1 else "2", d[3], d[1]))

def taq():
    # 谜题连结
    sql = "select genre, taq_type, difficulty, detail, detail_2, assist_detail from taq_data order by taq_no"
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        txt = '|-data-param1="%d" data-param2="%d" data-param3="%d"\n|%s||%s||%s\n' % (d[0], d[1], d[2], d[3], d[4], d[5])
        txt = txt.replace("\\n", "<br>")
        f.write(txt)

def arena_daily():
    id_name = {
        91002: "宝石",
        94002: "玛那",
        20001: "迷你经验药剂",
        20002: "经验药剂",
        20003: "高级经验药剂",
        20004: "超级经验药剂",
        20005: "究极经验药剂",
        22001: "精炼石",
        22002: "上等精炼石",
        22003: "精炼结晶",
        0: ""
    }
    sql = "select rank_from, rank_to, reward_id_1, reward_num_1, reward_id_2, reward_num_2, reward_id_3, reward_num_3, reward_id_4, reward_num_4 from arena_daily_rank_reward order by id"
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        if d[0] == d[1]:
            rank_from_to = str(d[0])
        else:
            rank_from_to = "%d-%d" % (d[0], d[1])
        if d[9] > 0:
            _22 = "[[file:%s.png|35px|link=]]*%d" % (id_name[d[8]], d[9])
        else:
            _22 = "无"
        txt = "|-\n|%s||[[file:%s.png|35px|link=]]*%d||[[file:%s.png|35px|link=]]*%d||[[file:%s.png|35px|link=]]*%d||%s\n" % (rank_from_to, id_name[d[2]], d[3], id_name[d[4]], d[5], id_name[d[6]], d[7], _22)
        f.write(txt)

def experience():
    from math import ceil
    exps = [60, 300, 1500, 7500, 37500]
    items = [20001, 20002, 20003, 20004, 20005]
    sql1 = "select team_level, total_exp, max_stamina from experience_team order by team_level;"
    sql2 = "select unit_level, total_exp from experience_unit order by unit_level;"
    cursor_jp.execute(sql1)
    team = cursor_jp.fetchall()
    cursor_jp.execute(sql2)
    unit = cursor_jp.fetchall()
    last_team_total_exp = 0
    last_unit_total_exp = 0
    for idx in range(len(unit)):
        if idx >= len(team):
            team_str = " || || || "
        else:
            team_str = "[[File:佑树.png|25px]] Lv.%d||%d||%d||%d" % (team[idx][0], team[idx][1]-last_team_total_exp, team[idx][1], team[idx][2])
            last_team_total_exp = team[idx][1]
        need_exp = unit[idx][1] - last_unit_total_exp
        for i in range(len(exps)):
            if exps[i] >= need_exp or i == len(exps) - 1:
                items_idx1 = items[i]
                items_num1 = ceil(need_exp / exps[i])
                break
        for i in range(len(exps)):
            if exps[i] >= unit[idx][1] or i == len(exps) - 1:
                items_idx2 = items[i]
                items_num2 = ceil(unit[idx][1] / exps[i])
                break
        unit_str = "[[File:Icon_unit_170131.png|25px]] Lv.%d||%d||[[File:Icon_item_%d.png|25px]]x%d||%d||[[File:Icon_item_%d.png|25px]]x%d" % (unit[idx][0], need_exp, items_idx1, items_num1, unit[idx][1], items_idx2, items_num2)
        last_unit_total_exp = unit[idx][1]
        f.write("|-\n|%s||%s\n" % (team_str, unit_str))

def level_cost():
    sql = "select target_level, cost from skill_cost order by target_level"

def unique_cost():
    sql = "select unit_level, consume_num_2, consume_num_1, crafted_cost from unique_equipment_rankup where equip_id=130011 order by unit_level"
    cursor_jp.execute(sql)
    data = cursor_jp.fetchall()
    sql2 = "select enhance_level, needed_point, needed_mana from unique_equipment_enhance_data where equip_slot=1 order by enhance_level"
    cursor_jp.execute(sql2)
    enhance = cursor_jp.fetchall()
    data = [[1, 0, 0, 0]] + data
    data.append([enhance[-1][0], 0, 0, 0])
    for i in range(1, len(data)-1):
        txt = "|-\n|界限突破(Lv%d-Lv%d)||碎片%d||%d||%d万\n" % (data[i][0], data[i+1][0], data[i][1], data[i][2], data[i][3]/10000)
        f.write(txt)
    i = 1
    total_point, total_mana = 0, 0
    all_point, all_mana = 0, 0
    for e in enhance:
        total_point += e[1]
        total_mana += e[1] * e[2]
        if e[0] == data[i][0]:
            txt = "|-\n|Lv{:d}-Lv{:d} || {:d} || {:g}万\n".format(data[i-1][0], data[i][0], total_point, total_mana/10000)
            f.write(txt)
            i += 1
            all_point += total_point
            all_mana += total_mana
            total_point, total_mana = 0, 0
    txt = "|-\n|合计|| {:d} || {:g}万\n".format(all_point, all_mana/10000)
    f.write(txt)

if __name__ == "__main__":
    f = open(write_file, "w+", encoding="UTF-8")
    # role()
    # psy()
    # nop()
    # wac()
    # dragonFilter()
    # taq()
    # arena_daily()
    # experience()
    unique_cost()
    f.close()
    conn.close()
    conn_jp.close()