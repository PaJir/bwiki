# 通过数据特征反hash
from config import data_path_jp, data_path_jp2, data_path_jp_hash, data_path_jp_hash2
import os
import json
import sqlite3
import hashlib

def rehash(real_path, hash_path, out_path):
    # 最简单粗暴的方法，已过时
    tables = os.listdir(real_path)
    tables_hash = os.listdir(hash_path)
    tables_real, tables_v1 = [], []
    for t in tables:
        if not t.startswith("v1_"):
            tables_real.append(t)
    for t in tables_hash:
        if t.startswith("v1_"):
            tables_v1.append(t)
    count = 0
    for t1 in tables_real:
        lines1 = open(os.path.join(real_path, t1), "r", encoding="utf-8").readlines()
        if len(lines1) < 6:
            continue
        for t2 in tables_v1:
            lines2 = open(os.path.join(hash_path, t2), "r", encoding="utf-8").readlines()
            if len(lines2) < 6:
                continue
            found = True
            for i in range(1, 6):
                if lines1[i][lines1[i].find("("):] != lines2[i][lines2[i].find("("):]:
                    found = False
                    break
            if found:
                table_name1 = t1[:-4]
                table_name2 = t2[:-4]
                wf = open(os.path.join(out_path, t1), "w", encoding="utf-8")
                wf.write(lines1[0])
                for i in range(1, len(lines2)):
                    wf.write(lines2[i].replace(table_name2, table_name1))
                wf.close()
                tables_v1.remove(t2)
                count += 1
                break

    print("replaced %d tables" % count)

def rehash2(dbmap, hash_path, out_path, mp=None):
    succ, fail = 0, 0
    # 调用现有的dbmap
    if mp is None:
        mp = json.load(open(dbmap, "r", encoding="utf-8"))
    tables_hash = os.listdir(hash_path)
    for th in tables_hash:
        lines = open(os.path.join(hash_path, th), "r", encoding="utf-8").readlines()
        header, i, j = "", 0, 0
        while j < len(lines[0]):
            while j < len(lines[0]) and lines[0][j] != "'":
                j += 1
            header += lines[0][i:j]
            i = j + 1
            j = i
            while j < len(lines[0]) and lines[0][j] != "'":
                j += 1
            if j < len(lines[0]):
                header += "'" + mp.get(lines[0][i:j], "") + "'"
            i = j + 1
            j = i
        header += lines[0][i:j]
        i = lines[0].find("'") + 1
        j = lines[0][i:].find("'")
        real_tbname = mp.get(lines[0][i:i+j])
        if real_tbname is None:
            fail += 1
            # print(lines[0][i:i+j])
            continue
        succ += 1
        wf = open(os.path.join(out_path, real_tbname + ".sql"), "w+", encoding="utf-8")
        wf.write(header)
        for line in lines[1:]:
            wf.write(line[:13] + real_tbname + line[13+j:])
        wf.close()
    print(f"rehsah2 succ: {succ}, fail: {fail}")

def get_table_and_column_names(database_path, v1):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    tables = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        table_name = table[0]
        if (v1 and table_name[:2] != "v1") or (table_name[:2] == "v1" and not v1):
            continue
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100") # 会有重复，比如全是0，待优化
        records = cursor.fetchall()
        column_hash = [] # column及其对应的数据hash
        for idx, column in enumerate(columns):
            hash_column_idx = hashlib.sha256()
            for record in records:
                hash_column_idx.update(str(record[idx]).encode("utf-8"))
            column_hash.append([column, hash_column_idx.hexdigest()])
        column_hash = sorted(column_hash, key=lambda x: x[1])
        hash_records = hashlib.sha256()
        for x in column_hash:
            hash_records.update(str(x[1]).encode("utf-8"))
        # hash_column_map = {item[1]: item[0] for item in column_hash} # 数据hash对应的column
        tables[hash_records.hexdigest()] = {"tablename": table_name, "columns": column_hash}
    cursor.close()
    conn.close()
    return tables

def find_matching_table_and_column(db1_data : dict, db2_data : dict):
    hash_map = {}
    succ, fail = 0, 0
    for db1_table_hash, db1 in db1_data.items():
        db2 = db2_data.get(db1_table_hash)
        if db2 is None:
            fail += 1
            continue
        succ += 1
        hash_map[db2["tablename"]] = db1["tablename"]
        for db2_col, db2_col_hash in db2["columns"]:
            for i, col_hash_1 in enumerate(db1["columns"]):
                if db2_col_hash == col_hash_1[1]:
                    hash_map[db2_col] = col_hash_1[0]
                    del db1["columns"][i]
                    break

    print(f"len of db1: {len(db1_data)}, len of db2: {len(db2_data)}, succ: {succ}, fail: {fail}")
    return hash_map

def rehash3(db1_path, db2_path):
    db1_data = get_table_and_column_names(db1_path, False) # 明文
    db2_data = get_table_and_column_names(db2_path, True) # v1 hash
    
    hash_map = find_matching_table_and_column(db1_data, db2_data)
    rehash2("", data_path_jp_hash2, data_path_jp2, hash_map)

if __name__ == "__main__":
    # rehash(data_path_jp, data_path_jp_hash2, data_path_jp2)
    # rehash2(os.path.join(data_path_jp_hash, "../dbmap.json"), data_path_jp_hash2, data_path_jp2)
    rehash3("./redive_jpt.db", "./redive_jph.db")