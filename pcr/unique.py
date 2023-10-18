# 专用装备
# 装备数据
import sqlite3
import io

from config import db_name, db_name_jp, split_at

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)
cursor_jp = conn_jp.cursor()

def write_same(data):
    s = str(data[0]) + split_at
    for i in range(0, 33):
        s += str(data[i]).replace("\\\\n","<br/>").replace("\\n","<br/>") + split_at
    return s[:-1] + "\n"

def equipment_craft():
    f = open("unique.txt", "w", encoding="UTF-8")
    # 7 + 15 + 15 + 21
    sql_main_cn = """
select d.equipment_id, d.equipment_name, d.description, 
d.hp, d.atk, d.magic_str, d.def, d.magic_def, d.physical_critical, d.magic_critical, d.wave_hp_recovery, d.wave_energy_recovery, d.dodge, d.life_steal, d.hp_recovery_rate, d.energy_recovery_rate, d.energy_reduce_rate, d.accuracy, 
r.hp, r.atk, r.magic_str, r.def, r.magic_def, r.physical_critical, r.magic_critical, r.wave_hp_recovery, r.wave_energy_recovery, r.dodge, r.life_steal, r.hp_recovery_rate, r.energy_recovery_rate, r.energy_reduce_rate, r.accuracy 
from unique_equipment_data d join unique_equipment_enhance_rate r on d.equipment_id = r.equipment_id
order by d.equipment_id"""
    sql_main = """
select d.equipment_id, d.equipment_name, d.description, 
d.hp, d.atk, d.magic_str, d.def, d.magic_def, d.physical_critical, d.magic_critical, d.wave_hp_recovery, d.wave_energy_recovery, d.dodge, d.life_steal, d.hp_recovery_rate, d.energy_recovery_rate, d.energy_reduce_rate, d.accuracy, 
r.hp, r.atk, r.magic_str, r.def, r.magic_def, r.physical_critical, r.magic_critical, r.wave_hp_recovery, r.wave_energy_recovery, r.dodge, r.life_steal, r.hp_recovery_rate, r.energy_recovery_rate, r.energy_reduce_rate, r.accuracy 
from unique_equipment_data d join unique_equip_enhance_rate r on d.equipment_id = r.equipment_id
order by d.equipment_id"""
    cursor.execute(sql_main_cn)
    all_data = cursor.fetchall()
    # all_data = []
    for data in all_data:
        f.write(write_same(data))

    cursor_jp.execute(sql_main)
    all_data_jp = cursor_jp.fetchall()
    for data in all_data_jp:
        in_cn = False
        for d in all_data:
            if d[0] == data[0]:
                in_cn = True
                break
        if in_cn:
            continue
        f.write(write_same(data))
    f.close()

equipment_craft()
conn.close()
conn_jp.close()
"""
select equipment_id, equipment_name, description, 
"""

"""备忘
unique_equipment_data: 专用装备的一些数据
unique_equipment_enhance_rate: 专用装备的强化数据
skill_action: 各个技能的数值数据
skill_data: 技能的数据
日服unique_equipment_enhance_rate表名改为了unique_equip_enhance_rate，
因此和简中服不通用，故L28-32被注释
"""