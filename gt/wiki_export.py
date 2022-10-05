from bs4 import BeautifulSoup

input_file = "./wiki_export.xml"
output_file = "./wiki_export.txt"

fields = ["未实装",
"简称",
"名字",
"星级",
"职业",
"年龄",
"身高",
"体重",
"种族",
"属性",
"可携带武器",
"等级",
"攻击力",
"回血值",
"血量",
"防御",
"减伤",
"暴击率",
"技能",
"普通攻击",
"普通攻击基础伤害倍率",
"特殊技能基础伤害倍率",
"专武技能基础伤害倍率",
"连携技能基础伤害倍率",
"普通攻击基础伤害倍率2",
"特殊技能基础伤害倍率2",
"专武技能基础伤害倍率2",
"连携技能基础伤害倍率2",
"连携发起状态",
"连携效果",
"连携技能",
"特殊能力",
"被动加成",
"主要伤害种类",
"普通攻击2",
"连携发起状态2",
"连携效果2",
"连携技能2",
"特殊能力2",
"被动加成2",
"主要伤害种类2",
"专武名称",
"专武名称-含歧义",
"专武属性",
"专武技能名",
"专武攻击力",
"专武恢复时间",
"专武技能",
"专武状态",
"专武专属效果",
"专武名称2",
"专武属性2",
"专武技能名2",
"专武攻击力2",
"专武恢复时间2",
"专武技能2",
"专武状态2",
"专武专属效果2",
"故事解锁",
"背景故事",
"角色外号",
"推荐武器",
"推荐武器理由",
"推荐饰品",
"推荐饰品理由",
"推荐盾牌",
"推荐盾牌理由",
"评价优势",
"评价劣势",
"国服评价",
"国际服评价",
"PVE评价",
"角斗场评价",
"竞技场评价",
"公会战评价",
"公会战挂件",
"园区评价",
"角色外号2",
"评价优势2",
"评价劣势2",
"国服评价2",
"国际服评价2",
"PVE评价2",
"角斗场评价2",
"竞技场评价2",
"公会战评价2",
"公会战挂件2",
"皮肤1名称",
"皮肤1价格",
"皮肤2名称",
"皮肤2价格",
"皮肤3名称",
"皮肤3价格",
"皮肤4名称",
"皮肤4价格",
"皮肤5名称",
"皮肤5价格",
"皮肤6名称",
"皮肤6价格",
"皮肤7名称",
"皮肤7价格",
"皮肤8名称",
"皮肤8价格",
"皮肤9名称",
"皮肤9价格",
"皮肤10名称",
"皮肤10价格",
"皮肤11名称",
"皮肤11价格",
"皮肤12名称",
"皮肤12价格",
"皮肤13名称",
"皮肤13价格",
"皮肤14名称",
"皮肤14价格",
"皮肤15名称",
"皮肤15价格",
"皮肤16名称",
"皮肤16价格",
"皮肤17名称",
"皮肤17价格",
"皮肤18名称",
"皮肤18价格",
"皮肤19名称",
"皮肤19价格",
"皮肤20名称",
"皮肤20价格",
"皮肤21名称",
"皮肤21价格",
"皮肤22名称",
"皮肤22价格",
"皮肤23名称",
"皮肤23价格",
"皮肤24名称",
"皮肤24价格",
"皮肤25名称",
"皮肤25价格",
"皮肤26名称",
"皮肤26价格",
"皮肤27名称",
"皮肤27价格",
"皮肤28名称",
"皮肤28价格",
"皮肤29名称",
"皮肤29价格",
"皮肤30名称",
"皮肤30价格",
"皮肤31名称",
"皮肤31价格",
"皮肤32名称",
"皮肤32价格",
"皮肤33名称",
"皮肤33价格",
"皮肤34名称",
"皮肤34价格",
"皮肤35名称",
"皮肤35价格",
"皮肤36名称",
"皮肤36价格",
"皮肤37名称",
"皮肤37价格",
"皮肤38名称",
"皮肤38价格",
"皮肤39名称",
"皮肤39价格",
"皮肤40名称",
"皮肤40价格",
"皮肤41名称",
"皮肤41价格",
"皮肤42名称",
"皮肤42价格",
"皮肤43名称",
"皮肤43价格",
"皮肤44名称",
"皮肤44价格",
"皮肤45名称",
"皮肤45价格",
"皮肤46名称",
"皮肤46价格",
"皮肤47名称",
"皮肤47价格",
"皮肤48名称",
"皮肤48价格",
"皮肤49名称",
"皮肤49价格",
"低阶攻击觉醒石",
"中阶攻击觉醒石",
"高阶攻击觉醒石",
"低阶防御觉醒石",
"中阶防御觉醒石",
"高阶防御觉醒石",
"低阶生命觉醒石",
"中阶生命觉醒石",
"高阶生命觉醒石",
"低阶梦幻觉醒石",
"中阶梦幻觉醒石",
"高阶梦幻觉醒石",
"传说中的觉醒石",
"配音-汉语",
"配音-英语",
"配音-日语",
"配音-韩语",
"抽到该角色颁奖时",
"胜利-普通战斗",
"胜利-首领",
"阵亡",
"获得经验结晶",
"升级",
"佩戴装备",
"佩戴时装",
"进化",
"攻击1",
"攻击2",
"攻击3",
"技能1",
"技能2",
"受到攻击1",
"受到攻击2",
"主角友善值选项",
"主角邪恶值选项",
"挑战简单敌人",
"挑战普通敌人",
"挑战困难敌人",
"挑战首领",
"首次加入队伍",
"战斗-攻击",
"战斗-请求使用回血技能",
"战斗-注意",
"战斗-胜利",
"战斗-最佳队员",
"战斗-问候",
"战斗-急迫",
"战斗-信任",
"点击人物时反应-积极态度1",
"点击人物时反应-积极态度2",
"点击人物时反应-消极态度1",
"点击人物时反应-消极态度2",
"邮件提醒",
"活动提醒",
"召唤-台词1",
"召唤-台词2",
"召唤-台词3",
"特殊对话1",
"特殊对话2",
"特殊对话3",
"特殊对话4",
"特殊对话5",
"特殊对话6",
"特殊对话7",
"特殊对话8"
]

def read_xml():
    html = None
    with open(input_file, "r", encoding="utf-8") as rf:
        html = rf.readlines()
    html = "".join(html)
    soup = BeautifulSoup(html, "xml")
    pages = soup.find_all("page")
    with open(output_file, "w+", encoding="utf-8") as wf:
        for page in pages:
            text = page.find("revision").find("text").string
            data = text[:-2].split("\n|")[1:]
            field_map = {}
            for d in data:
                eq_idx = d.find("=")
                field = d[:eq_idx]
                value = d[eq_idx+1:].replace("\n\n", "<br>").replace("\n", "")
                field_map[field] = value
                if field not in fields:
                    print(field)
                    # print(field_map["名字"], field)
            output = []
            for field in fields:
                # output.append("|" + field + "=" + field_map.get(field, ""))
                output.append(field_map.get(field, ""))
            # output = "{{角色\n" + "\n".join(output) + "}}\n"
            output = field_map.get("名字", "") + "\t" + "\t".join(output) + "\n"
            wf.write(output)


if __name__ == "__main__":
    read_xml()
