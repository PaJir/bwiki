import os
import json
import en2cn

ROOT_PATH = "wf-assets-gl\\orderedmap"

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
characters_status = read_json_file(os.path.join(ROOT_PATH, "character\\character_status.json"))

def search_equip_prob():
    for score_reward in score_rewards:
        for score_reward_subid in score_rewards[score_reward]:
            rare_score_reward_id = score_rewards[score_reward][score_reward_subid][0][6]
            rare_score_reward_prob = score_rewards[score_reward][score_reward_subid][0][7]
            rare_score_reward = rare_score_rewards.get(rare_score_reward_id)
            if rare_score_reward is None:
                continue
            for rare_score_reward_subid in rare_score_reward:
                rare_score_reward_name = rare_score_reward[rare_score_reward_subid][0][0]
                if rare_score_reward_name.find("equip") != -1:
                    equipment_id = rare_score_reward[rare_score_reward_subid][0][2]
                    equipment = equipments.get(equipment_id)
                    if equipment is None:
                        continue
                    equipment_name = equipment[0][0]
                    if rare_score_reward_name.startswith("boss_battle"):
                        print(rare_score_reward_name, equipment_name, rare_score_reward_prob)
                        # pass
                elif rare_score_reward_name.find("character") != -1:
                    character_id = rare_score_reward[rare_score_reward_subid][0][2]
                    character = characters.get(character_id)
                    if character is None:
                        continue
                    character_name = character[0][0]
                    character_name_cn = en2cn.en2cn(character_name)
                    print(rare_score_reward_name, character_name, character_name_cn, rare_score_reward_prob)


def character_hp_atk():
    for character_id in characters_status:
        character = characters.get(character_id)
        if character is None:
            continue
        character_name = character[0][0]
        character_name_cn = en2cn.en2cn(character_name)
        if character_name_cn == "":
            continue
        status = characters_status[character_id]
        print(character_name_cn, status["1"][0][0], status["100"][0][0], status["1"][0][1], status["100"][0][1])

def mana_node_need():
    """点mana板所需的材料"""
    mana_node = read_json_file(os.path.join(ROOT_PATH, "mana_board\\mana_node.json"))
    for character_id in mana_node:
        character = characters.get(character_id)
        if character is None:
            continue
        character_name = character[0][0]
        character_name_cn = en2cn.en2cn(character_name)
        if character_name_cn == "":
            continue
        board = mana_node[character_id]
        board1 = board.get("1")
        board2 = board.get("2")
        if board1 is not None:
            sums = {}
            for _id in board1:
                materials = board1[_id][0][2].split(",")
                nums = board1[_id][0][3].split(",")
                materials.append("mana")
                nums.append(board1[_id][0][4])
                for (m, n) in zip(materials, nums):
                    if sums.get(m) is None:
                        sums[m] = int(n)
                    else:
                        sums[m] += int(n)
            if sums["99"] != 31:
                print(character_name_cn, str(sums.values()))
            print(character_name_cn, str(sums))
        if board2 is not None:
            sums = {}
            for _id in board2:
                materials = board2[_id][0][2].split(",")
                nums = board2[_id][0][3].split(",")
                materials.append("mana")
                nums.append(board2[_id][0][4])
                for (m, n) in zip(materials, nums):
                    if sums.get(m) is None:
                        sums[m] = int(n)
                    else:
                        sums[m] += int(n)
            # if sums["99"] != 117:
            #     print(character_name_cn, str(sums.values()))
            print(character_name_cn, str(sums))
                


if __name__ == "__main__":
    # search_equip_prob()
    # character_hp_atk()
    mana_node_need()
