# TheSecretArea
# 秘密空间

***

### 简介

一个黑窗口游戏，类似于早期文字冒险游戏的玩法，基于python（可移植）

正在缓慢施工中

作者：@卍看破苍穹卐

本游戏必要的文件有三个：main.py（引擎），gameScript.txt（游戏脚本），save（存档文件，首次运行之前不会出现），运行请确保三个文件位于同一目录下。

如果您想使用本游戏的引擎（命名为krill）开发其他游戏或改编本游戏，请注明出处。

但是需要注意的是，此引擎目前只能用于制作复古式文字冒险游戏，这一游戏类型在当代非常不受欢迎；而且本引擎的游戏脚本解释器也较不完善，缺少某些异常处理功能，安全性也欠佳。

***

### krillScript

gameScript.txt中所使用的脚本语言被称为krill script（简称KS）。

stage(场景)：游戏中的一个场景，可以是某一片地区、一个房间或游戏的一个阶段等，是KS的容器。  
用`<NAME>`作为起始符，`</NAME>`作为终止符——有点类似xml，但不能也不需要嵌套。  
游戏会从名为beginning的stage开始。

entity(实体)：场景中的一个可互动目标，可以是一个人、一本书或一个箱子等。  
一个实体可以有多个可用的名称。

KS中共有12种语句，以半角分号`;`分割，忽略行首缩进（空格或制表符）和换行。

`msg TEXT`：输出一行文本。

`say NAME TEXT`：产生一句对白。  
尽管用msg语句也可以达到相同的效果，但为了保证足够的可移植性，我们不推荐用msg替代say。  
在krill for html中，方括号`[]`会被编译成`<b>`标签，显示为粗体。

`goto NAME`：转换至另一个场景。

`show NAME`：显示一个实体，使其可以与玩家互动。所有实体默认都处于显示状态。

`hide NAME`：隐藏一个实体，使其无法与玩家互动。

`getItem NAME`：使玩家获得一个物品，通常是一件对玩家有帮助的道具，如一把钥匙、一把刀或一张地图等。  
一个物品的名称仅可包含：

* 英文字母，区分大小写
* 数字
* 下划线
* 中文

其他字符均为非法字符（尽管通常情况下不会出现错误）  
下划线可以作为空格的替代品——在GUI中，下划线会被显示为空格。

`removeItem NAME`：移除玩家身上的一个物品。

`ask {ITEM1 {CODEBLOCK1};ITEM2 {CODEBLOCK2};...}`：给玩家提供数个选项并要求玩家从中选择一个。  
一个简单的例子：  
```
msg 请选择你最喜欢的水果;
ask {
    苹果 {
    	msg 你喜欢苹果！;
    };
    香蕉 {
        msg 你喜欢香蕉？;
        say 苍穹 可是我不喜欢……;
    };
    橘子 {
    	msg 你喜欢橘子！
    }
```
输出为：  
```
请选择你最喜欢的水果
1   苹果
2   香蕉
3   橘子
输入你的选择 >>> 
```

`[VARNAME] = NUMBER`：变量的赋值。  
KS中用方括号`[]`包含变量名称来表示一个变量。  
不同于大部分脚本语言，KS的变量名称中仅可以包含：

* 英文字母，区分大小写
* 数字
* 下划线
* 中文

其他字符全部为非法字符（尽管大部分字符在通常情况下不会引发错误）  
变量的内容只能是数字。

`[VARNAME] += NUMBER`：变量的加值。  
如果VARNAME没有被赋值过则默认为0。

`if (CONDITION) {CODEBLOCK1} else {CODEBLOCK2}`：条件语句。  
else是可选的。  
CONDITION中可以填入`[VARNAME] ==/>/>=/</<= NUMBER`（判断一个变量的值），`item[NAME]`（判断玩家是否拥有一个物品），`and/or/not`（逻辑与或非）

`entity (NAME1,NAME2,...) {INTRODUCTION;events {EVENT1 {CODEBLOCK1};EVENT2 {CODEBLOCK2};...}`:定义一个实体。  
INTRODUCTION（events之前的代码块）为玩家执行“环顾四周”（遍历实体表）时执行的代码。  
实体名称仅可以包含：

* 英文字母，区分大小写
* 数字
* 下划线
* 中文

一个简单的例子：  
```
entity (箱子,箱,宝箱) {
    msg 你的前方有一个>箱子<;
    msg 你可以打开看一看。;
    events {
        walkTo {
            msg 你走向箱子。
        };
        open {
            msg 你尝试打开这个箱子。;
            msg 但它上了锁。
        };
        lookAt {
            msg 这个箱子的造型十分古朴。
        };
        use {
            钥匙 {
                msg 你掏出钥匙，打开了箱子上的锁。
            };
            锤子 {
                msg 这个箱子非常结实，你无法用蛮力打开它。
            };
            default {
                msg 当玩家使用其他物品时会执行这里的代码。;
            }
        }
    }
}
```
events用于定义与实体关联的事件。可用的事件有：  
* walkTo：走向
* lookAt：查看
* pickUp：捡起
* open：打开
* close：关闭
* talkTo：交谈
* push：推
* pull：拉
* use：使用物品
