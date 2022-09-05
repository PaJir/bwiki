import requests
import json
import random
import time
import re


# 获取bilibili动态数据，uid为公主连结官方号
# 垃圾数据太多，没清理完
def get_data(next_offset, wf):
    next_offset = str(next_offset)
    print(next_offset)
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=353840826&offset_dynamic_id=" + \
        next_offset + \
        "&need_top=1&platform=web"

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://space.bilibili.com/8578857/video?tid=0&page=3&keyword=&order=pubdate',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache'
    }
    req = requests.get(url, headers=headers).text
    # print(req)
    json_str = json.loads(req)
    if json_str["code"] != 0:
        print(json_str)
        return
    data = json_str["data"]
    if "cards" not in data:
        print("finish")
        return
    cards = data["cards"]
    for card in cards:
        # wf.write(repr(card))
        wf.write("https://t.bilibili.com/" + str(card["desc"]["dynamic_id"]) + "\t")
        item_card = json.loads(card["card"])
        # item_card = card["card"]
        # print(item_card)
        description = ""
        if "item" in item_card:
            if "description" in item_card["item"]:
                description = item_card["item"]["description"]
            elif "content" in item_card["item"]:
                description = "\t\t" + item_card["item"]["content"]
        elif "title" in item_card:
            description = "\t" + item_card["title"]
        description = description.replace("\n", "<br>")
        wf.write(description + "\n")
    next_offset = data["next_offset"]
    t = 0.2 + random.random()
    time.sleep(t)
    get_data(next_offset)


def get_all_data():
    wf = open("activity.txt", "a", encoding="utf-8")
    get_data(948263989047341476, wf)
    wf.close()


def get_date(dy):
    """ reutrn: [m1, d1, h1, min1, m2, d2, h2, min2]"""
    # dy = dy.split("庆典期间")[1]
    date_all = re.findall(r"(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})", dy)
    if len(date_all) != 2:
        return [""] * 8
    m1d1, h1min1 = date_all[0].split(" ")
    m1, d1 = m1d1.split("/")
    h1, min1 = h1min1.split(":")
    m2d2, h2min2 = date_all[1].split(" ")
    m2, d2 = m2d2.split("/")
    h2, min2 = h2min2.split(":")
    min2 = str((int(min2)+1) % 60)
    if min2 == "0":
        h2 = str((int(h2)+1) % 24)
    if h2 == "0":
        print(m2, h2, "---------")
        m2 = str(int(m2)+1)
    return [m1, d1, h1, min1, m2, d2, h2, min2]


def format_data():
    rf = open("activity.txt", "r", encoding="utf-8")
    wf = open("activity2.txt", "w", encoding="utf-8")
    line = rf.readline()
    wf.write(line)
    line = rf.readline()
    while line:
        [y1, m1, d1, h1, min1, y2, m2, d2, h2, min2, activity0, detail0, note, link, dy1, dy2, dy3] = line.split("\t")
        dy = dy1 + dy2 + dy3  # dynamic
        new_date = [""] * 8
        if "「普通关卡」掉落量2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "N2"
        elif "「普通关卡」掉落量3倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "N3"
        elif "「困难关卡」掉落量2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "H2"
        elif "「困难关卡」掉落量3倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "H3"
        elif "「探索」掉落量2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "探索2倍"
        elif "「探索」掉落量3倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "探索3倍"
        elif "「地下城」玛那掉落量2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "地下城2倍"
        elif "「地下城」玛那掉落量3倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "地下城3倍"
        elif "「神殿调查」掉落量2倍庆典" in dy or "「圣迹调查」掉落量2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "调查2倍"
        elif "「每日任务报酬」2倍庆典" in dy:
            new_date = get_date(dy)
            activity = "加倍"
            detail = "每日任务报酬2倍"
        if m1 == "" and new_date != [""] * 8:
            (m1, d1, h1, min1, m2, d2, h2, min2) = new_date
            activity0 = activity
            detail0 = detail
        if m1 != "":
            [m1, d1, h1, min1, m2, d2, h2, min2] = [_.zfill(2) for _ in [m1, d1, h1, min1, m2, d2, h2, min2]]
        wf.write("\t".join([y1, m1, d1, h1, min1, y2, m2, d2, h2, min2, activity0, detail0, note, link, dy1, dy2, dy3]))
        line = rf.readline()

    rf.close()
    wf.close()


format_data()
"""
data
	cards[]
		desc
			dynamic_id
		card 解析
			item
				description
"""
