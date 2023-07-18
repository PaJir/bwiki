import os
import json
import requests

PARTY_ALL_URL = "https://www.laysong.com/api/party_all"
PARTY_ALL = "./wx_party_all.json"
ICON_CHARA_URL = "https://www.laysong.com/api/get_icon/chara"
ICON_CHARA = "./wx_icon_chara.json"
ICON_WEAPO_URL = "https://www.laysong.com/api/get_icon/weapon"
ICON_WEAPO = "./wx_icon_weapo.json"
OUTPUT_FILE = "./wx_dump.txt"

fix_name = {
    "舒尔特": "休尔特",
    "帕亚舒战斧": "帕拉修",
    "八尺镜": "八咫镜",
    "八尺琼曲玉": "八尺琼勾玉",
    "菲利亚": "菲莉亚",
    "菲利亚(周年)": "菲莉亚(周年)",
    "基因穿孔器": "基因组穿孔器",
    "娜西尔": "娜希尔",
    "卡莉奥斯特罗": "卡莉奥丝特罗",
    "彩虹发射器": "虹彩起爆器",
    "黄金钉耙": "黄金耙",
    "潮湿法杖": "湛蓝魔杖",
    "尤娜": "优娜",
    "雷吉斯(礼服)": "雷吉斯(周年)",
    "杰拉尔(夏日)": "杰拉尔(泳装)",
    "24/7": "24／7",
    "捉弄爪": "捣蛋钩爪",
    "糖果杖": "糖果长杖",
    "镭射标枪": "激光标枪",
    "爱丽丝(夏日)": "爱丽丝(泳装)",
    "塞西莉亚": "赛希莉亚",
    "塞西莉亚(周年)": "赛希莉亚(周年)",
    "蒂妮(黎明)": "蒂妮(沙漠)",
    "亚美莉亚(半周年)": "亚美莉亚(礼服)",
    "月桂女神的石板": "达佛涅斯石板",
    "菜月昴": "菜月·昴",
    "艾丝缇莉艾尔(半周年)": "艾丝缇莉艾尔(礼服)",
    "赛吉尔(半周年)": "赛吉尔(礼服)",
    "太平经": "太平清领",
    "索缇艾丝": "索媞艾丝",
    "兹因可": "兹茵可",
    "索妮雅(黎明)": "索妮雅(沙漠)",
    "露格尼卡童话集": "露格尼卡童话抄本",
    "炽热之剑": "高热剑",
    "希望之刃": "希望誓剑",
    "玛丽娜(夏日)": "玛丽娜(泳装)",
    "塞里奥尔": "塞里奥尔",
    "奥莉维亚": "奥莉维尔",
}

wf = open(OUTPUT_FILE, "w+", encoding="utf-8")

def read_json_file(filename, url):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as rf:
            lines = rf.readlines()
        lines = "".join(lines)
        return json.loads(lines)
    else:
        req = requests.get(url).text
        with open(filename, "w+", encoding="utf=8") as wf:
            wf.write(req)
        return json.loads(req)
    
def list_to_map(lists):
    ret = {}
    for l in lists:
        ret[l["id"]] = l
    return ret

party = read_json_file(PARTY_ALL, PARTY_ALL_URL)
chara = read_json_file(ICON_CHARA, ICON_CHARA_URL)
chara = list_to_map(chara)
weapo = read_json_file(ICON_WEAPO, ICON_WEAPO_URL)
weapo = list_to_map(weapo)

def chara_id_to_name(id):
    cnname = chara[id]["cnname"].replace("（", "(").replace("）", ")")
    if cnname == "-":
        return ""
    return fix_name.get(cnname, cnname)

def weapo_id_to_name(id):
    cnname = weapo[id]["cnname"]
    if cnname == "-":
        return ""
    return fix_name.get(cnname, cnname)

start = 600
for plate_idx in range(start, min(start+100, len(party))):
    plate = party[plate_idx]
    c = [""] * 6
    w = [""] * 6
    info = [""] * 6
    bad_plate = ""
    for item in plate["items"]:
        if item["sort"] is None or not (1 <= item["sort"] <= 6):
            print(item, "error")
            bad_plate = "no"
            continue
        if item["type"] == 1:
            c[item["sort"]-1] = chara_id_to_name(item["targetId"])
        elif item["type"] == 2:
            w[item["sort"]-1] = weapo_id_to_name(item["targetId"])
        elif item["type"] == 3:
            if not (1 <= item["sort"] <= 3):
                print(item, "error4")
                continue
            w[item["sort"]+2] = weapo_id_to_name(item["targetId"])
        else:
            print(item, "error2")
    # info
    if plate["mb2"]:
        info = plate["mb2"].split(",")
        info = ["二板：" + i for i in info]
    # title
    title = ""
    if plate["description"]:
        title += plate["description"].lower()
    source = plate["source"].strip()
    if source != "待补充":
        if source.find("bilibili") != -1 or source.find("b23") != -1:
            title += "-[%s B站]" % source
        elif source.find("nga") != -1:
            title += "-[%s NGA]" % source
        elif source.find("BV") != -1:
            title += "-[https://www.bilibili.com/video/%s B站]" % source
        elif source.find("tieba") != -1:
            title += "-[%s 贴吧]" % source
        elif source.find("taptap") != -1:
            title += "-[%s taptap]" % source
        elif source.find("gamer") != -1:
            title += "-[%s 磁场]" % source
        else:
            title += "-[%s 来源]" % source
            print(plate, "error3")
    
    wf.write("{{盘子<!--%d-->\n" % plate["id"])
    for i in range(6):
        wf.write("|%s|%s|%s\n" % (c[i], w[i], info[i]))
    wf.write("|标题=%s|%s|%s\n}}" % (title, bad_plate, plate["property"]))
