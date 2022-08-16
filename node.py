import tkinter as tk
from tkinter import LEFT, RIGHT, ttk, messagebox
from typing import List


class Node:

    SETVARIABLE = 1

    def __init__(self) -> None:
        self.widget: tk.Widget = None
        self.nextNode: List[Node] = []
        self.lastNode: List[Node] = []
        self.connector = []

    def connect(self, canva: tk.Canvas):
        if len(self.nextNode) > 0:
            try:
                for id in self.connector:
                    canva.delete(id)
            except:
                print("no existing line")
                #print(tag)

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
                self.connector.append(line_id)
        if len(self.lastNode) > 0:
            for node in self.lastNode:
                node.connect(canva)

    def setNextNode(self, node):
        self.nextNode = node

    def removeNextNode(self):
        self.nextNode = []

    def placeNode(self):
        self.widget.pack()


class SetVariable(Node):

    def __init__(self, window) -> None:
        self.var = None
        self.widget = tk.Frame(window, bg="green", height=50, width=50, border=3)
        self.nextNode: Node = []
        self.lastNode: Node = []
        self.connector = []

    def placeNode(self):
        self.widget.pack()
        self.widget.place(x=0, y=0)

    def activate(self, time:int):
        self.widget.after(time,lambda:self.widget.config(background='red'))
        self.widget.after(time+500,lambda:self.widget.config(background='green'))
        
