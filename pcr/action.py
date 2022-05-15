from enum import Enum


class ActionType(Enum):
    unknown = 0
    damage = 1
    move = 2
    knock = 3
    heal = 4
    cure = 5
    guard = 6
    chooseArea = 7
    ailment = 8
    dot = 9
    aura = 10
    charm = 11
    blind = 12
    silence = 13
    changeMode = 14
    summon = 15
    changeEnergy = 16
    trigger = 17
    charge = 18
    damageCharge = 19
    taunt = 20
    invulnerable = 21
    changePattern = 22
    ifForChildren = 23
    revival = 24
    continuousAttack = 25
    additive = 26
    multiple = 27
    ifForAll = 28
    changeSearchArea = 29
    instantDeath = 30
    continuousAttackNearby = 31
    enhanceLifeSteal = 32
    enhanceStrikeBack = 33
    accumulativeDamage = 34
    seal = 35
    attackField = 36
    healField = 37
    changeParameterField = 38
    dotField = 39
    ailmentField = 40
    changeUBTime = 41
    loopTrigger = 42
    ifHasTarget = 43
    waveStartIdle = 44
    skillCount = 45
    gravity = 46
    upperLimitAttack = 47
    hot = 48
    dispel = 49
    channel = 50
    division = 51
    changeWidth = 52
    ifExistsFieldForAll = 53
    stealth = 54
    moveParts = 55
    countBlind = 56
    countDown = 57
    stopFieldAction = 58
    inhibitHealAction = 59
    attackSeal = 60
    fear = 61
    awe = 62
    loop = 63
    toad = 69
    knightGuard = 71
    logBarrier = 73
    divide = 74
    actionByHitCount = 75
    healDown = 76
    passiveSeal = 77
    passiveDamageUp = 78
    damageByBehaviourAction = 79
    changeSpeedOverlapAction = 83
    ex = 90
    exPlus = 91
    changeEnergyRecoveryRatioByDamage = 92
    ignoreDecoyAction = 93
    effectAction = 94

""" (class_id, action_type, action_detail_1, action_detail_2, action_detail_3, 
        action_value_1, action_value_2, action_value_3, action_value_4, action_value_5, action_value_6, action_value_7, 
        target_assign, target_area, target_range, target_type, target_number, target_count) = action
"""
def DamageAction(action, depend_action_id):
    pass

def MoveAction(action, depend_action_id):
    pass

def KnockAction(action, depend_action_id):
    pass

def HealAction(action, depend_action_id):
    pass

def CureAction(action, depend_action_id):
    pass

def BarrierAction(action, depend_action_id):
    pass

def ReflexiveAction(action, depend_action_id):
    pass

def AilmentAction(action, depend_action_id):
    pass

def AuraAction(action, depend_action_id):
    pass

def CharmAction(action, depend_action_id):
    pass

def ModeChangeAction(action, depend_action_id):
    pass

def SummonAction(action, depend_action_id):
    pass

def ChangeEnergyAction(action, depend_action_id):
    pass

def TriggerAction(action, depend_action_id):
    pass

def DamageChargeAction(action, depend_action_id):
    pass

def ChargeAction(action, depend_action_id):
    pass

def DecoyAction(action, depend_action_id):
    pass

def NoDamageAction(action, depend_action_id):
    pass

def ChangePatternAction(action, depend_action_id):
    pass

def IfForChildrenAction(action, depend_action_id):
    pass

def RevivalAction(action, depend_action_id):
    pass

def ContinuousAttackAction(action, depend_action_id):
    pass

def AdditiveAction(action, depend_action_id):
    pass

def MultipleAction(action, depend_action_id):
    pass

def IfForAllAction(action, depend_action_id):
    pass

def SearchAreaChangeAction(action, depend_action_id):
    pass

def DestroyAction(action, depend_action_id):
    pass

def ContinuousAttackNearbyAction(action, depend_action_id):
    pass

def EnchantLifeStealAction(action, depend_action_id):
    pass

def EnchantStrikeBackAction(action, depend_action_id):
    pass

def AccumulativeDamageAction(action, depend_action_id):
    pass

def SealAction(action, depend_action_id):
    pass

def AttackFieldAction(action, depend_action_id):
    pass

def HealFieldAction(action, depend_action_id):
    pass

def ChangeParameterFieldAction(action, depend_action_id):
    pass

def AbnormalStateFieldAction(action, depend_action_id):
    pass

def ChangeSpeedFieldAction(action, depend_action_id):
    pass

def UBChangeTimeAction(action, depend_action_id):
    pass

def LoopTriggerAction(action, depend_action_id):
    pass

def IfHasTargetAction(action, depend_action_id):
    pass

def WaveStartIdleAction(action, depend_action_id):
    pass

def SkillExecCountAction(action, depend_action_id):
    pass

def RatioDamageAction(action, depend_action_id):
    pass

def UpperLimitAttackAction(action, depend_action_id):
    pass

def RegenerationAction(action, depend_action_id):
    pass

def DispelAction(action, depend_action_id):
    pass

def ChannelAction(action, depend_action_id):
    pass

def ChangeBodyWidthAction(action, depend_action_id):
    pass

def IFExistsFieldForAllAction(action, depend_action_id):
    pass

def StealthAction(action, depend_action_id):
    pass

def MovePartsAction(action, depend_action_id):
    pass

def CountBlindAction(action, depend_action_id):
    pass

def CountDownAction(action, depend_action_id):
    pass

def StopFieldAction(action, depend_action_id):
    pass

def InhibitHealAction(action, depend_action_id):
    pass

def AttackSealAction(action, depend_action_id):
    pass

def FearAction(action, depend_action_id):
    pass

def AweAction(action, depend_action_id):
    pass

def LoopMotionRepeatAction(action, depend_action_id):
    pass

def ToadAction(action, depend_action_id):
    pass

def KnightGuardAction(action, depend_action_id):
    pass

def LogBarrierAction(action, depend_action_id):
    pass

def DivideAction(action, depend_action_id):
    pass

def ActionByHitCountAction(action, depend_action_id):
    pass

def HealDownAction(action, depend_action_id):
    pass

def PassiveSealAction(action, depend_action_id):
    pass

def PassiveDamageUpAction(action, depend_action_id):
    pass

def DamageByBehaviourAction(action, depend_action_id):
    pass

def ChangeSpeedOverlapAction(action, depend_action_id):
    pass

def PassiveAction(action, depend_action_id):
    pass

def PassiveInermittentAction(action, depend_action_id):
    pass

def ChangeEnergyRecoveryRatioByDamageAction(action, depend_action_id):
    pass

def IgnoreDecoyAction(action, depend_action_id):
    pass

def EffectAction(action, depend_action_id):
    pass