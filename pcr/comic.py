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

# comic("D:\Extra\pcr\comic\\角色漫画\\", "D:\Extra\pcr\comic\\comic1\\")
comic("D:\Extra\pcr\\row\\Texture2D_storytop\\", "D:\Extra\pcr\\row\\Texture2D_storytop2\\")