# 裁剪、更改图片尺寸
import os
import numpy as np
from PIL import Image
from config import assert_path

def comic(filepath, savepath):
    files = os.listdir(filepath)
    for file in files:
        filename = os.path.join(filepath, file)
        # savename = os.path.join(savepath, "comic_" + file[8:14] + ".png")
        savename = os.path.join(savepath, file)
        if file.startswith("comic"):
            savename = os.path.join(savepath, "comic_"+file[8:14]+".png")
        if os.path.exists(savename):
            continue
        im = Image.open(filename)
        if file.startswith("comic"):
            out = im.resize((512, 400), Image.ANTIALIAS)
        else:
            out = im.resize((240,135), Image.ANTIALIAS)
        out.save(savename)


def story_still(filepath, savepath):
    files = os.listdir(filepath)
    for file in files:
        if not file.startswith("still"):
            continue
        filename = os.path.join(filepath, file)
        savename = os.path.join(savepath, file[6:-3] + "jpg")
        if os.path.exists(savename):
            continue
        im = Image.open(filename)
        out_size = (1024,576)
        if im.size == (1024, 1024):
            out_size = (1024, 1024)
        elif im.size == (2048, 1024):
            out_size = (2048, 1152)
        elif im.size != (1024, 512):
            print(file)
            continue
        im = im.convert("RGB")
        out = im.resize(out_size, Image.ANTIALIAS)
        out.save(savename)


def cut(file):
    """检测边缘范围并裁剪"""
    root_path = os.path.join(assert_path, "pcr2")
    output_path = os.path.join(assert_path, "pcr3")
    img = Image.open(os.path.join(root_path, file))
    l, r, t, d = len(img[0]), 0, len(img), 0
    height = len(img)
    width = len(img[0])
    for i in range(0, height):
        for j in range(0, width):
            if float(img[i][j][3]) != 0:
                l = min(l, j)
                r = max(r, j)
                t = min(t, i)
                d = max(d, i)
    size = (max(8, l-0), max(4, t-0), min(173, r+0), d)
    cropped = img.crop(size)
    cropped.save(os.path.join(output_path, file))

if __name__ == "__main__":
    comic(os.path.join(assert_path, "comic\\角色漫画"), os.path.join(assert_path, "comic\\comic1"))
    # comic(os.path.join(assert_path, "row\\story_thumb"), os.path.join(assert_path, "row\\story_thumb_output"))
    # story_still(os.path.join(assert_path, "row\\story_cg"), os.path.join(assert_path, "row\\story_cg_output"))

# https://wiki.biligame.com/pcr/api.php?action=query&format=json&list=allimages&aisort=name&aifrom=Comic_100000&aito=Comic_999999&aimime=image%2Fpng&ailimit=500