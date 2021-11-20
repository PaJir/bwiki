# 地图掉落数据
import sqlite3

areaid      = "110"                    # 110 for Normal, 120 for Hard
# mapid       = ["21"]                     # 地图编号，是字符串，要改
# questid_max = 17                       # 关卡的最大编号，是数字，默认14
from config import db_name, db_name_jp  # db放在同一目录下，如果db名不同，可以换
conn = sqlite3.connect(db_name_jp)
cursor = conn.cursor()


def search_equipment(questid, quest_id_nozero, mapid_nozero, mapid):
    
    sql_main = """select e.equipment_id id, r.odds_1 odds
from enemy_reward_data r join equipment_data e on r.reward_id_1 = e.equipment_id
where r.drop_reward_id in (""" + \
    areaid + mapid + questid + "1," + \
    areaid + mapid + questid + "2," + \
    areaid + mapid + questid + "3," + \
    areaid + mapid + questid + "4)" + \
    """order by odds desc"""
    cursor.execute(sql_main)
    # print(cursor.fetchall())
    main_data = cursor.fetchall()
    if len(main_data) == 0:
        return

    sql_where = """where r.drop_reward_id in (
	select w.drop_reward_id_1 w from wave_group_data as w 
	join (
		select wave_group_id_1 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_2 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_3 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """) as q 
	where w.wave_group_id = q.w
	UNION
	select w.drop_reward_id_2 w from wave_group_data as w 
	join (
		select wave_group_id_1 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_2 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_3 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """) as q 
	where w.wave_group_id = q.w
	UNION
	select w.drop_reward_id_3 w from wave_group_data as w 
	join (
		select wave_group_id_1 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_2 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """ UNION
		select wave_group_id_3 w from quest_data where quest_id = """ + areaid + mapid + "0" + questid + """) as q 
	where w.wave_group_id = q.w)"""
    sql_by_where = sql_where + " AND substr(id, 3, 2) == \"99\" "
    sql_by = "select e.equipment_id name, r.odds_1 odds, r.drop_reward_id id from enemy_reward_data r join equipment_data e on r.reward_id_1 = e.equipment_id " + sql_by_where + "UNION ALL " + \
        "select e.equipment_id name, r.odds_2 odds, r.drop_reward_id id from enemy_reward_data r join equipment_data e on r.reward_id_2 = e.equipment_id " + sql_by_where + "UNION ALL " + \
        "select e.equipment_id name, r.odds_3 odds, r.drop_reward_id id from enemy_reward_data r join equipment_data e on r.reward_id_3 = e.equipment_id " + sql_by_where + "UNION ALL " + \
        "select e.equipment_id name, r.odds_4 odds, r.drop_reward_id id from enemy_reward_data r join equipment_data e on r.reward_id_4 = e.equipment_id " + sql_by_where + "UNION ALL " + \
        "select e.equipment_id name, r.odds_5 odds, r.drop_reward_id id from enemy_reward_data r join equipment_data e on r.reward_id_5 = e.equipment_id " + sql_by_where + \
        "order by odds desc"
    cursor.execute(sql_by)
    # print(cursor.fetchall())
    by_data = cursor.fetchall()

    sql_unit = "select r.reward_id_1 id, r.odds_1 odds from enemy_reward_data r " + sql_where + \
        " AND substr(id, 1, 1) == \"3\" AND length(id) == 5"
    cursor.execute(sql_unit)
    # print(cursor.fetchall())
    unit_data = cursor.fetchall()

    # 打印
    print_str = ""
    if areaid == "110":
        print_str += mapid_nozero + "-" + quest_id_nozero + " "
    elif areaid == "120":
        print_str += "H" + mapid_nozero + "-" + quest_id_nozero + " "
    else:
        print_str += "VH" + mapid_nozero + "-" + quest_id_nozero + " "
    print_str += print_str

    main_by_str = ""
    main_by_prob = ""
    # print(main_data)
    for index in range(len(main_data)):
        equipment = main_data[index][0]
        main_by_str += str(equipment) + "," 
        main_by_prob += str(main_data[index][1]) + "%,"
    for index in range(len(by_data)):
        equipment = by_data[index][0]
        main_by_str += str(equipment) + "," 
        main_by_prob += str(by_data[index][1]) + "%,"
    # print(main_by_str[:-1])
    print_str += main_by_str[:-1] + " " + main_by_prob[:-1] + " "
    

    if len(unit_data) > 0:
        if(str(unit_data[0][0])[1]=="1"):
            print_str += str(unit_data[0][0])[2:] + " " + str(unit_data[0][1]) + "% "
        else:
            print_str += "  "
        if(str(unit_data[0][0])[1]=="2"):
            print_str += str(unit_data[0][0])[2:] + " " + str(unit_data[0][1]) + "% "
        else:
            print_str += "  "
    else:
        print_str += "    "

    # print("|编号=" + areaid + mapid + questid)
    print_str += areaid + mapid + questid
    # print("}}")
    print(print_str)

mapid = [str(a) for a in range(50, 60)]
questid_max = [a for a in range(1, 20)]
for m in mapid:
    for i in questid_max:
        tmp = str(i)
        
        if i < 10:
            tmp = "0" + tmp
        mapid_zero = ("0" + m) if len(m) == 1 else m
        # nozero, withzero, nozero, withzero
        search_equipment(tmp, str(i), m, mapid_zero)

conn.close()

"""
quest_area_data: area_id, area_name
quest_data: quest_id(11021014), area_id, quest_name -> wave_group_id_1(11021014{1-3})
wave_group_data: wave_group_id(11021014{1-3}) -> drop_reward_id_{1-3}
11021141 九天之铠的设计图     11999291 扫荡券 11999293 金币
11021142 少女服的设计图       11999292 经验   11999903 副掉落
11021143 人鱼公主的灵泪（碎片）
enemy_reward_data: drop_reward_id, reward_id_{1-5}, odds_{1-5}
equipment_data: equipment_id, equipment_name"

quest_id: 12021003
wave_group_id_{1-3}: 12021003{1-3}
drop_reward_id_{1-3}:
12021031 11999591             11999593
12021032 11999592             11999803
12021033 12021049 角色碎片31037

quest_id: 13018001
wave_group_id_{1-3}: 13018001{1-3}
drop_reward_id_{1-3}:
13018011/115554    0
13018012/115194    11999591 扫荡券    11999801 副掉落     13018014/125343
13018029/32058    11999592 经验      13018013/125134    11999593 金币
"""