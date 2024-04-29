import os
import json
import requests
from common import get_keywords
import random
import time
from tqdm import tqdm

MINION_URL = 'https://api.blizzard.com/hearthstone/cards?gameMode=battlegrounds&pageSize=500&locale=zh_CN'
'https://api.blizzard.com/hearthstone/cards?bgCardType=minion&gameMode=battlegrounds&pageSize=500&locale=zh_CN' # 随从 手下
FULL_JSON_FILE = "./blizzard_2922.json"
LAST_JSON_FILE = "./blizzard_292.json"
IMG_PATH = "blizzard"
OUTPUT_FILE = "./blizzard.txt"
headers = {
  'Accept': '*/*', 
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', 
  'Authorization': 'Bearer KRWpkSRImus70XdDJxtFmU78r8l2hXSIpR', 
  'Cache-Control': 'no-cache', 
  'Connection': 'keep-alive', 
  'Content-Type': 'application/json', 
  'Host': 'api.blizzard.com',
  'If-None-Match': 'W/"695c5-xqQ+Mj5oyaYeQ6gOI/KHvRc/xgU"',
  'Origin': 'https://hearthstone.blizzard.com', 
  'Pragma': 'no-cache', 
  'Referer': 'https://hearthstone.blizzard.com/zh-tw/battlegrounds', 
  'Sec-Fetch-Dest': 'empty', 
  'Sec-Fetch-Mode': 'cors', 
  'Sec-Fetch-Site': 'same-site', 
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
}
def read_json_file(filename, url, force=False, write_format="w+"):
    if not force and os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as rf:
            lines = rf.readlines()
        lines = "".join(lines)
        return json.loads(lines)
    else:
        req = requests.get(url, headers=headers).text
        req = json.loads(req)
        if req["page"] < req["pageCount"]:
            more = read_json_file("", MINION_URL+"&page="+str(req["page"]+1), True, "a")
            req["cards"] += more
        if req["page"] == 1:
            with open(filename, write_format, encoding="utf=8") as wf:
                wf.write(json.dumps(req["cards"], ensure_ascii=False))
        return req["cards"]

def get_img(img_path, filename, url, force=False):
    filename = os.path.join(img_path, filename)
    if not force and (os.path.exists(filename) or url == ""):
        return
    try:
        myfile = requests.get(url)
    except:
        print("error get file: %s" % filename)
        return
    if myfile.status_code != 200:
        return
    open(filename, "wb").write(myfile.content)
    myfile.close()
    t = 0.2 + random.random()
    time.sleep(t)


# 衍生、金色卡都扒下来，不知道含不含退环境的
def get_full_json():
    cards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards_id_map = {}
    for card in cards:
        cards_id_map[card["id"]] = card
    for card in tqdm(cards):
        childs = card.get("childIds", [])
        if card["battlegrounds"].get("companionId") is not None:
            childs.append(card["battlegrounds"]["companionId"])
        if card["battlegrounds"].get("upgradeId") is not None:
            childs.append(card["battlegrounds"]["upgradeId"])
        for childId in childs:
            if cards_id_map.get(childId) is None:
                more = requests.get(MINION_URL+"&ids="+str(childId), headers=headers).text
                more = json.loads(more)
                if more["cardCount"] != 0:
                    cards_id_map[more["cards"][0]["id"]] = more["cards"][0]
    with open(FULL_JSON_FILE, "w+", encoding="UTF-8") as wf:
        wf.write(json.dumps(cards_id_map, ensure_ascii=False))

wf = None

minion_type_map = {
    0: "",
    11: "亡灵",
    14: "鱼人",
    15: "恶魔",
    17: "机械",
    18: "元素",
    20: "野兽",
    23: "海盗",
    24: "龙",
    26: "全部",
    43: "野猪人",
    92: "纳迦"
}
force_update_ids = [
]
def diff_desc(card1, card2, _type):
    if card1 is None:
        return "{{更新|类型=%s|dbfid=%d|描述=%s。}}" % (_type, card2["id"], "新增")
    if card2 is None:
        return "{{更新|类型=%s|dbfid=%d|描述=%s。}}" % (_type, card1["id"], "移除")
    diff = []
    mode1 = "单人,双打"
    if card1["battlegrounds"]["duosOnly"]:
        mode1 = "双打"
    elif card1["battlegrounds"]["solosOnly"]:
        mode1 = "单人"
    mode2 = "单人,双打"
    if card2["battlegrounds"]["duosOnly"]:
        mode2 = "双打"
    elif card2["battlegrounds"]["solosOnly"]:
        mode2 = "单人"
    if card1["name"] != card2["name"]:
        diff.append("中文名「%s」->「%s」" % (card1["name"], card2["name"]))
    if card1["battlegrounds"].get("tier", 0) != card2["battlegrounds"].get("tier", 0):
        diff.append("等级%d->%d" % (card1["battlegrounds"].get("tier", 0), card2["battlegrounds"].get("tier", 0)))
    if card1.get("attack", 0) != card2.get("attack", 0):
        diff.append("攻击力%d->%d" % (card1.get("attack", 0), card2.get("attack", 0)))
    if card1.get("health", 0) != card2.get("health", 0):
        diff.append("血量%d->%d" % (card1.get("health", 0), card2.get("health", 0)))
    if card1.get("armor", 0) != card2.get("armor", 0):
        diff.append("护甲%d->%d" % (card1.get("armor", 0), card2.get("armor", 0)))
    if card1.get("manaCost", 0) != card2.get("manaCost", 0):
        diff.append("费用%d->%d" % (card1.get("manaCost", 0), card2.get("manaCost", 0)))
    if mode1 != mode2:
        diff.append("模式%s->%s" % (mode1, mode2))
    if card1.get("text", "") != card2.get("text", ""):
        diff.append("效果「%s」->「%s」" % (card1.get("text", ""), card2.get("text", "")))
    

    return "{{更新|类型=%s|dbfid=%d|描述=%s。}}" % (_type, card1["id"], "，".join(diff))
# 4
def minions_str(card, force=False):
    if card is None:
        return ""
    info = []
    version = "普通"
    if card.get("金色", False):
        version = "金色"
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["imageGold"], card["id"] in force_update_ids or force)
    elif card.get("衍生", False):
        version = "衍生"
        # get_img(IMG_PATH, str(card["id"])+".png", card["image"])
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"], card["id"] in force_update_ids or force)
    # elif card["imageGold"] != "":
    #     get_img(IMG_PATH, str(card["id"])+".png", card["imageGold"])
    else:
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"], card["id"] in force_update_ids or force)
    # 名称 dbfid 等级 攻 血 类型 跟随随从池 版本 描述
    info.append(card["id"])
    info.append(card["name"])
    info.append(card["id"])
    info.append(card["battlegrounds"]["tier"])
    info.append(card["attack"])
    info.append(card["health"])
    # TODO: multiTypeIds
    card["minionTypeId"] = card.get("minionTypeId", 0)
    info.append(minion_type_map.get(card["minionTypeId"], card["minionTypeId"]))
    info.append(minion_type_map.get(card["minionTypeId"], ""))
    info.append(version)
    # 模式
    modes = "单人,双打"
    if card["battlegrounds"]["duosOnly"]:
        modes = "双打"
    elif card["battlegrounds"]["solosOnly"]:
        modes = "单人"
    info.append(modes)
    info.append(card["text"])
    # 关键字
    info.append(get_keywords(card["text"]))
    childIds = card.get("childIds", [])
    childIds = list(set(childIds))
    upgradeId = card["battlegrounds"].get("upgradeId", "")
    if upgradeId in childIds:
        childIds.remove(upgradeId)
    # 金色版dbfid （金色版本描述）
    info.append(upgradeId)
    # 衍生
    info.append(",".join([str(c) for c in childIds]))
    return "\t".join([str(c) for c in info]) + "\n"
def minions_prepare(cards):
    # prepare
    for card in cards.values():
        for id in card.get("childIds", []):
            if cards.get(str(id)) is not None:
                cards[str(id)]["衍生"] = True
        upId = card["battlegrounds"].get("upgradeId")
        if upId is not None and cards.get(str(upId)) is not None:
            cards[str(upId)]["金色"] = True
    cards = list(filter(lambda x : x["cardTypeId"] == 4, cards.values()))
    cards.sort(key=lambda x : x["id"])
    cards = dict(map(lambda x: (x["id"], x), cards))
    return cards
def minions_dump():
    cards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = minions_prepare(cards)
    for card in tqdm(cards.values()):
        _str = minions_str(card)
        wf.write(_str)
def minions_diff(force=True):
    cards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = minions_prepare(cards)
    lastcards = read_json_file(LAST_JSON_FILE, "")
    lastcards = minions_prepare(lastcards)
    diffs = []
    for card in tqdm(cards.values()):
        _str = minions_str(card)
        _str2 = minions_str(lastcards.get(card["id"]))
        if _str != _str2:
            minions_str(card, force)
            wf.write(_str)
            diffs.append(diff_desc(lastcards.get(card["id"]), card, "随从"))
    for id in tqdm(lastcards.keys()):
        if cards.get(id) is None:
            diffs.append(diff_desc(lastcards[id], None, "随从"))
    wf.write("\n".join(diffs))
# 3
def heroes_str(card, fullcards):
    if card is None:
        return ""
    info = []
    # 名称 dbfid 血 护甲 画家 介绍
    info.append(card["id"])
    info.append(card["name"])
    info.append(card["id"])
    info.append(card.get("health", 0))
    info.append(card.get("armor", 0))
    info.append(card["artistName"])
    info.append(card["flavorText"])
    # 模式
    modes = "单人,双打"
    if card["battlegrounds"]["duosOnly"]:
        modes = "双打"
    elif card["battlegrounds"]["solosOnly"]:
        modes = "单人"
    info.append(modes)

    # 技能dbfid 伙伴dbfid 衍生
    childIds = card["childIds"]
    companionId = card["battlegrounds"].get("companionId")
    if companionId is not None and companionId not in childIds:
        childIds.append(companionId)
    childIds = list(set(childIds))
    child_cards = list(filter(lambda x : x["id"] in childIds, fullcards.values()))

    skills = list(filter(lambda x : x["cardTypeId"] == 10, child_cards))
    companions = list(filter(lambda x : x["id"] == companionId, child_cards))
    more = list(filter(lambda x : x["cardTypeId"] == 4 and x["id"] != companionId, child_cards))
    info.append(",".join([str(c["id"]) for c in skills]))
    info.append(",".join([str(c["id"]) for c in companions]))
    info.append(",".join([str(c["id"]) for c in more]))
    return "\t".join([str(c) for c in info]) + "\n"
def heroes_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 3, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
        _str = heroes_str(card, fullcards)
        wf.write(_str)
def heroes_diff(force=True):
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 3, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    cards = dict(map(lambda x: (x["id"], x), cards))
    fulllastcards = read_json_file(LAST_JSON_FILE, "")
    lastcards = list(filter(lambda x : x["cardTypeId"] == 3, fulllastcards.values()))
    lastcards = dict(map(lambda x: (x["id"], x), lastcards))
    diffs = []
    for card in tqdm(cards.values()):
        _str = heroes_str(card, fullcards)
        _str2 = heroes_str(lastcards.get(card["id"]), fulllastcards)
        if _str != _str2:
            get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"], force)
            wf.write(_str)
            diffs.append(diff_desc(lastcards.get(card["id"]), card, "英雄"))
    for id in tqdm(lastcards.keys()):
        if cards.get(id) is None:
            diffs.append(diff_desc(lastcards[id], None, "英雄"))
    wf.write("\n".join(diffs))
# 10
def skills_str(card):
    if card is None:
        return ""
    info = []
    # 名称 dbfid 消耗 描述
    info.append(card["id"])
    info.append(card["name"])
    info.append(card["id"])
    info.append(card["manaCost"])
    info.append(card["text"])
    return "\t".join([str(c) for c in info]) + "\n"
def skills_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 10, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        _str = skills_str(card)
        wf.write(_str)
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
def skills_diff(force=True):
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 10, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    cards = dict(map(lambda x: (x["id"], x), cards))
    lastcards = read_json_file(LAST_JSON_FILE, "")
    lastcards = list(filter(lambda x : x["cardTypeId"] == 10, lastcards.values()))
    lastcards = dict(map(lambda x: (x["id"], x), lastcards))
    diffs = []
    for card in tqdm(cards.values()):
        _str = skills_str(card)
        _str2 = skills_str(lastcards.get(card["id"]))
        if _str != _str2:
            get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"], force)
            wf.write(_str)
            diffs.append(diff_desc(lastcards.get(card["id"]), card, "英雄"))
    for id in tqdm(lastcards.keys()):
        if cards.get(id) is None:
            diffs.append(diff_desc(lastcards[id], None, "英雄"))
    wf.write("\n".join(diffs))
# 5 12
def tasks_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 5 and x["classId"] == 12, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        if card["text"].find("任务") == -1:
            continue
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
# 40
def rewards_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 40, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
# 43
def distortions_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 43, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
# 42
def spells_str(card):
    if card is None:
        return ""
    modes = "单人,双打"
    if card["battlegrounds"]["duosOnly"]:
        modes = "双打"
    elif card["battlegrounds"]["solosOnly"]:
        modes = "单人"
    _str = "{{酒馆法术|dbfid=%d|名称=%s|等级=%d|消耗=%d|模式=%s|描述=%s}}\n" % (card["id"], card["name"], card["battlegrounds"]["tier"], card["manaCost"], modes, card["text"])
    return _str
def spells_dump():
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 42, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    for card in tqdm(cards):
        _str = spells_str(card)
        get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"])
        wf.write(_str)
def spells_diff(force=True):
    fullcards = read_json_file(FULL_JSON_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 42, fullcards.values()))
    cards.sort(key=lambda x : x["id"])
    cards = dict(map(lambda x: (x["id"], x), cards))
    lastcards = read_json_file(LAST_JSON_FILE, "")
    lastcards = list(filter(lambda x : x["cardTypeId"] == 42, lastcards.values()))
    lastcards = dict(map(lambda x: (x["id"], x), lastcards))
    diffs = []
    for card in tqdm(cards.values()):
        _str = spells_str(card)
        _str2 = spells_str(lastcards.get(card["id"]))
        if _str != _str2:
            get_img(IMG_PATH, str(card["id"])+".png", card["battlegrounds"]["image"], force)
            wf.write(_str)
            diffs.append(diff_desc(lastcards.get(card["id"]), card, "酒馆法术"))
    for id in tqdm(lastcards.keys()):
        if cards.get(id) is None:
            diffs.append(diff_desc(lastcards[id], None, "酒馆法术"))
    wf.write("\n".join(diffs))


if __name__ == "__main__":
    # read_json_file(FULL_JSON_FILE, MINION_URL, True)
    # get_full_json()
    wf = open(OUTPUT_FILE, "w+", encoding="utf-8")
    # minions_dump()
    # heroes_dump()
    # skills_dump()
    # tasks_dump()
    # rewards_dump()
    # distortions_dump()
    # spells_dump()
    minions_diff(True)
    # heroes_diff(False)
    # skills_diff()
    # spells_diff(False)
    wf.close()