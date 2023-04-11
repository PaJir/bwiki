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
# 141003
characters = read_json_file(os.path.join(ROOT_PATH, "character\\character.json"))

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
                

if __name__ == "__main__":
    search_equip_prob()
