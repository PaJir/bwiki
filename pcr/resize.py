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


def cut(file, in_path, out_path):
    """检测边缘范围并裁剪"""
    img = Image.open(os.path.join(in_path, file))
    width, height = img.size
    l, r, t, d = width, 0, height, 0
    pixels = img.load()
    for i in range(0, height):
        for j in range(0, width):
            if float(pixels[j, i][3]) != 0:
                l = min(l, j)
                r = max(r, j)
                t = min(t, i)
                d = max(d, i)
    size = (max(0, l-0), max(0, t-0), min(width, r+0), d)
    print(size)
    cropped = img.crop(size)
    cropped.save(os.path.join(out_path, file))

def cut_all(in_path, out_path):
    files = os.listdir(in_path)
    for file in files:
        cut(file, in_path, out_path)

def png_2_jpg(filepath, savepath):
    files = os.listdir(filepath)
    for file in files:
        if not file.endswith(".png"):
            continue
        filename = os.path.join(filepath, file)
        savename = os.path.join(savepath, file[:-3] + "jpg")
        if os.path.exists(savename):
            continue
        im = Image.open(filename)
        im = im.convert("RGB")
        im.save(savename)

if __name__ == "__main__":
    # comic(os.path.join(assert_path, "comic\\角色漫画"), os.path.join(assert_path, "comic\\comic1"))
    # comic(os.path.join(assert_path, "row\\story_thumb"), os.path.join(assert_path, "row\\story_thumb_output"))
    # story_still(os.path.join(assert_path, "row\\story_cg"), os.path.join(assert_path, "row\\story_cg_output"))
    png_2_jpg(os.path.join(assert_path, "_redive\\card\\story"), os.path.join(assert_path, "row\\story_cg_output"))
    # cut_all(os.path.join(assert_path, "pcr2"), os.path.join(assert_path, "pcr3"))

# https://wiki.biligame.com/pcr/api.php?action=query&format=json&list=allimages&aisort=name&aifrom=Comic_100000&aito=Comic_999999&aimime=image%2Fpng&ailimit=500