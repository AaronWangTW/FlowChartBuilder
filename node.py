from sqlite3 import Row
import tkinter as tk
from tkinter import BOTH, LEFT, RIGHT, X, OptionMenu, StringVar, ttk, messagebox, font
from typing import Any, Dict, List


class Node:

    SETVARIABLE = "Set Variable"
    IFBLOCK = "If Statement"
    FORLOOP = "For Loop"
    WHILELOOP = "While Loop"

    types = [SETVARIABLE, IFBLOCK, FORLOOP, WHILELOOP]

    descriptions = {
        SETVARIABLE: "set up a variable of any customized name",
        IFBLOCK: "If statement block that execute correspondingly to the result of the if statment",
        FORLOOP: "A block that can execute its inside contents in a for loop structure",
        WHILELOOP: "A block that can execute its inside contents in a while loop structure"
    }

    def __init__(self) -> None:
        self.widget: tk.Widget = None
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def connect(self, canva: tk.Canvas):
        if len(self.nextNode) > 0:
            try:
                for line in self.connector:
                    canva.delete(line[1])
                self.connector = []
            except:
                print("no existing line")

            ax0 = self.widget.winfo_x()
            ay0 = self.widget.winfo_y()
            ax1 = ax0+self.widget.winfo_width()
            ay1 = ay0+self.widget.winfo_height()

            for node in self.nextNode:
                bx0 = node.widget.winfo_x()
                by0 = node.widget.winfo_y()
                bx1 = bx0+node.widget.winfo_width()
                by1 = by0+node.widget.winfo_height()

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

    def deleteConnectors(self):
        pass

    def removeConnector(self,node):
        pass

class SetVariable(Node):

    types = ['int','string','double']

    def __init__(self, window, varDict) -> None:
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=100, width=200)
        
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

    def placeNode(self):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)

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

class IfBlock(Node):

    operators = ['>','<','==','!=']
    types = ['int','string','double','variable']

    def __init__(self, window, variables:Dict) -> None:
        self.firstValue = StringVar()
        self.firstValue.set('')
        self.operator = StringVar()
        self.secondType = StringVar()
        self.secondValue = StringVar()
        self.secondValue.set('')

        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=100, width=200)

        fontGroup = font.Font(size=13,family="Arial")

        self.ifLabel = tk.Label(self.widget, text="If", font=fontGroup)
        self.ifLabel.grid(row=1, column=0)

        self.varNames = list(variables.keys())
        self.firstValue.trace('w',lambda *args:self.refresh(variables))
        self.firstItem = OptionMenu(self.widget,self.firstValue,*self.varNames)
        self.firstItem['font']=fontGroup
        self.firstItem.grid(row=1,column=1)

        self.operatorChoice = OptionMenu(self.widget, self.operator, IfBlock.operators[0] ,*IfBlock.operators)
        self.operatorChoice['font']=fontGroup
        self.operatorChoice.grid(row=1,column=2)

        self.secondTypeItem = OptionMenu(self.widget,self.secondType,*IfBlock.types)
        self.secondTypeItem['font']=fontGroup
        self.secondTypeItem.grid(row=0,column=3)

        self.secondType.trace('w',lambda *args:self.changeType())

        self.secondEntry = tk.Entry(self.widget,font=fontGroup,textvariable=self.secondValue,width=10)

        self.secondValue.trace('w',lambda *args:self.refresh(variables))
        self.secondItem = OptionMenu(self.widget,self.secondValue,*self.varNames)
        self.secondItem['font']=fontGroup
        self.secondItem.grid(row=1,column=3)

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
                self.secondEntry.grid(row=1,column=3)
            case 'variable':
                self.secondValue.set('')
                self.secondEntry.grid_forget()
                self.secondItem.grid(row=1,column=3)

    def placeNode(self):
        self.widget.pack(expand=True, fill=BOTH)
        self.widget.grid_propagate(False)
        self.widget.place(x=0, y=0)
    
    def activate():
        pass

    def destroy(self):
        return super().destroy()

    def output():
        pass

class ForLoop(Node):

    def __init__(self, window) -> None:
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=200, width=150)

        self.workspace = tk.Frame(self.widget,bg="#FFF", height=150, width=100)
        
        fontGroup = font.Font(size=13,family="Arial")

        self.titleLabel = tk.Label(self.widget, text="For Loop",font=fontGroup, background="#c7c7c7", width=28)
        self.titleLabel.pack()

        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []
    
    def placeNode(self):
        self.widget.pack(expand=True, fill=BOTH)
        self.workspace.pack(side="right")
        self.widget.pack_propagate(False)
        self.widget.place(x=0, y=0)