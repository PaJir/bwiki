from bs4 import BeautifulSoup
from role import unit_skill_data, rank
from config import split_at

fields = ["角色ID",
          "角色名",
          "日文名",
          "翻译名",
          "片假名",
          "平假名",
          "角色介绍",
          "是否实装",
          "是否6星",
          "是否专武",
          "是否二专",
          "kana",
          "外号",
          "CV",
          "初始星级",
          "限定",
          "节日",
          "类型",
          "属性",
          "所属",
          "碎片获取",
          "1星立绘语音",
          "3星立绘语音",
          "6星立绘语音",
          "UB语音",
          "六星UB语音",
          "身高",
          "体重",
          "年龄",
          "生日",
          "血型",
          "种族",
          "兴趣",
          "位置",
          "攻击方式",
          "普攻时间",
          "剧情短评",
          "绊2",
          "绊3",
          "绊4",
          "绊5",
          "绊6",
          "绊7",
          "绊8",
          "绊9",
          "绊10",
          "绊11",
          "绊12",
          "动态立绘",
          "动态立绘分p",
          "6星动态立绘",
          "6星动态立绘分p",
          "UB动画2",
          "UB",
          "UB图",
          "UB描述",
          "UB效果",
          "6星UB",
          "6星UB描述",
          "6星UB效果",
          "技能1",
          "技能1图",
          "技能1描述",
          "技能1效果",
          "技能2",
          "技能2图",
          "技能2描述",
          "技能2效果",
          "特殊技能1",
          "特殊技能1图",
          "特殊技能1描述",
          "特殊技能1效果",
          "特殊技能2",
          "特殊技能2图",
          "特殊技能2描述",
          "特殊技能2效果",
          "特殊技能3",
          "特殊技能3图",
          "特殊技能3描述",
          "特殊技能3效果",
          "EX技能",
          "EX技能图",
          "EX技能描述",
          "EX技能效果",
          "EX技能plus",
          "EX技能plus描述",
          "EX技能plus效果",
          "专属技能描述",
          "专属技能效果",
          "二专技能描述",
          "二专技能效果",
          "起手顺序",
          "行动顺序",
          "R1",
          "R2",
          "R3",
          "R4",
          "R5",
          "R6",
          "R7",
          "R8",
          "R9",
          "R10",
          "R11",
          "R12",
          "R13",
          "R14",
          "R15",
          "R16",
          "R17",
          "R18",
          "R19",
          "R20",
          "R21",
          "R22",
          "R23",
          "R24",
          "R25",
          "R26",
          "R27",
          "R28",
          "R29",
          "R30",
          "R31",
          "R32",
          "1x属性",
          "1x属性强化",
          "2x属性",
          "2x属性强化",
          "3x属性",
          "3x属性强化",
          "4x属性",
          "4x属性强化",
          "5x属性",
          "5x属性强化",
          "6x属性",
          "6x属性强化"]


def process():
    data = None
    with open("公主连结WIKI_BWIKI.xml", "r", encoding="utf-8") as rf:
        data = rf.readlines()
    data = "".join(data)
    data = data.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    data = data.split(">{{角色")[1:]
    units = []
    for d in data:
        d = d.split("\n}}</text")[0]
        id = d[d.find("=")+1:d.find("=")+5]
        units.append([int(id), d])
    units = sorted(units, key=lambda x: x[0])

    with open("公主连结页面导出.txt", "w+", encoding="utf-8") as wf:
        for unit in units:
            data = unit[1].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "<br>").replace("\t", "")
                field_map[field] = value
            output = []
            for field in fields:
                output.append(field_map.get(field, ""))
            output = "\t".join(output)
            wf.write(output + "\n")


def skill_rank(field_map):
    id = field_map["角色ID"]
    db_skill = unit_skill_data(id).split(split_at)[1:]
    if db_skill[0] != "":
        field_map["UB"] = db_skill[0]
        field_map["UB图"] = db_skill[1]
        field_map["UB描述"] = db_skill[2]
    if db_skill[4] != "":
        field_map["6星UB"] = db_skill[4]
        field_map["6星UB描述"] = db_skill[5]
    if db_skill[7] != "":
        field_map["技能1"] = db_skill[7]
        field_map["技能1图"] = db_skill[8]
        field_map["技能1描述"] = db_skill[9]
    if db_skill[11] != "":
        field_map["技能2"] = db_skill[11]
        field_map["技能2图"] = db_skill[12]
        field_map["技能2描述"] = db_skill[13]
    if db_skill[15] != "":
        field_map["特殊技能1"] = db_skill[15]
        field_map["特殊技能1图"] = db_skill[16]
        field_map["特殊技能1描述"] = db_skill[17]
    if db_skill[19] != "":
        field_map["特殊技能2"] = db_skill[19]
        field_map["特殊技能2图"] = db_skill[20]
        field_map["特殊技能2描述"] = db_skill[21]
    if db_skill[23] != "":
        field_map["特殊技能3"] = db_skill[23]
        field_map["特殊技能3图"] = db_skill[24]
        field_map["特殊技能3描述"] = db_skill[25]
    if db_skill[27] != "":
        field_map["EX技能"] = db_skill[27]
        field_map["EX技能图"] = db_skill[28]
        field_map["EX技能描述"] = db_skill[29]
    if db_skill[31] != "":
        field_map["EX技能plus"] = db_skill[31]
        field_map["EX技能plus描述"] = db_skill[32]
    if db_skill[34] != "":
        field_map["专属技能描述"] = db_skill[34]
    
    rk = rank(id).split(split_at)
    for i in range(20, 25):
        field_map["R" + str(i+1)] = rk[i]


def read_xml():
    html = None
    with open("wiki_export.xml", "r", encoding="utf-8") as rf:
        html = rf.readlines()
    html = "".join(html)
    soup = BeautifulSoup(html, "xml")
    pages = soup.find_all("page")
    with open("wiki_export.txt", "w+", encoding="utf-8") as wf:
        for page in pages:
            text = page.find("revision").find("text").string
            data = text[:-2].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "")
                field_map[field] = value
            # skill_rank(field_map)
            output = []
            for field in fields:
                # output.append("|" + field + "=" + field_map.get(field, ""))
                output.append(field_map.get(field, ""))
            # output = "{{角色\n" + "\n".join(output) + "}}\n"
            output = field_map.get("翻译名", "") + "\t" + "\t".join(output) + "\n"
            wf.write(output)


def read_xml_equip():
    fields = ["装备编号", 
"装备名称", 
"装备描述", 
"装备种类", 
"装等", 
"售价", 
"使用等级", 
"HP", 
"物理攻击", 
"魔法攻击", 
"物理防御", 
"魔法防御", 
"物理暴击", 
"魔法暴击", 
"HP自动回复", 
"TP自动回复", 
"回避", 
"生命吸收", 
"HP上升", 
"TP上升", 
"TP消耗减少", 
"命中", 
"HP强化", 
"物理攻击强化", 
"魔法攻击强化", 
"物理防御强化", 
"魔法防御强化", 
"物理暴击强化", 
"魔法暴击强化", 
"HP自动回复强化", 
"TP自动回复强化", 
"回避强化", 
"生命吸收强化", 
"HP上升强化", 
"TP上升强化", 
"TP消耗减少强化", 
"命中强化", 
"初始RANK", 
"初始地图", 
"合成价格", 
"合成材料", 
"孤儿装"]
    html = None
    with open("wiki_export_equip.xml", "r", encoding="utf-8") as rf:
        html = rf.readlines()
    html = "".join(html)
    soup = BeautifulSoup(html, "xml")
    pages = soup.find_all("page")
    with open("wiki_export.txt", "w+", encoding="utf-8") as wf:
        for page in pages:
            text = page.find("revision").find("text").string
            data = text[:-2].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "")
                field_map[field] = value
            output = []
            for field in fields:
                output.append(field_map.get(field, ""))
            output = page.find("title").string + "\t" + "\t".join(output) + "\n"
            wf.write(output)

if __name__ == "__main__":
    # process()
    read_xml()
    # read_xml_equip()
