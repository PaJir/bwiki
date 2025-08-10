# 与story.py的区别在于，这个脚本基于unity-texture-toolkit导出的json格式剧情
import os
import json
import sqlite3
from story.story import story_config, replaceId
from config import assert_path, db_name

in_path = os.path.join(assert_path, "_redive_cn", "story", "data")
out_path = ".\\story\\json_out"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
active_story_type = { 6 }

def preprocess(lines):
    for i in range(len(lines)):
        for j in range(len(lines[i]["args"])):
            lines[i]["args"][j] = lines[i]["args"][j].replace("{player}", "佑树").replace("\n", "<br>").replace("~~~", "<nowiki>~~~</nowiki>")

def getArgsForName(lines, name):
    for line in lines[:50]:
        if line["name"] == name:
            return line["args"][0]
    return ""

def talks(lines, wf):
    i = 0
    # if len(lines) > 1:
    #     print(lines)
    while i < len(lines):
        if lines[i]["name"] == "bust":
            _id = lines[i]["args"][0]
        elif lines[i]["name"] == "focus": # 对话角色转换
            name, talk = "", ""
            while lines[i]["name"] != "touch" and lines[i]["name"] != "choice":
                if lines[i]["name"] == "bust": # face focus
                    _id = lines[i]["args"][0]
                if lines[i]["name"] == "print": # 对话
                    if name != "" and name != lines[i]["args"][0]: # 无touch、同id、不同name的两段对话
                        wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
                        talk = ""
                    name = lines[i]["args"][0]
                    talk += lines[i]["args"][1]
                i += 1
            if talk != "":
                wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
            if lines[i]["name"] == "choice":
                i -= 1
        elif lines[i]["name"] == "print": # 没有focus的对话
            # while lines[i-1]["name"] != "bust": # face
            #     i -= 1
            # _id = lines[i-1]["args"][0]
            talk = ""
            while lines[i]["name"] != "touch":
                if lines[i]["name"] == "print": # 对话
                    name = lines[i]["args"][0]
                    talk += lines[i]["args"][1]
                i += 1
            wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
        elif lines[i]["name"] == "choice" and lines[i+1]["name"] == "choice": # 多选项
            _idx = 1
            max_i = i
            tags = set()
            tag_start = i
            later_choice = None # 后面分支数
            end_tag = None
            while lines[tag_start]["name"] == "choice":
                tags.add(lines[tag_start]["args"][1])
                tag_start += 1
            while lines[i]["name"] == "choice":
                # 支持choice嵌套，支持部分choice的分支相同
                wf.write("{{折叠|宽度=100%\n|" + "标题=选项%d：%s\n|内容=" % (_idx, lines[i]["args"][0]))
                start = tag_start
                later_choice = len(tags)
                while True:
                    if lines[start]["name"] == "tag":
                        # print(lines[start]["args"])
                        if lines[start]["args"][0] == lines[i]["args"][1]:
                            later_choice -= 1
                            while lines[start+1]["name"] == "tag" and lines[start+1]["args"][0] in tags: # 分支相同
                                start += 1
                                later_choice -= 1
                            start += 1
                            break
                        elif lines[start]["args"][0] in tags:
                            later_choice -= 1
                    start += 1
                end = start + 1
                # print(_idx, later_choice, tags)
                if later_choice == 0 and end_tag is None: # 单分支
                    end = start
                else:
                    while end < len(lines):
                        if later_choice > 0:
                            if lines[end]["name"] == "goto":
                                end_tag = lines[end]["args"][0]
                            elif lines[end]["name"] == "tag" and lines[end]["args"][0] in tags:
                                break
                        elif later_choice == 0 and lines[end]["name"] == "tag" and lines[end]["args"][0] == end_tag:
                            break
                        end += 1
                    if end == len(lines):
                        end = start
                        wf.write("重新选择选项")
                talks(lines[start:end], wf)
                wf.write("}}\n")
                _idx += 1
                i += 1
                max_i = max(max_i, end)
            i = max_i
        elif lines[i]["name"] == "choice": # 单选项
            wf.write("{{对话|191711|佑树|%s}}\n" % lines[i]["args"][0])
        elif lines[i]["name"] == "still_unit" and lines[i]["args"][0] != "end":
            chr = lines[i]["args"][0]
            if chr[4] == "3":
                wf.write("\n[[file:Chr_%s.jpg|center|600px]]\n\n" % chr)
            elif chr[4] == "6":
                unit_id = chr[:4]
                sql = "select unit_name from actual_unit_background where substr(unit_id, 1, 4)='" + unit_id + "'"
                cursor.execute(sql)
                unit_name = cursor.fetchone()[0]
                wf.write("\n[[file:%s6星.png|center|600px]]\n\n" % unit_name)
            else:
                assert 0
        elif lines[i]["name"] == "still":
            chr = lines[i]["args"][0]
            if chr != "end":
                wf.write("\n[[file:%s.jpg|center|600px]]\n\n" % chr)
        i += 1

# 直接打tag
def talks2(lines, wf):
    i = 0
    # if len(lines) > 1:
    #     print(lines)
    while i < len(lines):
        if lines[i]["name"] == "tag":
            wf.write("tag %s\n" % lines[i]["args"][0])
        if lines[i]["name"] == "bust":
            _id = lines[i]["args"][0]
        elif lines[i]["name"] == "focus": # 对话角色转换
            name, talk = "", ""
            while lines[i]["name"] != "touch" and lines[i]["name"] != "choice":
                if lines[i]["name"] == "bust": # face focus
                    _id = lines[i]["args"][0]
                if lines[i]["name"] == "print": # 对话
                    if name != "" and name != lines[i]["args"][0]: # 无touch、同id、不同name的两段对话
                        wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
                        talk = ""
                    name = lines[i]["args"][0]
                    talk += lines[i]["args"][1]
                i += 1
            if talk != "":
                wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
            if lines[i]["name"] == "choice":
                i -= 1
        elif lines[i]["name"] == "print": # 没有focus的对话
            talk = ""
            while lines[i]["name"] != "touch":
                if lines[i]["name"] == "print": # 对话
                    name = lines[i]["args"][0]
                    talk += lines[i]["args"][1]
                i += 1
            wf.write("{{对话|%s|%s|%s}}\n" % (replaceId(_id), name, talk))
        elif lines[i]["name"] == "choice" and lines[i+1]["name"] == "choice": # 多选项
            _idx = 1
            while lines[i]["name"] == "choice":
                wf.write("{{折叠|宽度=100%\n|" + "标题=选项%d：%s\n|内容=前往tag %s}}\n" % (_idx, lines[i]["args"][0], lines[i]["args"][1]))
                _idx += 1
                i += 1
            i -= 1
        elif lines[i]["name"] == "choice": # 单选项
            wf.write("{{对话|191711|佑树|%s}}\n" % lines[i]["args"][0])
        elif lines[i]["name"] == "still_unit" and lines[i]["args"][0] != "end":
            chr = lines[i]["args"][0]
            if chr[4] == "3":
                wf.write("\n[[file:Chr_%s.jpg|center|600px]]\n\n" % chr)
            elif chr[4] == "6":
                unit_id = chr[:4]
                sql = "select unit_name from actual_unit_background where substr(unit_id, 1, 4)='" + unit_id + "'"
                cursor.execute(sql)
                unit_name = cursor.fetchone()[0]
                wf.write("\n[[file:%s6星.png|center|600px]]\n\n" % unit_name)
            else:
                assert 0
        elif lines[i]["name"] == "still":
            chr = lines[i]["args"][0]
            if chr != "end":
                wf.write("\n[[file:%s.jpg|center|600px]]\n\n" % chr)
        i += 1

def transform(in_file, out_file, episode, first=False, story_type=1):
    lines = json.load(open(os.path.join(in_path, in_file), "r", encoding="utf-8"))
    # json.dump(lines, open(os.path.join(in_path, in_file), "w+", encoding="utf-8"), ensure_ascii=False)
    preprocess(lines)
    title = getArgsForName(lines, "title")
    situation = getArgsForName(lines, "situation")
    outline = getArgsForName(lines, "outline")
    # 页面前缀
    if first:
        wf = open(os.path.join(out_path, out_file), "w+", encoding="utf-8")
        if story_type == 1:
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + title.split(" ")[0] + "}" + "}[[分类:角色剧情]]")
        elif story_type == 2:
            wf.write("{" + "{#set:\n|部=" + str(int(in_file[1])+1) + "\n|章=" + in_file[2:4] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + "}" + "}[[分类:主线剧情]]")
        elif story_type == 3:
            wf.write("{" + "{#set:\n|编号=" + in_file[2:4] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + title.split(" ")[0] + "}" + "}[[分类:公会剧情]]")
            wf.write("\n{" + "{剧情|公会成员|所属::" + title.split(" ")[0] + "}" + "}")
        elif story_type in {4, 9}:
            wf.write("{" + "{#set:\n|编号=" + in_file[2:4] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + title.split(" ")[0] + "}" + "}[[分类:其他剧情]]")
        elif story_type == 5: # hatsune_item
            sql = "select substr(unit_material_id_1, 3, 3), substr(unit_material_id_2, 3, 3) from hatsune_item where substr(event_id, 3, 3)='" + in_file[1:4] + "'"
            cursor.execute(sql)
            items = cursor.fetchone()
            wf.write("{" + "{#set:\n|编号=" + in_file[2:4] + "\n|碎片掉落=%s、%s|+sep=、" % (items[0], items[1]) + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + title[:-4] + "}" + "}[[分类:活动剧情]][[分类:地图掉落]]")
        elif story_type == 6:
            wf.write("\n==信赖度==")
        elif story_type == 7:
            sql = "select title from tower_story_data where story_group_id="+in_file[:4]
            cursor.execute(sql)
            title = cursor.fetchone()
            title = title[0] if title is not None else ""
            wf.write("{" + "{#set:\n|编号=" + in_file[2:4] + "\n}" + "}")
            wf.write("__TOC__{" + "{ResourceLoader|MediaWiki:Replacename|MIME=text/javascript}}{{DISPLAYTITLE:" + title + "}" + "}[[分类:露娜塔剧情]]")
    else:
        wf = open(os.path.join(out_path, out_file), "a+", encoding="utf-8")
    wf.write("\n")
    # 标题
    if story_type in {1, 2, 3, 4, 9}:
        if episode == "500":
            wf.write("==角色生日特别剧情==\n")
        elif title[:2] == "幕间":
            wf.write("==%s==\n" % title)
        else:
            wf.write("==%s%s%s==\n" % (title.split(" ")[-1], " ", situation))
    elif story_type in {5, 7}:
        _id = {"101":"预告 ","000":"序章 ","001":"第1话 ","002":"第2话 ","003":"第3话 ","004":"第4话 ","005":"第5话 ","006":"第6话 ","007":"终章 ","008":"真·终章 "}.get(episode, "")
        if episode == "202":
            wf.write("==首领战相关==\n===普通解锁===\n")
        elif episode == "301":
            wf.write("===普通挑战===\n")
        elif episode == "203":
            wf.write("===普通获胜===\n")
        elif episode == "204":
            wf.write("===困难解锁===\n")
        elif episode == "302":
            wf.write("===困难挑战===\n")
        elif episode == "401":
            wf.write("===困难获胜·%s===\n" % situation)
        elif episode == "308":
            wf.write("===高难挑战===\n")
        elif episode in {"402","422"}:
            wf.write("===高难获胜·%s===\n" % situation)
        elif episode == "321":
            wf.write("===SP挑战===\n")
        elif episode == "322":
            wf.write("===SP升阶段2===\n")
        elif episode == "323":
            wf.write("===SP升阶段3===\n")
        elif episode in {"403","423"}:
            wf.write("===击破10只·%s===\n" % situation)
        elif episode in {"404","424"}:
            wf.write("===击破20只·%s===\n" % situation)
        elif episode in {"405","425"}:
            wf.write("===击破30只·%s===\n" % situation)
        elif episode in {"406","426"}:
            wf.write("==活动主页==\n'''%s'''\n" % situation)
        elif episode in {"407", "408", "409", "410","427","428","429","430"}:
            wf.write("'''%s'''\n" % situation)
        else:
            if episode in {"101"}:
                situation = title[:-4]
            elif episode >= "600":
                situation = "特别·" + episode + situation
            wf.write("==%s%s==\n" % (_id, situation))
    elif story_type == 6:
        wf.write("'''%s'''\n" % situation)
    # 剧情梗概
    if outline.strip() != "":
        wf.write("{{折叠|宽度=100%\n|标题=剧情梗概\n|" + "内容=%s\n}}\n" % outline)
    # 普通对话
    if in_file not in ["2114099.json", "5100423.json"]:
        talks(lines, wf)
    elif in_file not in ["5100423.json"]:
        talks2(lines, wf)
    wf.close()
    

def story():
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    story_json_files = os.listdir(in_path)
    last_out_file = "txt"
    for in_file in story_json_files:
        if len(in_file) != 12:
            continue
        if in_file[:4] not in {"5100","6100"}:
            continue
        story_type = int(in_file[0])
        if story_type not in active_story_type:
            continue
        out_file = in_file[:4] + ".txt"
        first = False
        if out_file != last_out_file:
            first = True
        last_out_file = out_file
        episode = in_file[4:7]
        if story_type == 5:
            if first:
                yugao = in_file[:4] + "101.json"
                if os.path.exists(os.path.join(in_path, yugao)):
                    transform(yugao, out_file, "101", True, story_type)
            elif episode == "101":
                # 小剧情，排排队
                for e in ["202","301","203","204","302","401","308",
                        #   "402", # 下面的备选
                          "422",
                          "321","322","323",
                        #   "403","404","405" # 下面的备选
                          "423","424","425"
                          ]:
                    i = in_file[:4] + e + ".json"
                    if os.path.exists(os.path.join(in_path, i)):
                        print(i)
                        transform(i, out_file, e, False, story_type)
                continue
            elif episode in ["202","301","203","204","302","401","308","402","321","322","323","403","404","405",
                             "422","423","424","425",
                            #  "406","407","408","409","410","411",
                            #  "426","427","428","429","430","431",
                             "442","443","444","445",
                            #  "446","447","448","449","450","451"
                            ]:
                continue
            first = False
        elif story_type == 6:
            out_file = "5" + out_file[1:]
            first = False
        print(in_file)
        transform(in_file, out_file, episode, first, story_type)
        

if __name__ == "__main__":
    story()