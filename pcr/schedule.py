# 活动日历
import sqlite3
import io
import re

write_file = "schedule.txt"

clans = ["水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "魔羯座"]


def dateFormat(d):
    return d.replace("/", "-")[:-3].replace(" 5:", " 05:").replace(" 4:", " 04:").replace("  ", " ")


def schedule(db_name, note=""):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # 卡池
    sql = """select gacha_id, gacha_name, description, start_time, end_time
    from gacha_data
    where gacha_id >= 30000 and gacha_id < 60000 and start_time > '2020/1/3 15:59:59'
    order by exchange_id;"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    with open(write_file, "w+", encoding="utf-8") as wf:
        p = re.compile(r'「(.*?)」', re.S)
        for data in all_data:
            roles = re.findall(p, data[2])
            wf.write("{{活动记录|开始时间=" + dateFormat(data[3]) + "|结束时间=" + dateFormat(data[4]) + "|活动=卡池|角色=")
            wf.write('、'.join(roles))
            wf.write("|详情=|备注=")
            if data[1] == "附奖扭蛋" or data[2].find("复刻") != -1:
                wf.write("复刻")
            elif 40000 <= data[0] < 50000:
                wf.write("3★概率2倍")
            elif 50000 <= data[0]:
                wf.write("fes")
            wf.write("}}\n")
    # 外传
    sql = """select hs.event_id, hs.start_time, hs.end_time, ud.unit_name, ud2.unit_name
    from hatsune_schedule hs, hatsune_item ht, unit_data ud, unit_data ud2
    where hs.event_id = ht.event_id and 
    substr(ht.unit_material_id_1, 2, 4)=substr(ud.unit_id, 1, 4) and 
    substr(ht.unit_material_id_2, 2, 4)=substr(ud2.unit_id, 1, 4)
    order by hs.start_time;"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    with open(write_file, "a+", encoding="utf-8") as wf:
        for data in all_data:
            wf.write("{{活动记录|开始时间=" + dateFormat(data[1]) + "|结束时间=" + dateFormat(data[2]) + "|活动=")
            wf.write("外传|角色=" + data[3] + "、" + data[4] + "|详情=" + str(data[0])[3:] + "|备注=}}\n")
    # 庆典
    """id campaign_category value system_id icon_image 
    start_time end_time level_id shiori_group_id duplication_order
    3+装备, 4+玛那
    N2       31/41, 2000.0, 101, 30
    H2       32/42, 2000.0, 102, 30
    探索2倍  34/44, 2000.0, 103, 30
    地下城2倍 45, 2000.0, 104, 40
    调查2倍  37/38
    VH3      39/49, 3000.0, 111, 30
    大师币1.5 91-101
    活动1.5倍 x51/x52
    """
    sql = """select campaign_category, value, start_time, end_time
    from campaign_schedule
    where campaign_category < 100
    order by id;"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    with open(write_file, "a+", encoding="utf-8") as wf:
        for data in all_data:
            if data[0] not in [31, 32, 34, 45, 37, 39, 91]:
                continue
            wf.write("{{活动记录|开始时间=" + dateFormat(data[2]) + "|结束时间=" + dateFormat(data[3]) + "|活动=")
            if data[0] == 31:
                wf.write("普通关卡庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 32:
                wf.write("困难关卡庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 34:
                wf.write("探索庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 45:
                wf.write("地下城庆典|角色=|详情=%s倍玛那|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 37:
                wf.write("调查庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 39:
                wf.write("高难关卡庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
            elif data[0] == 91:
                wf.write("大师币庆典|角色=|详情=%s倍掉落|备注=%s}}\n" % ('{:g}'.format(data[1]/1000), note))
    # 露娜之塔
    sql = """select tower_schedule_id, max_tower_area_id, start_time, end_time
    from tower_schedule
    order by tower_schedule_id;"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    with open(write_file, "a+", encoding="utf-8") as wf:
        for data in all_data:
            wf.write("{{活动记录|开始时间=" + dateFormat(data[2]) + "|结束时间=" + dateFormat(data[3]) + "|活动=")
            wf.write("露娜之塔|角色=|详情=" + "0EX|备注=}}\n")
    # 团队战
    sql = """select clan_battle_id, release_month, start_time, end_time
    from clan_battle_schedule
    order by clan_battle_id;"""
    cursor.execute(sql)
    all_data = cursor.fetchall()
    with open(write_file, "a+", encoding="utf-8") as wf:
        for data in all_data:
            id = clans[data[1] - 1]
            wf.write("{{活动记录|开始时间=" + dateFormat(data[2]) + "|结束时间=" + dateFormat(data[3]) + "|活动=")
            wf.write("团队战|角色=|详情=" + id + "|备注=}}\n")
    # 兰德索尔杯
    # chara_fortune_schedule

if __name__ == "__main__":
    from config import db_name, db_name_jp
    schedule(db_name)
    # schedule(db_name_jp, "日服")