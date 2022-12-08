import tkinter as tk
import math
from tkinter import BOTH, LEFT, RIGHT, X, OptionMenu, StringVar, ttk, messagebox, font
from typing import Any, Dict, List


class Node:

    SETVARIABLE = "Set Variable"
    IFBLOCK = "Old If Statement"
    FORLOOP = "Old For Loop"
    WHILELOOP = "Old While Loop"
    NEWIFBLOCK = "If Statement"
    IFTRUEBLOCK = "If True Branch"
    IFFALSEBLOCK = "If False Branch"
    LOOPENDBLOCK = "Loop End Block"
    NEWWHILELOOP = "While Loop"
    NEWFORLOOP = "For Loop"
    CHANGEVARIABLE = "Change Variable"

    types = [SETVARIABLE, NEWIFBLOCK, NEWWHILELOOP, NEWFORLOOP, CHANGEVARIABLE]

    sizes = {SETVARIABLE:125,IFBLOCK:100}

    descriptions = {
        SETVARIABLE: "set up a variable of any customized name",
        NEWIFBLOCK: "If statement block that execute correspondingly to the result of the if statment",
        NEWWHILELOOP: "A block that can execute its inside contents in a while loop structure",
        NEWFORLOOP: "A block that can execute its inside contents in a for loop structure",
        CHANGEVARIABLE: "Change the value of an existing variable"
    }

    def __init__(self) -> None:
        self.widget: tk.Widget = None
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []
        self.window = ""
        self.snap_distance = 20


    def connect(self, canva: tk.Canvas):
        if len(self.nextNode) > 0:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")

            pos = canva.bbox(self.window)
            ax0 = pos[0]
            ay0 = pos[1]
            ax1 = pos[2]
            ay1 = pos[3]

            for node in self.nextNode:
                pos = canva.bbox(node.window)
                bx0 = pos[0]
                by0 = pos[1]
                bx1 = pos[2]
                by1 = pos[3]

                x0 = (ax0 + ax1) / 2
                y0 = (ay0 + ay1) / 2

                x1 = (bx0 + bx1) / 2
                y1 = (by0 + by1) / 2

                # create the line, then lower it below all other
                # objects
                line_id = canva.create_line(
                    x0, y0, x1, y1, fill="black", width=4, tags=())
                canva.tag_lower(line_id)
                self.connector.append((node, line_id))
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)

    def setNextNode(self, node):
        self.nextNode = node

    def removeNextNode(self):
        self.nextNode = []

    def placeNode(self):
        self.widget.pack()

    def activate():
        pass

    def output():
        pass

    def destroy(self):
        pass

    def deleteConnectors(self, canvas: tk.Canvas):
        try:
            for line in self.connector:
                canvas.delete(line[1])
            self.connector = []
        except:
            print("no existing line")

    def removeConnector(self,node):
        pass

class SetVariable(Node):

    types = ['int','string','double']

    def __init__(self, window, varDict) -> None:
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=100, width=200)

        self.blockType = Node.SETVARIABLE
        
        self.lastVarName = ""
        self.typeChoice = StringVar()
        self.typeChoice.set(SetVariable.types[0])
        self.value = StringVar()
        self.value.trace("w", lambda name, index, mode, value=self.value: self.output(varDict))
        self.varName = StringVar()
        self.varName.trace("w", lambda name, index, mode, varName=self.varName: self.output(varDict))

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="Set Variable",font=fontGroup, background="#c7c7c7", width=28)
        self.titleLabel.grid(row=0, column=0, columnspan=3)

        self.typeLabel = tk.Label(self.widget, text="Type:",font=fontGroup)
        self.typeLabel.grid(row=1,column=0)
        self.dropdown = OptionMenu(self.widget, self.typeChoice, *SetVariable.types)
        self.dropdown['font']=fontGroup
        self.dropdown.grid(row=1,column=1, columnspan=2)

        self.nameLabel = tk.Label(self.widget, text="Variable Name:",font=fontGroup)
        self.nameLabel.grid(row=2,column=0,padx=(20,5))
        self.nameEntry = tk.Entry(self.widget,font=fontGroup,textvariable=self.varName,width=10)
        self.nameEntry.grid(row=2,column=1,columnspan=2,pady=5,padx=(5,20))

        self.valueLabel = tk.Label(self.widget, text="Variable Value:",font=fontGroup)
        self.valueLabel.grid(row=3,column=0,padx=(20,5))
        self.valueEntry = tk.Entry(self.widget,font=fontGroup,textvariable=self.value,width=10)
        self.valueEntry.grid(row=3,column=1,columnspan=2,pady=5,padx=(5,20))
        
        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def activate(self, time: int):
        self.widget.after(time, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            time+500, lambda: self.widget.config(background='#e6e6e6'))

    def setVarName(self, varName: str):
        self.varName = varName

    def output(self, varDict: Dict):
        if self.varName.get() != "":
            varDict.pop(self.lastVarName,None)
            name = self.varName.get()
            value = self.value.get()
            match self.typeChoice.get():
                case 'int':
                    if value != "":
                        varDict[name] = int(value)
                    else:
                        varDict[name] = None
                case 'string':
                    varDict[name] = value
                case 'double':
                    if value != "":
                        varDict[name] = float(value)
                    else:
                        varDict[name] = None
        self.lastVarName = self.varName.get()

    def destroy(self):
        self.widget.destroy()

    def deleteConnectors(self, canvas: tk.Canvas):
        try:
            for line in self.connector:
                canvas.delete(line[1])
            self.connector = []
        except:
            print("no existing line")

    def removeConnector(self,canvas:tk.Canvas,node):
        try:
            for line in self.connector:
                if line[0] == node:
                    canvas.delete(line[1])
        except:
            print("no such line or node")

class ChangeVariable(Node):

    types = ['input','var']
    operators = ['=','+=','-=','/=','//=','%=','*=']
    
    def __init__(self, window, varDict) -> None:
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=100, width=300)

        self.blockType = Node.CHANGEVARIABLE
        
        self.firstVar = StringVar()
        self.typeChoice = StringVar()
        self.typeChoice.set(ChangeVariable.types[0])
        self.operator = StringVar()
        self.value = StringVar()
        
        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="Change Variable",font=fontGroup, background="#c7c7c7", width=50)
        self.titleLabel.grid(row=0, column=0, columnspan=4)

        self.varNames = list(varDict.keys())
        self.firstVar.trace('w',lambda *args:self.refresh(varDict))
        self.firstVarChoice = OptionMenu(self.widget,self.firstVar,'',*self.varNames)
        self.firstVarChoice['font']=fontGroup
        self.firstVarChoice.grid(row=1,column=0)

        self.operatorChoice = OptionMenu(self.widget, self.operator, ChangeVariable.operators[0] ,*ChangeVariable.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.grid(row=1,column=1)

        self.typeDrop = OptionMenu(self.widget, self.typeChoice, *ChangeVariable.types)
        self.typeDrop['font']=fontGroup
        self.typeDrop.grid(row=1,column=2)

        self.typeChoice.trace('w',lambda *args:self.changeType())

        self.valueEntry = tk.Entry(self.widget,font=fontGroup,textvariable=self.value,width=10)
        self.valueEntry.grid(row=1,column=3)

        self.value.trace('w',lambda *args:self.refresh(varDict))
        self.valueDrop = OptionMenu(self.widget,self.value,'',*self.varNames)
        self.valueDrop['font']=fontGroup
        
        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []
    
    def changeType(self):
        match self.typeChoice.get():
            case 'input':
                self.value.set('')
                self.valueDrop.grid_forget()
                self.valueEntry.grid(row=1,column=3)
            case 'var':
                self.value.set('')
                self.valueEntry.grid_forget()
                self.valueDrop.grid(row=1,column=3)

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_columnconfigure(1,weight=1)
        self.widget.grid_columnconfigure(2,weight=1)
        self.widget.grid_columnconfigure(3,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        self.widget.grid_rowconfigure(1,weight=7)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def activate(self, time: int):
        self.widget.after(time, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            time+500, lambda: self.widget.config(background='#e6e6e6'))

    def setVarName(self, varName: str):
        self.varName = varName
    
    def refresh(self, variables:Dict):
        self.varNames = list(variables.keys())
        self.firstVarChoice['menu'].delete(0, 'end')
        for name in self.varNames:
            self.firstVarChoice['menu'].add_command(label=name, command=tk._setit(self.firstVar, name))

    def output(self, varDict: Dict):
        pass

    def destroy(self):
        self.widget.destroy()

    def deleteConnectors(self, canvas: tk.Canvas):
        try:
            for line in self.connector:
                canvas.delete(line[1])
            self.connector = []
        except:
            print("no existing line")

    def removeConnector(self,canvas:tk.Canvas,node):
        try:
            for line in self.connector:
                if line[0] == node:
                    canvas.delete(line[1])
        except:
            print("no such line or node")

class IfBlock(Node):

    operators = ['>','<','==','!=','>=','<=']
    types = ['int','string','double','var']

    def __init__(self, window, variables:Dict) -> None:
        self.blockType = Node.IFBLOCK

        self.firstValue = StringVar()
        self.firstValue.set('')
        self.operator = StringVar()
        self.secondType = StringVar()
        self.secondValue = StringVar()
        self.secondValue.set('')

        self.size = 200
        self.layer = 0

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=self.size, width=400+self.layer*50)

        self.workspace = tk.Canvas(self.widget,bg="#FFF", height=self.size-100, width=350+self.layer*50)

        self.header = tk.Frame(self.widget,height=50,width=400+self.layer*50,bg="#e6e6e6")

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="If Block",font=fontGroup, background="#c7c7c7", width=self.widget.winfo_screenwidth())
        self.titleLabel.pack()

        self.ifLabel = tk.Label(self.header, text="If", font=fontGroup)
        self.ifLabel.grid(row=1, column=0)

        self.varNames = list(variables.keys())
        self.firstValue.trace('w',lambda *args:self.refresh(variables))
        self.firstItem = OptionMenu(self.header,self.firstValue,'',*self.varNames)
        self.firstItem['font']=fontGroup
        self.firstItem.grid(row=1,column=1)

        self.operatorChoice = OptionMenu(self.header, self.operator, IfBlock.operators[0] ,*IfBlock.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.grid(row=1,column=2)

        self.secondTypeItem = OptionMenu(self.header,self.secondType,*IfBlock.types)
        self.secondTypeItem['font']=fontGroup
        self.secondTypeItem.grid(row=1,column=3)

        self.secondType.trace('w',lambda *args:self.changeType())

        self.secondEntry = tk.Entry(self.header,font=fontGroup,textvariable=self.secondValue,width=10)

        self.secondValue.trace('w',lambda *args:self.refresh(variables))
        self.secondItem = OptionMenu(self.header,self.secondValue,'',*self.varNames)
        self.secondItem['font']=fontGroup
        self.secondItem.grid(row=1,column=4)

        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []

    def refresh(self, variables:Dict):
        self.varNames = list(variables.keys())
        self.firstItem['menu'].delete(0, 'end')
        self.secondItem['menu'].delete(0, 'end')
        for name in self.varNames:
            self.firstItem['menu'].add_command(label=name, command=tk._setit(self.firstValue, name))
            self.secondItem['menu'].add_command(label=name, command=tk._setit(self.secondValue, name))

    def changeType(self):
        match self.secondType.get():
            case 'int' | 'string' | 'double':
                self.secondValue.set('')
                self.secondItem.grid_forget()
                self.secondEntry.grid(row=1,column=4)
            case 'variable':
                self.secondValue.set('')
                self.secondEntry.grid_forget()
                self.secondItem.grid(row=1,column=4)

    def placeNode(self,canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)
        self.header.pack(side="top",anchor="nw")
        self.workspace.pack(side="top", anchor="ne")

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")
    
    def activate():
        pass

    def destroy(self):
        return super().destroy()

    def output():
        pass

class NewIfBlock(Node):
    
    operators = ['>','<','==','!=','>=','<=']
    types = ['int','string','double','var']

    def __init__(self, window, variables:Dict, placeChild) -> None:
        fontGroup = font.Font(size=13,family="Arial")
        
        self.blockType = Node.NEWIFBLOCK

        self.firstValue = StringVar()
        self.firstValue.set('')
        self.operator = StringVar()
        self.secondType = StringVar()
        self.secondValue = StringVar()
        self.secondValue.set('')

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=250, width=300)

        self.background = tk.Canvas(self.widget,background="white",height=200,width=300)

        self.header = tk.Frame(self.background,height=5,width=40,bg="white")

        rhombusPoints = [
            5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,self.background.winfo_reqheight()-5,
            self.background.winfo_reqwidth()-5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,5
        ]
        self.shape = self.background.create_polygon(rhombusPoints,outline="black",fill="white",width=2)

        self.ifLabel = tk.Label(self.header, text="If", font=fontGroup, background="white")
        self.ifLabel.grid(row=1, column=0, columnspan=4)

        self.varNames = list(variables.keys())
        self.firstValue.trace('w',lambda *args:self.refresh(variables))
        self.firstItem = OptionMenu(self.header,self.firstValue,'',*self.varNames)
        self.firstItem['font']=fontGroup
        self.firstItem.grid(row=2,column=0)

        self.operatorChoice = OptionMenu(self.header, self.operator, IfBlock.operators[0] ,*IfBlock.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.grid(row=2,column=1)

        self.secondTypeItem = OptionMenu(self.header,self.secondType,*IfBlock.types)
        self.secondTypeItem['font']=fontGroup
        self.secondTypeItem.grid(row=2,column=2)

        self.secondType.trace('w',lambda *args:self.changeType())

        self.secondEntry = tk.Entry(self.header,font=fontGroup,textvariable=self.secondValue,width=10)

        self.secondValue.trace('w',lambda *args:self.refresh(variables))
        self.secondItem = OptionMenu(self.header,self.secondValue,'',*self.varNames)
        self.secondItem['font']=fontGroup
        self.secondItem.grid(row=2,column=3)

        self.trueBranchNode = TextNode(window,Node.IFTRUEBLOCK)
        self.falseBranchNode = TextNode(window,Node.IFFALSEBLOCK)

        self.trueBranchNode.lastNode.append(self)
        self.falseBranchNode.lastNode.append(self)

        self.placeChild = placeChild
        
        self.varDict = variables

        self.nextNode: Node = [self.trueBranchNode,self.falseBranchNode]
        self.lastNode: Node = []
        self.connector = []

    def refresh(self, variables:Dict):
        self.varNames = list(variables.keys())
        self.firstItem['menu'].delete(0, 'end')
        self.secondItem['menu'].delete(0, 'end')
        for name in self.varNames:
            self.firstItem['menu'].add_command(label=name, command=tk._setit(self.firstValue, name))
            self.secondItem['menu'].add_command(label=name, command=tk._setit(self.secondValue, name))

    def changeType(self):
        match self.secondType.get():
            case 'int' | 'string' | 'double':
                self.secondValue.set('')
                self.secondItem.grid_forget()
                self.secondEntry.grid(row=2,column=3)
            case 'variable':
                self.secondValue.set('')
                self.secondEntry.grid_forget()
                self.secondItem.grid(row=2,column=3)
    
    def placeNode(self,canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)
        self.header.pack()
        self.header.place(in_=self.background,anchor="c",relx=.5,rely=.5)
        self.background.pack()
        self.background.pack_propagate(False)
        self.background.place(in_=self.widget,anchor="c",relx=.5,rely=.5)

        self.placeChild(self.trueBranchNode, 0,280)
        self.placeChild(self.falseBranchNode, 300,280)

        self.window=canvas.create_window(50,0,window=self.widget, anchor="nw")
        self.connect(canvas)
    
    def activate():
        pass

    def destroy(self):
        super().destroy()
        self.trueBranchNode.destroy()
        self.falseBranchNode.destroy()

    def output():
        pass

class ForLoop(Node):

    iterators = ["i","j","k"]
    operators = ['>','<','>=','<=']
    modifiers = ['+=','-=','*=','//=']

    def __init__(self, window, choice, varDict) -> None:
        super().__init__()
        self.blockType = Node.FORLOOP
        self.parent = None

        self.size = 200
        self.layer = 0

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=self.size, width=400+self.layer*50)

        self.workspace = tk.Canvas(self.widget,bg="#FFF", height=self.size-100, width=350+self.layer*50)

        self.header = tk.Frame(self.widget,height=50,width=400+self.layer*50,bg="#e6e6e6")
        
        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="For Loop",font=fontGroup, background="#c7c7c7", width=self.widget.winfo_screenwidth())
        self.titleLabel.pack()

        self.addButton = tk.Button(self.header, text="+",command=self.addNode, height=1,width=4)
        self.addButton.pack(side="left",padx=10,pady=6)

        self.forLabel = tk.Label(self.header,text="for",font=fontGroup,bg="#e6e6e6")
        self.forLabel.pack(side="left",padx=5)

        self.iterator = StringVar()
        def updateLabel(*args):
            self.iterLabel.config(text="; "+self.iterator.get())
            self.iterLabel2.config(text="; "+self.iterator.get())

        self.iterator.trace_add("write",updateLabel)

        self.iteratorChoice = OptionMenu(self.header, self.iterator ,*ForLoop.iterators)
        self.iteratorChoice['font']=fontGroup
        self.iteratorChoice.pack(side="left")

        self.equalLabel = tk.Label(self.header,text="=",font=fontGroup,bg="#e6e6e6")
        self.equalLabel.pack(side="left")

        self.initValue = tk.IntVar()
        self.initInput = tk.Entry(self.header,textvariable=self.initValue,borderwidth=0,width=3)
        self.initInput.pack(side="left",ipady=3)

        self.iterLabel = tk.Label(self.header,text="; ",font=fontGroup,bg="#e6e6e6")
        self.iterLabel.pack(side="left")

        self.operator = StringVar()

        self.operatorChoice = OptionMenu(self.header, self.operator, *ForLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetValue = tk.IntVar()
        self.targetInput = tk.Entry(self.header,textvariable=self.targetValue,borderwidth=0,width=3)
        self.targetInput.pack(side="left",ipady=3)

        self.iterLabel2 = tk.Label(self.header,text="; ",font=fontGroup,bg="#e6e6e6")
        self.iterLabel2.pack(side="left")

        self.modifier = StringVar()

        self.modifierChoice = OptionMenu(self.header, self.modifier, *ForLoop.modifiers)
        self.modifierChoice['font']=fontGroup
        self.modifierChoice.pack(side="left")

        self.changeValue = tk.IntVar()
        self.changeInput = tk.Entry(self.header,textvariable=self.changeValue,borderwidth=0,width=3)
        self.changeInput.pack(side="left",ipady=3)

        self.nodes = []

        self.choice = choice
        self.varDict = varDict

        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []
    
    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.header.pack(side="top",anchor="nw")
        self.workspace.pack(side="top", anchor="ne")
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def _make_draggable(self,node:Node):
        node.widget.bind("<Button-1>", self._on_drag_start)
        node.widget.bind("<B1-Motion>", self._on_drag_motion)
        node.widget._node = node

    def _on_drag_start(self,event:tk.Event):
        widget = event.widget
        widget._drag_start_y = event.y

    def _on_drag_motion(self,event:tk.Event):
        y = event.y-event.widget._drag_start_y

        pos = self.workspace.bbox(event.widget._node.window)

        if pos[3] + y > self.size-100:
            y = 0
        if pos[1] + y < 0:
            y = 0

        nodeIndex = self.nodes.index(event.widget._node)
        currentMagnet = 0
        for i in range(nodeIndex):
            size=Node.sizes.get(self.nodes[i].blockType,0)
            if size == 0:
                size=self.nodes[i].size
            currentMagnet += size
        
        lastBlockHeight = Node.sizes.get(self.nodes[nodeIndex-1].blockType,0)
        if lastBlockHeight == 0:
            lastBlockHeight = self.nodes[nodeIndex-1].size
        thisBlockHeight = Node.sizes.get(self.nodes[nodeIndex].blockType,0)
        if thisBlockHeight == 0:
            thisBlockHeight = self.nodes[nodeIndex].size
        lastMagnet = currentMagnet-lastBlockHeight
        if nodeIndex == 0:
            lastMagnet = 0
        nextMagnet = currentMagnet+thisBlockHeight

        if abs(lastMagnet-(pos[1] + y)) < self.snap_distance:
            y+=lastMagnet - (pos[1] + y)
            if nodeIndex != 0:
                self.workspace.move(self.nodes[nodeIndex-1].window,0,thisBlockHeight)
                self.nodes[nodeIndex-1], self.nodes[nodeIndex] = self.nodes[nodeIndex], self.nodes[nodeIndex-1]
        elif abs(nextMagnet-(pos[1] + y)) < self.snap_distance:
            y+=nextMagnet - (pos[1] + y)
            if nodeIndex != len(self.nodes)-1:
                self.workspace.move(self.nodes[nodeIndex+1].window,0,-thisBlockHeight)
                self.nodes[nodeIndex+1], self.nodes[nodeIndex] = self.nodes[nodeIndex], self.nodes[nodeIndex+1]
        elif abs(currentMagnet-(pos[1]+y)) < self.snap_distance:
            y+=currentMagnet-(pos[1]+y)

        self.workspace.move(event.widget._node.window,0,y)

    def getDepth(self,node):
        if node == None:
            return 0
        else:
            maxDepth = 0
            for n in node.nodes:
                if Node.sizes.get(n.blockType,0) == 0:
                    depth = node.getDepth(n)
                    if depth+1 > maxDepth:
                        maxDepth = depth+1
            return maxDepth

    def addNode(self):
        choice = self.choice()
        match choice.get():
            case Node.SETVARIABLE:
                self.nodes.append(SetVariable(self.workspace, self.varDict))
            case Node.IFBLOCK:
                self.nodes.append(IfBlock(self.workspace,self.varDict))
            case Node.FORLOOP:
                loop = ForLoop(self.workspace,self.choice,self.varDict)
                self.nodes.append(loop)
                loop.parent = self
            case Node.WHILELOOP:
                self.nodes.append(SetVariable(self.workspace,self.varDict))
        
        self.nodes[-1].placeNode(self.workspace)
        self._make_draggable(self.nodes[-1])
        self.adjustSize()
        if self.parent != None:
            self.parent.adjustSize()
        nodeIndex = len(self.nodes)-1
        currentMagnet = 0
        for i in range(nodeIndex):
            size=Node.sizes.get(self.nodes[i].blockType,0)
            if size == 0:
                size=self.nodes[i].size
            currentMagnet += size
        self.workspace.move(self.nodes[-1].window,0,currentMagnet)
          
    def adjustSize(self):
        self.size = 0
        for node in self.nodes:
            size=self.sizes.get(node.blockType,0)
            if size == 0:
                self.size+=node.size
            else:
                self.size+=size
        self.size += 100
        self.layer = self.getDepth(self)
        self.widget.configure(height=self.size,width=400+self.layer*50)
        self.workspace.configure(height=self.size-100,width=350+self.layer*50)

class WhileLoop(Node):

    operators = ['>','<','>=','<=']

    def __init__(self, window, choice, varDict:Dict) -> None:
        super().__init__()
        self.blockType = Node.WHILELOOP
        self.parent = None

        self.size = 200
        self.layer = 0

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=self.size, width=400+self.layer*50)

        self.workspace = tk.Canvas(self.widget,bg="#FFF", height=self.size-100, width=350+self.layer*50)

        self.header = tk.Frame(self.widget,height=50,width=400+self.layer*50,bg="#e6e6e6")
        
        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="While Loop",font=fontGroup, background="#c7c7c7", width=self.widget.winfo_screenwidth())
        self.titleLabel.pack()

        self.addButton = tk.Button(self.header, text="+",command=self.addNode, height=1,width=4)
        self.addButton.pack(side="left",padx=10,pady=6)

        self.whileLabel = tk.Label(self.header,text="while",font=fontGroup,bg="#e6e6e6")
        self.whileLabel.pack(side="left",padx=5)

        self.var = StringVar()

        self.varChoice = OptionMenu(self.header, self.var, *varDict)
        self.varChoice['font']=fontGroup
        self.varChoice.pack(side="left")

        self.operator = StringVar()

        self.operatorChoice = OptionMenu(self.header, self.operator, *ForLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetType = StringVar()

        self.targetTypeChoice = OptionMenu(self.header,self.targetType,*IfBlock.types)
        self.targetTypeChoice['font']=fontGroup
        self.targetTypeChoice.pack(side="left")

        self.targetType.trace('w',lambda *args:self.changeType())

        self.targetValue = StringVar()

        self.targetEntry = tk.Entry(self.header,font=fontGroup,textvariable=self.targetValue,width=10)
        self.varNames = varDict.keys()

        self.targetValue.trace('w',lambda *args:self.refresh(varDict))
        self.targetChoice = OptionMenu(self.header,self.targetValue,*self.varNames)
        self.targetChoice['font']=fontGroup
        self.targetChoice.pack(side="left")

        self.nodes = []

        self.choice = choice
        self.varDict = varDict

        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []
    
    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.header.pack(side="top",anchor="nw")
        self.workspace.pack(side="top", anchor="ne")
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def changeType(self):
        match self.targetType.get():
            case 'int' | 'string' | 'double':
                self.targetValue.set('')
                self.targetChoice.pack_forget()
                self.targetEntry.pack(side="left")
            case 'variable':
                self.targetValue.set('')
                self.targetEntry.pack_forget()
                self.targetChoice.pack(side="left")

    def refresh(self,varDict:Dict):
        self.varNames = list(varDict.keys())
        self.targetChoice['menu'].delete(0, 'end')
        for name in self.varNames:
            self.targetChoice['menu'].add_command(label=name, command=tk._setit(self.targetValue, name))

    def _make_draggable(self,node:Node):
        node.widget.bind("<Button-1>", self._on_drag_start)
        node.widget.bind("<B1-Motion>", self._on_drag_motion)
        node.widget._node = node

    def _on_drag_start(self,event:tk.Event):
        widget = event.widget
        widget._drag_start_y = event.y

    def _on_drag_motion(self,event:tk.Event):
        y = event.y-event.widget._drag_start_y

        pos = self.workspace.bbox(event.widget._node.window)

        if pos[3] + y > self.size-100:
            y = 0
        if pos[1] + y < 0:
            y = 0

        nodeIndex = self.nodes.index(event.widget._node)
        currentMagnet = 0
        for i in range(nodeIndex):
            size=Node.sizes.get(self.nodes[i].blockType,0)
            if size == 0:
                size=self.nodes[i].size
            currentMagnet += size
        
        lastBlockHeight = Node.sizes.get(self.nodes[nodeIndex-1].blockType,0)
        if lastBlockHeight == 0:
            lastBlockHeight = self.nodes[nodeIndex-1].size
        thisBlockHeight = Node.sizes.get(self.nodes[nodeIndex].blockType,0)
        if thisBlockHeight == 0:
            thisBlockHeight = self.nodes[nodeIndex].size
        lastMagnet = currentMagnet-lastBlockHeight
        if nodeIndex == 0:
            lastMagnet = 0
        nextMagnet = currentMagnet+thisBlockHeight

        if abs(lastMagnet-(pos[1] + y)) < self.snap_distance:
            y+=lastMagnet - (pos[1] + y)
            if nodeIndex != 0:
                self.workspace.move(self.nodes[nodeIndex-1].window,0,thisBlockHeight)
                self.nodes[nodeIndex-1], self.nodes[nodeIndex] = self.nodes[nodeIndex], self.nodes[nodeIndex-1]
        elif abs(nextMagnet-(pos[1] + y)) < self.snap_distance:
            y+=nextMagnet - (pos[1] + y)
            if nodeIndex != len(self.nodes)-1:
                self.workspace.move(self.nodes[nodeIndex+1].window,0,-thisBlockHeight)
                self.nodes[nodeIndex+1], self.nodes[nodeIndex] = self.nodes[nodeIndex], self.nodes[nodeIndex+1]
        elif abs(currentMagnet-(pos[1]+y)) < self.snap_distance:
            y+=currentMagnet-(pos[1]+y)

        self.workspace.move(event.widget._node.window,0,y)

    def getDepth(self,node):
        if node == None:
            return 0
        else:
            maxDepth = 0
            for n in node.nodes:
                if Node.sizes.get(n.blockType,0) == 0:
                    depth = node.getDepth(n)
                    if depth+1 > maxDepth:
                        maxDepth = depth+1
            return maxDepth

    def addNode(self):
        choice = self.choice()
        match choice.get():
            case Node.SETVARIABLE:
                self.nodes.append(SetVariable(self.workspace, self.varDict))
            case Node.IFBLOCK:
                self.nodes.append(IfBlock(self.workspace,self.varDict))
            case Node.FORLOOP:
                loop = ForLoop(self.workspace,self.choice,self.varDict)
                self.nodes.append(loop)
                loop.parent = self
            case Node.WHILELOOP:
                self.nodes.append(SetVariable(self.workspace,self.varDict))
        
        self.nodes[-1].placeNode(self.workspace)
        self._make_draggable(self.nodes[-1])
        self.adjustSize()
        if self.parent != None:
            self.parent.adjustSize()
        nodeIndex = len(self.nodes)-1
        currentMagnet = 0
        for i in range(nodeIndex):
            size=Node.sizes.get(self.nodes[i].blockType,0)
            if size == 0:
                size=self.nodes[i].size
            currentMagnet += size
        self.workspace.move(self.nodes[-1].window,0,currentMagnet)
          
    def adjustSize(self):
        self.size = 0
        for node in self.nodes:
            size=self.sizes.get(node.blockType,0)
            if size == 0:
                self.size+=node.size
            else:
                self.size+=size
        self.size += 100
        self.layer = self.getDepth(self)
        self.widget.configure(height=self.size,width=400+self.layer*50)
        self.workspace.configure(height=self.size-100,width=350+self.layer*50)

class NewWhileLoop(Node):
    
    operators = ['>','<','>=','<=']

    def __init__(self, window, varDict:Dict,placeChild) -> None:
        super().__init__()
        self.blockType = Node.NEWWHILELOOP

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=250, width=300)

        self.background = tk.Canvas(self.widget,background="white",height=200,width=300)

        self.header = tk.Frame(self.widget,height=50,width=300,bg="white")
        
        rhombusPoints = [
            5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,self.background.winfo_reqheight()-5,
            self.background.winfo_reqwidth()-5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,5
        ]
        self.shape = self.background.create_polygon(rhombusPoints,outline="black",fill="white",width=2)

        fontGroup = font.Font(size=13,family="Arial")

        self.whileLabel = tk.Label(self.header,text="while",font=fontGroup,bg="white")
        self.whileLabel.pack(side="left",padx=5)

        self.var = StringVar()

        self.varChoice = OptionMenu(self.header, self.var, *varDict)
        self.varChoice['font']=fontGroup
        self.varChoice.pack(side="left")

        self.operator = StringVar()

        self.operatorChoice = OptionMenu(self.header, self.operator, *ForLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetType = StringVar()

        self.targetTypeChoice = OptionMenu(self.header,self.targetType,*IfBlock.types)
        self.targetTypeChoice['font']=fontGroup
        self.targetTypeChoice.pack(side="left")

        self.targetType.trace('w',lambda *args:self.changeType())

        self.targetValue = StringVar()

        self.targetEntry = tk.Entry(self.header,font=fontGroup,textvariable=self.targetValue,width=10)
        self.varNames = varDict.keys()

        self.targetValue.trace('w',lambda *args:self.refresh(varDict))
        self.targetChoice = OptionMenu(self.header,self.targetValue,*self.varNames)
        self.targetChoice['font']=fontGroup
        self.targetChoice.pack(side="left")

        self.loopEndNode = TextNode(window,Node.LOOPENDBLOCK)

        self.loopEndNode.lastNode.append(self)

        self.placeChild = placeChild

        self.varDict = varDict

        self.nextNode: Node = [self.loopEndNode]
        self.lastNode: Node = []
        self.connector = []
    
    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)
        self.widget.grid_rowconfigure(0,weight=1)
        self.widget.grid_columnconfigure(0,weight=1)

        self.header.grid(row=0,column=0)
        self.background.pack()
        self.background.pack_propagate(False)
        self.background.place(in_=self.widget,anchor="c",relx=.5,rely=.5)

        self.placeChild(self.loopEndNode, 100, 300)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")
        self.connect(canvas)

    def changeType(self):
        match self.targetType.get():
            case 'int' | 'string' | 'double':
                self.targetValue.set('')
                self.targetChoice.pack_forget()
                self.targetEntry.pack(side="left")
            case 'variable':
                self.targetValue.set('')
                self.targetEntry.pack_forget()
                self.targetChoice.pack(side="left")

    def refresh(self,varDict:Dict):
        self.varNames = list(varDict.keys())
        self.targetChoice['menu'].delete(0, 'end')
        for name in self.varNames:
            self.targetChoice['menu'].add_command(label=name, command=tk._setit(self.targetValue, name))

    def connect(self, canva: tk.Canvas):
        if len(self.nextNode) > 0:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")

            pos = canva.bbox(self.window)
            ax0 = pos[0]
            ay0 = pos[1]
            ax1 = pos[2]
            ay1 = pos[3]

            x0 = (ax0 + ax1) / 2
            y0 = (ay0 + ay1) / 2

            for node in self.nextNode:
                pos = canva.bbox(node.window)
                bx0 = pos[0]
                by0 = pos[1]
                bx1 = pos[2]
                by1 = pos[3]

                x1 = (bx0 + bx1) / 2
                y1 = (by0 + by1) / 2

                if node.blockType == Node.LOOPENDBLOCK:
                    startConnnector = canva.create_line(
                        x0,y0,x0+200,y0,fill="black",width=4, tags=("loopEndConnector"))
                    midConnector = canva.create_line(
                        x0+200,y0,x0+200,y1,fill="black",width=4,tags=("loopEndConnector"))
                    endConnector = canva.create_line(
                        x0+200,y1,x1,y1,fill="black",width=4,tags=("loopEndConnector"))
                    canva.tag_lower(startConnnector)
                    canva.tag_lower(midConnector)
                    canva.tag_lower(endConnector)
                    self.connector.append((node,startConnnector))
                    self.connector.append((node,midConnector))
                    self.connector.append((node,endConnector))
                else:
                    line_id = canva.create_line(
                        x0, y0, x1, y1, fill="black", width=4, tags=())
                    canva.tag_lower(line_id)
                    self.connector.append((node, line_id))
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)

    def destroy(self):
        super().destroy()
        self.loopEndNode.destroy()

class NewForLoop(Node):
    
    iterators = ["i","j","k"]
    operators = ['>','<','>=','<=']
    modifiers = ['+=','-=','*=','//=']

    def __init__(self, window, varDict, placeChild) -> None:
        super().__init__()
        self.blockType = Node.NEWFORLOOP

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=250, width=300)

        self.background = tk.Canvas(self.widget,background="white",height=200,width=300)

        self.header = tk.Frame(self.widget,height=50,width=300,bg="white")

        rhombusPoints = [
            5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,self.background.winfo_reqheight()-5,
            self.background.winfo_reqwidth()-5,self.background.winfo_reqheight()/2,
            self.background.winfo_reqwidth()/2,5
        ]
        self.shape = self.background.create_polygon(rhombusPoints,outline="black",fill="white",width=2)
        
        fontGroup = font.Font(size=13,family="Arial")

        self.forLabel = tk.Label(self.header,text="for",font=fontGroup,bg="white")
        self.forLabel.pack(side="left",padx=5)

        self.iterator = StringVar()
        def updateLabel(*args):
            self.iterLabel.config(text="; "+self.iterator.get())
            self.iterLabel2.config(text="; "+self.iterator.get())

        self.iterator.trace_add("write",updateLabel)

        self.iteratorChoice = OptionMenu(self.header, self.iterator ,*ForLoop.iterators)
        self.iteratorChoice['font']=fontGroup
        self.iteratorChoice.pack(side="left")

        self.equalLabel = tk.Label(self.header,text="=",font=fontGroup,bg="white")
        self.equalLabel.pack(side="left")

        self.initValue = tk.IntVar()
        self.initInput = tk.Entry(self.header,textvariable=self.initValue,borderwidth=0,width=3)
        self.initInput.pack(side="left",ipady=3)

        self.iterLabel = tk.Label(self.header,text="; ",font=fontGroup,bg="white")
        self.iterLabel.pack(side="left")

        self.operator = StringVar()

        self.operatorChoice = OptionMenu(self.header, self.operator, *ForLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetValue = tk.IntVar()
        self.targetInput = tk.Entry(self.header,textvariable=self.targetValue,borderwidth=0,width=3)
        self.targetInput.pack(side="left",ipady=3)

        self.iterLabel2 = tk.Label(self.header,text="; ",font=fontGroup,bg="white")
        self.iterLabel2.pack(side="left")

        self.modifier = StringVar()

        self.modifierChoice = OptionMenu(self.header, self.modifier, *ForLoop.modifiers)
        self.modifierChoice['font']=fontGroup
        self.modifierChoice.pack(side="left")

        self.changeValue = tk.IntVar()
        self.changeInput = tk.Entry(self.header,textvariable=self.changeValue,borderwidth=0,width=3)
        self.changeInput.pack(side="left",ipady=3)

        self.loopEndNode = TextNode(window,Node.LOOPENDBLOCK)

        self.loopEndNode.lastNode.append(self)

        self.placeChild = placeChild

        self.varDict = varDict

        self.nextNode: Node = [self.loopEndNode]
        self.lastNode: Node = []
        self.connector = []
    
    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)
        self.widget.grid_rowconfigure(0,weight=1)
        self.widget.grid_columnconfigure(0,weight=1)

        self.background.pack()
        self.background.pack_propagate(False)
        self.background.place(in_=self.widget,anchor="c",relx=.5,rely=.5)
        self.header.grid(row=0,column=0)

        self.placeChild(self.loopEndNode, 100, 300)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")
        self.connect(canvas)

    def connect(self, canva: tk.Canvas):
        if len(self.nextNode) > 0:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")

            pos = canva.bbox(self.window)
            ax0 = pos[0]
            ay0 = pos[1]
            ax1 = pos[2]
            ay1 = pos[3]

            x0 = (ax0 + ax1) / 2
            y0 = (ay0 + ay1) / 2

            for node in self.nextNode:
                pos = canva.bbox(node.window)
                bx0 = pos[0]
                by0 = pos[1]
                bx1 = pos[2]
                by1 = pos[3]

                x1 = (bx0 + bx1) / 2
                y1 = (by0 + by1) / 2

                if node.blockType == Node.LOOPENDBLOCK:
                    startConnnector = canva.create_line(
                        x0,y0,x0+200,y0,fill="black",width=4, tags=("loopEndConnector"))
                    midConnector = canva.create_line(
                        x0+200,y0,x0+200,y1,fill="black",width=4,tags=("loopEndConnector"))
                    endConnector = canva.create_line(
                        x0+200,y1,x1,y1,fill="black",width=4,tags=("loopEndConnector"))
                    canva.tag_lower(startConnnector)
                    canva.tag_lower(midConnector)
                    canva.tag_lower(endConnector)
                    self.connector.append((node,startConnnector))
                    self.connector.append((node,midConnector))
                    self.connector.append((node,endConnector))
                else:
                    line_id = canva.create_line(
                        x0, y0, x1, y1, fill="black", width=4, tags=())
                    canva.tag_lower(line_id)
                    self.connector.append((node, line_id))
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)

class TextNode(Node):

    textDict = {Node.IFTRUEBLOCK:"True", Node.IFFALSEBLOCK:"False", Node.LOOPENDBLOCK:"End Loop"}

    def __init__(self, window, type) -> None:
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=75, width=100)

        self.blockType = type

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text=TextNode.textDict[type],font=fontGroup, background="#e6e6e6", width=10)
        self.titleLabel.grid(row=0,column=0)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        
        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []

    def placeNode(self, canvas, xpos, ypos):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(xpos,ypos,window=self.widget, anchor="nw")

    def activate(self, time: int):
        self.widget.after(time, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            time+500, lambda: self.widget.config(background='#e6e6e6'))

    def output(self):
        pass

    def destroy(self):
        self.widget.destroy()

    def deleteConnectors(self, canvas: tk.Canvas):
        try:
            for line in self.connector:
                canvas.delete(line[1])
            self.connector = []
        except:
            print("no existing line")

    def removeConnector(self,canvas:tk.Canvas,node):
        try:
            for line in self.connector:
                if line[0] == node:
                    canvas.delete(line[1])
        except:
            print("no such line or node")