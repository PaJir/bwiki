import os

# 新手教学 0
# in_path = "./new"
# 角色剧情 1
in_path = "./unit"
# 主线剧情 2
# in_path = "./main"
# 公会剧情 3
# in_path = "./guild"
# 公会之家、竞技场、地下城等 4
# in_path = "./others"
# 活动剧情 5 信赖度 6
# in_path = "./activity"
# 露娜塔 7
# in_path = "./lunar"
# 推图BOSS 9
# in_path = "./battle"
out_path = in_path + "_out"

start_episode = "001"  # from 000 or 001
include_empty_title = True


def getNext(rf):
    line = rf.readline()
    return line[:-1]


def getText(rf):
    text = getNext(rf)
    return text.replace("{0" + "}", "佑树").replace("\\n", "<br>")


rep = {
    "101112": "101111", "101421": "101412", "101821": "101802",
    "102312": "102311", "102321": "102303", "102821": "102803",
    "103112": "103111", "105213": "105211", "105612": "105611",
    "105812": "105811", "105913": "105911", "106012": "106011",
    "106412": "106411", "106613": "106611", "106834": "106803",
    "110812": "110811", "111412": "111411", "112912": "112911"
}


def replaceId(id):
    if id == "0":
        id = ""
    elif len(id) == 3:
        id = "000" + id
    elif len(id) == 4:
        id = "00" + id
    elif len(id) == 5:
        id = "0" + id
    elif id[0] == "1":
        id = rep.get(id, id)
        if id[4] == "3":
            id = id[:4] + "0" + id[5]
    return id


def transform(in_file, out_file, first=False, _title=""):
    rf = open(os.path.join(in_path, in_file), "r", encoding="utf-8")
    wf = open(os.path.join(out_path, out_file), "a+", encoding="utf-8")
    if first:
        wf.close()
        wf = open(os.path.join(out_path, out_file), "w+", encoding="utf-8")
        # wf.write("{" + "{#set:\n|部=" + str(int(in_file[11])+1) + "\n|章=" + in_file[12:14] + "\n}" + "}")
        # wf.write("{" + "{#set:\n|标题=\n|部=" + str(int(in_file[11])+1) + "\n|章=" + in_file[12:14] + "\n|话="+ in_file[15:17] + "\n}" + "}")
        wf.write("{" + "{#set:\n|编号=" + in_file[12:14] + "\n}" + "}")
        wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{")
        wf.write("{DISPLAYTITLE:" + _title + "}" + "}[[分类:其他剧情]]")
        # wf.write("\n{" + "{剧情|公会成员|所属:" + _title + "}" + "}")
    wf.write("\n")
    line = rf.readline()
    title = ""  # 故事序号
    outline = ""  # 故事梗概
    black_in = ""  # 故事标题
    chord = ""  # 103611
    name = ""
    bgms = {}
    bgms_count = 0
    bgm_cur = 1
    ttt = 0
    # shake = False
    while line:
        # print(ttt, line)
        line = line[:-1]
        if line == "title":
            title = getText(rf)
        elif line == "outline":
            outline = getText(rf)
        elif line == "black_in":
            black_in = getText(rf)
            # black_in = title
            wf.write("==")
            # wf.write("第" + title.split("第")[-1])
            episode = in_file[14:17]
            if in_path == "./activity":
                if episode == "000":
                    wf.write("序章")
                elif episode == "007":
                    wf.write("终章")
                elif episode == "101":
                    wf.write("预告")
                else:
                    wf.write("第" + episode[2] + "话")
            else:
                wf.write("第" + episode[2] + "话")
            wf.write(" " + black_in + "==\n")
            wf.write("{" + "{折叠|宽度=100%\n|标题=剧情梗概\n|内容=" + outline + "\n}" + "}\n")
        elif line == "chord_l":  # type / chord_l 对话角色转换
            chord = getNext(rf)
            chord = replaceId(chord)
        elif line == "focus":  # 一个对话的一部分，也可能是对话的开始
            new_name = getNext(rf)
            text = getText(rf)
            if name != new_name:
                name = new_name
                wf.write("{" + "{对话|" + chord + "|" + name + "|")
                # if shake == True:
                #     wf.write("（思考）")
            wf.write(text)
        elif line == "goto":  # 一个对话结束
            system = getNext(rf)
            if system == "System":
                name = ""
                wf.write("}" + "}\n")
        elif line == "pop":  # 动画
            pass
        elif line == "bgm":  # 佑树发言
            bgms = {}
            bgms_count = 0
            bgm_cur = 1
            while line == "bgm":
                text = getText(rf)
                bg = getNext(rf)
                bgms[bg] = text
                bgms_count += 1
                line = getNext(rf)
                while line != "":
                    line = getNext(rf)
                line = getNext(rf)
            line += "\n"
            print(bgms)
            if bgms_count == 1:
                bgms = {}
                wf.write("{" + "{对话|191711|佑树|" + text)  # + "}" + "}\n")
            name = ""
            continue
        elif line == "background":
            bg = getNext(rf)
            if bgms.get(bg) is not None:
                if bgm_cur > 1:
                    wf.write("}" + "}\n")
                wf.write("{" + "{折叠|宽度=100%\n|标题=选项" + str(bgm_cur) + "：" + bgms[bg] + "\n|内容=")
                bgm_cur += 1
            else:
                wf.write("}" + "}\n")
        elif line == "laugh_r": # 立绘
            laugh = getNext(rf)
            if laugh == "end":
                continue
            wf.write("\n[[file:" + laugh + ".jpg|600px|center]]\n\n")
        # elif line == "print": # 相当于汇编中的goto语句
        #     pass
        # elif line == "shake_screen": # 思考
        #     t = getNext(rf)
        #     if t == "TRUE":
        #         shake = True
        #         print(t, shake)
        #     elif t == "FALSE":
        #         shake = False
        #         print(t, shake)
        ttt += 1
        line = rf.readline()
    # wf.write("{" + "{剧情导航" + "}" + "}")


if __name__ == "__main__":
    files = os.listdir(in_path)
    for in_file in files:
        if not include_empty_title and in_file.find("[ ]") != -1:
            continue
        out_file = in_file[:14] + ".txt"
        episode = in_file[14:17]
        first = True if episode == start_episode else False  # TODO: 000 or 001
        # out_file = in_file[:17] + ".txt"
        # first = True
        t = int(in_file[12:14])
        guilds = [
            "",
            "美食殿堂",
            "王宫骑士团",
            "咲恋救济院",
            "自卫团",
            "伊丽莎白牧场",
            "拉比林斯",
            "破晓之星",
            "墨丘利财团",
            "森林守卫",
            "慈乐之音",
            "暮光流星群",
            "纯白之翼",
            "小小甜心",
            "恶魔伪王国军",
            "月光学院",
            "圣特蕾莎女子学院（好朋友社）",
            "龙族据点"]

        transform(in_file, out_file, first)
