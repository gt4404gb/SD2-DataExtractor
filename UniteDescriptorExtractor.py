from pyparsing import *
import json
import re
file = open("mymod/GameData/Generated/Gameplay/Gfx/111.ts",'r')
#file = open("mymod/GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf",'r')
data = file.readlines()



from pyparsing import (Word, alphanums, Forward, Suppress, Group, OneOrMore,
                       ZeroOrMore, restOfLine, Literal,Optional)

# 初始化
identifier = Word(alphanums + "_")  # 定义标识符

# 使用Forward预留空间，为之后的递归定义做准备
value = Forward()
key_value = Forward()
value_list = Forward()
key_value_list = Forward()

# 符号定义
LPAREN = Literal("(").suppress()
RPAREN = Literal(")").suppress()
LBRACK = Literal("[").suppress()
RBRACK = Literal("]").suppress()
COMMA = Literal(",").suppress()
EQUAL = Literal("=").suppress()

# 注释处理
comment = Suppress("//") + restOfLine

# 值和键值对的定义
value <<= identifier | value_list
key_value <<= Group(identifier + EQUAL + value)

# 值列表和键值列表的定义
value_list <<= Group(LBRACK + ZeroOrMore(value + Optional(COMMA)) + RBRACK)
key_value_list <<= Group(Optional(identifier) + LPAREN + OneOrMore((key_value_list | key_value) + Optional(COMMA)) + RPAREN)

# Key-value pairs and module/block structures
module = key_value_list

# 主数据定义
data = (Suppress("export") + identifier + Suppress("is") + identifier + module)

# 测试
test_str = '''
export key1 is key2 (
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

parsed_data = data.parseString(test_str)
print(parsed_data)