import tkinter as tk
from tkinter import BOTH, LEFT, NONE, RIGHT, TOP, IntVar, OptionMenu, StringVar, mainloop, messagebox, ttk
from tkinter import font
from typing import List

from node import Node, SetVariable


class App:

    root = tk.Tk()
    toolBox = tk.Frame(root, bg="#c7cdd6", height=760, width=1200/6)
    workSpace = tk.Frame(root, bg="white", height=760, width=5*1200/6)
    canvas = tk.Canvas(workSpace, width=5*1200/6,
                       height=760, background="white")

    rootNode: Node = None
    nextNode: Node = None
    waitFlag = tk.IntVar()

    nodes = []
    variables = {}

    cancel = False

    def createNode():

        fontGroup = font.Font(size=13,family="Arial")
        types = Node.types

        choice = StringVar(App.root)
        choice.set(types[0])

        def close_event():
            choice.set(None)
            creator.destroy()
            creator.update()

        creator = tk.Toplevel()
        creator.title("Block Creator")
        creator.geometry("300x200+200+150")
        creator.resizable(False,False)
        creator.protocol("WM_DELETE_WINDOW",close_event)

        desText = StringVar()
        desText.set(Node.descriptions[choice.get()])
        typeDescription = tk.Label(creator,textvariable=desText,wraplength=300,font=("Arial",13))
        typeDescription.pack(pady=(15,0))

        menuLabel = tk.Label(creator,text="Block Type",font=("Arial",10))
        menuLabel.pack(pady=(15,0))
        dropdown = OptionMenu(creator, choice, *types, command=lambda e:desText.set(Node.descriptions[choice.get()]))
        dropdown['font']=fontGroup
        dropdown.pack(pady=(0,15))

        def end():
            creator.destroy()
            creator.update()

        decide = tk.Button(creator,text="Create Block",command=end)
        decide['font']=fontGroup
        decide.pack()

        creator.deiconify()

        creator.wait_window(creator)

        return choice

    def addNode():
        choice=App.createNode()
        
        if choice.get()=="None":
            print("creator closed")
            return

        if choice.get() == Node.SETVARIABLE:
            App.nodes.append(SetVariable(App.workSpace))
        App.nodes[-1].placeNode()
        App.make_draggable(App.nodes[-1])

    def make_draggable(node: Node):
        node.widget.bind("<Button-1>", App.on_drag_start)
        node.widget.bind("<B1-Motion>", App.on_drag_motion)
        node.widget._node = node

    def on_drag_start(event:tk.Event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(event:tk.Event):
        widget = event.widget
        window_width = App.workSpace.winfo_width()-widget.winfo_width()
        window_height = App.workSpace.winfo_height()-widget.winfo_height()
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        if (x < 0):
            x = 0
        if (x > window_width):
            x = window_width
        if (y < 0):
            y = 0
        if (y > window_height):
            y = window_height
        widget.place(x=x, y=y)

        node: Node = event.widget._node
        node.connect(App.canvas)

    def cancelFunc(event: tk.Event):
        App.cancel = True
        App.waitFlag.set(1)

    def locateRootNode(event: tk.Event):
        if App.rootNode == None:
            App.rootNode = event.widget._node
            App.waitFlag.set(1)
        else:
            pass

    def locateNextNode(event: tk.Event):
        if App.nextNode == None:
            App.nextNode = event.widget._node
            App.waitFlag.set(1)
        else:
            pass

    def link():
        App.cancel = False
        frame = tk.Frame(App.workSpace)
        text = tk.StringVar()
        text.set("select the starting block")
        label = tk.Label(App.canvas, textvariable=text,
                         background="#c7c7c7", height=1, width=1000, font=("Arial", 18))
        App.canvas.bind("<Button-3>",App.cancelFunc)

        App.rootNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateRootNode)
        label.pack()
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda:label.destroy())
            return
        
        text.set("select the ending block")
        App.nextNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateNextNode)
        frame.wait_variable(App.waitFlag)

        # cancel check
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda:label.destroy())
            return
        
        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>",None)

        if App.nextNode == App.rootNode:
            messagebox.showwarning('Same Block Linking',
                                   "Please do not link a block to itself")
            return

        if (App.nextNode not in App.rootNode.lastNode and App.rootNode not in App.nextNode.nextNode):
            if (App.nextNode not in App.rootNode.nextNode and App.rootNode not in App.nextNode.lastNode):
                App.rootNode.nextNode.append(App.nextNode)
                App.nextNode.lastNode.append(App.rootNode)
        else:
            messagebox.showwarning('Recursive Linking',
                                   "Please do not link two nodes in a loop")

    def unlink():
        App.cancel = False
        frame = tk.Frame(App.workSpace)
        text = tk.StringVar()
        text.set("select the first block")
        label = tk.Label(App.canvas, textvariable=text,
                         background="#c7c7c7", height=1, width=1000, font=("Arial", 18))
        App.canvas.bind("<Button-3>",App.cancelFunc)

        App.rootNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateRootNode)
        label.pack()
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda:label.destroy())
            return

        text.set("select the second block")
        App.nextNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateNextNode)
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda:label.destroy())
            return
        
        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>",None)

        if App.nextNode == App.rootNode:
            messagebox.showwarning('Same Block Unlinking',
                                   "Please do not unlink a block by itself")
            return

        if App.nextNode in App.rootNode.nextNode:
            App.rootNode.nextNode.remove(App.nextNode)
        if App.nextNode in App.rootNode.lastNode:
            App.rootNode.lastNode.remove(App.nextNode)
        if App.rootNode in App.nextNode.nextNode:
            App.nextNode.nextNode.remove(App.rootNode)
        if App.rootNode in App.nextNode.lastNode:
            App.nextNode.lastNode.remove(App.rootNode)

    def run(delay: int):
        print("run")
        nodes: List[Node] = [App.nodes[0]]
        nextNodes: List[Node] = []
        d = delay
        while (len(nodes) > 0):
            for node in nodes:
                node.activate(d)
            nextNodes = []
            for node in nodes:
                for nextNode in node.nextNode:
                    if nextNode not in nextNodes:
                        nextNodes.append(nextNode)
            nodes = nextNodes.copy()
            d = d+delay

    def about():
        messagebox.showinfo('About', 'What do you expect of a test program?')

    def initialize():
        App.root.title("Test Program")
        App.root.geometry("1200x760+200+150")
        App.root.resizable(False, False)

    def menu():
        menubar = tk.Menu(App.root, background='#fff', foreground='black',
                          activebackground='white', activeforeground='black')
        file = tk.Menu(menubar, tearoff=0,
                       background='#fff', foreground='black')
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_command(label="Exit", command=App.root.quit)
        menubar.add_cascade(label="File", menu=file)

        edit = tk.Menu(menubar, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_separator()
        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit)

        help = tk.Menu(menubar, tearoff=0)
        help.add_command(label="About", command=App.about)
        menubar.add_cascade(label="Help", menu=help)

        App.root.config(menu=menubar)

    def widgets():

        App.toolBox.pack(side=LEFT, expand=True, fill=BOTH)
        App.workSpace.pack(expand=True, fill=BOTH)
        App.canvas.pack_propagate(False)
        App.canvas.pack(expand=True, fill=BOTH)

        addButton = tk.Button(App.toolBox, text="add", command=App.addNode, height=10, width=22)
        addButton.pack()
        addButton.grid(column=0, row=0, padx=20, pady=20, rowspan=2)

        linkButton = tk.Button(App.toolBox, text="link", height=5, width=22,
                               command=App.link)
        linkButton.grid(column=0, row=2, padx=20, pady=10, rowspan=1)

        unlinkButton = tk.Button(App.toolBox, text="unlink", height=5, width=22,
                                 command=App.unlink)
        unlinkButton.grid(column=0, row=3, padx=20, pady=10, rowspan=1)

        runButton = tk.Button(App.toolBox, text="run",
                              height=10, width=22, command=lambda: App.run(1000))
        runButton.grid(column=0, row=4, padx=20, pady=20, rowspan=2)

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

finally:
    App.initialize()
    App.menu()
    App.widgets()
    # App.root.mainloop()
    mainloop()