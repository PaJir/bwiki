# 角色数据
# output log:
# 97 166
# 102 169
import sqlite3
import io
import re
from config import db_name, db_name_jp, split_at, status_map
from skill import attackPattern

write_file = "role.txt"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)
cursor_jp = conn_jp.cursor()

f = open(write_file, "w", encoding="UTF-8")

bad_unit = [110201] #, 106701]
p1 = re.compile(r'[（](.*?)[）]', re.S) # 匹配括号内的内容
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
        desp.append(d[0].replace("\\\\n","<br/>").replace("\\n", "<br/>").replace("\\u3000", "　"))
    x1 = "￥".join(desp[0:5])
    x3 = "￥".join(desp[5:10])
    birth = "￥".join(desp[10:12])
    x6 = ""
    if len(desp) == 17:
        x6 = "￥".join(desp[12:17])
    return (x1+split_at+x3+split_at+birth+split_at+x6+split_at*3).replace("?", "♪").replace("\\u3000", "　")
# JP RANK装备
def rank(id):
    if id == "1701":
        id = "1057"
    elif id == "1702":
        id = "1076"
    r = []
    # print(id)
    for i in range(1, 33):
        sql = "select equip_slot_1, equip_slot_2, equip_slot_3, equip_slot_4, equip_slot_5, equip_slot_6 from unit_promotion" + \
            " where unit_id = " + id + "01 and promotion_level = " + str(i)
        cursor_jp.execute(sql)
        r_i = cursor_jp.fetchone()
        if r_i is None:
            r.append("")
            continue
        r_i = [str(s) for s in r_i]
        r.append("、".join(r_i))
    return split_at.join(r) + split_at
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
            r.append("") # 30/15=2个
            r.append("")
        else:
            r_i = [str(s) for s in r_i]
            r.append("、".join(r_i[0:15]))
            r.append("、".join(r_i[15:30]))
    return split_at.join(r) + split_at

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
            ret += "无变化"+split_at+"无变化"+split_at
        elif i == 2 and len(data_jp) == 3:
            ret += "无变化"+split_at+"无变化"+split_at
        # 全部用日服数据
        # if data is not None and len(data) >= i + 1:
        #     ret += status_map[data[i][1]] + "+" + str(data[i][2])
        #     if data[i][3] > 0:
        #         ret += "、" + status_map[data[i][3]] + "+" + str(data[i][4])
        #     if data[i][5] > 0:
        #         ret += "、" + status_map[data[i][5]] + "+" + str(data[i][6])
        #     if data[i][7] > 0:
        #         ret += "、" + status_map[data[i][7]] + "+" + str(data[i][8])
        #     if data[i][9] > 0:
        #         ret += "、" + status_map[data[i][9]] + "+" + str(data[i][10])
        # else:
        ret += status_map[d_jp[1]] + "+" + str(d_jp[2])
        if d_jp[3] > 0:
            ret += "、" + status_map[d_jp[3]] + "+" + str(d_jp[4])
        if d_jp[5] > 0:
            ret += "、" + status_map[d_jp[5]] + "+" + str(d_jp[6])
        if d_jp[7] > 0:
            ret += "、" + status_map[d_jp[7]] + "+" + str(d_jp[8])
        if d_jp[9] > 0:
            ret += "、" + status_map[d_jp[9]] + "+" + str(d_jp[10])
        
        ret += split_at
    if len(data_jp) < 11:
        ret += split_at*4
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
    ret = split_at
    # 001 UB        UB图      UB描述        UB效果
    # 011 6星UB     xxxxxxxx  6星UB描述     6星UB效果
    # 002 技能1     技能1图    技能1描述     技能1效果
    # 003 技能2     技能2图    技能2效果     技能2描述
    # 101 特殊技能1 特殊技能1图 特殊技能1描述 特殊技能1效果
    # 102 特殊技能2 特殊技能2图 特殊技能2描述 特殊技能2效果
    # 103 特殊技能3 特殊技能3图 特殊技能3描述 特殊技能3效果
    # 111 特殊技能1+（不考虑）
    # 501 EX技能    EX技能图    EX技能描述   EX技能效果
    # 511 EX技能plus xxxxxxxx  EX技能plus描述 EX技能plus效果
    # 012 xxxxx     xxxxxxxx   专属技能描述   专属技能效果
    # 二专技能描述 二专技能效果 待定
    for skill_type in skill_id:
        skill = skill_map.get(skill_type, [""] * 11)
        if skill_type == "011" or skill_type == "511":
            ret += skill[1] + split_at + skill[9] + split_at*2
        elif skill_type == "012":
            ret += skill[9] + split_at*2
        else:
            ret += skill[1] + split_at + ("Icon_skill_" if str(skill[0]) != "" else "")  + str(skill[10]) + split_at + skill[9] + split_at*2
    return ret + split_at*2

# CN/JP
def attack_pattern(id, cur):
    (starts, loops) = attackPattern(id + "01", cur)
    return starts + split_at + loops + split_at

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
    # 页面名 角色ID 角色名/手动 日文名/手动 翻译名 片假名/手动 平假名/手动 角色介绍 是否实装/手动 是否专武/手动 是否6星/手动 是否二专/手动
    f.write(data[3]+split_at+id+split_at+(role_name if fes=="" else "")+split_at*2+data[3]+split_at*3+data[0].replace("\\\\n","<br/>")+split_at*5) 
    # kana 外号（手动） CV 初始星级 限定 节日 类型 所属 碎片获取（手动）
    f.write(data[4]+split_at*2+(data[5] if fes=="" else "")+split_at+str(data[6])+split_at+str(data[7])+split_at+fes+split_at+pos_type+split_at+data[8]+split_at*2)
    # 1星立绘语音 3星立绘语音 生日语音 UB语音 六星UB语音
    f.write(audio(id, cur))
    # 身高 体重 年龄 生日 血型 种族 兴趣 
    if fes != "":
        f.write(split_at*7)
    else:
        f.write(str(data[9])+split_at+str(data[10])+split_at+str(data[11])+split_at+birthday+split_at+data[14]+split_at+data[15]+split_at+data[16]+split_at)
    # 位置 攻击方式 普攻时间 剧情短评 
    f.write(str(data[17])+split_at+atk_type+split_at+str(data[19])+split_at+(data[20] if fes=="" else "")+split_at)
    # 绊2-12
    f.write(chara_story_status(id))
    # 动态立绘 动态立绘分p 6星动态立绘 6星动态立绘分p
    f.write(split_at*4)
    # UB动画2 UB UB图 UB描述 UB效果 6星UB 6星UB描述 6星UB效果 （全手动）
    # 技能1 技能1图 技能1描述 技能1效果 技能2 技能2图 技能2效果 技能2描述 
    # 特殊技能1 特殊技能1图 特殊技能1描述 特殊技能1效果 特殊技能2 特殊技能2图 特殊技能2描述 特殊技能2效果 特殊技能3 特殊技能3图 特殊技能3描述 特殊技能3效果 
    # EX技能 EX技能图 EX技能描述 EX技能效果 EX技能plus EX技能plus描述 EX技能plus效果 
    # 专属技能描述 专属技能效果 二专技能描述 二专技能效果
    f.write(unit_skill_data(id))
    # 起手顺序 行动顺序 
    f.write(attack_pattern(id, cur))
    # R1-R32
    f.write(rank(id))
    # R1-R24属性
    # f.write(unit_promotion_status(id))
    # 基础属性及其成长速度 (15)2*6
    f.write(rarity(id)[:-1])
    f.write("\n")

def role(filter=[]):
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
    ret = []
    cursor.execute(sql)
    all_data = cursor.fetchall()
    cursor_jp.execute(sql)
    all_data_jp = cursor_jp.fetchall()
    print(len(all_data), len(all_data_jp))
    for data in all_data:
        if data[1] in bad_unit or data[1] in filter:
            continue
        # ret.append(data[1])
        role_main(data, cursor)
    for data_jp in all_data_jp:
        if data_jp[1] in bad_unit or data_jp[1] in filter:
            continue
        in_cn = False
        for data in all_data:
            if data[1] == data_jp[1]:
                in_cn = True
                break
        # if in_cn:
        #     continue
        ret.append(data_jp[1])
        role_main(data_jp, cursor_jp)
    return ret

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

if __name__ == "__main__":
    role()
    # attack_pattern("1061", cursor)
    # print(audio(1115, cursor))
    f.close()
    conn.close()
    conn_jp.close()