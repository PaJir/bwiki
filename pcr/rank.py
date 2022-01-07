# 从花舞RANK推荐表搬运到WikiRANK推荐表的脚本
# 输入为rank_input.txt
# 输出为rank.txt
import requests


def get_page():
    page = requests.get(
        "https://docs.qq.com/sheet/DYWxDbGdRYWV1bHFv?tab=6lwsay")
    page = page.content
    page = str(page.decode("utf-8"))
    with open("./rank.txt", "a+", encoding="utf-8") as f:
        f.write(page)


kv = {
    "空花(大江户)": "空花（大江户）",
    "怜(新年)": "怜（新年）",
    "日和莉(新年)": "日和莉（新年）",
    "妮侬(大江户)": "妮侬（大江户）",
    "真琴(夏日)": "真琴（夏日）",
    "惠理子(情人节)": "惠理子（情人节）",
    "绫音(圣诞节)": "绫音（圣诞节）",
    "珠希(夏日)": "珠希（夏日）",
    "朱希": "珠希",
    "佩可莉姆(夏日)": " 佩可莉姆（夏日）",
    "克里斯缇娜": "克莉丝提娜",
    "胡桃(圣诞节)": "胡桃（圣诞节）",
    "静流(情人节)": "静流（情人节）",
    "香织(夏日)": "香织（夏日）",
    "忍(万圣节)": "忍（万圣节）",
    "美冬(夏日)": "美冬（夏日）",
    "古蕾娅": "古蕾雅",
    "环奈(振袖)": "环奈（振袖）",
    "可可萝(夏日)": " 可可萝（夏日）",
    "蕾姆": "雷姆",
    "咲恋(夏日)": "咲恋（夏日）",
    "宫子(万圣节)": "宫子（万圣节）",
    "碧(插班生)": "碧（插班生）",
    "玲奈": "铃奈",
    "铃奈(夏日)": "铃奈（夏日）",
    "伊绪(夏日)": "伊绪（夏日）",
    "霞": "香澄",
    "优衣(新年)": "优衣（新年）",
    "千歌(圣诞节)": "千歌（圣诞节）",
    "铃莓(夏日)": "铃莓（夏日）",
    "凯露(夏日)": "凯露（夏日）",
    "真步(夏日)": "真步（夏日）",
    "美咲(万圣节)": "美咲（万圣节）",
    "镜华(万圣节)": "镜华（万圣节）",
    "未奏希(万圣节)": "未奏希（万圣节）",
    "美美(万圣节)": "美美（万圣节）",
    "克萝依": "克罗依"
}

with open("./rank_input.txt", encoding="utf-8") as rf:
    with open("./rank.txt", "w", encoding="utf-8") as wf:
        lines = ""
        for line in rf:
            lines += line
        lines = lines.split("图片\t")
        for line in lines:
            line = line[:-1].replace("\n", "<br/>")
            if line == "":
                continue
            line = line.split("\t")
            # print(line)
            wf.write("{{RANK推荐/行|")
            name = line[0].split("<br/>")[0]
            # 角色
            wf.write(kv.get(name, name))
            # 定位D 会战 竞技进攻 竞技防守 六星特性 星级 专武等级 专武解锁 升级 培养顺序M
            str2 = "|"+line[2]+"|"+line[3]+"|"+line[4]+"|"+line[5]+"|"+line[6]+"|"+line[7]+"|"+line[8]+"|"+line[9]+"|"+line[10]+"|"+line[11]
            # 花舞RANK推荐U 说明/备注V
            str2 += "|"+line[19]+"|"+line[20]+"}}\n"
            # str2.replace("~~~", "<nowiki>~~~</nowiki>")
            wf.write(str2)
            # break
