# 半身图裁剪多余的边缘
import os
import numpy as np
from PIL import Image
from config import assert_path

root_path = os.path.join(assert_path, "pcr2")
output_path = os.path.join(assert_path, "pcr3")


def cut(img):
    """检测边缘范围"""
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
    return (max(0, l-10), max(0, t-10), min(width, r+10), d)


if __name__ == "__main__":
    files = os.listdir(root_path)
    files2 = os.listdir(output_path)
    for file in files:
        if not file.endswith(".png") or file in files2:
            continue
        img = Image.open(os.path.join(root_path, file))
        size = cut(np.array(img))
        cropped = img.crop(size)
        cropped.save(os.path.join(output_path, file))
