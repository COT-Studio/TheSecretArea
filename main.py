#————类————

class script:
    #游戏脚本解析器对象

    def exec(self,code):
        t = code.replace("\r","").replace("\n","")
        l = [""]
        i = 0
        while i < len(t):
            if t[i] == ";":
                if t[i-1] == "\\":
                    l[-1] += ";"
                elif t[0:i].count("{") > t[0:i].count("}"):
                    l[-1] += ";"
                else:
                    l.append("")
            else:
                l[-1] += t[i]
            i += 1

        for x in l:
            self.eval(x)

    def parseActList(self,code):
        l = [""]
        i = 0
        d = dict()
        c = code.replace("\r","").replace("\n","").replace("\t","")
        while i < len(c):
            if c[i] == ";":
                if c[i-1] == "\\":
                    l[-1] += ";"
                elif c[0:i].count("{") > c[0:i].count("}"):
                    l[-1] += ";"
                elif i < len(c) - 1:
                    l.append("")
            else:
                l[-1] += c[i]
            i += 1

        for x in l:
            k = list(x.lstrip(" \t").partition(" "))
            k[0] = k[0].lstrip("{")
            if k[2].startswith("{"):
                d[k[0]] = k[2][1:-1]
            else:
                d[k[0]] = k[2]
        return d

    def parseEvents(self,code):
        l = [""]
        i = 0
        d = dict()
        while i < len(code):
            if code[i] == ";":
                if code[i-1] == "\\":
                    l[-1] += ";"
                elif code[0:i].count("{") > code[0:i].count("}"):
                    l[-1] += ";"
                else:
                    l.append("")
            else:
                l[-1] += code[i]
            i += 1

        for x in l:
            k = x.lstrip(" \t").partition(" ")
            if k[0] == "use":
                d["use"] = self.parseActList(k[2])
            else:
                if k[2].startswith("{"):
                    d[k[0]] = k[2][1:-1]
                else:
                    d[k[0]] = k[2]

        if "use" in d and "default" not in d.get("use"):
            d["use"]["default"] = "msg 这东西在这没用！"

        d.setdefault("walkTo","msg 走不到")
        d.setdefault("lookAt","msg 看不见")
        d.setdefault("pickUp","msg 捡不起来")
        d.setdefault("open","msg 打不开")
        d.setdefault("close","msg 关不上")
        d.setdefault("talkTo","msg 笑死，根本不会说话")
        d.setdefault("push","msg 推不走")
        d.setdefault("pull","msg 拽不动")
        d.setdefault("use",{"default":"msg 人工智障表示不懂你要用这玩意干嘛"})

        return d

    def eval(self,code):
        l = code.lstrip(" \t").split(" ")
        j = l[0]
        if j == "msg":
            msg(" ".join(l[1:]))
        elif j == "say":
            say(l[1]," ".join(l[2:]))
        elif j == "goto":
            goto(" ".join(l[1:]))
        elif j == "ask":
            ask(self.parseActList(" ".join(l[1:])[1:-1]))
        elif j == "show":
            findEntity(" ".join(l[1:])).show()
        elif j == "hide":
            findEntity(" ".join(l[1:])).hide()
        elif j == "getItem":
            if " ".join(l[1:]) not in varDict[".items"]:
                varDict[".items"].append(" ".join(l[1:]))
        elif j == "removeItem":
            if " ".join(l[1:]) in varDict[".items"]:
                varDict[".items"].remove(" ".join(l[1:]))

        elif j.startswith("[") and j.endswith("]"):
            #变量赋值和加值
            if l[1] == "=":
                varDict[j[1:-1]] = eval(" ".join(l[2:]))
            if l[1] == "+=":
                if varDict.get(j[1:-1]) == None:
                    varDict[j[1:-1]] = eval(" ".join(l[2:]))
                else:
                    varDict[j[1:-1]] += eval(" ".join(l[2:]))

        elif j == "if":
            p1 = code.index("(") + 1
            p2 = code.index(")",p1,len(code))
            i = code.index("{") + 1
            def f(x,y):
                #这个y是我偷懒用的，没有任何实际作用
                return x in varDict[".items"]
            b = eval(code[p1:p2].replace("item[","f('").replace("[","varDict.get('").replace("]","',0)"))
            l = [""]
            while i < len(code):
                if code[i:i+8] == "} else {" and code[0:i+1].count("{") == code[0:i+1].count("}"):
                    l.append("")
                    i += 7
                elif i == len(code)-1 and code[i] == "}":
                    i += 1
                else:
                    l[-1] += code[i]
                i += 1
            if b:
                self.exec(l[0])
            elif len(l) == 2:
                self.exec(l[1])

        elif j == "entity":
            p1 = code.index("{") + 1
            p2 = code.rindex("}")
            p3 = code.index("events {") + 8
            p4 = code.rindex("}",0,p2)
            names = eval(('{"' + code[code.find("(") + 1:code.find(")")] + '"}').replace(",",'","'))
            intro = code[p1:code.index("events {")]
            events = self.parseEvents(code[p3:p4])
            stage.append(entity(names,intro,events))

class entity:

    display = True

    def __init__(self,names,intro,events):
        self.names = names#表示此实体所有可能的名称
        self.intro = intro
        self.events = events

    def do(self,type):
        #无参数指令
        script.exec(self.events[type])

    def use(self,item):
        #对此使用物品
        if item in varDict[".items"]:
            script.exec(self.events["use"].get(item,self.events["use"]["default"]))
        else:
            msg("你似乎没有这个物品。可以尝试输入“查看物品栏”来查看自己都有什么。")

    def introduce(self):
        #环顾四周时此实体的提示
        script.exec(self.intro)

    def show(self):
        self.display = True

    def hide(self):
        self.display = False

#————变量————

f = open("gameScript.txt",encoding="utf-8")
gameScript = ""
for x in f:
    gameScript += x.lstrip(" \t")
f.close()
stage = list()
varDict = {".items":list()}
actions = {
    "walkTo":{"走向","走到","移到","移动到"},
    "lookAt":{"查看","察看","观察","检查","检察","调查"},
    "pickUp":{"捡起","拿起","拿","拿出","拿取","拿到","抄起"},
    "open":{"打开","开启","开","启动"},
    "close":{"关闭","关上","关掉","关"},
    "talkTo":{"交谈","交流","谈话"},
    "push":{"推","推动","推挤","推搡","按压","按","按下"},
    "pull":{"拉","拽","拉动","拉开","拉拽","拔","拔出"}
}
script = script()
try:
    f = open("save",encoding="utf-8")
except:
    f = open("save","w",encoding="utf-8")
    f.write("<__save is empty,do not modify this text__>")
    f.close()

#————函数————

def save():
    f = open("save","w",encoding="utf-8")
    stageInfo = list()
    for x in stage:
        stageInfo.append("entity({},'{}',{})".format(x.names,x.intro,x.events))
    f.write("<__Delimiter__>".join((str(stageInfo),str(varDict))))
    f.close()

def say(name:str,text:str):
    msg("   ".join((name,text)))

def msg(text:str):
    input(text)

def ask(selections:dict):
    i = 1
    for x in selections:
        print(str(i) + "   " + x)
        i += 1
    while True:
        inp = input("输入你的选择 >>> ")
        if inp.isnumeric() and int(inp) in range(1,len(selections) + 1):
            num = int(inp) - 1
            script.exec(list(selections.values())[num])
            return None

def goto(name:str):
    #转换场景
    stage.clear()
    if "<{}>".format(name) in gameScript:
        p1 = gameScript.index("<{}>".format(name)) + len(name) + 2
        p2 = gameScript.index("</{}>".format(name))
        script.exec(gameScript[p1:p2])
    else:
        raise KeyError("不存在名为“{}”的stage".format(name))

def findEntity(name:str):#找到舞台上第一个可以被称作name的实体
    for x in stage:
        if name in x.names:
            return x
    return None

def textParser(text:str):
    #世界上最不近人情的文本解析器
    #基本指令：走向（walkTo），查看（lookAt），捡起（pickUp），打开（open）
    #关闭（close），交谈（talkTo），推（push），拉（pull），使用物品（use）
    li = text.split(" ")

    if li[0] in {"把"} and li[2] in {"给","给予"}:
        #这里是use的判定
        if len(li) != 4:
            msg("我承认我是个人工智障，但你这语法好像不太对。")
        else:
            item = li[1]
            targetName = li[3]
            target = findEntity(targetName)
            if target == None or not target.display:
                msg("现在周围没有“{}”这个东西".format(targetName))
            else:
                findEntity(targetName).use(item)
    elif li[0] in {"对","对着"} and li[2] in {"使用","用","出示","展示"}:
        if len(li) != 4:
            msg("我承认我是个人工智障，但你这语法好像不太对。")
        else:
            item = li[3]
            targetName = li[1]
            target = findEntity(targetName)
            if target == None or not target.display:
                msg("现在周围没有“{}”这个东西".format(targetName))
            else:
                target.use(item)

    else:
        for i in actions:
            if li[0] in actions[i]:
                if len(li) == 1:
                    msg("你这话别说半截啊。")
                else:
                    targetName = " ".join(li[1:])
                    target = findEntity(targetName)
                    if target == None or not target.display:
                        msg("现在周围没有“{}”这个东西".format(targetName))
                    else:
                        target.do(i)
                return None
        if text in {"环顾四周","观察四周","观察周围","查看四周","查看周围"}:
            if len(stage) == 0:
                msg("周围空无一物......")
            else:
                for i in stage:
                    i.introduce()
        elif text in {
            "查看物品","查看物品栏","查看物品列表","查看物品清单",
            "物品","物品栏","物品列表","物品清单",
            "打开物品栏","打开物品列表","打开物品清单"
        }:
            if len(varDict[".items"]) == 0:
                msg("你现在什么也没有，你个穷光蛋！")
            else:
                msg("你现在有：" + "、".join(varDict[".items"]) + "。")
        elif text == "帮助":
            print("大部分操作的格式都是“操作名称 目标”，注意中间有一个空格")
            print("如果你想走向一个地方，操作名称可以是：" + str(actions["walkTo"]))
            print("如果你想观察某个地方或一个什么东西，操作名称可以是：" + str(actions["lookAt"]))
            print("如果你想拿起一件物品，操作名称可以是：" + str(actions["pickUp"]))
            print("如果你想打开一扇门或者打开一个开关，操作名称可以是：" + str(actions["open"]))
            print("如果你想关上一扇门或者关闭一个开关，操作名称可以是：" + str(actions["close"]))
            print("如果你想与某人交谈，操作名称可以是：" + str(actions["talkTo"]))
            print("如果你想推动一个物体，操作名称可以是：" + str(actions["push"]))
            print("如果你想拉动一个物体，操作名称可以是：" + str(actions["pull"]))
            print("如果你想对某人或某物出示或者使用一个物品（你首先需要拥有这个物品），你可以输入“对 xxx 使用/展示 xxx”或“把 xxx 给予 xxx”,注意空格")
            print("如果你想观察周围（获取场景中所有可交互物体的列表），你可以输入环顾四周、观察四周、观察周围、查看四周、查看周围")
            print("如果你想看看你都有什么物品，你可以输入查看物品、查看物品栏、查看物品列表、查看物品清单、物品、物品栏、物品列表、物品清单、打开物品栏、打开物品列表、打开物品清单")
            print("最后，如果你想再次查看这些说明的话，请输入“帮助”。")
        elif text != "":
            msg("完全听不懂你在说什么呢")

#————主进程————

def main():
    msg("按enter来继续。")
    msg("本游戏支持自动存档，存档数据将保存于同目录下的“save”文件。")
    msg("每当您看到“输入操作 >>> ”的提示时，游戏都将自动保存。\n\n\n")
    print("——秘 密 空 间——")
    print("1   新游戏")
    print("2   读取存档")
    while True:
        inp = input("输入你的选择 >>> ")
        if inp in {"1","2"}:
            if inp == "1":
                goto("beginning")
            else:
                f = open("save",encoding="utf-8")
                saveCode = f.read()
                if saveCode == "<__save is empty,do not modify this text__>":
                    script.goto("beginning")
                else:
                    l = saveCode.partition("<__Delimiter__>")
                    global stage
                    global varDict
                    stage = eval(l[0])
                    for x in range(len(stage)):
                        stage[x] = eval(stage[x])
                    varDict = eval(l[2])
                    f.close()
            break

    inputLog = ["","","","","","","","",""]
    while True:
        save()
        inputLog.append(input("输入操作 >>> ").lstrip(" "))
        inputLog.pop(0)
        if inputLog[-1] != "":
            if inputLog[-1][0] == "/":
                print(eval(inputLog[-1][1:]))
            elif inputLog[-9:].count(inputLog[-1]) == 9:
                msg("用魔法打败魔法，我也变成复读机。")
            elif inputLog[-8:].count(inputLog[-1]) == 8:
                msg("想看看我还有什么骚话是吗？")
            elif inputLog[-7:].count(inputLog[-1]) == 7:
                msg("你调戏旁白是吧？？")
            elif inputLog[-6:].count(inputLog[-1]) == 6:
                msg("你还上瘾了是吧？")
            elif inputLog[-5:].count(inputLog[-1]) == 5:
                msg("看来是了。")
            elif inputLog[-4:].count(inputLog[-1]) == 4:
                msg("问一下，你就是传说中的复读机吗？")
            else:
                textParser(inputLog[-1])
        else:
            textParser(inputLog[-1])

main()
