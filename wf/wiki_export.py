from bs4 import BeautifulSoup
split_at = "\t"

fields = ["中文名",
    "日文名",
    "昵称",
    "性别",
    "类型",
    "职责",
    "种族",
    "属性",
    "稀有度",
    "CV",
    "简介",
    "获取方式",
    "id",
    "是否实装",
    "是否限定",
    "是否二板",
    "初始HP",
    "初始ATK",
    "最大HP",
    "最大ATK",
    "倍率",
    "段数",
    "必杀消耗",
    "能力",
    "日服实装日期",
    "体系",
    "称号1",
    "必杀",
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
    "日常",
    "加入",
    "进化"]

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
            data = text[:-3].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>")#.replace("\n", "<br>")
                field_map[field] = value
            output = []
            for field in fields:
                output.append(field_map.get(field, ""))
            output = field_map.get("中文名", "") + "\t" + "\t".join(output) + "\n"
            wf.write(output)


if __name__ == "__main__":
    read_xml()
