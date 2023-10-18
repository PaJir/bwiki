import os
from shutil import move
import shutil
import requests
import time
import random
import logging
logger = logging.getLogger("log mp3")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("log.txt")
logger.addHandler(file_handler)

# https://redive.estertion.win/sound/unit_battle_voice/103601/vo_btl_103601_applaud.m4a
redive = "https://redive.estertion.win/sound/unit_battle_voice/"
m4a_path = "D:\Extra\pcr\mp3\\1191-m4a\\"
mp3_path = "D:\Extra\pcr\mp3\\"

role_list = [str(a) for a in range(1207, 1213)]
role_list += [str(a) for a in range(1801, 1809)]

voice_list = [
    "applaud",      # 喝彩？
    "attack_001",   # 攻击
    "attack_002",
    "attack_003",
    "cutin_001",    # UB第一段
    "cutin_002",
    "damage_001",   # 受伤
    "damage_002",
    "damage_003",
    "lastwave",     # 进入最后一波战斗
    "lose_001",     # 失败
    "lose_002",
    "lose_003",
    "nextwave",     # 进入第二波战斗
    "retire_001",   # 阵亡
    "retire_002",
    "retire_003",
    "skill_100",    # 技能
    "skill_200",
    "skillsp_100",  # 特殊技能
    "skillsp_200",
    "thanks",
    "ub_100",       # UB第二段
    "ub_200",
    "wavestart",    # 战斗开始
    "win_001",      # 胜利
    "win_002",
    "win_003",
    # "vo_btl_xxxx61_cutin_001",  # 六星UB第一段
    # "vo_btl_xxxx61_ub_100",  # 六星UB第二段
    # "vo_btl_xxxx61_ub_200"
    # 进入地图一个关卡有个语音，不知道在哪
]

# 已经上传的文件
uploaded = [
        """
        "vo_btl_100101_applaud.mp3",
        "vo_btl_100101_attack_001.mp3"...
        API见最下方
        """
    ]

def get_a_m4a(role, voice):
    """ 爬取一个m4a文件 """
    file_name = "vo_btl_" + role + "01_" + voice + ".m4a"
    if os.path.exists(m4a_path + file_name):
        return False
    url = redive + role + "01/" + file_name
    try:
        myfile = requests.get(url)
    except:
        logger.debug("--------------error.get---------------")
    try:
        open(m4a_path + file_name, 'wb').write(myfile.content)
    except:
        logger.debug("---------------error----------------")
    myfile.close()
    logger.debug(file_name)
    t = 0.2 + random.random() / 10
    time.sleep(t)
    return True

def get_m4a():
    """ 批量爬取m4a文件 """
    for role in role_list:
        for voice in voice_list:
            get_a_m4a(role, voice)

def m4a_2_mp3():
    m4a_file = os.listdir(m4a_path)

    for i, m4a in enumerate(m4a_file):
        if not m4a.endswith("m4a"):
            continue
        logger.debug(i, m4a)
        os.system("ffmpeg -i " + m4a_path + m4a + " " + mp3_path + m4a.replace("m4a", "mp3"))

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

from pydub import AudioSegment
def wav_2_mp3(filepath, savepath):
    """
    TODO: 有点偏移
    filepath: D:\Extra\pcr\mp3\\主页语音\\
    savepath: D:\Extra\pcr\mp3\\
    01: 1-battle start, 2x 3x 4x 5x 6x
    11: 1/8 2-7
    31: 1/8 2-7
    61: 1/7 2-6
    """
    # vo_cmn_100111
    filepath2 = os.listdir(filepath)
    for path2 in filepath2:
        files = {"1": "0", "2": "1", "3": "2", "4": "3", "5": "4", "6": "5"}
        if path2.endswith("11") or path2.endswith("31"):
            files = {"1": "6", "8": "7"}
        if path2.endswith("61"):
            files = {"1": "6", "7": "7"}
        # 2.wav
        for file in files:
            filename = file + ".wav"
            filepath3 = os.path.join(filepath, path2, filename)
            savepath3 = os.path.join(savepath, path2[:12] + files[file] + ".mp3")
            if os.path.exists(savepath3):
                continue
            if not os.path.exists(filepath3):
                filepath3 = os.path.join(filepath, path2, "0" + filename)
            if not os.path.exists(filepath3):
                continue

            sourcefile = AudioSegment.from_wav(filepath3)
            sourcefile.export(savepath3, format="mp3")

def rename(path):
    files = os.listdir(path)
    for file in files:
        if not file.endswith(".mp3"):
            continue
        shutil.move(os.path.join(path, file), os.path.join(path, "vo_cmn_"+file))

# get_m4a()
# m4a_2_mp3()
# move_mp3()
# get_a_m4a("1186", "thanks")
# get_a_m4a("1197", "win_003")
wav_2_mp3("D:\Extra\pcr\mp3\\主页语音\\", "D:\Extra\pcr\mp3\\")
# rename("D:\Extra\pcr\mp3\\")

""" 有问题的：
vo_btl_100101_ub_100.m4a等等，还有好多
部分文件没有上传，api：
https://wiki.biligame.com/pcr/api.php?action=query&list=allimages&aimime=audio/mpeg&aisort=timestamp&aidir=descending&aiprop=&prop=&aifrom=Vo_btl&ailimit=5000&format=json
https://www.mediawiki.org/wiki/API:Allimages

errorget:
"""