import re
import pandas as pd
#file = open("111.ndf",'r')
file = open("mymod/GameData/Generated/Gameplay/Gfx/WeaponDescriptor.ndf",'r')
test_str = file.read()


#以export为单位分割字符串
def CutExport(data):
    parts = re.split(r'\bexport\b', data)
    results = []
    for part in parts[1:]:
        match = re.match(r'\s*(\w+)\s+is\s+\w+(.*)', part, re.DOTALL)
        if match:
            results.append((match.group(1), match.group(2)))
    return results

#提取单元中的键值
def CutUnite(data):
    pattern = re.compile(r'(\w+)\s*=\s*(\S.*?)\s*$', re.MULTILINE)
    result_dict = {}
    for match in pattern.finditer(data):
        key = match.group(1)
        value = match.group(2).strip().rstrip(',')
        if key not in result_dict:
            result_dict[key] = value
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

        result_dict = CutUnite(itemExport[1])
        items.append([itemExport[0],result_dict])
    # 创建空的DataFrame
    df = pd.DataFrame()

    # 为每个item填充DataFrame
    for item_name, item_data in items:
        #print(item_data)
        temp_df = pd.DataFrame([item_data], index=[item_name])
        df = pd.concat([df, temp_df], axis=0)
    # 字段名和翻译的字典
    translation_dict = {
        "DelayIdleAmmoSorting": "延迟空闲弹药排序",
        "DefaultHoldFireState": "默认停火状态",
        "DefaultSmartHoldFireState": "默认智能停火状态",
        "DefaultRiposteStance": "默认还击姿态",
        "NeedsExplicitOrderToUseSmoke": "需要明确命令使用烟雾",
        "Salves": "齐射次数",
        "HasMainSalvo": "是否有主齐射",
        "SalvoIsMainSalvo": "齐射是否为主齐射",
        "AlwaysOrientArmorTowardsThreat": "始终朝向威胁方向",
        "TurretDescriptorList": "炮塔描述符列表",
        "AngleRotationBase": "基础旋转角度",
        "AngleRotationBasePitch": "基础俯仰角度",
        "AngleRotationMax": "最大旋转角度",
        "AngleRotationMaxPitch": "最大俯仰角度",
        "AngleRotationMinPitch": "最小俯仰角度",
        "MountedWeaponDescriptorList": "搭载武器描述符列表",
        "Ammunition": "弹药",
        "AnimateOnlyOneSoldier": "仅动画一个士兵",
        "DispersionRadiusOffColor": "散布圈关闭颜色",
        "DispersionRadiusOffThickness": "散布圈关闭厚度",
        "DispersionRadiusOnColor": "散布圈开启颜色",
        "DispersionRadiusOnThickness": "散布圈开启厚度",
        "EffectTag": "效果标签",
        "IgnoreFriendlyFireOnMoveAndAttack": "移动攻击时忽略友军伤害",
        "IgnoreFriendlyFireOnReflexShoot": "反应射击时忽略友军伤害",
        "MaxRangeDisplay_Color": "最大射程显示颜色",
        "MaxRangeDisplay_Thickness": "最大射程显示厚度",
        "MinRangeDisplay_Color": "最小射程显示颜色",
        "MinRangeDisplay_Thickness": "最小射程显示厚度",
        "OverwritedTrait_ForInterface": "覆盖特性_界面",
        "OwnerTurnHisChassisVerticallyToAttack": "车体转向攻击",
        "PowerIcon": "威力图标",
        "Power_ForInterface": "威力_界面",
        "SalvoStockIndex": "齐射库存索引",
        "SalvoStockIndex_ForInterface": "齐射库存索引_界面",
        "ShowDispersion": "显示散布",
        "ShowMaximumRange": "显示最大射程",
        "ShowMaximumRange_HA": "显示最大射程_防空",
        "ShowMaximumRange_Projectile": "显示最大射程_弹丸",
        "ShowMaximumRange_SuperWeapon": "显示最大射程_超级武器",
        "ShowMaximumRange_TBA": "显示最大射程_TBA",
        "ShowMinimumRange": "显示最小射程",
        "ShowMinimumRange_HA": "显示最小射程_防空",
        "ShowMinimumRange_Projectile": "显示最小射程_弹丸",
        "ShowMinimumRange_SuperWeapon": "显示最小射程_超级武器",
        "ShowMinimumRange_TBA": "显示最小射程_TBA",
        "ShowSplashRadius": "显示溅射半径",
        "SplashRadiusOffColor": "溅射半径关闭颜色",
        "SplashRadiusOffThickness": "溅射半径关闭厚度",
        "SplashRadiusOnColor": "溅射半径开启颜色",
        "SplashRadiusOnThickness": "溅射半径开启厚度",
        "Tag": "标签",
        "TagIndex": "标签索引",
        "TagIndexForMissileStart": "导弹发射标签索引",
        "TargetPositionPhysicalPropertyName": "目标位置物理属性名",
        "TirContinu": "持续射击",
        "TirEnMouvement": "移动射击",
        "TirSurPosition": "定点射击",
        "UnitIdleManagerDescriptor": "单位空闲管理器描述符",
        "VitesseRotation": "旋转速度",
        "WeaponNumber_ForInterface": "武器数量_界面",
        "AimingPriority": "瞄准优先级",
        "FlyingAltitude": "飞行高度",
        "FlyingSpeed": "飞行速度",
        "FlyingTimeAndHitPhysicalPropertyName": "飞行时间和命中物理属性名",
        "IKGoals": "IK目标",
        "IKIndex": "IK索引",
        "MasterTurretIndex": "主炮塔索引",
        "NbFX": "特效数量",
        "OutOfRangeTargetTrackingDuration": "超出射程目标跟踪时间",
    }
    # 将字段名替换为中文
    df = df.rename(columns=translation_dict)
    # 保存DataFrame到CSV
    df.to_csv('WeaponDescriptor.csv')