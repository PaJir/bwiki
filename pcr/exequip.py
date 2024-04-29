# EX装备数据
import sqlite3
from config import db_name, db_name_jp

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
conn_jp = sqlite3.connect(db_name_jp)
cursor_jp = conn_jp.cursor()

def exequip(cur=cursor_jp):
    f = open("exequip.txt", "w", encoding="UTF-8")
    sql_main = """
select d.ex_equipment_id, d.name, d.description, c.category_name, d.rarity, d.clan_battle_equip_flag, d.is_force_protected, d.max_rank_flag, 
d.default_hp, d.default_atk, d.default_magic_str, d.default_def, d.default_magic_def, d.default_physical_critical, d.default_magic_critical, d.default_wave_hp_recovery, d.default_wave_energy_recovery, d.default_dodge, d.default_life_steal, d.default_hp_recovery_rate, d.default_energy_recovery_rate, d.default_energy_reduce_rate, d.default_accuracy, 
d.max_hp, d.max_atk, d.max_magic_str, d.max_def, d.max_magic_def, d.max_physical_critical, d.max_magic_critical, d.max_wave_hp_recovery, d.max_wave_energy_recovery, d.max_dodge, d.max_life_steal, d.max_hp_recovery_rate, d.max_energy_recovery_rate, d.max_energy_reduce_rate, d.max_accuracy 
from ex_equipment_data d join ex_equipment_category c on d.category=c.category"""
    cur.execute(sql_main)
    all_data = cur.fetchall()
    ret = []
    for data in all_data:
        ret.append(data[0])
        f.write(str(data[0]) + "\t" + "\t".join([str(x).replace("\\\\n", "<br>") for x in data]) + "\n")
    f.close()
    return ret

if __name__ == "__main__":
    exequip(cursor)
    conn.close()
    conn_jp.close()