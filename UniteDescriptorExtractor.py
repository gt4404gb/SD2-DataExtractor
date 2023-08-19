from pyparsing import (Word, alphanums, Forward, Suppress, Group, OneOrMore,Regex,re,Combine,
                       ZeroOrMore, restOfLine, Literal,Optional,Dict,SkipTo,StringEnd)
file = open("111.ndf",'r')
#file = open("mymod/GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf",'r')
test_str = file.read()
# 测试
test_str1 = '''
export key1 is key1 (
    key3 = [
        val1,
        val2,
        val3
    ],
    key4 = aaa(
        key5 = val4
    ),
    key6 = val5
)
export key2 is key2 (
    key3 = [
        val1,
        val2,
        val3
    ],
    key4 = aaa(
        key5 = val4
    ),
    key6 = val5
)
'''


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
    comment = Combine(Literal("//").suppress() + restOfLine).setResultsName("comment")
    # 使用SkipTo来跳过内容直到下一个注释或字符串结束
    content_to_next_comment = SkipTo(comment | StringEnd(), include=False).setResultsName("content")
    # 主数据定义
    mainData = Dict(Group(comment + content_to_next_comment))
    # 解析字符串
    result = mainData.searchString(moduleDict[1])
    return UniteName, result[0]

if __name__ == "__main__" :
    # 使用Forward预留空间，为之后的递归定义做准备
    value = Forward()
    key_value = Forward()
    value_list = Forward()
    key_value_list = Forward()

    # 值和键值对的定义
    value <<= identifier | value_list
    key_value <<= Group(identifier + EQUAL + value)

    # 值列表和键值列表的定义
    value_list <<= Group(LBRACK + ZeroOrMore(value + Optional(COMMA)) + RBRACK)
    key_value_list <<= Group(Optional(identifier) + LPAREN + OneOrMore((key_value_list | key_value) + Optional(COMMA)) + RPAREN)

    # Key-value pairs and module/block structures
    module = key_value_list

    allExport = CutExport(test_str)
    for itemExport in allExport:
        itemName,itemResult = CutComment(itemExport)
        print(itemName)
        print(itemResult[0])