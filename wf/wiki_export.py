from bs4 import BeautifulSoup
split_at = "\t"

fields = ["中文名",
    "日文名",
    "称号1",
    "昵称",
    "稀有度",
    "定位",
    "属性",
    "种族",
    "性别",
    "初始HP",
    "最大HP",
    "初始ATK",
    "最大ATK",
    "CV",
    "获取方式",
    "必杀",
    "必杀消耗",
    "必杀效果",
    "技能效果",
    "队长技",
    "队长技效果",
    "被动一",
    "被动二",
    "被动三",
    "被动四",
    "被动五",
    "被动六",
    "故事一",
    "故事二",
    "故事三",
    "评价人B站UID",
    "评价人名称",
    "评价",
    "配队人B站UID",
    "配队人名称",
    "配队"]

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
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "<br>")
                field_map[field] = value
            output = []
            for field in fields:
                output.append(field_map.get(field, ""))
            output = field_map.get("中文名", "") + "\t" + "\t".join(output) + "\n"
            wf.write(output)


if __name__ == "__main__":
    read_xml()
