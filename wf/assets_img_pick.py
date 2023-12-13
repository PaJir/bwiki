# 提取特定的一些文件并命名为中文
import os
import shutil
from en2cn import en2cn
from pngToGif import zoomIn, zoomInMargin
from assets_map import equipments

root_path = "E:\\wf_cn\\output\\assets\\"
battle_path = root_path + "battle"
character_path = root_path + "character"
boss_coin_path = root_path + "item\\materials\\boss_coin"
equip_coin_path = root_path + "item\\equipment"
icon_path = root_path + "out"
icon_path2 = root_path + "out2"
chr_path = root_path + "chr"
battle_icon_path = root_path + "battle_icon"
coin_out_path = root_path + "coin_out"
equip_coin_out_path = root_path + "item\\equipment_cn"
special_out_path = root_path + "special"
pixel_out_path = root_path + "pixel"

def copyIfNotExist(from_path, to_path):
    if not os.path.exists(from_path):
        return
    if os.path.exists(to_path):
        return
    shutil.copyfile(from_path, to_path)

def battle(path):
    file_list = os.listdir(path)
    for name in file_list:
        full_name = os.path.join(path, name)
        if os.path.isdir(full_name):
            battle(full_name)
        elif name.endswith(".png"):
            shutil.copyfile(full_name, os.path.join(battle_icon_path, name))


def character(path):
    file_list = os.listdir(path)
    for name in file_list:
        full_path = os.path.join(path, name, "ui", "square_132_132_1.png")
        if not os.path.exists(full_path):
            continue
        name_cn = en2cn(name)
        if name_cn == "":
            print("error: no cn name ", name)
            # continue
            name_cn = name
        icon_path0 = os.path.join(path, name, "ui", "square_132_132_0.png")
        icon_path1 = os.path.join(path, name, "ui", "square_132_132_1.png")
        copyIfNotExist(icon_path0, os.path.join(icon_path, name_cn+".png"))
        copyIfNotExist(icon_path1, os.path.join(icon_path2, name_cn+"5.png"))
        chr_path0 = os.path.join(path, name, "ui", "full_shot_1440_1920_0.png")
        chr_path1 = os.path.join(path, name, "ui", "full_shot_1440_1920_1.png")
        copyIfNotExist(chr_path0, os.path.join(chr_path, name_cn+"0.png"))
        copyIfNotExist(chr_path1, os.path.join(chr_path, name_cn+"1.png"))
        special_path = os.path.join(path, name, "pixelart", "animated", "special.gif")
        copyIfNotExist(special_path, os.path.join(special_out_path, name_cn+"special.gif"))
        pixel_list = os.listdir(os.path.join(path, name, "pixelart", "sprite_sheet"))
        pixel_path = os.path.join(path, name, "pixelart", "sprite_sheet", pixel_list[0])
        zoomInMargin(pixel_path, os.path.join(pixel_out_path, "像素"+name_cn+".png"), 5, 100, 100)

def materials(path):
    file_list = os.listdir(path)
    for name in file_list:
        name = name[:-4]
        tp = name[-1]
        name_cn = en2cn(name[:-2])
        if name_cn == "":
            print("error: no cn boss name: ", name)
            continue
        icon_path = os.path.join(path, name + ".png")
        if tp == "1":
            name_cn += "银币"
        elif tp == "2":
            name_cn += "金币"
        elif tp == "3":
            name_cn += "紫币"
        else:
            print("error: no boss icon type: ", tp)
            continue
        new_image = os.path.join(coin_out_path, name_cn+".png")
        zoomIn(icon_path, new_image, 5, 0, 20, 0, 20)

def equip_coin(path, out_path):
    file_list = os.listdir(path)
    for name in file_list:
        full_name = os.path.join(path, name)
        if os.path.isdir(full_name):
            equip_coin(full_name, out_path)
        elif name.endswith(".png"):
            name_en = name[:-4]
            found = False
            for e in equipments:
                if equipments[e][6].split("/")[-1] == name_en:
                    shutil.copyfile(full_name, os.path.join(out_path, equipments[e][1]+".png"))
                    found = True
                    break
            if not found:
                shutil.copyfile(full_name, os.path.join(out_path, name))

def bossProfile(bossname, frame, right, down):
    in_ = os.path.join(root_path, "battle\\boss", bossname, ".gen", bossname, frame+".png")
    out_ = os.path.join(root_path, "battle\\boss", bossname, ".gen", bossname, frame+"2.png")
    zoomIn(in_ , out_, 5, 0, right, 0, down)


if __name__ == "__main__":
    for path in [
        icon_path, 
        icon_path2, 
        chr_path, 
        battle_icon_path,
        coin_out_path,
        equip_coin_out_path,
        special_out_path,
        pixel_out_path
        ]:
        if not os.path.exists(path):
            os.makedirs(path)
    # battle(battle_path)
    character(character_path)
    # materials(boss_coin_path)
    # equip_coin(equip_coin_path, equip_coin_out_path)
    # bossProfile("devil_commander_evil_envy", "00cm", 68, 51)