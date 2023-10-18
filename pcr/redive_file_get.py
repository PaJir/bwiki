import os
import sys
import requests
import time
import random
from PIL import Image
from config import assert_path

# https://redive.estertion.win/sound/unit_battle_voice/103601/vo_btl_103601_applaud.m4a
redive_equip = "https://redive.estertion.win/icon/equipment/"
redive_item_icon = "https://redive.estertion.win/icon/item/"
redive_unit_icon = "https://redive.estertion.win/icon/unit/"
redive_unit_card = "https://redive.estertion.win/card/full/"
redive_unit_story = "https://redive.estertion.win/card/story/"
redive_spine = "https://redive.estertion.win/spine/still/unit/"
redive_spine_q = "https://redive.estertion.win/spine/unit/"

def get_png(redive, img_list=[], format="png", prefix=""):
    img_path = os.path.join(assert_path, "row")
    for name in img_list:
        name = str(name)
        print(name)
        name_webp = str(name) + ".webp"
        url = redive + name_webp
        try:
            myfile = requests.get(url)
        except:
            print("--------------error.get %s---------------" % name)
            continue
        if myfile.status_code != 200:
            myfile.close()
            continue
        open(os.path.join(img_path, name_webp), 'wb').write(myfile.content)
        myfile.close()
        try:
            im = Image.open(os.path.join(img_path, name_webp))
            im = im.convert("RGB")
            im.save(os.path.join(img_path, prefix + name + "." + format))
            os.remove(os.path.join(img_path, name_webp))
        except:
            pass
        t = 0.2 + random.random()
        time.sleep(t)


def get_spine(unit_list=[]):
    redive = redive_spine
    img_path = os.path.join(assert_path, "动画", "unit")
    for name in unit_list:
        for tp in [".skel", ".atlas", ".png"]:
            file_name = name + tp
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile, file_name)
                continue
            if myfile.status_code != 200:
                myfile.close()
                continue
            wf = ""
            if tp == ".skel":
                wf = "Skel " + name + ".odg"
            elif tp == ".atlas":
                wf = "Spine " + name + ".odp"
            else:
                wf = "Unit " + name + ".png"
            open(os.path.join(img_path, wf), "wb").write(myfile.content)
            myfile.close
        t = 0.2 + random.random()
        time.sleep(t)


def get_spine_q(unitq_list=[]):
    redive = redive_spine_q
    img_path = os.path.join(assert_path, "动画", "unitq")
    for name in unitq_list:
        if name[4] == "1":
            file_name = name[:4] + "01_BATTLE.cysp"
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            if myfile.status_code != 200:
                myfile.close()
                continue
            wf = name[:4] + "01_BATTLE.odg"
            open(os.path.join(img_path, wf), "wb").write(myfile.content)
            t = 0.2 + random.random()
            time.sleep(t)
        for tp in [".atlas", ".png"]:
            file_name = name + tp
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            if myfile.status_code != 200:
                myfile.close()
                continue
            wf = ""
            if tp == ".atlas":
                wf = "Spineq " + name + ".odp"
            else:
                wf = "Unitq " + name + ".png"
            open(os.path.join(img_path, wf), "wb").write(myfile.content)
            myfile.close
            t = 0.2 + random.random()
            time.sleep(t)


def get_spine_q2(unitq_list=[]):
    """特殊骨骼"""
    redive = "https://redive.estertion.win/spine/common/"
    # unitq_list = ["107001", "180101", "180201", "180301", "180401", "180501","180601",
    # "180701", "180801", "180901", "191501", "191601", "191701" ]
    img_path = os.path.join(assert_path, "动画", "unitq")
    for name in unitq_list:
        for tp in ["CHARA_BASE", "DEAR", "NO_WEAPON", "POSING", "RACE", "RUN_JUMP", "SMILE", "COMMON_BATTLE"]:
            file_name = name + "_" + tp + ".cysp"
            url = redive + file_name
            try:
                myfile = requests.get(url)
            except:
                print(myfile)
                continue
            if myfile.status_code != 200:
                myfile.close()
                continue
            wf = name + "_" + tp + ".odg"
            open(os.path.join(img_path, wf), "wb").write(myfile.content)
            t = 0.2 + random.random()
            time.sleep(t)


def webp2png(name):
    img_path = os.path.join(assert_path, "row")
    im = Image.open(os.path.join(img_path, name))
    im = im.convert("RGB")
    im.save(os.path.join(img_path, "Chr " + name[3:9] + ".jpg"))


def get_new_imgs(id : str):
    """获得一个角色的图标、立绘、剧情插图和动画文件"""
    get_png(redive_unit_icon, [id+"11", id+"31"], "png", "Icon_unit_")
    get_png(redive_unit_card, [id+"31"], "jpg", "Chr_")
    storys = []
    for i in range(1, 9):
        storys.append(id + "00" + str(i) + "01")
    get_png(redive_unit_story, storys, "png")
    get_spine([id+"11", id+"12", id+"13", id+"14", id+"15", id+"16", id+"17", id+"18", id+"31", id+"32"])
    get_spine_q([id+"11", id+"12", id+"31", id+"32"])


def get_6x_icon_chr(id : str):
    """开6x所需图片"""
    get_png(redive_unit_icon, [id+"61"], "png", "Icon_unit_")
    get_png(redive_unit_card, [id+"61"], "png", "Chr_")
    # storys = [id+"00501", id+"00601", id+"00701", id+"00801"] # 5-8
    storys = [id+"00801", id+"00901", id+"01001", id+"01101", id+"01201"]
    get_png(redive_unit_story, storys, "png")
    get_png(redive_item_icon, ["32"+id[1:]], "png", "Icon_item_")
    get_spine([id+"61", id+"62"])
    get_spine_q([id+"61"])


def get_equip_craft(img_list=[], format="png", prefix=""):
    """获取装备及其材料"""
    for equip in img_list:
        get_png(redive_equip, [equip, equip+10000, equip+20000])


if __name__ == "__main__":
    # for name in equip_list:
    #     webp2png(name)
    ids = ["1275"]
    # for id in ids:
        # get_new_imgs(id)
    # get_6x_icon_chr("1064")
    # get_spine_q2(["106401"])
    ids = [130772, 130792, 130802] # [131641, 132101, 132111, 132121]
    # get_equip_craft(ids)

    # get_png(redive_item_icon, ["32061"], "png", "Icon_item_")
    get_png(redive_unit_story, ["507600401", "507600501", "507600601", "507600602"], "jpg")
    # get_png(redive_unit_icon, ["106415", "191312"], "png", "Icon_unit_")