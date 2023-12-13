import os
import sqlite3
import io
import sys
from config import *


def create(db_name, data_path):
    """生成db"""
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql_files = os.listdir(data_path)
    for sql_file in sql_files:
        if not sql_file.endswith('sql'):
            continue
        sql_path_name = os.path.join(data_path, sql_file)
        # print(sql_path_name)
        with open(sql_path_name, 'r', encoding='utf-8') as rf:
            lines = rf.readlines()
            try:
                cursor.execute(lines[0])
                conn.commit()
            except:
                # print(lines[0])
                pass
            for line in lines[1:]:
                try:
                    cursor.execute(line)
                except:
                    # print(line)
                    pass
            conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("start")
    where = sys.argv[1]
    if where == 'cn':
        create(db_name, data_path)
    elif where == 'jp':
        create(db_name_jp, data_path_jp)
    else:
        print('input cn / jp')
    print("finish")