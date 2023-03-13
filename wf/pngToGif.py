# -*- coding: UTF-8 -*-
import os
from PIL import Image
import numpy as np
from en2cn import en2cn

root_path = ".\\"
output_path = ".\\output"
reuse_files = True # 复用之前生成的文件

def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGBA')#.convert('P', palette=Image.ADAPTIVE, colors=255)
    # Set all pixel values below 128 to 255 , and the rest to 0
    # mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    # Paste the color of index 255 and use alpha as a mask
    # im.paste(255, mask)
    # The transparency index is 255
    im.info['transparency'] = 0
    return im


l, r, t, d = 255, 0, 255, 0
def get_edge(skill_path):
    """检测边缘范围"""
    global l,r,t,d
    image_list = os.listdir(skill_path)
    for image_name in image_list:
        if image_name.endswith('.png'):
            # print(image_name)
            full_image = os.path.join(skill_path, image_name)
            img = Image.open(full_image)
            img = np.array(img)
            height = len(img)
            width = len(img[0])
            for i in range(0, height):
                for j in range(0, width):
                    if float(img[i][j][3]) != 0:
                        l = min(l, j)
                        r = max(r, j)
                        t = min(t, i)
                        d = max(d, i)


def getPixelColor(fileName):
    # print(fileName)
    img = Image.open(fileName)
    # img.show()
    return np.array(img)


def zoomIn(old_image, new_image, pow, left, right, top, down):
    inData = getPixelColor(old_image)
    height = int((down-top)*pow)
    width = int((right-left)*pow)
    if len(inData) == 64:
        return
    outData = np.zeros([height, width, 4])
    for i in range(height):
        for j in range(width):
            x = int(i//pow) + top
            y = int(j//pow) + left
            outData[i][j] = [inData[x][y][0], inData[x][y][1], inData[x][y][2], inData[x][y][3]] 
    outData = np.uint8(outData)
    im = Image.fromarray(outData)
    im.save(new_image)


def create_gif(skill_path, role_name):
    print("start " + skill_path)
    gif_name = os.path.join(output_path, role_name) + ".gif"
    if reuse_files == True and os.path.exists(gif_name):
        return
    image_list = os.listdir(skill_path)
    frames = []
    # print(skill_path)
    durations = []
    last_duration = 0
    for image_name in image_list:
        if image_name.endswith('.png') and not image_name.endswith("_4x.png"):
            # print(image_name)
            full_image = os.path.join(skill_path, image_name)
            full_4x_image = os.path.join(skill_path, image_name[:-4] + "_4x.png")
            cur_duration = int(image_name[-8:-4])
            durations.append((cur_duration-last_duration)*16.6)
            last_duration = cur_duration
            if reuse_files == False or not os.path.exists(full_4x_image):
                zoomIn(full_image, full_4x_image, 4, 64, 192, 45, 173)
            # frames.append(imageio.imread(full_4x_image))
            frames.append(gen_frame(full_4x_image))

    # Save them as frames into a gif
    # imageio.mimsave(gif_name, frames, 'GIF', duration=0.1, loop=0)
    frames[0].save(gif_name, save_all=True, append_images=frames[1:], loop=0, duration=durations, disposal=2)
    print("ok " + role_name)
    return


def main(path, role_name):
    file_list = os.listdir(path)
    for file in file_list:
        full_path = os.path.join(path, file)
        if not os.path.isdir(full_path):
            continue
        if file == "pixelart":
            front_path = os.path.join(full_path, "front")
            front_path512 = os.path.join(full_path, "front512")
            role_name_cn = en2cn(role_name)
            if role_name_cn == "":
                role_name_cn = role_name
            if os.path.exists(front_path):
                fronts = os.listdir(front_path)
                fronts.sort()
                fronts = list(filter(lambda x: x.endswith(".png"), fronts))
                if len(fronts) > 0:
                    zoomIn(os.path.join(front_path, fronts[0]), os.path.join(output_path, role_name_cn + "-front.png"), 5, 118, 138, 109, 129)
            elif os.path.exists(front_path512):
                fronts = os.listdir(front_path512)
                fronts.sort()
                fronts = list(filter(lambda x: x.endswith(".png"), fronts))
                if len(fronts) > 0:
                    zoomIn(os.path.join(front_path512, fronts[0]), os.path.join(output_path, role_name_cn + "-front512.png"), 2.5, 236, 276, 218, 258)
            # skill_path = os.path.join(full_path, "skill")
            # if os.path.exists(skill_path):
            #     create_gif(skill_path, role_name_cn + "-skill")

            special_path = os.path.join(full_path, "special")
            if os.path.exists(special_path):
                create_gif(special_path, role_name_cn + "-special")
            return
        elif file in ["0怪物", "build", "dist"]:
            continue
        else: # dfs
            main(full_path, file)


if __name__ == "__main__":
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    main(root_path, "_root")
# print(l, r, t, d)