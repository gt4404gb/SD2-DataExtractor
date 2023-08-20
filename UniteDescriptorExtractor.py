from pyparsing import (Word, alphanums, Forward, Suppress, Group, OneOrMore,Regex,re,Combine,
                       ZeroOrMore, restOfLine, Literal,Optional,Dict,SkipTo,StringEnd)
file = open("111.ndf",'r')
#file = open("mymod/GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf",'r')
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
    result = mainData.searchString(data)
    return result

#以注释为单位分割
def CutComment(itemExport):
    GUID = Group("GUID" + ":{" + identifier + "}")
    DescriptorId = Group(identifier + EQUAL + GUID)
    ClassNameForDebug = Suppress(identifier) + EQUAL + SQUOTE + identifier + SQUOTE
    # 使用正则表达式全部匹配直到最后一个')'字符
    module_content = Regex(".*(?=\)$)", re.DOTALL)
    # 主数据语法
    moduleData = LPAREN + Suppress(DescriptorId) + ClassNameForDebug + Suppress("Modules") + EQUAL + module_content
    moduleDict = moduleData.parseString(itemExport[1])
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
    results = pattern.searchString(data)
    result_dict = {}
    # print(results.dump())
    for item in results:
        if not result_dict.get(item[0]):
            result_dict[item[0]] = item[1]
    return result_dict

if __name__ == "__main__" :

    allExport = CutExport(test_str)
    for itemExport in allExport:
        itemName,itemResult = CutComment(itemExport)
        print(itemName)
        for uniteKey, uniteValue in itemResult.items():
            print(uniteKey)
            result_dict = CutUnite(uniteValue)
            print(result_dict)