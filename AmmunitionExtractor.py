import pandas as pd
import re
file = open("mymod/GameData/Generated/Gameplay/Gfx/Ammunition.ndf",'r')
data = file.readlines()

lines = [i for i in data if i != '\n']

# 正则表达式模式
pattern = re.compile(r'(\w+)\s*=\s*(.*)')
export_pattern = re.compile(r'export\s+(\w+)\s+is')
list_pattern = re.compile(r'\[\s*([\w\s\./,]+)\s*\]')

parsed_data = []

current_record = {}
in_nested_mode = False
list_mode = False
list_key = None
for line in lines:
    stripped_line = line.strip()

    # 在解析模式中检查是否进入列表模式
    if "[" in stripped_line:
        list_mode = True
        list_data = []
        list_key = stripped_line.split('=')[0].strip()
        continue

    # 在列表模式中处理数据
    if list_mode:
        if "]" in stripped_line:
            list_mode = False
            current_record[list_key] = list_data
            list_data = []
            list_key = None
            continue
        else:
            list_data.extend([item.strip() for item in stripped_line.split(",") if item.strip()])
            continue

    # 检查是否进入嵌套模式
    if "= TDiceHitRollRuleDescriptor" in stripped_line:
        in_nested_mode = True
        nested_key = stripped_line.split("=")[0].strip()
        nested_data = {}
        continue

    # 处理嵌套模式中的数据
    if in_nested_mode:
        if ")" in stripped_line:
            in_nested_mode = False
            current_record[nested_key] = nested_data
            nested_data = {}
            continue

        match = pattern.match(stripped_line)
        if match:
            key, value = match.groups()
            value = value.rstrip(',')
            nested_data[key] = value
            continue

    # 处理主模式中的数据
    match = pattern.match(stripped_line)
    if match:
        key, value = match.groups()
        value = value.rstrip(',')
        current_record[key] = value
    elif 'export' in stripped_line:
        match = export_pattern.match(stripped_line)
        if match:
            current_record['ExportValue'] = match.group(1)
    elif ')' in stripped_line:
        parsed_data.append(current_record)
        current_record = {}

# 转换为pandas DataFrame并保存为CSV
df = pd.DataFrame(parsed_data)
column_list = df.columns.tolist()
for i in column_list:
    print(i)
# 字段名和翻译的字典
translation_dict = {
    'ExportValue': '导出价值',
    'DescriptorId': '描述符标识',
    'Name': '名称',
    'TypeName': '类型名称',
    'TypeArme': '武器类型',
    'TypeCategoryName': '类型类别名称',
    'Caliber': '口径',
    'WeaponDescriptionToken': '武器描述标记',
    'WeaponCursorType': '武器光标类型',
    'MinMaxCategory': '最小最大类别',
    'Level': '等级',
    'NeedModelChange': '需要模型更改',
    'Arme': '武器',
    'IsAPCR': '是否为穿甲弹',
    'ProjectileType': '弹丸类型',
    'FxWeaponType': '特效武器类型',
    'FxPower': '特效威力',
    'Puissance': '功率',
    'TempsEntreDeuxTirs': '射击间隔时间',
    'TempsEntreDeuxTirs_Min': '最小射击间隔时间',
    'TempsEntreDeuxTirs_Max': '最大射击间隔时间',
    'TempsEntreDeuxFx': '特效间隔时间',
    'PorteeMaximale': '最大射程',
    'PorteeMinimaleTBA': 'TBA最小射程',
    'PorteeMaximaleTBA': 'TBA最大射程',
    'PorteeMinimaleHA': 'HA最小射程',
    'PorteeMaximaleHA': 'HA最大射程',
    'PorteeMinimaleProjectile': '弹丸最小射程',
    'PorteeMaximaleProjectile': '弹丸最大射程',
    'PorteeMinimale': '最小射程',
    'AltitudeAPorteeMaximale': '最大射程高度',
    'AffecteParNombre': '受数量影响',
    'EfficaciteSelonPortee': '射程效果',
    'AngleDispersion': '扩散角度',
    'DispersionAtMaxRange': '最大射程扩散',
    'DispersionAtMinRange': '最小射程扩散',
    'CorrectedShotAimtimeMultiplier': '修正射击瞄准时间倍数',
    'CanFxDestinationShiftFromRealPosition': '是否可以从真实位置进行特效位移',
    'RadiusSplashPhysicalDamages': '爆炸物理伤害半径',
    'PhysicalDamages': '物理伤害',
    'RadiusSplashSuppressDamages': '爆炸抑制伤害半径',
    'SuppressDamages': '抑制伤害',
    'RayonPinned': '固定半径',
    'TirIndirect': '间接射击',
    'TirReflexe': '反射射击',
    'InterdireTirReflexe': '禁止反射射击',
    'FX_vitesse_de_depart': '特效发射速度',
    'FX_tir_sans_physic': '特效无物理发射',
    'FX_frottement': '特效摩擦',
    'FX_shot_duration_min_ratio': '最小特效射击持续时间比率',
    'FX_shot_duration_max_ratio': '最大特效射击持续时间比率',
    'FX_pause_duration': '特效暂停持续时间',
    'FX_pause_duration_min_ratio': '最小特效暂停持续时间比率',
    'FX_pause_duration_max_ratio': '最大特效暂停持续时间比率',
    'TempsAnimation': '动画时间',
    'NoiseDissimulationMalus': '噪音伪装惩罚',
    'ShotsBeforeMaxNoise': '达到最大噪音前的射击次数',
    'SupplyCost': '供应成本',
    'TargetsDistricts': '目标区域',
    'WeaponRessourcesNeeded': '武器所需资源',
    'AmbushShotDamageMultiplier': '伏击射击伤害倍数',
    'HitRollRuleDescriptor': '命中规则描述符',
    'BaseCriticModifier': '基础批评修饰符',
    'BaseEffectModifier': '基础效果修饰符',
    'BaseHitValueModifiers': '基础命中值修饰符',
    'HitModifierList': '命中修饰符列表',
    'TempsDeVisee': '瞄准时间',
    'TempsEntreDeuxSalves': '两次射击之间的时间',
    'TempsEntreDeuxSalves_Min': '最小两次射击之间的时间',
    'TempsEntreDeuxSalves_Max': '最大两次射击之间的时间',
    'NbTirParSalves': '每波射击次数',
    'NbrProjectilesSimultanes': '同时发射的弹丸数',
    'AffichageMunitionParSalve': '每波显示弹药量',
    'MissileDescriptor': '导弹描述符',
    'AffichageMenu': '菜单显示',
    'InterfaceWeaponTexture': '武器界面纹理',
    'SmokeDescriptor': '烟雾描述符',
    'FireDescriptor': '火焰描述符',
    'FireTriggeringProbability': '触发火灾的概率',
    'TargetUnitCenter': '目标单位中心',
    'CanHarmInfantry': '是否可以伤害步兵',
    'CanHarmVehicles': '是否可以伤害车辆',
    'CanHarmHelicopters': '是否可以伤害直升机',
    'CanHarmAirplanes': '是否可以伤害飞机',
    'CanHarmGuidedMissiles': '是否可以伤害制导导弹',
    'IsHarmlessForAllies': '是否对盟友无害',
    'PiercingWeapon': '穿甲武器',
    'DamageTypeEvolutionOverRangeDescriptor': '范围内伤害类型演变描述符',
    'UnitWeight': '单位权重',
    'MaxSuccessiveHitCount': '最大连续命中次数',
    'IgnoreInflammabilityConditions': '忽略易燃条件',
    'AltitudeAPorteeMinimale': '最小射程高度',
    'NbSalvosShootOnPosition': '在位置上射击次数',
    'CorrectedShotDispersionMultiplier': '修正射击扩散倍数',
    'IsSubAmmunition': '是否为子弹药'
}
# 将字段名替换为中文
#df = df.rename(columns=translation_dict)
df.to_csv("output.csv", index=False)