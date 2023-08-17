from pyparsing import *
import json
import re
file = open("mymod/GameData/Generated/Gameplay/Gfx/111.ts",'r')
#file = open("mymod/GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf",'r')
data = file.readlines()

lines = [i for i in data if i != '\n']
str_all = "".join(lines)
import re

data = str_all
#data = data.replace('(','{')
#data = data.replace(')','}')
def adjust_indentation(match):
    level = len(match.group(1))
    return ' ' * (level * 2) + match.group(2)

def myre(data):
    # 使用正则表达式匹配并移除 Selection 字段及其内容
    pattern = r"\bSelection\b\s*=\s*\[[\s\S]*?\[[\s\S]*?\][\s\S]*?\](?=\s*,|\s*\))"
    output_text = re.sub(pattern, "", data)
    # 使用正则表达式匹配并移除 // Flags 部分及其内容
    pattern = r"// Flags\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // TargetCoordinator 部分及其内容
    pattern = r"// TargetCoordinator\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // TargetManager 部分及其内容
    pattern = r"// TargetManager\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // Critical 部分及其内容
    pattern = r"// Critical\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // PlayerMission 部分及其内容
    pattern = r"// PlayerMission\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // LinkTeam 部分及其内容
    pattern = r"// LinkTeam\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // Tags 部分及其内容
    pattern = r"// Tags\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // Debug 部分及其内容
    pattern = r"// Debug\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // Selection 部分及其内容
    pattern = r"// Selection\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // EffectApplier 部分及其内容
    pattern = r"// EffectApplier\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // InfluencePosition 部分及其内容
    pattern = r"// InfluencePosition\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // InfluenceMap 部分及其内容
    pattern = r"// InfluenceMap\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // OrderConfig 部分及其内容
    pattern = r"// OrderConfig\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // OrderDisplay 部分及其内容
    pattern = r"// OrderDisplay\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // GroupableUnit 部分及其内容
    pattern = r"// GroupableUnit\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)
    # 使用正则表达式匹配并移除 // PackSignaux 部分及其内容
    pattern = r"// PackSignaux\s*[\s\S]*?(?=// \w+|\Z)"
    output_text = re.sub(pattern, "", output_text)


    return output_text




output_text = myre(data)
with open('output.ts', 'w', encoding='utf-8') as f:
    f.write(output_text)

print("转换完成，结果已保存到output.yaml")