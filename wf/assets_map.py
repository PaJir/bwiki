import os
import json
import en2cn
import shutil

ROOT_PATH = "E:\\wf_jp\\output\\orderedmap"
# ROOT_PATH = "C:\\github\\wf-assets\\orderedmap"
ASSETS_PATH = "E:\\wf_cn\\output\\assets"
ASSETS_PATH2 = "E:\\wf\\output\\assets"
ASSETS_PATH3 = "E:\\wf\\assets"

wf = open("assets_map.txt", "w+", encoding="utf-8")

def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as rf:
        lines = rf.readlines()
    lines = "".join(lines)
    return json.loads(lines)
# 200071
score_rewards = read_json_file(os.path.join(ROOT_PATH, "reward\\score_reward.json"))
# 3001401
rare_score_rewards = read_json_file(os.path.join(ROOT_PATH, "reward\\rare_score_reward.json"))
# 5090014
equipments = read_json_file(os.path.join(ROOT_PATH, "item\\equipment.json"))
items = read_json_file(os.path.join(ROOT_PATH, "item\\item.json"))
# 141003
characters = read_json_file(os.path.join(ROOT_PATH, "character\\character.json"))
# 简介
characters_text = read_json_file(os.path.join(ROOT_PATH, "character\\character_text.json"))
# 等级
characters_status = read_json_file(os.path.join(ROOT_PATH, "character\\character_status.json"))
# name - name_cn, color
story_character = read_json_file(os.path.join(ROOT_PATH, "story\\story_character.json"))
gacha = read_json_file(os.path.join(ROOT_PATH, "gacha\\gacha.json"))

def search_equip_prob():
    for score_reward in score_rewards:
        for score_reward_subid in score_rewards[score_reward]:
            rare_score_reward_id = score_rewards[score_reward][score_reward_subid][6]
            rare_score_reward_prob = score_rewards[score_reward][score_reward_subid][7]
            rare_score_reward = rare_score_rewards.get(rare_score_reward_id)
            if rare_score_reward is None:
                continue
            for rare_score_reward_subid in rare_score_reward:
                rare_score_reward_name = rare_score_reward[rare_score_reward_subid][0]
                if rare_score_reward_name.find("equip") != -1:
                    equipment_id = rare_score_reward[rare_score_reward_subid][2]
                    equipment = equipments.get(equipment_id)
                    if equipment is None:
                        continue
                    equipment_name = equipment[0]
                    if rare_score_reward_name.startswith("boss_battle"):
                        wf.write("%s\t%s\t%s\n" % (rare_score_reward_name, equipment_name, rare_score_reward_prob))
                        # pass
                elif rare_score_reward_name.find("character") != -1:
                    character_id = rare_score_reward[rare_score_reward_subid][2]
                    character = characters.get(character_id)
                    if character is None:
                        continue
                    character_name = character[0]
                    character_name_cn = en2cn.en2cn(character_name)
                    wf.write("%s\t%s\t%s\t%s\n" % (rare_score_reward_name, character_name, character_name_cn, rare_score_reward_prob))


def character_hp_atk():
    for character_id in characters_status:
        character = characters.get(character_id)
        if character is None:
            continue
        character_name = character[0]
        character_name_cn = en2cn.en2cn(character_name)
        if character_name_cn == "":
            continue
        status = characters_status[character_id]
        wf.write(character_name_cn, status["1"][0], status["100"][0], status["1"][1], status["100"][1])


def mana_node_need():
    """点mana板所需的材料"""
    mana_node = read_json_file(os.path.join(ROOT_PATH, "mana_board\\mana_node.json"))
    for character_id in mana_node:
        character = characters.get(character_id)
        if character is None:
            continue
        character_name = character[0]
        character_name_cn = en2cn.en2cn(character_name)
        if character_name_cn == "":
            continue
        board = mana_node[character_id]
        board1 = board.get("1")
        board2 = board.get("2")
        if board1 is not None:
            sums = {}
            for _id in board1:
                materials = board1[_id][2].split(",")
                nums = board1[_id][3].split(",")
                materials.append("mana")
                nums.append(board1[_id][4])
                for (m, n) in zip(materials, nums):
                    if sums.get(m) is None:
                        sums[m] = int(n)
                    else:
                        sums[m] += int(n)
            if sums["99"] != 31:
                wf.write(character_name_cn, str(sums.values()))
            wf.write(character_name_cn, str(sums))
        if board2 is not None:
            sums = {}
            for _id in board2:
                materials = board2[_id][2].split(",")
                nums = board2[_id][3].split(",")
                materials.append("mana")
                nums.append(board2[_id][4])
                for (m, n) in zip(materials, nums):
                    if sums.get(m) is None:
                        sums[m] = int(n)
                    else:
                        sums[m] += int(n)
            # if sums["99"] != 117:
            #     wf.write(character_name_cn, str(sums.values()))
            wf.write(character_name_cn, str(sums))


def copy_or_not(from_path, to_path):
    if not os.path.exists(from_path):
        return False
    elif os.path.exists(to_path):
        return True
    else:
        shutil.copyfile(from_path, to_path)
        return True
        
def character_info():
    character_quests = read_json_file(os.path.join(ROOT_PATH, "quest\\character_quest.json"))
    character_speechs = read_json_file(os.path.join(ROOT_PATH, "character\\character_speech.json"))
    for character_id in characters_text:
        if int(character_id) >= 700000:
            continue
        name_cn = characters_text[character_id][0] # 没有后缀
        name_jp = characters_text[character_id][1]
        intro = characters_text[character_id][2]
        banner = characters_text[character_id][3]
        skill_name = characters_text[character_id][4]
        skill_desp = characters_text[character_id][7].replace("\n", "<br>").replace("\\n", "<br>")
        leader_name = characters_text[character_id][8]
        cv = characters_text[character_id][9]
        if cv == "(None)":
            cv = ""
        character = characters.get(character_id)
        if character is not None:
            # character = character[0]
            name_en = character[0]
            name_cn_tmp = en2cn.en2cn(name_en)
            if name_cn_tmp == "":
                print(name_en, name_cn)
            else:
                name_cn = name_cn_tmp
            star = character[2]
            attr = en2cn.en2attr(character[3])
            race = en2cn.en2race(character[4])
            _type = en2cn.en2type(character[6])
            gender = en2cn.en2gender(character[7])
            stance = en2cn.en2stance(character[26])
        status = characters_status.get(character_id)
        hp_1, atk_1 = "", ""
        if status is not None:
            hp_1 = status["1"][0]
            atk_1 = status["1"][1]
        storys = []
        wf_story = open(os.path.join("story", "角色", name_cn+".txt"), "w+", encoding="utf-8")
        wf_story.write("{{DISPLAYTITLE:%s剧情}}__TOC__\n" % name_cn)
        for quest_suffix in ["01", "02", "03"]:
            quest = character_quests.get(character_id + quest_suffix)
            if quest is not None:
                # quest = quest[0]
                storys.append("《%s》<br>%s" % (quest[3], quest[106].replace("\n", "<br>").replace("\\n", "<br>")))
                wf_story.write("==%s==\n" % (quest[3]))
                wf_story.write("{" + "{折叠|宽度=100%\n|标题=剧情梗概\n|内容=" + quest[106] + "\n}}\n")
                scenario = read_json_file(os.path.join(ROOT_PATH, quest[109] + ".json"))
                write_scenario(scenario, wf_story)
            else:
                storys.append("")
        wf_story.close()
        voice_home = []
        voice_join = ""
        voice_evolution = ""
        voice_files = [
                       "skill_ready.mp3",
                       "skill_0.mp3",
                       "skill_1.mp3",
                       "battle_start_0.mp3",
                       "battle_start_1.mp3",
                       "win_0.mp3",
                       "win_1.mp3",
                       "power_flip_0.mp3",
                       "power_flip_1.mp3",
                       "outhole_0.mp3",
                       "outhole_1.mp3"
                    ]
        speech = character_speechs.get(character_id)
        if speech is not None:
            # speech = speech[0]
            for i in range(3, len(speech), 5):
                voice_path = os.path.join(ASSETS_PATH, "character", name_en, "voice", speech[i+1]+".mp3")
                voice_path2 = os.path.join(ASSETS_PATH2, "character", name_en, "voice", speech[i+1]+".mp3")
                # print(voice_path2)
                voice_path3 = os.path.join(ASSETS_PATH3, "character", name_en, "voice", speech[i+1]+".mp3")
                if speech[i-3] == "2": # "ally/join":
                    voice_join = speech[i].replace("\n", "<br>").replace("\\n", "<br>")
                    out_path = os.path.join(ASSETS_PATH, "out_voice", name_cn+"join.mp3")
                elif speech[i-3] == "1": # "ally/evolution":
                    voice_evolution = speech[i].replace("\n", "<br>").replace("\\n", "<br>")
                    out_path = os.path.join(ASSETS_PATH, "out_voice", name_cn+"evolution.mp3")
                else:
                    voice_suffix = str(len(voice_home))
                    voice_home.append(speech[i].replace("\n", "<br>").replace("\\n", "<br>"))
                    out_path = os.path.join(ASSETS_PATH, "out_voice", name_cn+"home"+voice_suffix+".mp3")
                if not copy_or_not(voice_path, out_path):
                    # print("-----------")
                    if not copy_or_not(voice_path2, out_path):
                        copy_or_not(voice_path3, out_path)
        for voice_file in voice_files:
            voice_path = os.path.join(ASSETS_PATH, "character", name_en, "voice", "battle", voice_file)
            voice_path2 = os.path.join(ASSETS_PATH2, "character", name_en, "voice", "battle", voice_file)
            voice_path3 = os.path.join(ASSETS_PATH3, "character", name_en, "voice", "battle", voice_file)
            out_path = os.path.join(ASSETS_PATH, "out_voice", name_cn+voice_file)
            if not copy_or_not(voice_path, out_path):
                if not copy_or_not(voice_path2, out_path):
                    if not copy_or_not(voice_path3, out_path):
                        # print(name_cn, voice_file)
                        pass
        wf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % 
                 (name_cn, name_cn, name_jp, name_en, gender, 
                  _type, stance, race, attr, star, 
                  cv, intro, hp_1, atk_1, banner, 
                  skill_name, skill_desp, leader_name, "\t".join(storys), "￥".join(voice_home), 
                  voice_join, voice_evolution))
        # break
    return


def pedia_help():
    encyclopedia = read_json_file(os.path.join(ROOT_PATH, "encyclopedia\\encyclopedia.json"))
    pedia_ids = [str(i) for i in range(1, 10)]
    for pedia in encyclopedia.values():
        _type = pedia["1"][1]
        if _type.startswith("character"):
            wf.write("%s\t%s\t" % ("角色", en2cn.en2cn(pedia["1"][5])))
        elif _type.startswith("npc"):
            wf.write("%s\t%s\t" % ("npc", pedia["1"][16]))
        elif _type.startswith("main_") or _type.startswith("prologue"):
            wf.write("%s\t%s\t" % ("主线章节", pedia["1"][16]))
        elif _type.startswith("event"):
            wf.write("%s\t%s\t" % ("剧情活动", pedia["1"][16]))
        elif _type.startswith("keyword"):
            wf.write("%s\t%s\t" % ("关键字", pedia["1"][16]))
        else:
            wf.write("%s\t%s\t" % (_type, pedia["1"][16]))
        explain = []
        for pedia_id in pedia_ids:
            p = pedia.get(pedia_id)
            if p is None:
                break
            explain.append(p[19].replace("\n", "<br/>"))
        wf.write("%s\n" % ("<br>".join(explain)))


def story_main():
    main_quest = read_json_file(os.path.join(ROOT_PATH, "quest\\main_quest.json"))
    main_chapter = read_json_file(os.path.join(ROOT_PATH, "quest\\main_chapter.json"))
    for chapter_id in main_quest:
        if chapter_id != "10":
            continue
        chapter = main_quest[chapter_id]
        wf.write("%s\n" % main_chapter[chapter_id][0])
        for main_id in chapter:
            main = chapter[main_id]
            for quest_id in main:
                quest = main[quest_id]
                if not quest[2].endswith("story"):
                    continue
                title = quest[1]
                intro = quest[104]
                file_path = quest[107]
                wf.write("==%s-%s-%s %s==\n" % (chapter_id, main_id, quest_id, title))
                wf.write("{" + "{折叠|宽度=100%\n|标题=剧情梗概\n|内容=" + intro + "\n}}\n")
                scenario = read_json_file(os.path.join(ROOT_PATH, file_path + ".json"))
                write_scenario(scenario, wf)

def write_scenario(scenario, wf):
    for _s in scenario.values():
        for s in _s.values():
            if s[5] == "":
                continue
            name = story_character[s[4]][0]
            # color = story_character[s[4]][3]
            chara_ui = story_character[s[4]][4]
            if chara_ui == "":
                img_name = ""
            else:
                img_name_ = chara_ui.split("/")[1]
                if chara_ui.find("unknown") != -1:
                    img_name_ += "_unknown"
                img_name = en2cn.en2cn(img_name_)
                if img_name == "":
                    print(img_name_)
                    img_name = ""
            wf.write("{" + "{对话|%s|%s|%s}}\n" % (img_name, name, s[5].replace("\n", "<br>").replace("\\n", "<br>").replace("~~~", "<nowiki>~~~</nowiki>")))

def equip_info():
    equipment_status = read_json_file(os.path.join(ROOT_PATH, "item\\equipment_status.json"))
    elements = {"0": "火", "1": "水", "2": "雷", "3": "风", "4": "光", "5": "暗"}
    for equip_id in equipments:
        equip_en_name = equipments[equip_id][0]
        equip_name = equipments[equip_id][1]
        equip_element = elements.get(items[equip_id][11], "全")
        equip_info = equipments[equip_id][7]
        equip_story = equipments[equip_id][5]
        hp_1 = equipment_status[equip_id]["1"][0]
        atk_1 = equipment_status[equip_id]["1"][1]
        if equipment_status[equip_id].get("5") is None:
            hp_5 = hp_1
            hp_1 = ""
            atk_5 = atk_1
            atk_1 = ""
        else:
            hp_5 = equipment_status[equip_id]["5"][0]
            atk_5 = equipment_status[equip_id]["5"][1]
        wf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (equip_id, equip_en_name, equip_element, equip_name, equip_info, equip_story, hp_1, hp_5, atk_1, atk_5))

def gacha_info():
    for g in gacha.values():
        wf.write("%s\t%s\t%s\t%s\n" % (g[1], g[0], g[29], g[30]))

if __name__ == "__main__":
    # search_equip_prob()
    # character_hp_atk()
    # mana_node_need()
    # character_info()
    # pedia_help()
    # story_main()
    # equip_info()
    gacha_info()
