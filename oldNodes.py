import tkinter as tk
import math
from node import Node, SetVariable
from tkinter import BOTH, LEFT, RIGHT, X, OptionMenu, StringVar, ttk, messagebox, font
from typing import Any, Dict, List

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

        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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

        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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

        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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