from action import *


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
    sql = "SELECT * FROM unit_attack_pattern WHERE unit_id=" + \
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

def actionDetail(action_id, depend_action_id, cur):
    sql = "SELECT class_id, action_type, action_detail_1, action_detail_2, action_detail_3, " + \
        "action_value_1, action_value_2, action_value_3, action_value_4, action_value_5, action_value_6, action_value_7, " + \
        "target_assign, target_area, target_range, target_type, target_number, target_count " + \
        "FROM skill_action " + \
        "WHERE action_id=" + \
        str(action_id)
    cur.execute(sql)
    action = cur.fetchone()
    action_type = action[1]
    if action_type == 1:
        return DamageAction(action, depend_action_id)
    elif action_type == 2:
        return MoveAction(action, depend_action_id)
    elif action_type == 3:
        return KnockAction(action, depend_action_id)
    elif action_type == 4:
        return HealAction(action, depend_action_id)
    elif action_type == 5:
        return CureAction(action, depend_action_id)
    elif action_type == 6:
        return BarrierAction(action, depend_action_id)
    elif action_type == 7:
        return ReflexiveAction(action, depend_action_id)
    elif action_type == 8 or action_type == 9 or action_type == 12 or action_type == 13:
        return AilmentAction(action, depend_action_id)
    elif action_type == 10:
        return AuraAction(action, depend_action_id)
    elif action_type == 11:
        return CharmAction(action, depend_action_id)
    elif action_type == 14:
        return ModeChangeAction(action, depend_action_id)
    elif action_type == 15:
        return SummonAction(action, depend_action_id)
    elif action_type == 16:
        return ChangeEnergyAction(action, depend_action_id)
    elif action_type == 17:
        return TriggerAction(action, depend_action_id)
    elif action_type == 18:
        return DamageChargeAction(action, depend_action_id)
    elif action_type == 19:
        return ChargeAction(action, depend_action_id)
    elif action_type == 20:
        return DecoyAction(action, depend_action_id)
    elif action_type == 21:
        return NoDamageAction(action, depend_action_id)
    elif action_type == 22:
        return ChangePatternAction(action, depend_action_id)
    elif action_type == 23:
        return IfForChildrenAction(action, depend_action_id)
    elif action_type == 24:
        return RevivalAction(action, depend_action_id)
    elif action_type == 25:
        return ContinuousAttackAction(action, depend_action_id)
    elif action_type == 26:
        return AdditiveAction(action, depend_action_id)
    elif action_type == 27:
        return MultipleAction(action, depend_action_id)
    elif action_type == 28:
        return IfForAllAction(action, depend_action_id)
    elif action_type == 29:
        return SearchAreaChangeAction(action, depend_action_id)
    elif action_type == 30:
        return DestroyAction(action, depend_action_id)
    elif action_type == 31:
        return ContinuousAttackNearbyAction(action, depend_action_id)
    elif action_type == 32:
        return EnchantLifeStealAction(action, depend_action_id)
    elif action_type == 33:
        return EnchantStrikeBackAction(action, depend_action_id)
    elif action_type == 34:
        return AccumulativeDamageAction(action, depend_action_id)
    elif action_type == 35:
        return SealAction(action, depend_action_id)
    elif action_type == 36:
        return AttackFieldAction(action, depend_action_id)
    elif action_type == 37:
        return HealFieldAction(action, depend_action_id)
    elif action_type == 38:
        return ChangeParameterFieldAction(action, depend_action_id)
    elif action_type == 39:
        return AbnormalStateFieldAction(action, depend_action_id)
    elif action_type == 40:
        return ChangeSpeedFieldAction(action, depend_action_id)
    elif action_type == 41:
        return UBChangeTimeAction(action, depend_action_id)
    elif action_type == 42:
        return LoopTriggerAction(action, depend_action_id)
    elif action_type == 43:
        return IfHasTargetAction(action, depend_action_id)
    elif action_type == 44:
        return WaveStartIdleAction(action, depend_action_id)
    elif action_type == 45:
        return SkillExecCountAction(action, depend_action_id)
    elif action_type == 46:
        return RatioDamageAction(action, depend_action_id)
    elif action_type == 47:
        return UpperLimitAttackAction(action, depend_action_id)
    elif action_type == 48:
        return RegenerationAction(action, depend_action_id)
    elif action_type == 49:
        return DispelAction(action, depend_action_id)
    elif action_type == 50:
        return ChannelAction(action, depend_action_id)
    elif action_type == 52:
        return ChangeBodyWidthAction(action, depend_action_id)
    elif action_type == 53:
        return IFExistsFieldForAllAction(action, depend_action_id)
    elif action_type == 54:
        return StealthAction(action, depend_action_id)
    elif action_type == 55:
        return MovePartsAction(action, depend_action_id)
    elif action_type == 56:
        return CountBlindAction(action, depend_action_id)
    elif action_type == 57:
        return CountDownAction(action, depend_action_id)
    elif action_type == 58:
        return StopFieldAction(action, depend_action_id)
    elif action_type == 59:
        return InhibitHealAction(action, depend_action_id)
    elif action_type == 60:
        return AttackSealAction(action, depend_action_id)
    elif action_type == 61:
        return FearAction(action, depend_action_id)
    elif action_type == 62:
        return AweAction(action, depend_action_id)
    elif action_type == 63:
        return LoopMotionRepeatAction(action, depend_action_id)
    elif action_type == 69:
        return ToadAction(action, depend_action_id)
    elif action_type == 71:
        return KnightGuardAction(action, depend_action_id)
    elif action_type == 73:
        return LogBarrierAction(action, depend_action_id)
    elif action_type == 74:
        return DivideAction(action, depend_action_id)
    elif action_type == 75:
        return ActionByHitCountAction(action, depend_action_id)
    elif action_type == 76:
        return HealDownAction(action, depend_action_id)
    elif action_type == 77:
        return PassiveSealAction(action, depend_action_id)
    elif action_type == 78:
        return PassiveDamageUpAction(action, depend_action_id)
    elif action_type == 79:
        return DamageByBehaviourAction(action, depend_action_id)
    elif action_type == 83:
        return ChangeSpeedOverlapAction(action, depend_action_id)
    elif action_type == 90:
        return PassiveAction(action, depend_action_id)
    elif action_type == 91:
        return PassiveInermittentAction(action, depend_action_id)
    elif action_type == 92:
        return ChangeEnergyRecoveryRatioByDamageAction(action, depend_action_id)
    elif action_type == 93:
        return IgnoreDecoyAction(action, depend_action_id)
    elif action_type == 94:
        return EffectAction(action, depend_action_id)
    else:
        assert 0
    

def skillAction(skill, cur):
    """ 一个action """
    (skill_id, name, skill_type, skill_area_width, skill_cast_time, description, icon_type, 
        action_1, action_2, action_3, action_4, action_5, action_6, action_7, 
        depend_action_1, depend_action_2, depend_action_3, depend_action_4, depend_action_5, depend_action_6, depend_action_7) = skill
    actions = [action_1, action_2, action_3, action_4, action_5, action_6, action_7]
    depend_actions = [depend_action_1, depend_action_2, depend_action_3, depend_action_4, depend_action_5, depend_action_6, depend_action_7]
    for action, depend_action in zip(actions, depend_actions):
        actionDetail(action, depend_action, cur)
    pass

def skillData(unit_id, cur):
    """ 6位unit_id 
        return [[skill_name, skill_icon, skill_level, skill_cast_time, skill_detail]]
    """
    sql = "SELECT skill_id, name, skill_type, skill_area_width, skill_cast_time, description, icon_type, " + \
        "action_1, action_2, action_3, action_4, action_5, action_6, action_7, " + \
        "depend_action_1, depend_action_2, depend_action_3, depend_action_4, depend_action_5, depend_action_6, depend_action_7 " + \
        "FROM skill_data WHERE substr(skill_id, 1, 4) = '" + \
        str(unit_id)[0:4] + \
        "' ORDER BY skill_id"
    cur.execute(sql)
    skills = cur.fetchall()
    for skill in skills:
        skillAction(skill, cur)