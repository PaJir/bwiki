# 抠图
from PIL import Image
import numpy as np
import os
import multiprocessing as mp

# 浅色背景 0
# 浅色人物 1
# 深色背景 2
# 深色人物 3
inputPath = "D:\Extra\pcr\GIF\香澄（魔法少女）"
outputPath = inputPath + "2"
# inputPath = "D:\Extra\pcr\Q\\bandicam"
# outputPath = "D:\Extra\pcr\Q\\nobg"
# lightFile = "D:\Extra\pcr\GIF\克莉丝提娜（圣诞节）\\0 0.png"
# lightFile = "D:\Extra\pcr\GIF\克莉丝提娜（圣诞节）\\0 0.png"
# darkFile = "D:\Extra\pcr\GIF\克莉丝提娜（圣诞节）\\0 1.png"
# darkFile = "D:\Extra\pcr\GIF\克莉丝提娜（圣诞节）\\0 1.png"
lightStart = "2"
darkStart = "1"


def getPixelColor(fileName):
    # print(fileName)
    img = Image.open(fileName)
    # img.show()
    # print(np.array(img)[100][100])
    return np.array(img)


# light = getPixelColor(lightFile)
# dark = getPixelColor(darkFile)
light = [255, 255, 255, 255]
dark = [0, 0, 0, 255]

# assert len(dark) == len(light) and len(dark[0]) == len(light[0])


def handle(l, d, n):
    height = len(l)
    width = len(l[0])
    # assert height <= len(dark) and width <= len(dark[0])
    outData = np.zeros([height, width, 4])
    for i in range(0, height):
        for j in range(0, width):
            a = [float(x) for x in light]
            A = [float(x) for x in l[i][j]]
            b = [float(x) for x in dark]
            B = [float(x) for x in d[i][j]]
            # if all(a == A) and all(b == B):
            if a == A and b == B:
                # 如果 浅色背景 和 浅色人物 的颜色相同，且 深色背景 和 深色人物的颜色相同，则为背景或图标
                outData[i][j] = [0, 0, 0, 0]
            # elif any(a != A) or any(b != B):
            elif a != A or b != B:
                # 如果浅色人物和深色人物的颜色相同，则为全色
                # if all(A == B):
                if A == B:
                    outData[i][j] = [A[0], A[1], A[2], 255]
                else:
                    # alpha = 1 - ((a1R - b1R) / (aR - bR))
                    Ra = min(1., 1 - ((A[0] - B[0]) / (a[0] - b[0])))
                    Ga = min(1., 1 - ((A[1] - B[1]) / (a[1] - b[1])))
                    Ba = min(1., 1 - ((A[2] - B[2]) / (a[2] - b[2])))
                    # print(a, A, b, B, Ra, Ga, Ba)
                    # alpha = max(Ra, max(Ga, Ba))
                    alpha = (Ra + Ga + Ba) / 3
                    R1 = a[0] if Ra == 0 else (A[0] - (1 - Ra) * a[0]) / Ra
                    G1 = a[1] if Ga == 0 else (A[1] - (1 - Ga) * a[1]) / Ga
                    B1 = a[2] if Ba == 0 else (A[2] - (1 - Ba) * a[2]) / Ba
                    R2 = b[0] if Ra == 0 else (B[0] - (1 - Ra) * b[0]) / Ra
                    G2 = b[1] if Ga == 0 else (B[1] - (1 - Ga) * b[1]) / Ga
                    B2 = b[2] if Ba == 0 else (B[2] - (1 - Ba) * b[2]) / Ba
                    R = (R1 + R2) / 2 + .5
                    G = (G1 + G2) / 2 + .5
                    B = (B1 + B2) / 2 + .5
                    outData[i][j] = [R, G, B, min(255., alpha * 256)]
            else:
                assert 1
    # print(len(outData), len(outData[0]), len(outData[0][0]), outData[100][100])
    outData = np.uint8(outData)
    # print(outData[100][100])
    im = Image.fromarray(outData)
    im.save(n)
    print("saved:", n)


if __name__ == "__main__":
    print("start")
    inputFiles = os.listdir(inputPath)
    pool = mp.Pool()
    for _, file in enumerate(inputFiles):
        if not file.startswith(lightStart):
            continue
        inputLightFileName = os.path.join(inputPath, file)
        inputDarkFileName = os.path.join(inputPath, darkStart + file[1:])
        newFileName = os.path.join(outputPath, file)
        l = getPixelColor(inputLightFileName)
        d = getPixelColor(inputDarkFileName)
        assert len(l) == len(d) and len(l[0]) == len(d[0])
        # handle(l, d, newFileName)
        # break
        pool.apply_async(handle, (l, d, newFileName))
    pool.close()
    pool.join()
    print("close")
    # getPixelColor("D:\Extra\pcr\GIF\露娜\\2 0.png")
