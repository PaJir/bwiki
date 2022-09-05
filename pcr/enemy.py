# 主线关卡BOSS魔物数据
import sqlite3
from config import db_name
from skill import attackPattern

write_file = "enemy.txt"
wf = open(write_file, "w", encoding="utf-8")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()


def questN(quest_id, area_id):
    """ example:
        quest_id: 11001001, 12001001
        area_id: 11001, 12001
    """
    assert area_id < 13000
    quest_main = str(area_id % 1000)
    quest_small = str(quest_id - area_id * 1000)
    suffix = "N" if area_id < 12000 else "H"
    quest = suffix + quest_main + "-" + quest_small
    return quest


def getEnemyData(quest):
    (quest_id, area_id, unit_id, enemy_id) = quest
    # assert unit_id % 100 == 0
    sql = "SELECT unit_name, comment FROM unit_enemy_data " + \
        "WHERE unit_id=" + \
        str(unit_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    comment = data[1].split("·")[0].replace("\\\\n", "")
    quest = questN(quest_id, area_id)
    wd = "\t".join([data[0], str(unit_id//100), data[0], comment, "", quest])  # write data
    wf.write(wd + "\n")


def getEnemyQuestData(quest):
    wd = list()  # write data
    (quest_id, area_id, unit_id, enemy_id) = quest
    # assert unit_id % 100 == 0
    sql = "SELECT u.unit_name, u.comment, e.level, e.hp, e.atk, e.magic_str, e.def, e.magic_def, e.physical_critical, e.magic_critical, e.wave_hp_recovery, e.wave_energy_recovery, e.dodge, e.life_steal, e.hp_recovery_rate, e.energy_recovery_rate, e.energy_reduce_rate, e.accuracy, " + \
        "e.main_skill_lv_1, e.main_skill_lv_2, e.main_skill_lv_3, e.main_skill_lv_4, e.main_skill_lv_5, e.main_skill_lv_6, e.main_skill_lv_7, e.main_skill_lv_8, e.main_skill_lv_9, e.main_skill_lv_10, e.ex_skill_lv_1, e.ex_skill_lv_2, e.ex_skill_lv_3, e.ex_skill_lv_4, e.ex_skill_lv_5, " + \
        "u.move_speed, u.search_area_width, u.normal_atk_cast_time " + \
        "FROM unit_enemy_data u, enemy_parameter e " + \
        "WHERE u.unit_id=" + \
        str(unit_id) + \
        " and e.enemy_id=" + \
        str(enemy_id) + \
        " and e.unit_id=u.unit_id"
    cursor.execute(sql)
    [name, comment, level, hp, atk, magic_str, _def, magic_def, physical_critical, magic_critical, wave_hp_recovery, wave_energy_recovery, dodge, life_steal, hp_recovery_rate, energy_recovery_rate, energy_reduce_rate, accuracy,
        main_skill_lv_1, main_skill_lv_2, main_skill_lv_3, main_skill_lv_4, main_skill_lv_5, main_skill_lv_6, main_skill_lv_7, main_skill_lv_8, main_skill_lv_9, main_skill_lv_10,
        ex_skill_lv_1, ex_skill_lv_2, ex_skill_lv_3, ex_skill_lv_4, ex_skill_lv_5, move_speed, search_area_width, normal_atk_cast_time] = cursor.fetchone()
    quest = questN(quest_id, area_id)
    skill_comment = "·" + "<br>·".join(comment.replace("\\\\n", "").replace("\\u3000", "").split("·")[1:])
    wd += [name+"/"+quest, unit_id, quest, skill_comment, level, hp, atk, magic_str, _def, magic_def, physical_critical, magic_critical,
           wave_hp_recovery, wave_energy_recovery, dodge, life_steal, hp_recovery_rate, energy_recovery_rate, energy_reduce_rate, accuracy, 
           move_speed, search_area_width, normal_atk_cast_time]
    (starts, loops) = attackPattern(unit_id, cursor)
    wd += [starts, loops]
    wd = [str(_) for _ in wd]
    wf.write("\t".join(wd) + "\n")


def getLastQuest():
    sql = "SELECT max(q.quest_id), q.area_id, e.unit_id, e.enemy_id " + \
        "FROM quest_data q, wave_group_data w, enemy_parameter e " + \
        "WHERE q.wave_group_id_3=w.wave_group_id and w.enemy_id_1=e.enemy_id and q.area_id<13000 " + \
        "GROUP BY q.area_id ORDER BY q.quest_id ASC"
    cursor.execute(sql)
    quest_list = cursor.fetchall()
    for quest in quest_list:
        getEnemyData(quest)
    for quest_idx in range(0, len(quest_list)//2):
        getEnemyQuestData(quest_list[quest_idx])
        getEnemyQuestData(quest_list[quest_idx + len(quest_list)//2])


getLastQuest()
wf.close()
cursor.close()
conn.close()

""" 备注
unity_enemy_data    | unit_id  | unit_name | prefab_id | move_speed | search_area_width | atk_type | normal_atk_cast_time | comment
                      301700     炸脖龙       301700      270         1000               1           2.6                    【物理】...
                      【物理】栖息于毒瘴的暗棱顶部的丑恶狂兽。通过剧毒的瘴气夺取生命，啃食尸体作为食粮。
                      ·必杀技能对敌方全体造成魔法伤害（大），赋予中毒状态并击飞。
                      ·对前方两名角色造成物理伤害，并降低其物理攻击力和技能值。
                      ·炸脖龙自身剩余生命值低于40%时，攻击会更加猛烈，同时还会召集3只怪兽。
                      ·当剩余时间小于20秒时，赋予敌方全体强力中毒状态，特大幅降低自身技能值。
enemy_parameter     | enemy_id | unit_id | name  | level | rarity | promotion_level | hp | atk | ... | 
                      501010501  301700    炸脖龙   130...
skill_data          | skill_id | skill_cast_time |action_x                | depend_action_x | description   | icon_type
                      3017001  | 0.0             | 301700101, 301700102, 301700103            炸脖龙必杀技能   1001
                    ~ 3017006
skill_action        | action_id | class_id | action_type | action_detail_x | action_value_x | target_assignment | target_area | target_range | target_type | target_number | target_count | description
                      301700101   1          1             2, 0, 0           180, 10, 0.66    1                   1             -1             3             0               99             物理伤害
                      301700102   1          9             1, 0, 0           80, 4.5, 4       1                   1             -1             1             0               99             毒
                      301700103   1          3             3, 0, 0           100, 0, 1500     1                   3             -1             3             0               99             击退
skill_action - action_type | action_detail_1 | action_detail_2 | action_detail_3  | action_value_1 | action_value_2 | action_value_3 |
                   1
                   2
                   3
                   4
召唤               15                          召唤物enemy_id

unit_attack_pattern | 
"""
