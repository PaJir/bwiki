from bs4 import BeautifulSoup
split_at = "\t"

fields = [
    "名称",
    "昵称",
    "稀有度",
    "属性",
    "id",
    "获取方式",
    "是否实装",
    "初始HP",
    "最大HP",
    "初始ATK",
    "最大ATK",
    "初始效果",
    "最大效果",
    "LV3觉醒",
    "LV5觉醒",
]

def read_xml():
    html = None
    with open("wiki_export_equip.xml", "r", encoding="utf-8") as rf:
        html = rf.readlines()
    html = "".join(html)
    soup = BeautifulSoup(html, "xml")
    pages = soup.find_all("page")
    with open("wiki_export_equip.txt", "w+", encoding="utf-8") as wf:
        for page in pages:
            text = page.find("revision").find("text").string
            data = text[:-3].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "<br>")
                field_map[field] = value
            output = []
            for field in fields:
                output.append(field_map.get(field, ""))
            output = field_map.get("名称", "") + "\t" + "\t".join(output) + "\n"
            wf.write(output)


if __name__ == "__main__":
    read_xml()
