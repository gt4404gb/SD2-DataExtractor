from pyparsing import (Word, alphanums, ParseException, Suppress, Group,Regex,re,Combine,
                       ZeroOrMore, restOfLine, Literal,Dict,SkipTo,StringEnd)
import pandas as pd
#file = open("111.ndf",'r')
file = open("mymod/GameData/Generated/Gameplay/Gfx/UniteCadavreDescriptor.ndf",'r')
test_str = file.read()


# 初始化
identifier = Word(alphanums + "_" + "-")  # 定义标识符
# 符号定义
LPAREN = Literal("(").suppress()
RPAREN = Literal(")").suppress()
LBRACK = Literal("[").suppress()
RBRACK = Literal("]").suppress()
COMMA = Literal(",").suppress()
EQUAL = Literal("=").suppress()
SQUOTE = Literal("'").suppress()


#以export为单位分割字符串
def CutExport(data):
    #将所有export分割
    # 使用SkipTo来跳过模块内容
    module_content = SkipTo("export", include=False) | SkipTo(StringEnd())
    # 主数据定义
    mainData = (Suppress("export") + identifier + Suppress("is") + Suppress(identifier) + module_content)
    # 解析字符串
    try:
        result = mainData.searchString(data)
        return result
    except ParseException as e:
        error_line = data.count('\n', 0, e.loc) + 1
        print(f"Error occurred at line {error_line}: {e}")
        return []

#以注释为单位分割
def CutComment(itemExport):
    GUID = Group("GUID" + ":{" + identifier + "}")
    DescriptorId = Group(identifier + EQUAL + GUID)
    ClassNameForDebug = Suppress(identifier) + EQUAL + SQUOTE + identifier + SQUOTE
    # 使用正则表达式全部匹配直到最后一个')'字符，添加了\s*避免空行的问题
    module_content = Regex(".*(?=\)\s*$)", re.DOTALL)
    # 主数据语法
    moduleData = LPAREN + Suppress(DescriptorId) + ClassNameForDebug + Suppress("Modules") + EQUAL + module_content
    try:
        moduleDict = moduleData.parseString(itemExport[1])
    except ParseException as e:
        error_line = itemExport[1].count('\n', 0, e.loc) + 1
        print(f"Error occurred at line {error_line}: {e}")
        return '',{}

    UniteName = moduleDict[0]
    # 定义注释内容
    comment = Combine(Literal("// ").suppress() + restOfLine).setResultsName("comment")
    # 使用SkipTo来跳过内容直到下一个注释或字符串结束
    content_to_next_comment = SkipTo(comment | StringEnd(), include=False).setResultsName("content")
    # 主数据定义
    mainData = Dict(Group(comment + content_to_next_comment))
    # 解析字符串
    result = mainData.searchString(moduleDict[1])
    result_dict = {}
    for item in result:
        result_dict[item[0][0]] = item[0][1]
    return UniteName, result_dict

#提取单元中的键值
def CutUnite(data):
    # 定义所需的解析元素
    Value = Word(alphanums + "_" + "-" + "'" + "(" + ")" + "*" + " " + "~" + "/" + "." + "$")  # 定义标识符
    pattern = (identifier("key") + EQUAL + Value("value"))
    # 识别所有的为键值的元素
    try:
        results = pattern.searchString(data)
    except ParseException as e:
        error_line = data.count('\n', 0, e.loc) + 1
        print(f"Error occurred at line {error_line}: {e}")
        return {}

    result_dict = {}
    # print(results.dump())
    for item in results:
        if not result_dict.get(item[0]):
            result_dict[item[0]] = item[1]
    return result_dict

def flatten_dict(d, parent_key='', sep='/'):
    """
    Convert nested dictionaries to flat dictionary.
    """
    items = {}
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


if __name__ == "__main__" :

    allExport = CutExport(test_str)
    items = []
    for itemExport in allExport:
        itemName,itemResult = CutComment(itemExport)
        #print(itemName)
        for uniteKey, uniteValue in itemResult.items():
            result_dict = CutUnite(uniteValue)
            itemResult[uniteKey] = result_dict
        #print(itemResult)
        flat_dict = flatten_dict(itemResult)
        items.append([itemName,flat_dict])
    # 创建空的DataFrame
    df = pd.DataFrame()

    # 为每个item填充DataFrame
    for item_name, item_data in items:
        #print(item_data)
        temp_df = pd.DataFrame([item_data], index=[item_name])
        df = pd.concat([df, temp_df], axis=0)
    # 字段名和翻译的字典
    translation_dict = {
        "TypeUnit/Default": "TypeUnit/Default: 默认类型单位",
        "TypeUnit/TypeUnitValue": "TypeUnit/TypeUnitValue: 类型单位值",
        "TypeUnit/Nationalite": "TypeUnit/Nationalite: 国籍",
        "TypeUnit/MotherCountry": "TypeUnit/MotherCountry: 母国",
        "TypeUnit/AcknowUnitType": "TypeUnit/AcknowUnitType: 承认的单位类型",
        "TypeUnit/TypeUnitFormation": "TypeUnit/TypeUnitFormation: 单位编队类型",
        "TypeUnit/Condition": "TypeUnit/Condition: 条件",
        "TypeUnit/ParamId": "TypeUnit/ParamId: 参数标识",
        "TypeUnit/ParamValue": "TypeUnit/ParamValue: 参数值",
        "TypeUnit/Descriptor": "TypeUnit/Descriptor: 描述",
        "Position/Default": "Position/Default: 默认位置",
        "Position/StickToGround": "Position/StickToGround: 粘附地面",
        "Position/InGeoDb": "Position/InGeoDb: 在地理数据库中",
        "Position/PorteurMustBeVisible": "Position/PorteurMustBeVisible: 携带者必须可见",
        "Position/MustUpdateZoneIndice": "Position/MustUpdateZoneIndice: 必须更新区域指数",
        "Position/ClampInWorld": "Position/ClampInWorld: 在世界中夹紧",
        "Position/ClampOutMap": "Position/ClampOutMap: 夹紧地图外",
        "Position/HasNearlyNullBBox": "Position/HasNearlyNullBBox: 具有几乎为零的包围盒",
        "Position/GfxDescriptorPorteur": "Position/GfxDescriptorPorteur: 图形描述携带者",
        "Position/Radius": "Position/Radius: 半径",
        "Position/RelativeScanningPosition": "Position/RelativeScanningPosition: 相对扫描位置",
        "Position/CameraFollower": "Position/CameraFollower: 相机跟随者",
        "Position/LowAltitudeFlyingAltitude": "Position/LowAltitudeFlyingAltitude: 低空飞行高度",
        "Position/NearGroundFlyingAltitude": "Position/NearGroundFlyingAltitude: 接近地面飞行高度",
        "Position/Condition": "Position/Condition: 条件",
        "Position/ParamValue": "Position/ParamValue: 参数值",
        "Position/Descriptor": "Position/Descriptor: 描述",
        "Inflammable/Default": "Inflammable/Default: 默认易燃性",
        "Experience/Default": "Experience/Default: 默认经验",
        "Experience/ExperienceLevelsPackDescriptor": "Experience/ExperienceLevelsPackDescriptor: 经验等级包描述",
        "Experience/CanWinExperience": "Experience/CanWinExperience: 可以赢得经验",
        "Experience/ExperienceGainBySecond": "Experience/ExperienceGainBySecond: 每秒经验获取",
        "Experience/KillExperienceBonus": "Experience/KillExperienceBonus: 击杀经验奖励",
        "Visibility/Default": "Visibility/Default: 默认可见性",
        "Visibility/AutoRevealType": "Visibility/AutoRevealType: 自动显示类型",
        "Visibility/UnitConcealmentBonus": "Visibility/UnitConcealmentBonus: 单位隐蔽奖励",
        "Visibility/VisionUnitType": "Visibility/VisionUnitType: 视觉单位类型",
        "Visibility/AlwaysComputeLoS": "Visibility/AlwaysComputeLoS: 始终计算视线",
        "Visibility/UnitIsStealth": "Visibility/UnitIsStealth: 单位隐身",
        "Visibility/HideFromDebug": "Visibility/HideFromDebug: 隐藏调试信息",
        "Visibility/VisionObstructionType": "Visibility/VisionObstructionType: 视觉遮挡类型",
        "Visibility/GroundDissimulationModifierType": "Visibility/GroundDissimulationModifierType: 地面伪装修改类型",
        "ApparenceModel/AllowMissingGameplayBBoxBone": "ApparenceModel/AllowMissingGameplayBBoxBone: 允许缺少的游戏包围盒骨骼",
        "ApparenceModel/Scale": "ApparenceModel/Scale: 缩放",
        "ApparenceModel/PickableObject": "ApparenceModel/PickableObject: 可拾取物体",
        "ApparenceModel/Depiction": "ApparenceModel/Depiction: 描述",
        "ApparenceModel/GameplayBBoxBoneName": "ApparenceModel/GameplayBBoxBoneName: 游戏包围盒骨骼名称",
        "ApparenceModel/IsBaseOnModelCenter": "ApparenceModel/IsBaseOnModelCenter: 基于模型中心",
        "Cover/Default": "Cover/Default: 默认掩体",
        "Cover/DefaultAutoCoverBehavior": "Cover/DefaultAutoCoverBehavior: 默认自动掩体行为",
        "Cover/AutoCoverRange": "Cover/AutoCoverRange: 自动掩体范围",
        "Cover/OccupationRadius": "Cover/OccupationRadius: 占领半径",
        "Cover/TerrainListMask": "Cover/TerrainListMask: 地形列表掩码",
        "Cover/UseTerrainsForEscape": "Cover/UseTerrainsForEscape: 使用地形逃生",
        "WeaponManager/Default": "WeaponManager/Default: 默认武器管理器",
        "Damage/Default": "Damage/Default: 默认伤害",
        "Damage/CommonDamageDescriptor": "Damage/CommonDamageDescriptor: 通用伤害描述",
        "Damage/SuppressDamagesRegenRatio": "Damage/SuppressDamagesRegenRatio: 抑制伤害再生比例",
        "Damage/SuppressDamagesRegenRatioOutOfRange": "Damage/SuppressDamagesRegenRatioOutOfRange: 抑制伤害再生比例超出范围",
        "Damage/StunDamagesRegen": "Damage/StunDamagesRegen: 震晕伤害再生",
        "Damage/StunDamagesToGetStunned": "Damage/StunDamagesToGetStunned: 震晕伤害造成眩晕",
        "Damage/StunFreezesUnits": "Damage/StunFreezesUnits: 震晕冻结单位",
        "Damage/BlindageProperties": "Damage/BlindageProperties: 装甲属性",
        "Damage/ArmorDescriptorFront": "Damage/ArmorDescriptorFront: 正面装甲描述",
        "Damage/ArmorDescriptorSides": "Damage/ArmorDescriptorSides: 侧面装甲描述",
        "Damage/ArmorDescriptorRear": "Damage/ArmorDescriptorRear: 后方装甲描述",
        "Damage/ArmorDescriptorTop": "Damage/ArmorDescriptorTop: 顶部装甲描述",
        "Damage/MaxSuppressionDamages": "Damage/MaxSuppressionDamages: 最大压制伤害",
        "Damage/MaxDamages": "Damage/MaxDamages: 最大伤害",
        "Damage/HitRollSize": "Damage/HitRollSize: 命中滚动大小",
        "Damage/HitRollECM": "Damage/HitRollECM: 命中滚动电子对抗措施",
        "Damage/MaxHPForHUD": "Damage/MaxHPForHUD: HUD最大生命值",
        "Damage/AutoOrientation": "Damage/AutoOrientation: 自动方向",
        "Damage/IsTargetableAsBoat": "Damage/IsTargetableAsBoat: 作为船只可被选中",
        "Damage/IsTargetableOutsideCenter": "Damage/IsTargetableOutsideCenter: 在中心之外可被选中",
        "Damage/SkipCadavreCreation": "Damage/SkipCadavreCreation: 跳过尸体创建",
        "Damage/FxDoImpactOnUnit": "Damage/FxDoImpactOnUnit: 在单位上进行撞击效果",
        "Damage/UseDamageMultiplierForFirePower": "Damage/UseDamageMultiplierForFirePower: 使用伤害乘数计算火力",
        "Damage/UseTopArmorAgainstFire": "Damage/UseTopArmorAgainstFire: 对抗火攻时使用顶部装甲",
        "Damage/PhysicalDamageLevelsPack": "Damage/PhysicalDamageLevelsPack: 物理伤害等级包",
        "Damage/SuppressDamageLevelsPack": "Damage/SuppressDamageLevelsPack: 抑制伤害等级包",
        "Damage/TypeForGroundDamageModifier": "Damage/TypeForGroundDamageModifier: 地面伤害修正类型",
        "Dangerousness/Dangerousness": "Dangerousness/Dangerousness: 危险性",
        "Rout/Default": "Rout/Default: 默认溃退",
        "Rout/MoralLevel": "Rout/MoralLevel: 士气等级",
        "LandMovement/Default": "LandMovement/Default: 默认陆地移动",
        "LandMovement/UnitMovingType": "LandMovement/UnitMovingType: 单位移动类型",
        "LandMovement/PathfindType": "LandMovement/PathfindType: 寻路类型",
        "LandMovement/PreferredLayerMask": "LandMovement/PreferredLayerMask: 首选图层掩码",
        "LandMovement/Maxspeed": "LandMovement/Maxspeed: 最大速度",
        "LandMovement/VitesseCombat": "LandMovement/VitesseCombat: 战斗速度",
        "LandMovement/SpeedFakefactorType": "LandMovement/SpeedFakefactorType: 速度虚拟因子类型",
        "LandMovement/SpeedBonusOnRoad": "LandMovement/SpeedBonusOnRoad: 路上速度奖励",
        "LandMovement/MaxAcceleration": "LandMovement/MaxAcceleration: 最大加速度",
        "LandMovement/MaxDeceleration": "LandMovement/MaxDeceleration: 最大减速度",
        "LandMovement/TempsDemiTour": "LandMovement/TempsDemiTour: 半轮转时间",
        "LandMovement/VehicleSubType": "LandMovement/VehicleSubType: 车辆子类型",
        "LandMovement/CriticalEffectModule": "LandMovement/CriticalEffectModule: 关键效果模块",
        "LandMovement/StartTime": "LandMovement/StartTime: 开始时间",
        "LandMovement/StopTime": "LandMovement/StopTime: 停止时间",
        "LandMovement/RotationStartTime": "LandMovement/RotationStartTime: 旋转开始时间",
        "LandMovement/RotationStopTime": "LandMovement/RotationStopTime: 旋转停止时间",
        "ScannerConfiguration/Default": "ScannerConfiguration/Default: 默认扫描配置",
        "ScannerConfiguration/OpticsAltitudeConfig": "ScannerConfiguration/OpticsAltitudeConfig: 光学高度配置",
        "ScannerConfiguration/DoesNotCountInScannerAbsoluteMaxRange": "ScannerConfiguration/DoesNotCountInScannerAbsoluteMaxRange: 不计入扫描绝对最大范围",
        "ScannerConfiguration/PorteeVisionTBA": "ScannerConfiguration/PorteeVisionTBA: 视野范围TBA",
        "ScannerConfiguration/PorteeVisionFOW": "ScannerConfiguration/PorteeVisionFOW: 视野范围FOW",
        "ScannerConfiguration/DetectionTBA": "ScannerConfiguration/DetectionTBA: 检测TBA",
        "ScannerConfiguration/PorteeVision": "ScannerConfiguration/PorteeVision: 视野范围",
        "ScannerConfiguration/PorteeIdentification": "ScannerConfiguration/PorteeIdentification: 识别范围",
        "ScannerConfiguration/OpticalStrength": "ScannerConfiguration/OpticalStrength: 光学强度",
        "ScannerConfiguration/OpticalStrengthAltitude": "ScannerConfiguration/OpticalStrengthAltitude: 光学强度高度",
        "ScannerConfiguration/UnitDetectStealthUnit": "ScannerConfiguration/UnitDetectStealthUnit: 单位检测隐形单位",
        "ScannerConfiguration/SpecializedDetections": "ScannerConfiguration/SpecializedDetections: 专门检测",
        "ScannerConfiguration/SpecializedOpticalStrengths": "ScannerConfiguration/SpecializedOpticalStrengths: 专门光学强度",
        "ScannerConfiguration/IgnoreObstacles": "ScannerConfiguration/IgnoreObstacles: 忽略障碍物",
        "Scanner/Default": "Scanner/Default: 默认扫描器",
        "Scanner/VisibilityRollRule": "Scanner/VisibilityRollRule: 可见性掷骰规则",
        "Scanner/IdentifyBaseProbability": "Scanner/IdentifyBaseProbability: 基本识别概率",
        "Scanner/TimeBetweenEachIdentifyRoll": "Scanner/TimeBetweenEachIdentifyRoll: 每次识别掷骰之间的时间",
        "Scanner/VisibilityRuleDescriptor": "Scanner/VisibilityRuleDescriptor: 可见性规则描述",
        "Scanner/DistanceMultiplierRule": "Scanner/DistanceMultiplierRule: 距离乘数规则",
        "Scanner/MultiplicateurAPorteeMaximale": "Scanner/MultiplicateurAPorteeMaximale: 最大范围乘数",
        "Scanner/MultiplicateurAPorteeMinimale": "Scanner/MultiplicateurAPorteeMinimale: 最小范围乘数",
        "Scanner/Exposant": "Scanner/Exposant: 指数",
        "Scanner/MultiplicateurAPorteeMaximaleEnMouvement": "Scanner/MultiplicateurAPorteeMaximaleEnMouvement: 移动中的最大范围乘数",
        "Scanner/MultiplicateurAPorteeMinimaleEnMouvement": "Scanner/MultiplicateurAPorteeMinimaleEnMouvement: 移动中的最小范围乘数",
        "Scanner/ExposantEnMouvement": "Scanner/ExposantEnMouvement: 移动指数",
        "Transportable/Default": "Transportable/Default: 默认可运输",
        "Transportable/NbSeatsOccupied": "Transportable/NbSeatsOccupied: 被占用座位数",
        "Transportable/TimeToLoad": "Transportable/TimeToLoad: 装载时间",
        "Transportable/IsTowable": "Transportable/IsTowable: 可拖曳",
        "Transportable/SuppressDamageRatioIfTransporterKilled": "Transportable/SuppressDamageRatioIfTransporterKilled: 如果运输者被击毁则抑制伤害比例",
        "GhostModule/Default": "GhostModule/Default: 默认幽灵模块",
        "GhostModule/Condition": "GhostModule/Condition: 条件",
        "GhostModule/ParamValue": "GhostModule/ParamValue: 参数值",
        "GhostModule/Descriptor": "GhostModule/Descriptor: 描述",
        "CommandManager/Default": "CommandManager/Default: 默认指挥官管理器",
        "CommandManager/DeploymentDuration": "CommandManager/DeploymentDuration: 部署持续时间",
        "CommandManager/WithdrawalDuration": "CommandManager/WithdrawalDuration: 撤退持续时间",
        "CommandManager/GiveMoraleBonusToSurroundingUnits": "CommandManager/GiveMoraleBonusToSurroundingUnits: 给予周围单位士气奖励",
        "CadavreGenerator/Default": "CadavreGenerator/Default: 默认尸体生成器",
        "CadavreGenerator/CadavreDescriptor": "CadavreGenerator/CadavreDescriptor: 尸体描述",
        "IAStrat/Default": "IAStrat/Default: 默认IAStrat",
        "IAStrat/DatabaseId": "IAStrat/DatabaseId: 数据库ID",
        "IAStrat/GameplayBehavior": "IAStrat/GameplayBehavior: 游戏行为",
        "StateEngineCompany/Default": "StateEngineCompany/Default: 默认公司状态引擎",
        "StateEngineCompany/InitialStateId": "StateEngineCompany/InitialStateId: 初始状态ID",
        "StateEngineCompany/StateEngineUpdateMode": "StateEngineCompany/StateEngineUpdateMode: 状态引擎更新模式",
        "StateEngine/Default": "StateEngine/Default: 默认状态引擎",
        "StateEngine/InitialStateId": "StateEngine/InitialStateId: 初始状态ID",
        "StateEngine/StateEngineUpdateMode": "StateEngine/StateEngineUpdateMode: 状态引擎更新模式",
        "Capacite/Default": "Capacite/Default: 默认能力",
        "Capacite/PostOrderSkillList": "Capacite/PostOrderSkillList: 后序技能列表",
        "Production/Default": "Production/Default: 默认生产",
        "Production/Factory": "Production/Factory: 工厂",
        "Production/ProductionYear": "Production/ProductionYear: 生产年份",
        "Production/ProductionTime": "Production/ProductionTime: 生产时间",
        "Production/DownPayment": "Production/DownPayment: 首付款",
        "Production/ProductionRessourcesNeeded": "Production/ProductionRessourcesNeeded: 生产所需资源",
        "Production/RaiseDynamicTagAtSpawn": "Production/RaiseDynamicTagAtSpawn: 在生成时提高动态标签",
        "CubeAction/Default": "CubeAction/Default: 默认立方体动作",
        "CubeAction/CubeActionDescriptor": "CubeAction/CubeActionDescriptor: 立方体动作描述",
        "MinimapDisplay/Default": "MinimapDisplay/Default: 默认小地图显示",
        "MinimapDisplay/Texture": "MinimapDisplay/Texture: 纹理",
        "MinimapDisplay/GhostTexture": "MinimapDisplay/GhostTexture: 幽灵纹理",
        "MinimapDisplay/IsAlwaysVisible": "MinimapDisplay/IsAlwaysVisible: 始终可见",
        "MinimapDisplay/UseTeamColor": "MinimapDisplay/UseTeamColor: 使用队伍颜色",
        "MinimapDisplay/FollowUnitOrientation": "MinimapDisplay/FollowUnitOrientation: 跟随单位方向",
        "Orderable/Default": "Orderable/Default: 默认可订购",
        "Orderable/CanHoldPosition": "Orderable/CanHoldPosition: 可以保持位置",
        "Orderable/CanMove": "Orderable/CanMove: 可以移动",
        "Orderable/CanBeHarvested": "Orderable/CanBeHarvested: 可以被收获",
        "Orderable/CanHarvest": "Orderable/CanHarvest: 可以收获",
        "Orderable/CanChangeTransferTarget": "Orderable/CanChangeTransferTarget: 可以改变转移目标",
        "Orderable/CanSell": "Orderable/CanSell: 可以出售",
        "Orderable/CanBuild": "Orderable/CanBuild: 可以建造",
        "Orderable/CanAttack": "Orderable/CanAttack: 可以攻击",
        "Orderable/CanStop": "Orderable/CanStop: 可以停止",
        "Orderable/CanFollowFormation": "Orderable/CanFollowFormation: 可以跟随编队",
        "Orderable/CanShoot": "Orderable/CanShoot: 可以射击",
        "Orderable/CanMerge": "Orderable/CanMerge: 可以合并",
        "Orderable/CanUnloadFromTransport": "Orderable/CanUnloadFromTransport: 可以从运输中卸载",
        "Orderable/CanLand": "Orderable/CanLand: 可以着陆",
        "Orderable/CanGoUp": "Orderable/CanGoUp: 可以上升",
        "Orderable/CanGoDown": "Orderable/CanGoDown: 可以下降",
        "Orderable/CanMoveAndAttack": "Orderable/CanMoveAndAttack: 可以移动并攻击",
        "Orderable/CanSpread": "Orderable/CanSpread: 可以扩散",
        "Orderable/CanReverse": "Orderable/CanReverse: 可以倒退",
        "Orderable/CanSupplyUnit": "Orderable/CanSupplyUnit: 可以补给单位",
        "Orderable/CanAskForSupply": "Orderable/CanAskForSupply: 可以请求补给",
        "Orderable/CanGoGetSupply": "Orderable/CanGoGetSupply: 可以前往获取补给",
        "Orderable/CanEnterDistrict": "Orderable/CanEnterDistrict: 可以进入区域",
        "Orderable/CanAirplanePatrol": "Orderable/CanAirplanePatrol: 可以进行飞机巡逻",
        "Orderable/CanAirplaneAttack": "Orderable/CanAirplaneAttack: 可以进行飞机攻击",
        "Orderable/CanLoadIntoTransport": "Orderable/CanLoadIntoTransport: 可以装载到运输工具中",
        "Orderable/CanLoadUnit": "Orderable/CanLoadUnit: 可以装载单位",
        "Orderable/CanAirplaneTakeOff": "Orderable/CanAirplaneTakeOff: 可以进行飞机起飞",
        "Orderable/CanAirplaneEvacuate": "Orderable/CanAirplaneEvacuate: 可以进行飞机撤离",
        "Orderable/CanRefuelAirplane": "Orderable/CanRefuelAirplane: 可以为飞机加油",
        "Orderable/CanRepairAirplane": "Orderable/CanRepairAirplane: 可以修理飞机",
        "Orderable/CanRearmAirplane": "Orderable/CanRearmAirplane: 可以给飞机重新装弹",
        "Orderable/CanAirplaneShoot": "Orderable/CanAirplaneShoot: 可以进行飞机射击",
        "Orderable/CanBombard": "Orderable/CanBombard: 可以进行轰炸",
        "Orderable/CanFortify": "Orderable/CanFortify: 可以设防",
        "Orderable/CanFortifyAntiAir": "Orderable/CanFortifyAntiAir: 可以设防防空",
        "Orderable/CanAIDefend": "Orderable/CanAIDefend: 可以进行AI防御",
        "Orderable/CanAIAiplaneAutoManage": "Orderable/CanAIAiplaneAutoManage: 可以进行AI飞机自动管理",
        "Orderable/CanAIAttack": "Orderable/CanAIAttack: 可以进行AI攻击",
        "Orderable/CanAIManageArtillery": "Orderable/CanAIManageArtillery: 可以进行AI火炮管理",
        "Orderable/CanAIStop": "Orderable/CanAIStop: 可以进行AI停止",
        "Orderable/CanSmartHoldFire": "Orderable/CanSmartHoldFire: 可以智能保持射击",
        "Label/Default": "Label/Default: 默认标签",
        "Label/IsAltitudeDependent": "Label/IsAltitudeDependent: 高度相关",
        "Label/IsBuilding": "Label/IsBuilding: 是建筑物",
        "Label/IsTransporter": "Label/IsTransporter: 是运输工具",
        "Label/MultiSelectionSortingOrder": "Label/MultiSelectionSortingOrder: 多重选择排序顺序",
        "Label/IsCommandementUnit": "Label/IsCommandementUnit: 是指挥单位",
        "Label/IsPlane": "Label/IsPlane: 是飞机",
        "Label/UnitName": "Label/UnitName: 单位名称",
        "Label/HintToken": "Label/HintToken: 提示标记",
        "Label/IdentifiedTexture": "Label/IdentifiedTexture: 已识别纹理",
        "Label/CommandNameTrigger": "Label/CommandNameTrigger: 指令名称触发器",
        "Label/Alterator": "Label/Alterator: 改变器",
        "Label/SpecialtyHintTitleToken": "Label/SpecialtyHintTitleToken: 特殊提示标题标记",
        "Label/SpecialtyHintBodyToken": "Label/SpecialtyHintBodyToken: 特殊提示正文标记",
        "Label/SpecialtyHintExtendedToken": "Label/SpecialtyHintExtendedToken: 扩展特殊提示标记",
        "Label/UnidentifiedTexture": "Label/UnidentifiedTexture: 未识别纹理",
        "Label/PositionHeightOffset": "Label/PositionHeightOffset: 位置高度偏移",
        "Label/APValue": "Label/APValue: 护甲值",
        "Label/APValueBazooka": "Label/APValueBazooka: 火箭筒护甲值",
        "Label/NbSoldiers": "Label/NbSoldiers: 士兵数量",
        "Label/IsParachutist": "Label/IsParachutist: 是伞兵",
        "LinkToDistrict/Default": "LinkToDistrict/Default: 默认链接到区域",
        "LinkToDistrict/DefaultOrderOnDistrict": "LinkToDistrict/DefaultOrderOnDistrict: 区域上的默认顺序",
        "LinkToDistrict/SpaceOccupied": "LinkToDistrict/SpaceOccupied: 占用空间",
        "StrategicData/Default": "StrategicData/Default: 默认战略数据",
        "StrategicData/UnitPowerValues": "StrategicData/UnitPowerValues: 单位战斗力值",
        "StrategicData/IsSupportUnit": "StrategicData/IsSupportUnit: 是支援单位",
        "UnitUI/Default": "UnitUI/Default: 默认单位界面",
        "UnitUI/HintToken": "UnitUI/HintToken: 提示标记",
        "UnitUI/NameToken": "UnitUI/NameToken: 名称标记",
        "UnitUI/InfoPanelConfigurationToken": "UnitUI/InfoPanelConfigurationToken: 信息面板配置标记",
        "UnitUI/TypeSpecificToken": "UnitUI/TypeSpecificToken: 特定类型标记",
        "UnitUI/RealRoadSpeed": "UnitUI/RealRoadSpeed: 实际路速",
        "UnitUI/ShowInMenu": "UnitUI/ShowInMenu: 在菜单中显示",
        "UnitUI/IsAce": "UnitUI/IsAce: 是王牌",
        "UnitUI/GenerateName": "UnitUI/GenerateName: 生成名称",
        "UnitUI/TopViewTexture": "UnitUI/TopViewTexture: 俯视图纹理",
        "UnitUI/MenuIconTexture": "UnitUI/MenuIconTexture: 菜单图标纹理",
        "UnitUI/ButtonTexture": "UnitUI/ButtonTexture: 按钮纹理",
        "UnitUI/CountryTexture": "UnitUI/CountryTexture: 国家纹理",
        "UnitUI/TypeStrategicCount": "UnitUI/TypeStrategicCount: 战略类型计数",
        "UnitUI/Condition": "UnitUI/Condition: 条件",
        "UnitUI/ParamId": "UnitUI/ParamId: 参数标识",
        "UnitUI/ParamValue": "UnitUI/ParamValue: 参数值",
        "UnitUI/Descriptor": "UnitUI/Descriptor: 描述",
        "Critical/Module": "Critical/Module: 关键模块",
        "Label/PlatingValue": "Label/PlatingValue: 装甲值",
        "Commander/Default": "Commander/Default: 默认指挥官",
        "Commander/CommanderLevel": "Commander/CommanderLevel: 指挥官等级",
        "GroupeCombat/Default": "GroupeCombat/Default: 默认作战组",
        "GroupeCombat/BehaviourDescriptor": "GroupeCombat/BehaviourDescriptor: 行为描述",
        "GroupeCombat/NbSoldatInGroupeCombat": "GroupeCombat/NbSoldatInGroupeCombat: 作战组中的士兵数量",
        "GroupeCombat/Dispersion": "GroupeCombat/Dispersion: 分散",
        "GroupeCombat/CircleFormation": "GroupeCombat/CircleFormation: 圆形编队",
        "GroupeCombat/IsSapery": "GroupeCombat/IsSapery: 是工兵",
        "GroupeCombat/GfxWeaponModels": "GroupeCombat/GfxWeaponModels: 武器模型",
        "GroupeCombat/GfxPorteur": "GroupeCombat/GfxPorteur: 携带者图形",
        "GroupeCombat/GfxPorteurGhost": "GroupeCombat/GfxPorteurGhost: 幽灵携带者图形",
        "GroupeCombat/BoundingBoxSize": "GroupeCombat/BoundingBoxSize: 包围盒大小",
        "GroupeCombat/Scale": "GroupeCombat/Scale: 缩放",
        "Observer/Default": "Observer/Default: 默认观察者",
        "Observer/Radius": "Observer/Radius: 半径",
        "Observer/ArtilleryToSpawn": "Observer/ArtilleryToSpawn: 要生成的火炮",
        "Transporter/Default": "Transporter/Default: 默认运输工具",
        "Transporter/NbSeatsAvailable": "Transporter/NbSeatsAvailable: 可用座位数量",
        "Transporter/WreckUnloadPhysicalDamageBonus": "Transporter/WreckUnloadPhysicalDamageBonus: 残骸卸载物理伤害奖励",
        "Transporter/WreckUnloadSuppressDamageBonus": "Transporter/WreckUnloadSuppressDamageBonus: 残骸卸载抑制伤害奖励",
        "Transporter/WreckUnloadStunDamageBonus": "Transporter/WreckUnloadStunDamageBonus: 残骸卸载震晕伤害奖励",
        "Transporter/LoadRadius": "Transporter/LoadRadius: 装载半径",
        "TypeUnit/Key": "TypeUnit/Key: 单位类型键",
        "TypeUnit/AceUnitType": "TypeUnit/AceUnitType: 王牌单位类型",
        "UnitUI/FixedName": "UnitUI/FixedName: 固定名称",
        "Supply/Default": "Supply/Default: 默认补给",
        "Supply/SupplyDescriptor": "Supply/SupplyDescriptor: 补给描述",
        "Supply/SupplyCapacity": "Supply/SupplyCapacity: 补给容量",
        "Supply/DeploymentDuration": "Supply/DeploymentDuration: 部署持续时间",
        "Supply/WithdrawalDuration": "Supply/WithdrawalDuration: 撤退持续时间",
        "Supply/SupplyPriority": "Supply/SupplyPriority: 补给优先级",
        "Label/IsSupply": "Label/IsSupply: 是补给",
        "AirplaneMovement/Default": "AirplaneMovement/Default: 默认飞机移动",
        "AirplaneMovement/Altitude": "AirplaneMovement/Altitude: 高度",
        "AirplaneMovement/AltitudeMax": "AirplaneMovement/AltitudeMax: 最大高度",
        "AirplaneMovement/AltitudeMin": "AirplaneMovement/AltitudeMin: 最小高度",
        "AirplaneMovement/AltitudeMinForRoll": "AirplaneMovement/AltitudeMinForRoll: 滚动的最小高度",
        "AirplaneMovement/MinRollSpeedForRoll": "AirplaneMovement/MinRollSpeedForRoll: 滚动的最小速度",
        "AirplaneMovement/Speed": "AirplaneMovement/Speed: 速度",
        "AirplaneMovement/AgilityRadius": "AirplaneMovement/AgilityRadius: 敏捷半径",
        "AirplaneMovement/PitchAngle": "AirplaneMovement/PitchAngle: 俯仰角度",
        "AirplaneMovement/PitchSpeed": "AirplaneMovement/PitchSpeed: 俯仰速度",
        "AirplaneMovement/RollAngle": "AirplaneMovement/RollAngle: 滚转角度",
        "AirplaneMovement/RollSpeed": "AirplaneMovement/RollSpeed:滚转速度",
        "AirplaneMovement/EvacAngle": "AirplaneMovement/EvacAngle: 撤离角度",
        "AirplaneMovement/FollowGround": "AirplaneMovement/FollowGround: 跟随地面",
        "AirplaneMovement/IgnoreBattlefieldOrders": "AirplaneMovement/IgnoreBattlefieldOrders: 忽略战场指令",
        "AirplaneMovement/EvacuateOnTargetReached": "AirplaneMovement/EvacuateOnTargetReached: 在到达目标时撤离",
        "AirplaneMovement/EvacToStartingPoint": "AirplaneMovement/EvacToStartingPoint: 撤离到起始点",
        "AirplaneMovement/ElevatorRotationMax": "AirplaneMovement/ElevatorRotationMax: 升降舵最大旋转",
        "AirplaneMovement/AileronRotationMax": "AirplaneMovement/AileronRotationMax: 副翼最大旋转",
        "AirplaneMovement/RudderRotationMax": "AirplaneMovement/RudderRotationMax: 方向舵最大旋转",
        "AirplaneMovement/MinPitchForDive": "AirplaneMovement/MinPitchForDive: 俯冲的最小俯仰",
        "AirplaneMovement/PitchForDive": "AirplaneMovement/PitchForDive: 俯冲的俯仰",
        "AirplaneMovement/MaxPitchForDive": "AirplaneMovement/MaxPitchForDive: 俯冲的最大俯仰",
        "Fuel/Default": "Fuel/Default: 默认燃料",
        "Fuel/FuelCapacity": "Fuel/FuelCapacity: 燃料容量",
        "Fuel/FuelMoveDuration": "Fuel/FuelMoveDuration: 移动燃料持续时间",
        "Flare/DistanceActivation": "Flare/DistanceActivation: 激活距离",
        "Flare/TimeBetweenFlare": "Flare/TimeBetweenFlare: 路过信号弹的时间",
        "Flare/MinimalTimeBetweenFlare": "Flare/MinimalTimeBetweenFlare: 最小路过信号弹时间",
        "Flare/BonusTimeBetweenFlareByProjectile": "Flare/BonusTimeBetweenFlareByProjectile: 通过弹道的额外信号弹时间",
        "Flare/SweepAngle": "Flare/SweepAngle: 扫描角度",
        "Airplane/EvacuationTime": "Airplane/EvacuationTime: 撤离时间",
        "Airplane/TravelDuration": "Airplane/TravelDuration: 飞行时间",
        "AirplaneMovement/BaseAirplaneMovementModuleDescriptor": "AirplaneMovement/BaseAirplaneMovementModuleDescriptor: 基础飞机移动模块描述",
        "MissileCarriage/Connoisseur": "MissileCarriage/Connoisseur: 导弹专家",
        "AirplaneMovement/MinDistanceBetweenFighterAndTargetForAttackOnSlowAirplaneStrategy": "AirplaneMovement/MinDistanceBetweenFighterAndTargetForAttackOnSlowAirplaneStrategy: 慢速飞机策略中战斗机和目标之间的最小距离",
        "AirplaneMovement/MaxDistanceBetweenFighterAndTargetForLateralMoveOnSlowAirplaneStrategy": "AirplaneMovement/MaxDistanceBetweenFighterAndTargetForLateralMoveOnSlowAirplaneStrategy: 慢速飞机策略中战斗机和目标之间的最大距离",
        "AirplaneMovement/SpeedRatioForAttackOnSlowAirplaneStrategy": "AirplaneMovement/SpeedRatioForAttackOnSlowAirplaneStrategy: 慢速飞机策略中攻击的速度比率",
        "AirplaneMovement/SpeedRatioForAttackOnVerySlowAirplaneStrategy": "AirplaneMovement/SpeedRatioForAttackOnVerySlowAirplaneStrategy: 非常慢速飞机策略中攻击的速度比率",
        "AirplaneMovement/MaxAngleDifferenceWithTarget": "AirplaneMovement/MaxAngleDifferenceWithTarget: 与目标的最大角度差",
        "AirplaneMovement/MaxAngleToConsiderTargetAhead": "AirplaneMovement/MaxAngleToConsiderTargetAhead: 考虑目标在前方的最大角度",
        "AirplaneMovement/AngleToFakeTargetPosition": "AirplaneMovement/AngleToFakeTargetPosition: 伪造目标位置的角度",
        "AutomaticBehavior/Default": "AutomaticBehavior/Default: 默认自动行为",
        "AutomaticBehavior/CanAssist": "AutomaticBehavior/CanAssist: 可以协助",
        "AutomaticBehavior/AssistRequestBroadcastRadius": "AutomaticBehavior/AssistRequestBroadcastRadius: 协助请求广播半径",
        "AutomaticBehavior/DistanceToFlee": "AutomaticBehavior/DistanceToFlee: 逃跑距离",
        "AutomaticBehavior/MaxDistanceForOffensiveReaction": "AutomaticBehavior/MaxDistanceForOffensiveReaction: 进攻反应的最大距离",
        "AutomaticBehavior/MaxDistanceForOffensiveReactionOnFlyingTarget": "AutomaticBehavior/MaxDistanceForOffensiveReactionOnFlyingTarget: 对飞行目标的进攻反应的最大距离",
        "AutomaticBehavior/MaxDistanceForEngagement": "AutomaticBehavior/MaxDistanceForEngagement: 参与的最大距离",
        "AutomaticBehavior/ApproachTargetEvenIfUndamageable": "AutomaticBehavior/ApproachTargetEvenIfUndamageable: 即使无法受损也接近目标",
        "AirplaneMovement/MinPitchForDiveBomb": "AirplaneMovement/MinPitchForDiveBomb: 俯冲轰炸的最小俯仰",
        "AirplaneMovement/PitchForDiveBomb": "AirplaneMovement/PitchForDiveBomb: 俯冲轰炸的俯仰",
        "AirplaneMovement/MaxPitchForDiveBomb": "AirplaneMovement/MaxPitchForDiveBomb: 俯冲轰炸的最大俯仰",
        "AirplaneMovement/DiveBombRecoveryDuration": "AirplaneMovement/DiveBombRecoveryDuration: 俯冲轰炸恢复持续时间",
        "AirplaneMovement/DistanceNosedive": "AirplaneMovement/DistanceNosedive: 俯冲距离",
        "AirplaneMovement/WaypointDistanceFromTarget": "AirplaneMovement/WaypointDistanceFromTarget: 路点距离目标的距离",
        "AirplaneMovement/AgilityMultiplicator": "AirplaneMovement/AgilityMultiplicator: 敏捷性乘数"
    }
    # 将字段名替换为中文
    df = df.rename(columns=translation_dict)
    # 保存DataFrame到CSV
    df.to_csv('UniteCadavreDescriptor.csv')