data_path = "../../pcr-tool-sql-diff/cn/data"
data_path_jp = "../../pcr-tool-sql-diff/jp/data"
# data_path_jp = "../../redive_master_db_diff"
db_name = "./redive_cnx.db"
db_name_jp = "./redive_jpx.db"
split_at = "\t"

assert_path = "D:\\pcr"

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