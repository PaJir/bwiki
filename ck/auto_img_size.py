from PIL import Image
import numpy as np
import os


inputPath = ".\贵重品"
outputPath = inputPath + "2"


def process(fileName, n):
    height = 64
    width = 64
    img = Image.open(fileName).convert("RGBA")
    # img.show()
    # print(np.array(img)[10][10])
    img = np.array(img)
    if len(img) == height and len(img[0]) == width:
        return
    height = max(height, len(img), len(img[0]))
    width = max(width, len(img), len(img[0]))

    outData = np.zeros([height, width, 4])

    top = (height - len(img)) // 2
    left = (width - len(img[0])) // 2
    # print(len(img), len(img[0]), top, left, img[32], outData[32])

    for i in range(top, top+len(img)):
        for j in range(left, left+len(img[0])):
            outData[i][j] = img[i-top][j-left]

    outData = np.uint8(outData)
    im = Image.fromarray(outData)
    im.save(n)
    print("saved:", n)


if __name__ == "__main__":
    inputFiles = os.listdir(inputPath)
    for _, file in enumerate(inputFiles):
        newFileName = os.path.join(outputPath, file)
        file = os.path.join(inputPath, file)
        process(file, newFileName)
        # break
