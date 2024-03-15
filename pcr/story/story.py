import os

story_config = {
    0: ["./new"],# 新手教学 0
    1: ["./unit"],# 角色剧情 1
    2: ["./main"],# 主线剧情 2
    3: ["./guild"],# 公会剧情 3
    4: ["./others"],# 公会之家、竞技场、地下城等 4
    5: ["./activity"],# 活动剧情 5 信赖度 6
    7: ["./lunar"],# 露娜塔 7
    9: ["./battle"]# 推图BOSS 9
}
in_path = ""
out_path = ""
include_empty_title = True


def getNext(rf):
    line = rf.readline()
    return line[:-1]


def getText(rf):
    text = getNext(rf)
    return text.replace("{0" + "}", "佑树").replace("\\n", "<br>")


rep = {
    "101112": "101111", "101421": "101412", "101821": "101802",
    "102212": "102211", "101512": "101511",
    "102312": "102311", "102321": "102303", "102821": "102803",
    "103112": "103111", "105213": "105211", "105612": "105611",
    "105812": "105811", "105913": "105911", "106012": "106011",
    "106412": "106411", "106414": "106413", "106532": "106501",
    "106613": "106611", "106834": "106803", "104914": "104911",
    "110812": "110811", "111412": "111411", "112912": "112911",
    "114612": "114611", "115512": "115511", "116712": "116711"
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


def transform(in_file, out_file, first=False, _title="", story_type=1):
    rf = open(os.path.join(in_path, in_file), "r", encoding="utf-8")
    if first:
        _title = _title.replace(" 下集预告", "")
        wf = open(os.path.join(out_path, out_file), "w+", encoding="utf-8")
        if story_type == 1:
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:角色剧情]]")
        elif story_type == 2:
            wf.write("{" + "{#set:\n|部=" + str(int(in_file[11])+1) + "\n|章=" + in_file[12:14] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:主线剧情]]")
        elif story_type == 3:
            wf.write("{" + "{#set:\n|编号=" + in_file[12:14] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:公会剧情]]")
            wf.write("\n{" + "{剧情|公会成员|所属:" + _title + "}" + "}")
        elif story_type == 4 or story_type == 9:
            wf.write("{" + "{#set:\n|编号=" + in_file[12:14] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:其他剧情]]")
        elif story_type == 5: # hatsune_item
            wf.write("{" + "{#set:\n|编号=" + in_file[12:14] + "\n|碎片掉落=、|+sep=、" + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:活动剧情]][[分类:地图掉落]]")
        elif story_type == 7:
            wf.write("{" + "{#set:\n|编号=" + in_file[12:14] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + _title + "}" + "}[[分类:露娜塔剧情]]")
        else:
            pass
    else:
        wf = open(os.path.join(out_path, out_file), "a+", encoding="utf-8")
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
    episode = in_file[14:17]
    if story_type == 5 and in_file[10] == '5':
        if episode == "202":
            wf.write("==首领战相关==\n===普通解锁===\n")
        elif episode == "203":
            wf.write("===普通获胜===\n")
        elif episode == "204":
            wf.write("===困难解锁===\n")
        elif episode == "301":
            wf.write("===普通挑战===\n")
        elif episode == "302":
            wf.write("===困难挑战===\n")
        elif episode == "308":
            wf.write("===高难挑战===\n")
        elif episode == "321":
            wf.write("===SP挑战===\n")
        elif episode == "322":
            wf.write("===SP升阶段2===\n")
        elif episode == "323":
            wf.write("===SP升阶段3===\n")
    elif episode == "500":
        wf.write("==角色生日特别剧情==\n")

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
            if story_type == 5 and in_file[10] == '5' and episode in ["202", "203", "204", "301", "302", "308", "321", "322", "323"]:
                pass
            elif episode == "500":
                pass
            wf.write("==")
            # wf.write("第" + title.split("第")[-1])
            if story_type == 5:
                if episode == "000":
                    wf.write("序章 ")
                elif episode == "007":
                    wf.write("终章 ")
                elif episode == "101":
                    wf.write("预告 ")        
                elif episode == "401":
                    wf.write("=困难获胜·")
                elif episode == "402":
                    wf.write("=高难获胜·")
                elif episode == "403":
                    wf.write("=击破10只·")
                elif episode == "404":
                    wf.write("=击破20只·")
                elif episode == "405":
                    wf.write("=击破30只·")
                elif episode in ["406", "407", "408", "409", "410"]:
                    pass
                else:
                    wf.write("第" + episode[2] + "话 ")
            elif not black_in.startswith("幕间"):
                wf.write("第" + str(int(episode[1:3])) + "话 ")
            wf.write(black_in)
            if story_type == 5 and episode in ["401", "402", "403", "404", "405"]:
                wf.write("=")
            wf.write("==\n")
            if outline not in ["", " ", "\t"]:
                wf.write("{" + "{折叠|宽度=100%\n|标题=剧情梗概\n|内容=" + outline + "\n}" + "}\n")
        elif line == "type" and black_in == "" and title != "": # 标题的备选项
            if story_type == 5 and in_file[10] == '5' and episode == "101":
                wf.write("==预告 " + title + "==\n")
                wf.write("{" + "{折叠|宽度=100%\n|标题=剧情梗概\n|内容=" + outline + "\n}" + "}\n")
            title = ""
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
                getNext(rf)
                line = getNext(rf)
                while line != "":
                    line = getNext(rf)
                line = getNext(rf)
            line += "\n"
            # print(bgms)
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

def story(story_type=1):
    global in_path, out_path, start_episode
    in_path = story_config[story_type][0]
    out_path = in_path + "_out"
    start_episode = "000"
    files = os.listdir(in_path)
    for in_file in files:
        if not include_empty_title and in_file.find("[ ]") != -1:
            continue
        out_file = in_file[:14] + ".txt"
        # if out_file != "storydata_5031.txt":
        #     continue
        episode = in_file[14:17]
        if story_type == 5:
            if episode in ["101", "422", "423", "424", "425"]:
                continue
            elif episode == "000":
                yugao = in_file[:14] + "101"
                for f in files:
                    if f.startswith(yugao):
                        yugao = f
                        transform(yugao, out_file, True, yugao.split("[")[1].split("]")[0], story_type)
                        break
        if in_file[10] == '5':
            start_episode = "101"
        elif in_file[10] == '6':
            start_episode = "101"
        elif in_file[10] == '7':
            start_episode = "000"
        else:
            start_episode = "001"
        first = True if episode == start_episode else False
        t = int(in_file[12:14])
        transform(in_file, out_file, first, in_file.split("[")[1].split("]")[0], story_type)

if __name__ == "__main__":
    story(5)