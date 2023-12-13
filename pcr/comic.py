import os
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

# comic(os.path.join(assert_path, "comic\\角色漫画"), os.path.join(assert_path, "comic\\comic1"))
comic(os.path.join(assert_path, "row\\story_thumb"), os.path.join(assert_path, "row\\story_thumb_output"))
# story_still(os.path.join(assert_path, "row\\story_cg"), os.path.join(assert_path, "row\\story_cg_output"))

# https://wiki.biligame.com/pcr/api.php?action=query&format=json&list=allimages&aisort=name&aifrom=Comic_100000&aito=Comic_999999&aimime=image%2Fpng&ailimit=500