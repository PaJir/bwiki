import os
import sys
import requests
import time
import random
from PIL import Image

# https://redive.estertion.win/sound/unit_battle_voice/103601/vo_btl_103601_applaud.m4a
redive_equip = "https://redive.estertion.win/icon/equipment/"
redive_item_icon = "https://redive.estertion.win/icon/item/"
redive_unit_icon = "https://redive.estertion.win/icon/unit/"
redive_unit_card = "https://redive.estertion.win/card/full/"
redive_unit_story = "https://redive.estertion.win/card/story/"
redive_spine = "https://redive.estertion.win/spine/still/unit/"
redive_spine_q = "https://redive.estertion.win/spine/unit/"

def get_png(redive, img_list=[], format="png", prefix=""):
    img_path = "D:\Extra\pcr\\row\\"
    for equip in img_list:
        # equip = str(equip)
        print(str(equip))
        file_name = str(equip) + ".webp"
        url = redive + file_name
        try:
            myfile = requests.get(url)
        except:
            print("--------------error.get---------------")
            continue
        open(img_path + file_name, 'wb').write(myfile.content)
        myfile.close()
        try:
            im = Image.open(img_path + file_name)
            im = im.convert("RGB")
            im.save(img_path + prefix + equip + "." + format)
        except:
            pass
        t = 0.2 + random.random()
        time.sleep(t)


def get_spine(unit_list=[]):
    redive = redive_spine
    img_path = "D:\Extra\pcr\\动画\\unit\\"
    for equip in unit_list:
        for tp in [".skel", ".atlas", ".png"]:
            file_name = equip + tp
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile, file_name)
                continue
            wf = ""
            if tp == ".skel":
                wf = "Skel " + equip + ".odg"
            elif tp == ".atlas":
                wf = "Spine " + equip + ".odp"
            else:
                wf = "Unit " + equip + ".png"
            open(img_path + wf, "wb").write(myfile.content)
            myfile.close
        t = 0.2 + random.random()
        time.sleep(t)


def get_spine_q(unitq_list):
    redive = redive_spine_q
    img_path = "D:\Extra\pcr\\动画\\unitq\\"
    for equip in unitq_list:
        if equip[4] == "1":
            file_name = equip[:4] + "01_BATTLE.cysp"
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            wf = equip[:4] + "01_BATTLE.odg"
            open(img_path + wf, "wb").write(myfile.content)
            t = 0.2 + random.random()
            time.sleep(t)
        for tp in [".atlas", ".png"]:
            file_name = equip + tp
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            wf = ""
            if tp == ".atlas":
                wf = "Spineq " + equip + ".odp"
            else:
                wf = "Unitq " + equip + ".png"
            open(img_path + wf, "wb").write(myfile.content)
            myfile.close
            t = 0.2 + random.random()
            time.sleep(t)


def get_spine_q2():
    """特殊骨骼"""
    redive = "https://redive.estertion.win/spine/common/"
    unitq_list = ["107001", "180101", "180201", "180301", "180401", "180501","180601",
    "180701", "180801", "180901", "191501", "191601", "191701" ]
    img_path = "D:\Extra\pcr\\动画\\unitq\\"
    for equip in unitq_list:
        for tp in ["CHARA_BASE", "DEAR", "NO_WEAPON", "POSING", "RACE", "RUN_JUMP", "SMILE", "COMMON_BATTLE"]:
            file_name = equip + "_" + tp + ".cysp"
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            wf = equip + "_" + tp + ".odg"
            open(img_path + wf, "wb").write(myfile.content)
            t = 0.2 + random.random()
            time.sleep(t)


def webp2png(name):
    img_path = "D:\Extra\pcr\\row"
    im = Image.open(img_path + name)
    im = im.convert("RGB")
    im.save(img_path + "Chr " + name[3:9] + ".jpg")


def get_new_imgs(id):
    """获得一个角色的图标、立绘、剧情插图和动画文件"""
    get_png(redive_unit_icon, [id+"11", id+"31"], "png", "Icon_unit_")
    get_png(redive_unit_card, [id+"31"], "jpg", "Chr_")
    storys = []
    for i in range(1, 7):
        storys.append(id + "00" + str(i) + "01")
    get_png(redive_unit_story, storys, "png")
    get_spine([id+"11", id+"12", id+"31", id+"32"])
    get_spine_q([id+"11", id+"12", id+"31", id+"32"])


if __name__ == "__main__":
    # get_spine_q2()
    # for name in equip_list:
    #     webp2png(name)
    id = sys.argv[1]
    if not id:
        id = "1236"
    get_new_imgs(id)
