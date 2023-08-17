# SD2-DataExtractor 钢铁之师2 数据提取器

----

所需环境：Python3.7+

使用`pip install -r requirements.txt`安装程序所需第三方包

----
使用步骤：

## 一、创建Mod
[mod创建原文](https://bbs.3dmgame.com/thread-6275968-1-1.html)
首先找到你SD2游戏所安装的地方
例如游戏路径为F:\Steam\steamapps\common\SteelDivision 2
进入mod文件夹，如果之前没有做过任何尝试的情况下，你会看到两个文件夹以及4个文件
在这其中，前两个文件夹为制作mod的模板，不要修改。
两个pdf文件以及一个txt文件为制作mod的简要教程，可以自己多研究下。

在此，运行CreateNewMod.bat，就会弹出一个命令行窗口要求你输入mod的名字，在这里输入mymod。
等待一段时间后，就会生成一个mymod文件夹。

## 二、提取数据
将生成的文件夹整个放在本程序根目录下，也就是py文件同路径

使用 `python AmmunitionExtractor.py` 提取武器信息





### 数据说明
注：Eugen使用ndf格式文件来保存相关数据。我们修改时用文本编辑工具修改就可以。（我举例时用的是Notepad++，你用记事本也可以，就是麻烦点）
1， 找到每个师的名字
文件位置：
Steel Division 2\Mods\1. Skijager\GameData\Generated\Gameplay\Decks里的DivisionList.ndf
以HB结尾的师是历史战役和将军模式的师，其他的是对战中的师，在此处找到自己想修改的师的名字，如Descriptor_Deck_Division_GR_1_Skijager_multi（注：实际上测试发现HB不是将军模式）

2， 每分钟经济修改
文件位置：
Steel Division2\Mods\1. Skijager\GameData\Gameplay\Decks里的DivisionEconomy.ndf
只需要修改前三十行中括号里的数字就可以修改单人和多人对战中的经济点数。
在这个ndf的文件的后面是一些历史战役的经济点数，同样可以在这里修改。

3，卡位修改
文件位置：文件位置：
Steel Division2\Mods\1. Skijager\GameData\Gameplay\Decks里的DivisionCostMatrix.ndf
找到你要修改的师的花费矩阵修改即可


4，每个师有哪几卡
文件位置：
Steel Division 2\Mods\1. Skijager\GameData\Generated\Gameplay\Decks里的Divisions.ndf
搜索你想修改的师的名字：Descriptor_Deck_Division_GR_1_Skijager_multi
每个括号是一种卡，前面的是武器装备的名字，后面是数量。
把第一行的1改为4 ，你在游戏中就可以带4卡电台摩托了。
也可以复制粘贴其他师的卡，比如把五装的Hummel条目直接粘贴进来（不过DivisionRule.ndf也要粘贴，一一按顺序对应即可）
在PackList后面这个地方可以改最大点数，比如芬步这里就是55


5，每一卡的数量和经验修改，以及载具
文件位置：
Steel Division 2\Mods\1. Skijager\GameData\Generated\Gameplay\Decks里的DivisionsRules.ndf
搜索你想修改的师的名字，
UnitRuleList里面是要修改的卡的数据，这里以Pak40举例：
第一行是单位的名字，后面会依靠这个名字搜索并修改单位的属性。
第三行是这个单位可用的载具，按原有格式修改即可。
第四行是可带几卡，但主要以Division里为主。
第五行为每阶段数量。
第六行为经验惩罚，游戏里实际的装备数量为两个数字相乘，小数部分大于0.5时向上取整，小于等于0.5时向下取整
再往下的TransportRuleList为载具的种类以及数量
第一行为载具名字，第二行为数量


6，单位的数据
文件位置：
Steel Division 2\Mods\1. Skijager\GameData\Generated\Gameplay\Gfx里的UniteDescriptor.ndf
搜索单位的名称如Descriptor_Unit_PaK_40_75mm即可
里面可以改很多东西，步兵装甲和飞机都有一些不同，这里只说几个常用的修改，其他的自己摸索一下吧。
//Damage里面MaxDamage就是血量（对步兵是人数），MaxHPforHUD是游戏里显示的血量
Armor里是装甲数据，分别为前侧后顶，数值*5为实际数据。（图二为Descriptor_Unit_T34_85_obr_43_GER）
//Production里，Factory表明是在反坦克栏
下面的Resource里的两个数是对战里的点数花费和将军模式里的点数花费


7，武器的数据
文件位置：
Steel Division 2\Mods\1. Skijager\GameData\Generated\Gameplay\Gfx里的WeaponDescriptor.ndf和Ammunition.ndf
在WeaponDescriptor.ndf这个文件里，搜索前文的武器数据（在这里只需要搜索Descriptor_Unit_PaK_40_75mm后面的部分，即PaK_40_75mm）
注意这里的Ammunition里的值Ammo_Pak40_75mmL_AP
在Ammunition.ndf搜索这个值。
Arme里面的值为该武器类型，穿甲值为29*5=145
PhysicalDamages为伤害
SuppressDamages为压制
SupplyCost为补给每一发弹药消耗的补给值
Idling为固定精度
Moving为移动进度