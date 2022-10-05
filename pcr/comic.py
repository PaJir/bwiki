import os
from PIL import Image


def comic(filepath, savepath):
    """
    filepath: D:\Extra\pcr\comic\\角色漫画\\
    savepath: D:\Extra\pcr\comic\\comic1\\
    """
    # vo_cmn_100111
    files = os.listdir(filepath)
    for file in files:
        filename = os.path.join(filepath, file)
        # savename = os.path.join(savepath, "comic_" + file[8:14] + ".png")
        savename = os.path.join(savepath, file)
        if os.path.exists(savename):
            continue
        im = Image.open(filename)
        out = im.resize((240,135), Image.ANTIALIAS)
        out.save(savename)


def story_still():
    filepath = "D:\Extra\pcr\\row\\Texture2D_story"
    savepath = "D:\Extra\pcr\\row\\Texture2D_storystill"

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

# comic("D:\Extra\pcr\comic\\角色漫画\\", "D:\Extra\pcr\comic\\comic1\\")
# comic("D:\Extra\pcr\\row\\Texture2D_storytop\\", "D:\Extra\pcr\\row\\Texture2D_storytop2\\")
story_still()