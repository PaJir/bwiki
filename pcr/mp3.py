import os
from shutil import move
import shutil
from config import assert_path
import logging
logger = logging.getLogger("log mp3")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("log.txt")
logger.addHandler(file_handler)

m4a_path = "D:\Extra\pcr\mp3\\1191-m4a\\"
mp3_path = os.path.join(assert_path, "mp3", "20240326")

voice_list = [
    "applaud",      # 6 喝彩？
    "applaud_001",
    "applaud_002",
    "applaud_003",  # 重复
    "attack_001",   # 1 普攻
    "attack_002",
    "attack_003",
    "attack_004",
    "attack_005",
    "attack_006",
    "cutin_001",    # UB第一段
    "cutin_002",    # 大概率重复，只供查询
    "damage_001",   # 2 受击
    "damage_002",
    "damage_003",
    "damage_004",
    "damage_005",
    "damage_006",
    "lastwave",     # 4 第3波战斗
    "lastwave_001",
    "lastwave_002",
    "lastwave_003",
    "lose_001",     # 5 失败
    "lose_002",
    "lose_003",
    "lose_004",
    "lose_005",
    "lose_006",
    "nextwave",     # 4 第2波战斗
    "nextwave_001",
    "nextwave_002",
    "nextwave_003",
    "retire_001",   # 3 阵亡
    "retire_002",
    "retire_003",
    "retire_004",
    "retire_005",
    "retire_006",
    "skill_100",    # 技能
    "skill_110",
    "skill_120",
    "skill_130",
    "skill_200",
    "skill_201",
    "skill_210",
    "skill_220",
    "skill_230",
    "skillsp_100",  # 特殊技能
    "skillsp_200",
    "skillsp_300",
    "subub_100",    # 变身UB
    "subub_200",
    "thanks",       # 7
    "thanks_001",
    "thanks_002",
    "thanks_003",
    "ub_100",       # UB第二段
    "ub_200",
    "ub_210",
    "ub_220",
    "ub_230",
    "ub_300",
    "ub_400",
    "ub_101",       # 目前只看到重复的，不显示在角色页面，只供查询
    "ub_102",
    "ub_103",
    "ub_201",
    "ub_202",
    "ub_203",
    "ub_301",
    "ub_302",
    "ub_401",
    "ub_402",
    "wavestart",    # 4 第1波战斗
    "wavestart_001",
    "wavestart_002",
    "wavestart_003",
    "win_001",      # 胜利
    "win_002",
    "win_003",
    "win_004",
    "win_005",
    "win_006",
    # "vo_btl_xxxx61_cutin_001",  # 六星UB第一段
    # "vo_btl_xxxx61_ub_100",  # 六星UB第二段
    # "vo_btl_xxxx61_ub_200"
    # 进入地图一个关卡有个语音，不知道在哪
]
voice_6x_list = [
    "cutin_001",
    "cutin_002",
    "ub_100",
    "ub_200",
    "ub_300",
    "ub_400",
    "ub_101",
    "ub_102",
    "ub_201",
    "ub_202",
    "ub_301",
    "ub_302",
    "ub_401",
    "ub_402"
]
voice_love = [
    "love_001_01", # 好感1->2
    "love_002_01",
    "love_003_01",
    "love_003_02",
    "love_003_03",
    "love_004_01",
    "love_005_01",
    "love_006_01",
    "love_007_01",
    "love_007_02",
    "love_007_03",
    "love_008_01",
    "love_009_01",
    "love_010_01",
    "love_011_01",
    "love_011_02",
    "love_011_03",
    # "anniversary_001",
    # "birthday_001",
    # "christmas_001",
    # "halloween_001",
    # "newyear_001",
    # "valentine_001"
]
voice_rarity = [
    "battlestart_001",
    "battlestart_002",
    "battlestart_003",
    "battlestart_004",
    "rarity_001", # 星级1->2
    "rarity_002",
    "rarity_003",
    "rarity_004",
    "rarity_005"
]
voice_mypage = [
    "gacha_001",
    "gacha_002",
    "gacha_003",
    "mypage_001",
    "mypage_002",
    "mypage_003",
    "mypage_004",
    "mypage_005",
    "mypage_006",
    "mypage_007",
    "mypage_008",
    "mypage_009",
    "mypage_010",
    "mypage_011",
    "mypage_012",
    "profile_001",
]
# 已经上传的文件
uploaded = [
    """
    "vo_btl_100101_applaud.mp3",
    "vo_btl_100101_attack_001.mp3"...
    API见最下方
    """
]

def move_mp3():
    """ 根据已经上传的文件，把本地mp3文件从一个目录移动到另一个目录 """
    from_path = "D:\Extra\pcr\mp3\\uploaded\\"
    to_path = "D:\Extra\pcr\mp3\\"
    from_files = os.listdir(from_path)
    for _, from_file in enumerate(from_files):
        # if not from_file.endswith(".mp3"):
        #     continue
        if from_file not in uploaded:
            move(from_path+from_file, to_path+from_file)

def wav_2_mp3(filepath, savepath):
    from pydub import AudioSegment
    for voice in os.listdir(filepath):
        filepath3 = os.path.join(filepath, voice)
        savepath3 = os.path.join(savepath, voice[:-4] + ".mp3")
        if os.path.exists(savepath3):
            continue
        sourcefile = AudioSegment.from_wav(filepath3)
        sourcefile.export(savepath3, format="mp3")

def rename(path):
    files = os.listdir(path)
    for file in files:
        if not file.endswith(".mp3"):
            continue
        shutil.move(os.path.join(path, file), os.path.join(path, "vo_cmn_"+file))

def unit_battle_voice():
    voice_path = os.path.join(assert_path, "_redive", "sound", "unit_battle_voice")
    for unit in os.listdir(voice_path):
        if int(unit) >= 200000:
            continue
        elif unit[4] == "0":
            voice_cur_list = voice_list
        elif unit[4] == "6":
            voice_cur_list = voice_6x_list
        else:
            print("more unit ", unit)
            continue
        unit_voice_path = os.path.join(voice_path, unit)
        for voice in os.listdir(unit_voice_path):
            if len(voice) < 18:
                print("too short ", unit, voice)
                continue
            if voice[14:-4] not in voice_cur_list:
                print("more type ", unit, voice)
                continue
            target = voice[:-4] + ".mp3"
            if target in uploaded or os.path.exists(os.path.join(mp3_path, target)):
                continue
            # logger.debug(unit, voice)
            os.system("ffmpeg -i %s %s -loglevel quiet" % (os.path.join(unit_voice_path, voice), os.path.join(mp3_path, target)))

def vo_ci_title():
    for vo in ["vo_ci", "vo_title"]:
        voice_path = os.path.join(assert_path, "_redive", "sound", vo)
        for id in os.listdir(voice_path):
            for voice in os.listdir(os.path.join(voice_path, id)):
                if voice[-7:-4] not in ["001", "002"]: # 成人 幼女
                    print("no 001/002 ", vo, id, voice)
                target = os.path.join(mp3_path, voice[:-4] + ".mp3")
                if os.path.exists(target):
                    continue
                os.system("ffmpeg -i %s %s -loglevel quiet" % (os.path.join(voice_path, id, voice), target))

def unit_common():
    voice_path = os.path.join(assert_path, "_redive", "sound", "unit_common")
    for unit in os.listdir(voice_path):
        if int(unit) >= 190000:
            continue
        elif int(unit) < 100000: # love
            voice_cur_list = voice_love
        elif unit[4] == "0":
            voice_cur_list = voice_rarity
        elif unit[4] in ["1", "3", "6"]:
            voice_cur_list = voice_mypage
        else:
            print("more unit ", unit)
            continue
        unit_voice_path = os.path.join(voice_path, unit)
        for voice in os.listdir(unit_voice_path):
            if voice[3:7] == "navi":
                continue
            if voice[8+len(unit):-4] not in voice_cur_list:
                print("more type ", unit, voice)
                continue
            target = os.path.join(mp3_path, voice[:-4] + ".mp3")
            if os.path.exists(target):
                continue
            os.system("ffmpeg -i %s %s -loglevel quiet" % (os.path.join(unit_voice_path, voice), target))

# move_mp3()
wav_2_mp3("D:\Extra\pcr\mp3\\主页语音\\vo_cmn_170231", "D:\Extra\pcr\mp3\\")
# rename("D:\Extra\pcr\mp3\\")
# unit_battle_voice()
# vo_ci_title()
# unit_common()

""" api：
https://wiki.biligame.com/pcr/api.php?action=query&list=allimages&aimime=audio/mpeg&aisort=name&aidir=descending&aiprop=&prop=&ailimit=5000&format=json
https://wiki.biligame.com/pcr/api.php?action=query&list=allimages&aimime=audio/mpeg&aisort=name&aidir=descending&aiprop=&prop=&aicontinue=vo_btl_110301_skill_200.mp3&ailimit=5000&format=json
https://www.mediawiki.org/wiki/API:Allimages
"""