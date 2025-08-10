def transformPattern(p):
    """ 1: 普攻
        100x: 技能x
        200x: 特殊技能x
    """
    if p == 0:
        return ""
    elif p < 1000:
        if p != 1:
            print(p)
        # assert p == 1
        return "{{行动|普攻}} → "
    elif p < 2000:
        return "{{行动|" + str(p-1000) + "}} → "
    else:
        assert p < 3000
        return "{{行动|特殊" + str(p-2000) + "}} → "


def attackPattern(unit_id, cur):
    """ unit_id: 六位 
        return (starts, loops)
    """
    starts = list()
    loops = list()
    idx = ["①", "②", "③", "④"]
    sql = "SELECT pattern_id , unit_id , loop_start , loop_end , atk_pattern_1 , atk_pattern_2 , atk_pattern_3 , atk_pattern_4 , atk_pattern_5 , atk_pattern_6 , atk_pattern_7 , atk_pattern_8 , atk_pattern_9 , atk_pattern_10 , atk_pattern_11 , atk_pattern_12 , atk_pattern_13 , atk_pattern_14 , atk_pattern_15 , atk_pattern_16 , atk_pattern_17 , atk_pattern_18 , atk_pattern_19 , atk_pattern_20 FROM unit_attack_pattern WHERE unit_id=" + \
        str(unit_id) + \
        " ORDER BY pattern_id"
    cur.execute(sql)
    patterns = cur.fetchall()
    add_idx = len(patterns) > 1
    for index in range(len(patterns)):
        _start = ""
        _loop = ""
        loop_start = patterns[index][2] - 1
        loop_end = patterns[index][3] # 不建议，左闭右开
        # delete atk_pattern_14
        loop = patterns[index][4:]
        if str(unit_id)[0] == "1":
            loop = loop[0:13] + loop[14:]
        if add_idx:
            _start = idx[index]
            _loop = idx[index]

        if loop_start == 0:
            _start += "无"
        else:
            for p in loop[0:loop_start]:
                _start += transformPattern(p)
            if  _start.endswith(" → "):
                _start = _start[:-3]

        assert loop_start < loop_end
        for p in loop[loop_start: loop_end]:
            _loop += transformPattern(p)
        if _loop.endswith(" → "):
            _loop = _loop[:-3]
        _loop += " ↻"

        starts.append(_start)
        loops.append(_loop)

    starts = "<br>".join(starts)
    loops = "<br>".join(loops)
    return (starts, loops)
