# 角色数据
# output log:
# 97 166
# 102 169
import sqlite3
import io
import re
from config import db_name, db_name_jp
from skill import attackPattern

write_file = "role2.txt"

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
# JP RANK装备
def rank(id):
    r = []
    # print(id)
    for i in range(1, 23):
        sql = "select equip_slot_1, equip_slot_2, equip_slot_3, equip_slot_4, equip_slot_5, equip_slot_6 from unit_promotion" + \
            " where unit_id = " + id + " and promotion_level = " + str(i)
        cursor_jp.execute(sql)
        r_i = cursor_jp.fetchone()
        if r_i is None:
            r.append("")
            continue
        r_i = [str(s) for s in r_i]
        r.append("、".join(r_i))
    return "	".join(r) + "	"
# JP
def rarity(id):
    r = []
    for i in range(1, 7):
        sql = "select hp, atk, magic_str, def, magic_def, physical_critical, magic_critical, wave_hp_recovery, wave_energy_recovery, dodge, life_steal, hp_recovery_rate, energy_recovery_rate, energy_reduce_rate, accuracy, " + \
            "hp_growth, atk_growth, magic_str_growth, def_growth, magic_def_growth, physical_critical_growth, magic_critical_growth, wave_hp_recovery_growth, wave_energy_recovery_growth, dodge_growth, life_steal_growth, hp_recovery_rate_growth, energy_recovery_rate_growth, energy_reduce_rate_growth, accuracy_growth " + \
            "from unit_rarity where unit_id=" + id + " and rarity = " + str(i)
        cursor_jp.execute(sql)
        r_i = cursor_jp.fetchone()
        if r_i is None:
            r.append("		") # 30/15=2个
        else:
            r_i = [str(s) for s in r_i]
            r.append("、".join(r_i[0:15]))
            r.append("、".join(r_i[15:30]))
    return "	".join(r) + "	"

# CN/JP
def unit_skill_data(id):
    sql = "select skill_id, name, action_1, action_2, action_3, action_4, action_5, action_6, action_7, description, icon_type " + \
        "from skill_data where substr(skill_id, 1, 6) = '" + id + "' order by skill_id"
    cursor.execute(sql)
    cursor_jp.execute(sql)
    (skill_data, skill_data_jp) = (cursor.fetchall(), cursor_jp.fetchall())
    print(skill_data)
    skill_id = ["1", "2", "3"]
    skill_map = {}
    for data in skill_data_jp:
        skill_map[str(data[0])[6:]] = data
    for data in skill_data:
        skill_map[str(data[0])[6:]] = data
    ret = ""
    # UB UB图 UB描述 UB效果
    # 技能1 技能1图 技能1描述 技能1效果 技能2 技能2图 技能2效果 技能2描述 
    for index in range(3):
        skill = skill_map.get(skill_id[index], None)
        if skill is None:
            ret += "				"
        else:
            ret += skill[1] + "	Icon_skill_" + str(skill[10]) + "	" + skill[9] + "		"
    return ret

# CN/JP
def attack_pattern(id, cur):
    (starts, loops) = attackPattern(id, cur)
    return starts + "	" + loops + "	"

def role_main(data, cur):
    # 节日
    fes = re.findall(p1, data[3])
    if fes == []:
        fes = ""
    else:
        fes = fes[0]
    # 6位id***
    id = str(data[1])[0:6]
    # 攻击方式
    atk_type = "物理" if data[8] == 1 else "魔法"

    # 页面名 角色ID 翻译名
    f.write(data[3]+"	"+id+"	"+data[3]+"	") 
    # 位置 攻击方式 普攻时间
    f.write(str(data[9])+"	"+atk_type+"	"+str(data[5])+"	")

    # UB动画2 UB UB图 UB描述 UB效果 （全手动）
    # 技能1 技能1图 技能1描述 技能1效果 技能2 技能2图 技能2效果 技能2描述 
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
    sql = """
        select d.comment _0, d.unit_id _1, d.unit_name _2, d.unit_name _3, 
        d.kana _4, d.normal_atk_cast_time _5, d.rarity _6, is_limited _7, d.atk_type _8,
        d.search_area_width _9 
        from unit_data d
        where d.unit_id > 200000 and d.unit_id < 500000 
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
f.close()
conn.close()
conn_jp.close()