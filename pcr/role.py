# 角色数据
# output log:
# 97 166
# 102 169
import sqlite3
import io
import re
from config import db_name, db_name_jp

write_file = "role.txt"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)
cursor_jp = conn_jp.cursor()

f = open(write_file, "w", encoding="UTF-8")

bad_unit = [110201] #, 106701]
p1 = re.compile(r'[（](.*?)[）]', re.S) # 匹配括号内的内容
status_map = {
    1: "生命值", 
    2: "物理攻击力", 
    4: "魔法攻击力", 
    3: "物理防御力", 
    5: "魔法防御力", 
    6: "物理暴击", 
    7: "魔法暴击", 
    10: "生命自动回复", 
    11: "技能值自动回复", 
    8: "回避", 
    9: "生命值吸收", 
    15: "回复量上升", 
    14: "技能值上升", 
    140: "技能值消耗降低", 
    17: "命中"
}
# CN/JP
def audio(id, cur):
    id = str(id)
    desp = []
    for i in range(1, 18):
        sql = "select description from unit_comments where id = " + id + str(i).zfill(3)
        cur.execute(sql)
        d = cur.fetchone()
        if d is None:
            break
        desp.append(d[0].replace("\\\\n","<br/>").replace("\\n", "<br/>"))
    x1 = "￥".join(desp[0:5])
    x3 = "￥".join(desp[5:10])
    birth = "￥".join(desp[10:12])
    x6 = ""
    if len(desp) == 17:
        x6 = "￥".join(desp[12:17])
    return x1+"@"+x3+"@"+birth+"@"+x6+"@@@"
# JP RANK装备
def rank(id):
    if id == "1701":
        id = "1057"
    elif id == "1702":
        id = "1076"
    r = []
    # print(id)
    for i in range(1, 23):
        sql = "select equip_slot_1, equip_slot_2, equip_slot_3, equip_slot_4, equip_slot_5, equip_slot_6 from unit_promotion" + \
            " where unit_id = " + id + "01 and promotion_level = " + str(i)
        cursor_jp.execute(sql)
        r_i = cursor_jp.fetchone()
        if r_i is None:
            r.append("")
            continue
        r_i = [str(s) for s in r_i]
        r.append("、".join(r_i))
    return "@".join(r) + "@"
# JP RANK属性
def unit_promotion_status(id):
    return

# JP
def rarity(id):
    if id == "1701":
        id = "1057"
    elif id == "1702":
        id = "1026"
    r = []
    for i in range(1, 7):
        sql = "select hp, atk, magic_str, def, magic_def, physical_critical, magic_critical, wave_hp_recovery, wave_energy_recovery, dodge, life_steal, hp_recovery_rate, energy_recovery_rate, energy_reduce_rate, accuracy, " + \
            "hp_growth, atk_growth, magic_str_growth, def_growth, magic_def_growth, physical_critical_growth, magic_critical_growth, wave_hp_recovery_growth, wave_energy_recovery_growth, dodge_growth, life_steal_growth, hp_recovery_rate_growth, energy_recovery_rate_growth, energy_reduce_rate_growth, accuracy_growth " + \
            "from unit_rarity where unit_id=" + id + "01 and rarity = " + str(i)
        cursor_jp.execute(sql)
        r_i = cursor_jp.fetchone()
        if r_i is None:
            r.append("@@") # 30/15=2个
        else:
            r_i = [str(s) for s in r_i]
            r.append("、".join(r_i[0:15]))
            r.append("、".join(r_i[15:30]))
    return "@".join(r) + "@"

# CN&JP
def chara_story_status(id):
    ret = ""
    sql = "select story_id, status_type_1, status_rate_1, status_type_2, status_rate_2, status_type_3, status_rate_3, status_type_4, status_rate_4, status_type_5, status_rate_5 " + \
        "from chara_story_status " + \
        "where chara_id_1 = " + id + \
        " order by story_id"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor_jp.execute(sql)
    data_jp = cursor_jp.fetchall()
    for i, d_jp in enumerate(data_jp):
        if i == 0 and len(data_jp) == 3:
            ret += "无变化@无变化@"
        elif i == 2 and len(data_jp) == 3:
            ret += "无变化@无变化@"
        if data is not None and len(data) >= i + 1:
            ret += status_map[data[i][1]] + "+" + str(data[i][2])
            if data[i][3] > 0:
                ret += "、" + status_map[data[i][3]] + "+" + str(data[i][4])
            if data[i][5] > 0:
                ret += "、" + status_map[data[i][5]] + "+" + str(data[i][6])
            if data[i][7] > 0:
                ret += "、" + status_map[data[i][7]] + "+" + str(data[i][8])
            if data[i][9] > 0:
                ret += "、" + status_map[data[i][9]] + "+" + str(data[i][10])
        else:
            ret += status_map[d_jp[1]] + "+" + str(d_jp[2])
            if d_jp[3] > 0:
                ret += "、" + status_map[d_jp[3]] + "+" + str(d_jp[4])
            if d_jp[5] > 0:
                ret += "、" + status_map[d_jp[5]] + "+" + str(d_jp[6])
            if d_jp[7] > 0:
                ret += "、" + status_map[d_jp[7]] + "+" + str(d_jp[8])
            if d_jp[9] > 0:
                ret += "、" + status_map[d_jp[9]] + "+" + str(d_jp[10])
        
        ret += "@"
    if len(data_jp) < 11:
        ret += "@@@@"
    return ret
# CN/JP
def unit_skill_data(id):
    sql = "select skill_id, name, action_1, action_2, action_3, action_4, action_5, action_6, action_7, description, icon_type " + \
        "from skill_data where substr(skill_id, 1, 4) = '" + id + "' order by skill_id"
    cursor.execute(sql)
    cursor_jp.execute(sql)
    (skill_data, skill_data_jp) = (cursor.fetchall(), cursor_jp.fetchall())
    skill_id = ["001", "011", "002", "003", "101", "102", "103", "501", "511", "012"]
    skill_map = {}
    for data in skill_data_jp:
        skill_map[str(data[0])[4:]] = data
    for data in skill_data:
        skill_map[str(data[0])[4:]] = data
    # UB动画2
    ret = "@"
    # UB UB图 UB描述 UB效果 6星UB 6星UB描述 6星UB效果 
    # 技能1 技能1图 技能1描述 技能1效果 技能2 技能2图 技能2效果 技能2描述 
    # 特殊技能1 特殊技能1图 特殊技能1描述 特殊技能1效果 特殊技能2 特殊技能2图 特殊技能2描述 特殊技能2效果 特殊技能3 特殊技能3图 特殊技能3描述 特殊技能3效果 
    # EX技能 EX技能图 EX技能描述 EX技能效果 EX技能plus EX技能plus描述 EX技能plus效果 
    for index in range(8):
        skill = skill_map.get(skill_id[index], None)
        if skill is None:
            ret += "@@@@"
        else:
            ret += skill[1] + "@Icon_skill_" + str(skill[10]) + "@" + skill[9] + "@@"
    # EX技能plus EX技能plus描述 EX技能plus效果 
    skill = skill_map.get(skill_id[8], None)
    if skill is None:
        ret += "@@@"
    else:
        ret += skill[1] + "@" + skill[9] + "@@"
    # 专属技能描述 专属技能效果 
    ret += "@@"
    return ret

# CN/JP
def attack_pattern(id, cur):
    idx = ["①", "②", "③", "④"]
    sql = "select * from unit_attack_pattern where unit_id=" + id + "01 order by pattern_id"
    cur.execute(sql)
    pattern = cur.fetchall()
    # print(pattern)
    add_idx = len(pattern) > 1
    ret = ""
    for index in range(len(pattern)):
        if add_idx:
            ret += idx[index]
        if 4 == 3 + pattern[index][2]:
            ret += "无<br/>"
            continue
        for p in pattern[index][4: 3 + pattern[index][2]]:
            if p < 1000:
                ret += "{{行动|普攻}}"
            elif p < 2000:
                ret += "{{行动|" + str(p-1000) + "}}"
            else:
                ret += "{{行动|特殊" + str(p-2000) + "}}"
            ret += " → "
        ret = ret[:-3] + "<br/>"
    ret = ret[:-5] + "@"
    for index in range(len(pattern)):
        if add_idx:
            ret += idx[index]
        for p in pattern[index][3 + pattern[index][2]: 4 + pattern[index][3]]:
            if p < 1000:
                ret += "{{行动|普攻}}"
            elif p < 2000:
                ret += "{{行动|" + str(p-1000) + "}}"
            else:
                ret += "{{行动|特殊" + str(p-2000) + "}}"
            ret += " → "
        ret = ret[:-3] + " ↻<br/>"
    ret = ret[:-5] + "@"
    # print(ret)
    return ret

def role_main(data, cur):
    # 节日
    fes = re.findall(p1, data[3])
    if fes == []:
        fes = ""
    else:
        fes = fes[0]
    # 4位id
    id = str(data[1])[0:4]
    # 角色（全）名
    role_name = data[2]
    # 类型
    pos_type = "前卫"
    if data[17] >= 600:
        pos_type = "后卫"
    elif data[17] >= 300:
        pos_type = "中卫"
    # 攻击方式
    atk_type = "物理" if data[18] == 1 else "魔法"
    # 生日
    birthday = str(data[12]) + "月" + str(data[13]) + "日"
    # 页面名 角色ID 角色名 翻译名 角色介绍 是否实装（手动） 是否6星（手动）
    f.write(data[3]+"@"+id+"@"+(role_name if fes=="" else "")+"@"+data[3]+"@"+data[0].replace("\\\\n","<br/>")+"@@@") 
        # kana 外号（手动） CV 初始星级 限定 节日 类型 所属 碎片获取（手动） 6星碎片获取（手动）
    f.write(data[4]+"@@"+(data[5] if fes=="" else "")+"@"+str(data[6])+"@"+str(data[7])+"@"+fes+"@"+pos_type+"@"+data[8]+"@@@")
    # 1星立绘语音 3星立绘语音 生日语音 cutin语音 UB语音
    f.write(audio(id, cur))
    # 身高 体重 年龄 生日 血型 种族 兴趣 
    if fes != "":
        f.write("@@@@@@@")
    else:
        f.write(str(data[9])+"@"+str(data[10])+"@"+str(data[11])+"@"+birthday+"@"+data[14]+"@"+data[15]+"@"+data[16]+"@")
    # 位置 攻击方式 普攻时间 剧情短评 
    f.write(str(data[17])+"@"+atk_type+"@"+str(data[19])+"@"+(data[20] if fes=="" else "")+"@")
    # 绊2-12
    f.write(chara_story_status(id))
    # UB动画2 UB UB图 UB描述 UB效果 6星UB 6星UB描述 6星UB效果 （全手动）
    # 技能1 技能1图 技能1描述 技能1效果 技能2 技能2图 技能2效果 技能2描述 
    # 特殊技能1 特殊技能1图 特殊技能1描述 特殊技能1效果 特殊技能2 特殊技能2图 特殊技能2描述 特殊技能2效果 特殊技能3 特殊技能3图 特殊技能3描述 特殊技能3效果 
    # EX技能 EX技能图 EX技能描述 EX技能效果 EX技能plus EX技能plus描述 EX技能plus效果 
    # 专属技能描述 专属技能效果 
    f.write(unit_skill_data(id))
    # 起手顺序 行动顺序 
    f.write(attack_pattern(id, cur))
    # R1-R22
    f.write(rank(id))
    # R1-R22属性
    # f.write(unit_promotion_status(id))
    # 基础属性及其成长速度 (15)2*6
    f.write(rarity(id))
    f.write("\n")

def role():
    sql2 = """
        select d.comment _0, d.unit_id _1, b.unit_name _2, d.unit_name _3, 
        d.kana _4, p.voice _5, d.rarity _6, is_limited _7, p.guild _8, 
        p.height _9, p.weight _10, p.age _11, p.birth_month _12, p.birth_day _13, p.blood_type _14, p.race _15, p.favorite _16, d.search_area_width _17, d.atk_type _18, d.normal_atk_cast_time _19, p.catch_copy _20 
        from unit_data d join unit_profile p join actual_unit_background b on d.unit_id = p.unit_id and substr(p.unit_id, 1, 4) = substr(b.unit_id, 1, 4) 
        where d.unit_id < 190801 
        order by d.unit_id asc"""
    # 忽略actural_unit_background.unit_name
    sql = """
        select d.comment _0, d.unit_id _1, d.unit_name _2, d.unit_name _3, 
        d.kana _4, p.voice _5, d.rarity _6, is_limited _7, p.guild _8, 
        p.height _9, p.weight _10, p.age _11, p.birth_month _12, p.birth_day _13, p.blood_type _14, p.race _15, p.favorite _16, d.search_area_width _17, d.atk_type _18, d.normal_atk_cast_time _19, p.catch_copy _20 
        from unit_data d join unit_profile p on d.unit_id = p.unit_id
        where d.unit_id < 190801 
        order by d.unit_id asc"""

    cursor.execute(sql)
    all_data = cursor.fetchall()
    cursor_jp.execute(sql)
    all_data_jp = cursor_jp.fetchall()
    print(len(all_data), len(all_data_jp))
    for data in all_data:
        if data[1] in bad_unit:
            continue
        role_main(data, cursor)
    for data_jp in all_data_jp:
        if data_jp[1] in bad_unit:
            continue
        in_cn = False
        for data in all_data:
            if data[1] == data_jp[1]:
                in_cn = True
                break
        # if in_cn:
        #     continue
        print(data_jp[1])
        role_main(data_jp, cursor_jp)

"""备忘
unit_attack_pattern: 技能循环
1 unit_background: 角色现实名字 actual_unit_background
1 unit_comments: 角色12条语音文字 001-005是1星立绘语音文字，006-010是3星立绘语音文字，011-012是生日语音，013-017是6星立绘语音文字
1 unit_data: 角色ID，角色名，kana，限定，初始星级，位置，攻击方式，普攻时间，角色介绍
1 unit_profile: 年龄，所属，种族，身高，体重，生日/月，生日/日，血型，兴趣，CV，剧情短评
1 unit_promotion: RANK装备
unit_promotion_status: 角色各RANK对应的属性【不要，日服他娘的改了装备属性】
1 unit_rarity: 角色各星级对应的属性及其成长速度
1 unit_skill_data: 角色技能数据【暂时不管】
unit_unique_equip: 角色专属武器ID映射【不要】
忘了 unlock_rarity_6: 6星开花额外的属性，需要把三项加起来
"""

role()
# attack_pattern("1061", cursor)
# print(audio(1115, cursor))
f.close()
conn.close()
conn_jp.close()