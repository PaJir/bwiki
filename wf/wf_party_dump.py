import os
from bs4 import BeautifulSoup
from en2cn import en2cn, jp2tag
from assets_map import read_json_file

WF_PARTY_PATH = "C:\\repository\\wf_party_archives"

unit_info = read_json_file(os.path.join(WF_PARTY_PATH, "static", "party", "unit_info.json"))
equip_info = unit_info["exist_equips"]
equip_pos_map = {
    "リーダー装備": 6,
    "リーダーソウル": 7,
    "2人目武器": 8,
    "2人目ソウル": 9,
    "3人目武器": 10,
    "3人目ソウル": 11
}
QUESTS = set()
TAGS = set()
def read_tag(path, wf):
    global QUESTS, TAGS
    soup = BeautifulSoup(open(path, "r", encoding="utf-8"), "lxml")
    select_list = soup.find_all("div", "questWrap")
    for s in select_list:
        name = s.find("a").string
        QUESTS.add(name)
    tags = soup.find_all("div", "tagwrap")
    for t in tags:
        TAGS.add(t.find("a").string[1:])



def read_html(path, wf):
    soup = BeautifulSoup(open(path, "r", encoding="utf-8"), "lxml")
    output = [""] * 20
    idx = 0
    units = soup.find_all("td", "colHeader")
    for unit in units:
        img = str(unit.find("img"))
        name_en = img.split("/")[5]
        name_cn = en2cn(name_en)
        output[idx] = name_cn if name_cn != "" else name_en.replace("blank", "")
        idx += 1
    detail = soup.find("table", id="detailTable")
    for equip in detail.find_all("tr")[3:]:
        equip_pos = equip.find("td", "col_header").string
        equip_jp = equip.find("td", "col_data").string
        equip_cn = ""
        for equip_i in equip_info:
            if equip_jp == equip_i["name_jp"]:
                equip_en = equip_i["unit_id"]
                equip_cn = en2cn(equip_en)
                if equip_cn == "":
                    equip_cn = equip_en
                output[equip_pos_map[equip_pos]] = equip_cn
    abi_vals = soup.find_all("div", "abiVal")
    idx = 12
    # for abi in abi_vals:
    for i in range(6):
        abis = "["
        for j in range(3):
            abi = int(str(abi_vals[i*3+j]).split("\"")[1][-1])-1
            abis += (str(abi) + ".") if abi>-1 else "-."
        output[idx] = abis + "]"
        idx += 1
    title = []
    select_list = soup.find_all("div", "questWrap")
    for s in select_list:
        name = jp2tag(s.find("a").string)
        name += s.find("div", "useful_cnt").string
        title.append(name)
    tags = soup.find_all("div", "tagwrap")
    for t in tags:
        title.append(jp2tag(t.find("a").string[1:]))
    memo_text = soup.find("div", id="memo_text")
    title.append(str(memo_text.find("p")).replace("\n", "").replace("<p>", "").replace("</p>", ""))
    output[18] = " ".join(title)
    output[19] = detail.find("td", "col_data").string
    # print(output)
    # wf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (output[0], output[6], output[12], output[2], output[8], output[14], output[4], output[10], output[16], output[1], output[7], output[13], output[3], output[9], output[15], output[5], output[11], output[17], output[18], output[19]))
    wf.write("{{盘子|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s}}\t%s\n" % (output[0], output[6], output[12], output[2], output[8], output[14], output[4], output[10], output[16], output[1], output[7], output[13], output[3], output[9], output[15], output[5], output[11], output[17], output[18], output[19]))



if __name__ == "__main__":
    wf = open("wf_party_dump.txt", "w+", encoding="utf-8")
    for file in os.listdir(os.path.join(WF_PARTY_PATH, "party")):
        # print(file)
        read_html(os.path.join(WF_PARTY_PATH, "party", file), wf)
        # read_tag(os.path.join(WF_PARTY_PATH, "party", file), wf)
    # for q in TAGS:
    #     wf.write(q+"\n")
    wf.close()