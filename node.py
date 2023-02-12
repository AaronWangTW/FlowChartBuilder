import tkinter as tk
from tkinter import BOTH, LEFT, RIGHT, X, OptionMenu, StringVar, ttk, messagebox, font
from typing import Any, Dict, List
from appConsole import AppConsole

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
    STARTBLOCK = "Start Block"
    ENDBLOCK = "End Block"
    INPUTBLOCK = "Input Block"
    OUTPUTBLOCK = "Output Block"

    types = [SETVARIABLE, NEWIFBLOCK, NEWWHILELOOP, NEWFORLOOP, CHANGEVARIABLE, INPUTBLOCK, OUTPUTBLOCK]

    descriptions = {
        SETVARIABLE: "set up a variable of any customized name",
        NEWIFBLOCK: "If statement block that execute correspondingly to the result of the if statment",
        NEWWHILELOOP: "A block that can execute its inside contents in a while loop structure",
        NEWFORLOOP: "A block that can execute its inside contents in a for loop structure",
        CHANGEVARIABLE: "Change the value of an existing variable",
        STARTBLOCK: "The starting point of the flowchart",
        ENDBLOCK: "The stopping point of the flowchart",
        INPUTBLOCK: "Getting external input from flowchart console",
        OUTPUTBLOCK: "Outputting values to the flowchart console"
    }

    def __init__(self) -> None:
        self.widget: tk.Widget = None
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []
        self.window = ""
        self.id = -1

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

    def placeNode(self):
        self.widget.pack()

    def activate(self):
        pass

    def output(self,varDict:Dict, console:AppConsole):
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
        for line in self.connector:
            if line[0] == node:
                canvas.delete(line[1])
                self.connector.remove(line)

    def run(self,varDict:Dict, console:AppConsole):
        self.output(varDict, console)
        self.activate()
        for node in self.nextNode:
            self.widget.after(500,lambda:node.run(varDict, console))

class SetVariable(Node):

    types = ['int','string','double']

    def __init__(self, window, varDict) -> None:
        super().__init__()
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
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def setVarName(self, varName: str):
        self.varName = varName

    def output(self, varDict: Dict, console:AppConsole = None):
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
            if console:
                console.print(f"Variable: {name} value updated to {value}")
                console.addVariableTrack(name,varDict)
        self.lastVarName = self.varName.get()
        
class ChangeVariable(Node):

    types = ['input','var']
    operators = ['=','+=','-=','/=','//=','%=','*=']
    
    def __init__(self, window, varDict) -> None:
        super().__init__()
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
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))
    
    def refresh(self, variables:Dict):
        self.varNames = list(variables.keys())
        self.firstVarChoice['menu'].delete(0, 'end')
        for name in self.varNames:
            self.firstVarChoice['menu'].add_command(label=name, command=tk._setit(self.firstVar, name))

    def output(self, varDict: Dict, console:AppConsole = None):
        if self.firstVar.get() != "":
            name = self.firstVar.get()
            value = self.value.get()
            match varDict[name]:
                case int():
                    value = int(value)
                case float():
                    value = float(value)
                case str():
                    pass
                case _:
                    raise Exception("Unexpected variable type detected")

            match self.operator.get():
                case '=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] = value
                    else:
                        varDict[name] = varDict[value]
                case '+=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] += value
                    else:
                        varDict[name] += varDict[value]
                case '-=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] -= value
                    else:
                        varDict[name] -= varDict[value]
                case '/=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] /= value
                    else:
                        varDict[name] /= varDict[value]
                case '//=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] //= value
                    else:
                        varDict[name] //= varDict[value]
                case '%=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] %= value
                    else:
                        varDict[name] %= varDict[value]
                case '*=':
                    if self.typeChoice.get() == 'input':
                        varDict[name] *= value
                    else:
                        varDict[name] *= varDict[value]
            if console:
                console.print(f"Variable: {name} value changed to {varDict[name]}")
                console.addVariableTrack(name,varDict)

class NewIfBlock(Node):
    
    operators = ['>','<','==','!=','>=','<=']
    types = ['int','string','double','var']

    comparators = {
    '>':"__gt__",
    '<':"__lt__",
    '==':"__eq__",
    '!=':"__ne__",
    '>=':"__ge__",
    '<=':"__le__"
    }

    def __init__(self, window, variables:Dict, placeChild) -> None:
        super().__init__()
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

        self.operatorChoice = OptionMenu(self.header, self.operator, NewIfBlock.operators[0] ,*NewIfBlock.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.grid(row=2,column=1)

        self.secondTypeItem = OptionMenu(self.header,self.secondType,*NewIfBlock.types)
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

        self.nextNode: List[Node] = [self.trueBranchNode,self.falseBranchNode]
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
    
    def evaluate(self,varDict:Dict):
        result = None

        varName = self.firstValue.get()
        value = self.secondValue.get()

        comp = NewIfBlock.comparators.get(self.operator.get())


        match self.secondType.get():
            case 'int':
                result = varDict[varName].__getattribute__(comp)(int(value))
            case'string':
                result = varDict[varName].__getattribute__(comp)(value)
            case 'double':
                result = varDict[varName].__getattribute__(comp)(float(value))
            case 'var':
                result = varDict[varName].__getattribute__(comp)(varDict[value])

        return result

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def destroy(self):
        super().destroy()
        self.trueBranchNode.destroy()
        self.falseBranchNode.destroy()

    def output(self,varDict:Dict, console:AppConsole, result:bool):
        console.print(f"Evaluate: {self.firstValue.get()} {self.operator.get()} {self.secondValue.get()} - {result}")

    def run(self, varDict: Dict, console:AppConsole):
        self.activate()
        result = self.evaluate(varDict)
        self.output(varDict, console, result)
        if result:
            self.widget.after(500,lambda:self.trueBranchNode.run(varDict, console))
        else:
            self.widget.after(500,lambda:self.falseBranchNode.run(varDict, console))

class NewWhileLoop(Node):
    
    operators = ['>','<','==','!=','>=','<=']

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

        self.operatorChoice = OptionMenu(self.header, self.operator, *NewWhileLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetType = StringVar()

        self.targetTypeChoice = OptionMenu(self.header,self.targetType,*NewIfBlock.types)
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

        self.loopEndNode = LoopEndBlock(window,self)

        self.placeChild = placeChild

        self.varDict = varDict

        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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

    def connectLoopEndNode(self,canva:tk.Canvas):
        pos = canva.bbox(self.window)
        ax0 = pos[0]
        ay0 = pos[1]
        ax1 = pos[2]
        ay1 = pos[3]
        x0 = (ax0 + ax1) / 2
        y0 = (ay0 + ay1) / 2
        pos = canva.bbox(self.loopEndNode.window)
        bx0 = pos[0]
        by0 = pos[1]
        bx1 = pos[2]
        by1 = pos[3]
        x1 = (bx0 + bx1) / 2
        y1 = (by0 + by1) / 2
        startConnnector = canva.create_line(
            x0, y0, x0+200, y0, fill="black", width=4, tags=("loopEndConnector"))
        midConnector = canva.create_line(
            x0+200, y0, x0+200, y1, fill="black", width=4, tags=("loopEndConnector"))
        endConnector = canva.create_line(
            x0+200, y1, x1, y1, fill="black", width=4, tags=("loopEndConnector"))
        canva.tag_lower(startConnnector)
        canva.tag_lower(midConnector)
        canva.tag_lower(endConnector)
        self.connector.append((self.loopEndNode, startConnnector))
        self.connector.append((self.loopEndNode, midConnector))
        self.connector.append((self.loopEndNode, endConnector))

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

                line_id = canva.create_line(
                    x0, y0, x1, y1, fill="black", width=4, tags=())
                canva.tag_lower(line_id)
                self.connector.append((node, line_id))
        else:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")
            
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)
        
        self.connectLoopEndNode(canva)

    def evaluate(self,varDict:Dict):
        result = None

        varName = self.var.get()
        value = self.targetValue.get()

        match self.operator.get():
            case '>':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] > int(value)
                    case'string':
                        result = varDict[varName] > value
                    case 'double':
                        result = varDict[varName] > float(value)
                    case 'var':
                        result = varDict[varName] > varDict[value]
            case '<':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] < int(value)
                    case'string':
                        result = varDict[varName] < value
                    case 'double':
                        result = varDict[varName] < float(value)
                    case 'var':
                        result = varDict[varName] < varDict[value]
            case '==':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] == int(value)
                    case'string':
                        result = varDict[varName] == value
                    case 'double':
                        result = varDict[varName] == float(value)
                    case 'var':
                        result = varDict[varName] == varDict[value]
            case '!=':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] != int(value)
                    case'string':
                        result = varDict[varName] != value
                    case 'double':
                        result = varDict[varName] != float(value)
                    case 'var':
                        result = varDict[varName] != varDict[value]
            case '>=':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] >= int(value)
                    case'string':
                        result = varDict[varName] >= value
                    case 'double':
                        result = varDict[varName] >= float(value)
                    case 'var':
                        result = varDict[varName] >= varDict[value]
            case '<=':
                match self.targetType.get():
                    case 'int':
                        result = varDict[varName] <= int(value)
                    case'string':
                        result = varDict[varName] <= value
                    case 'double':
                        result = varDict[varName] <= float(value)
                    case 'var':
                        result = varDict[varName] <= varDict[value]

        return result

    def output(self, varDict:Dict, console:AppConsole, result:bool):
        text = ""
        if result:
            text = "loop continues"
        else:
            text = "loop breaks"
        console.print(f"While {self.var.get()} {self.operator.get()} {self.targetValue.get()} - {text}")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def destroy(self):
        super().destroy()
        self.loopEndNode.destroy()

    def run(self, varDict: Dict, console:AppConsole):
        self.activate()
        result = self.evaluate(varDict)
        self.output(varDict, console, result)
        if result:
            for node in self.nextNode:
                self.widget.after(500,lambda:node.run(varDict, console))
        else:
            self.widget.after(500,lambda:self.loopEndNode.run(varDict, console, breakLoop=True))

class NewForLoop(Node):
    
    iterators = ["i","j","k"]
    operators = ['>','<','>=','<=']
    modifiers = ['+=','-=','*=','//=']

    def __init__(self, window, varDict, placeChild) -> None:
        super().__init__()
        self.blockType = Node.NEWFORLOOP

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=250, width=350)

        self.background = tk.Canvas(self.widget,background="white",height=200,width=350)

        self.header = tk.Frame(self.widget,height=50,width=300,bg="white")

        self.loopInit = True

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
        self.iterator.trace_add("write",lambda name, index, mode, value=self.iterator: self.putIterator(varDict))

        self.iteratorChoice = OptionMenu(self.header, self.iterator ,*NewForLoop.iterators)
        self.iteratorChoice['font']=fontGroup
        self.iteratorChoice.pack(side="left")

        self.equalLabel = tk.Label(self.header,text="=",font=fontGroup,bg="white")
        self.equalLabel.pack(side="left")

        self.initValue = tk.IntVar()
        self.initInput = tk.Entry(self.header,textvariable=self.initValue,borderwidth=0,width=3)
        self.initInput.pack(side="left",ipady=3)

        self.initValue.trace_add("write",lambda name, index, mode, value=self.initValue: self.putIterator(varDict))

        self.iterLabel = tk.Label(self.header,text="; ",font=fontGroup,bg="white")
        self.iterLabel.pack(side="left")

        self.operator = StringVar()

        self.operatorChoice = OptionMenu(self.header, self.operator, *NewForLoop.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.pack(side="left")

        self.targetValue = tk.IntVar()
        self.targetInput = tk.Entry(self.header,textvariable=self.targetValue,borderwidth=0,width=3)
        self.targetInput.pack(side="left",ipady=3)

        self.iterLabel2 = tk.Label(self.header,text="; ",font=fontGroup,bg="white")
        self.iterLabel2.pack(side="left")

        self.modifier = StringVar()

        self.modifierChoice = OptionMenu(self.header, self.modifier, *NewForLoop.modifiers)
        self.modifierChoice['font']=fontGroup
        self.modifierChoice.pack(side="left")

        self.changeValue = tk.IntVar()
        self.changeInput = tk.Entry(self.header,textvariable=self.changeValue,borderwidth=0,width=3)
        self.changeInput.pack(side="left",ipady=3)

        self.loopEndNode = LoopEndBlock(window,self)

        self.placeChild = placeChild

        self.varDict = varDict

        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
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

    def connectLoopEndNode(self,canva:tk.Canvas):
        pos = canva.bbox(self.window)
        ax0 = pos[0]
        ay0 = pos[1]
        ax1 = pos[2]
        ay1 = pos[3]
        x0 = (ax0 + ax1) / 2
        y0 = (ay0 + ay1) / 2
        pos = canva.bbox(self.loopEndNode.window)
        bx0 = pos[0]
        by0 = pos[1]
        bx1 = pos[2]
        by1 = pos[3]
        x1 = (bx0 + bx1) / 2
        y1 = (by0 + by1) / 2
        startConnnector = canva.create_line(
            x0, y0, x0+200, y0, fill="black", width=4, tags=("loopEndConnector"))
        midConnector = canva.create_line(
            x0+200, y0, x0+200, y1, fill="black", width=4, tags=("loopEndConnector"))
        endConnector = canva.create_line(
            x0+200, y1, x1, y1, fill="black", width=4, tags=("loopEndConnector"))
        canva.tag_lower(startConnnector)
        canva.tag_lower(midConnector)
        canva.tag_lower(endConnector)
        self.connector.append((self.loopEndNode, startConnnector))
        self.connector.append((self.loopEndNode, midConnector))
        self.connector.append((self.loopEndNode, endConnector))

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

                line_id = canva.create_line(
                    x0, y0, x1, y1, fill="black", width=4, tags=())
                canva.tag_lower(line_id)
                self.connector.append((node, line_id))
        else:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")
            
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)
        
        self.connectLoopEndNode(canva)

    def evaluate(self,varDict:Dict):
        result = None

        varName = self.iterator.get()
        value = self.targetValue.get()

        match self.operator.get():
            case '>':
                result = varDict[varName] > int(value)
            case '<':
                result = varDict[varName] < int(value)
            case '>=':
                result = varDict[varName] >= int(value)
            case '<=':
                result = varDict[varName] <= int(value)

        return result

    def putIterator(self, varDict:Dict):
        if self.iterator.get() != "":
            name = self.iterator.get()
            value = self.initValue.get()
            if value != "":
                varDict[name] = int(value)

    def modifyIterator(self,varDict:Dict):
        iterator = self.iterator.get()
        value = int(self.changeValue.get())
        match self.modifier.get():
            case '+=':
                varDict[iterator]+=value
            case '-=':
                varDict[iterator]-=value
            case '*=':
                varDict[iterator]*=value
            case '//=':
                varDict[iterator]//=value

    def output(self, varDict:Dict, console:AppConsole, result):

        if self.loopInit:
            self.putIterator(varDict)
            self.loopInit = False
        else:
            self.modifyIterator(varDict)

        text = ""
        if result:
            text = "loop continues"
        else:
            text = "loop breaks"
        console.print(f"For {self.iterator.get()} {self.operator.get()} {self.targetValue.get()} - {text}, {self.iterator.get()} = {varDict[self.iterator.get()]}")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def run(self, varDict: Dict, console:AppConsole):
        self.activate()
        result = self.evaluate(varDict)
        self.output(varDict,console,result)
        if result:
            for node in self.nextNode:
                self.widget.after(500,lambda:node.run(varDict, console))
        else:
            self.loopInit = True
            self.widget.after(500,lambda:self.loopEndNode.run(varDict,console,True))
    
    def destroy(self):
        super().destroy()
        self.loopEndNode.destroy()

class TextNode(Node):

    textDict = {Node.IFTRUEBLOCK:"True", Node.IFFALSEBLOCK:"False", Node.LOOPENDBLOCK:"End Loop"}

    def __init__(self, window, type) -> None:
        super().__init__()
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=75, width=100)

        self.blockType = type

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text=TextNode.textDict[type],font=fontGroup, background="#e6e6e6", width=10)
        self.titleLabel.grid(row=0,column=0)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas, xpos, ypos):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(xpos,ypos,window=self.widget, anchor="nw")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def output(self,varDict, console:AppConsole):
        pass

    def removeConnector(self, canvas: tk.Canvas, node):
        if self.blockType == Node.IFTRUEBLOCK or self.blockType == Node.IFFALSEBLOCK or self.blockType == Node.LOOPENDBLOCK:
            self.deleteConnectors(canvas)
            for node in self.nextNode:
                node.lastNode.remove(self)
                node.removeConnector(canvas,self)
            return

        super().removeConnector(canvas, node)

class LoopEndBlock(TextNode):

    def __init__(self, window, parentLoop:Node) -> None:
        self.id = -1
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=75, width=100)

        self.blockType = Node.LOOPENDBLOCK

        self.parentLoop = parentLoop

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="End Loop",font=fontGroup, background="#e6e6e6", width=10)
        self.titleLabel.grid(row=0,column=0)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def activate(self, breakLoop=False):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def output(self,varDict:Dict,console:AppConsole ,breakLoop = False):
        pass

    def run(self, varDict: Dict,console:AppConsole, breakLoop = False):
        self.output(varDict,console)
        self.activate()
        if breakLoop:
            for node in self.nextNode:
                self.widget.after(500,lambda:node.run(varDict, console))
        else:
            self.widget.after(500,lambda:self.parentLoop.run(varDict, console))
            
    
    def connect(self, canva: tk.Canvas):
        super().connect(canva)
        self.parentLoop.connect(canva)

class InputBlock(Node):
    
    def __init__(self, window, variables:Dict) -> None:
        super().__init__()
        self.inputCount = 1

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=75, width=150+self.inputCount*50)

        self.blockType = Node.INPUTBLOCK

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="Input",font=fontGroup, background="#e6e6e6", width=4)
        self.titleLabel.grid(row=0,column=0)

        initVar = StringVar()
        self.inputVars: List[tk.StringVar] = [initVar]

        initEntry = tk.Entry(self.widget,textvariable=initVar,borderwidth=0,width=6)
        self.inputEntries: List[tk.Entry] = [initEntry]
        initEntry.grid(row=0,column=1) 

        self.addButton = tk.Button(self.widget,text="+", command=self.addInput)
        self.addButton.grid(row=0,column=2)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_columnconfigure(1,weight=1)
        self.widget.grid_columnconfigure(2,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)

        self.variables = variables
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def addInput(self):
        self.inputVars.append(StringVar())
        self.inputCount+=1
        self.inputEntries.append(tk.Entry(self.widget,textvariable=self.inputVars[self.inputCount-1],borderwidth=0,width=6))
        self.inputEntries[self.inputCount-1].grid(row=0,column=self.inputCount)
        self.addButton.grid(row=0,column=self.inputCount+1)
        self.widget.grid_columnconfigure(self.inputCount+1,weight=1)
        self.widget.config(width=150+self.inputCount*50)

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def output(self,varDict, console:AppConsole):
        for var in self.inputVars:
            console.input(var.get(),varDict)
            console.print(f"Variable: {var.get()} inputted")
            console.addVariableTrack(var.get(),varDict)

class OutputBlock(Node):

    types = ['var','string']
    
    def __init__(self, window, variables:Dict) -> None:
        super().__init__()
        self.outputCount = 1

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=75, width=150+self.outputCount*60)

        self.blockType = Node.OUTPUTBLOCK

        self.fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="Output",font=self.fontGroup, background="#e6e6e6", width=5)
        self.titleLabel.grid(row=0,column=0)

        self.initOutput = StringVar()
        self.outputs: List[tk.StringVar] = [self.initOutput]

        self.outputType = StringVar()
        self.outputTypeDrop = OptionMenu(self.widget,self.outputType,*OutputBlock.types)
        self.outputTypeDrop['font']=self.fontGroup
        self.outputTypeDrop.grid(row=0,column=1)

        self.outputType.trace('w',lambda *args:self.changeType())

        self.outputEntry = tk.Entry(self.widget,textvariable=self.initOutput,borderwidth=0,width=6)

        self.varNames = list(variables.keys())
        self.initOutput.trace('w',lambda *args:self.refresh(variables))
        self.outputVar = OptionMenu(self.widget,self.initOutput,'',*self.varNames)
        self.outputVar['font']=self.fontGroup
        self.outputVar.grid(row=0,column=2)

        self.outputVars = [self.outputVar]

        self.addButton = tk.Button(self.widget,text="+", command=self.addInput)
        self.addButton.grid(row=0,column=3)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_columnconfigure(1,weight=1)
        self.widget.grid_columnconfigure(2,weight=1)
        self.widget.grid_columnconfigure(3,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)

        self.variables = variables
        
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def addInput(self):
        self.outputs.append(StringVar())
        self.outputCount+=1
        outputVar = OptionMenu(self.widget,self.outputs[-1],'',*self.varNames)
        outputVar['font']=self.fontGroup
        self.outputVars.append(outputVar)
        self.outputVars[self.outputCount-1].grid(row=0,column=self.outputCount+1)
        self.addButton.grid(row=0,column=self.outputCount+2)
        self.widget.grid_columnconfigure(self.outputCount+2,weight=1)

        self.widget.config(width=150+self.outputCount*60)

    def changeType(self):
        match self.outputType.get():
            case 'var':
                for output in self.outputs:
                    output.set('')
                self.outputEntry.grid_forget()
                self.outputCount = 1
                self.outputVar.grid(row=0,column=2)
                self.addButton.grid(row=0,column=3)
                self.widget.config(width=150+self.outputCount*60)
            case 'string':
                self.outputCount=1
                for output in self.outputs:
                    output.set('')
                for var in self.outputVars:
                    var.grid_forget()
                self.outputEntry.grid(row=0,column=2)
                self.addButton.grid_forget()
                self.widget.config(width=150+self.outputCount*60)

    def refresh(self, variables:Dict):
        self.varNames = list(variables.keys())
        self.outputVar['menu'].delete(0, 'end')
        for name in self.varNames:
            self.outputVar['menu'].add_command(label=name, command=tk._setit(self.outputs[0], name))

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#e6e6e6'))

    def output(self,varDict, console:AppConsole):
        match self.outputType.get():
            case 'var':
                for output in self.outputs:
                    console.print(f"Output Variable: {output.get()} : {varDict[output.get()]}")
            case 'string':
                console.print(f"Output: {self.initOutput.get()}")

class StartBlock(Node):
    
    def __init__(self, window) -> None:
        super().__init__()
        self.widget = tk.Frame(
            window, bg="#83c282", height=50, width=100)

        self.blockType = Node.STARTBLOCK

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="Start",font=fontGroup, background="#83c282", width=10)
        self.titleLabel.grid(row=0,column=0)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        
        self.lastNode = [] #don't use it
        self.nextNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)

        self.window=canvas.create_window(0,0,window=self.widget, anchor="nw")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#83c282'))

    def output(self,varDict, console:AppConsole):
        console.print("Flowchart Started")

class EndBlock(Node):
    
    def __init__(self, window) -> None:
        super().__init__()
        self.widget = tk.Frame(
            window, bg="#c46e71", height=50, width=100)

        self.blockType = Node.ENDBLOCK

        self.initVarDict = {}
        self.varReference = {}

        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="End",font=fontGroup, background="#c46e71", width=10)
        self.titleLabel.grid(row=0,column=0)

        self.widget.grid_columnconfigure(0,weight=1)
        self.widget.grid_rowconfigure(0,weight=1)
        
        self.nextNode = [] #Don't use this
        self.lastNode: List[Node] = []
        self.connector = []

    def placeNode(self, canvas):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)
        self.window=canvas.create_window(200,0,window=self.widget, anchor="nw")

    def activate(self):
        self.widget.after(0, lambda: self.widget.config(background='#ccafaf'))
        self.widget.after(
            500, lambda: self.widget.config(background='#c46e71'))

    def output(self, varDict, console:AppConsole):
        console.print("Flowchart Ended")