import tkinter as tk
from tkinter import BOTH, LEFT, NONE, RIGHT, TOP, IntVar, OptionMenu, StringVar, mainloop, messagebox
from tkinter import font
from typing import List

from node import ForLoop, IfBlock, Node, SetVariable, WhileLoop, NewIfBlock, NewWhileLoop, NewForLoop


class App:

    root = tk.Tk()
    toolBox = tk.Frame(root, bg="#c7cdd6", height=760, width=1200/6)
    workSpace = tk.Frame(root, bg="white", height=760, width=5*1200/6)
    canvas = tk.Canvas(workSpace, width=5*1200/6,
                       height=760, background="white", scrollregion=(0,0,2000,2000))
    hbar = tk.Scrollbar(workSpace,orient="horizontal")
    vbar = tk.Scrollbar(workSpace,orient="vertical")

    rootNode: Node = None
    nextNode: Node = None
    waitFlag = tk.IntVar()

    nodes = []
    variables = {'test':1}

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

        match choice.get():
            case Node.SETVARIABLE:
                App.nodes.append(SetVariable(App.canvas, App.variables))
            case Node.IFBLOCK:
                App.nodes.append(IfBlock(App.canvas,App.variables))
            case Node.FORLOOP:
                App.nodes.append(ForLoop(App.canvas,App.createNode, App.variables))
            case Node.WHILELOOP:
                App.nodes.append(WhileLoop(App.canvas,App.createNode,App.variables))
            case Node.NEWIFBLOCK:
                App.nodes.append(NewIfBlock(App.canvas,App.variables,App.placeChildNode))
            case Node.NEWWHILELOOP:
                App.nodes.append(NewWhileLoop(App.canvas,App.variables,App.placeChildNode))
            case Node.NEWFORLOOP:
                App.nodes.append(NewForLoop(App.canvas, App.variables, App.placeChildNode))
            
        App.nodes[-1].placeNode(App.canvas)
        App.make_draggable(App.nodes[-1])

    def placeChildNode(node:Node, xpos, ypos):
        node.placeNode(App.canvas,xpos,ypos)
        App.make_draggable(node)

    def removeNode():
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

        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>",None)
        
        for node in App.rootNode.nextNode:
            node.lastNode.remove(App.rootNode)
        for node in App.rootNode.lastNode:
            node.nextNode.remove(App.rootNode)
        App.nodes.remove(App.rootNode)
        App.rootNode.destroy()
        App.rootNode.deleteConnectors(App.canvas)
        App.canvas.delete(App.rootNode.window)

    def make_draggable(node: Node):
        node.widget.bind("<Button-1>", App.on_drag_start)
        node.widget.bind("<B1-Motion>", App.on_drag_motion)
        node.widget._node = node

    def on_drag_motion(event:tk.Event):
        x = event.x-event.widget._drag_start_x
        y = event.y-event.widget._drag_start_y

        pos = App.canvas.bbox(event.widget._node.window)

        if pos[2] + x > 2000:
            x = 0
        if pos[3] + y > 2000:
            y = 0
        if pos[0] + x < 0:
            x = 0
        if pos[1] + y < 0:
            y = 0

        App.canvas.move(event.widget._node.window,x,y)
        event.widget._node.connect(App.canvas)

    def on_drag_start(event:tk.Event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

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
                App.rootNode.connect(App.canvas)
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
            App.rootNode.removeConnector(App.canvas,App.nextNode)
        if App.nextNode in App.rootNode.lastNode:
            App.rootNode.lastNode.remove(App.nextNode)
            App.nextNode.removeConnector(App.canvas,App.rootNode)
        if App.rootNode in App.nextNode.nextNode:
            App.nextNode.nextNode.remove(App.rootNode)
            App.nextNode.removeConnector(App.canvas,App.rootNode)
        if App.rootNode in App.nextNode.lastNode:
            App.nextNode.lastNode.remove(App.rootNode)
            App.rootNode.removeConnector(App.canvas,App.nextNode)

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

        #add scrollbars
        App.hbar.pack(side="bottom",fill="x")
        App.hbar.config(command=App.canvas.xview)
        App.vbar.pack(side="right",fill="y")
        App.vbar.config(command=App.canvas.yview)
        #scroll region set to all so all objects follow
        App.canvas.config(xscrollcommand=App.hbar.set, yscrollcommand=App.vbar.set, scrollregion=App.canvas.bbox("all"))
        #setting up scrolling binding
        App.canvas.bind_all("<MouseWheel>",lambda e: App.canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
        #pack after setting up scrollbars 
        App.canvas.pack(expand=True, fill=BOTH,side="left")

        addButton = tk.Button(App.toolBox, text="add", command=App.addNode, height=5, width=22)
        addButton.grid(column=0, row=0, padx=20, pady=20, rowspan=1)

        removeButton = tk.Button(App.toolBox, text="remove", height=5, width=22, command=App.removeNode)
        removeButton.grid(column=0, row=1, padx=20, pady=10, rowspan=1)

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
    mainloop()
