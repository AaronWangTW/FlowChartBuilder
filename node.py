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

    def __init__(self, window) -> None:
        self.varName = StringVar()
        self.widget = tk.Frame(
            window, bg="#e6e6e6", height=100, width=200)
        
        self.typeChoice = StringVar()
        self.typeChoice.set(SetVariable.types[0])
        self.value = StringVar()

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
        varDict[self.varName] = self.value

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