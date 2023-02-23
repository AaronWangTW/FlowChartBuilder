import tkinter as tk
import json
import os.path
import os
from tkinter import BOTH, LEFT, NONE, RIGHT, TOP, IntVar, OptionMenu, StringVar, mainloop, messagebox
from tkinter import font
from typing import List
from pathvalidate import is_valid_filename

from node import Node, SetVariable, NewIfBlock, NewWhileLoop, NewForLoop, ChangeVariable, StartBlock, EndBlock, InputBlock, OutputBlock

import nodeSerializer
import nodeConstructor
import appConsole


class App:

    root = tk.Tk()
    toolBox = tk.Frame(root, bg="#c7cdd6", height=760, width=1200/6)
    workSpace = tk.Frame(root, bg="white", height=760, width=5*1200/6)
    canvas = tk.Canvas(workSpace, width=5*1200/6,
                       height=760, background="white", scrollregion=(0, 0, 2000, 2000))
    hbar = tk.Scrollbar(workSpace, orient="horizontal")
    vbar = tk.Scrollbar(workSpace, orient="vertical")

    console = appConsole.AppConsole()

    rootNode: Node = None
    nextNode: Node = None
    waitFlag = tk.IntVar()

    nodes: List[Node] = []
    variables = {'test':1}
    idCount = 0

    cancel = False

    currentChartName = None

    def createNode():

        fontGroup = font.Font(size=13, family="Arial")
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
        creator.resizable(False, False)
        creator.protocol("WM_DELETE_WINDOW", close_event)

        desText = StringVar()
        desText.set(Node.descriptions[choice.get()])
        typeDescription = tk.Label(
            creator, textvariable=desText, wraplength=300, font=("Arial", 13))
        typeDescription.pack(pady=(15, 0))

        menuLabel = tk.Label(creator, text="Block Type", font=("Arial", 10))
        menuLabel.pack(pady=(15, 0))
        dropdown = OptionMenu(
            creator, choice, *types, command=lambda e: desText.set(Node.descriptions[choice.get()]))
        dropdown['font'] = fontGroup
        dropdown.pack(pady=(0, 15))

        def end():
            creator.destroy()
            creator.update()

        decide = tk.Button(creator, text="Create Block", command=end)
        decide['font'] = fontGroup
        decide.pack()

        creator.deiconify()

        creator.wait_window(creator)

        return choice

    def addNode():
        choice = App.createNode()

        if choice.get() == "None":
            print("creator closed")
            return

        match choice.get():
            case Node.SETVARIABLE:
                App.nodes.append(SetVariable(App.canvas, App.variables))
            case Node.NEWIFBLOCK:
                App.nodes.append(NewIfBlock(
                    App.canvas, App.variables, App.placeChildNode))
            case Node.NEWWHILELOOP:
                App.nodes.append(NewWhileLoop(
                    App.canvas, App.variables, App.placeChildNode))
            case Node.NEWFORLOOP:
                App.nodes.append(NewForLoop(
                    App.canvas, App.variables, App.placeChildNode))
            case Node.CHANGEVARIABLE:
                App.nodes.append(ChangeVariable(App.canvas, App.variables))
            case Node.STARTBLOCK:
                count = 0
                for node in App.nodes:
                    if node.blockType == Node.STARTBLOCK:
                        count += 1
                if count >= 1:
                    messagebox.showwarning('Start Block Already Exist',
                                           "There cannot be more than one start block in one flowchart")
                    return
                App.nodes.append(StartBlock(App.canvas))
            case Node.ENDBLOCK:
                count = 0
                for node in App.nodes:
                    if node.blockType == Node.ENDBLOCK:
                        count += 1
                if count >= 1:
                    messagebox.showwarning('End Block Already Exist',
                                           "There cannot be more than one end block in one flowchart")
                    return
                App.nodes.append(EndBlock(App.canvas))
            case Node.INPUTBLOCK:
                App.nodes.append(InputBlock(App.canvas, App.variables))
            case Node.OUTPUTBLOCK:
                App.nodes.append(OutputBlock(App.canvas, App.variables))

        App.nodes[-1].id = App.idCount
        App.idCount += 1
        App.make_draggable(App.nodes[-1])
        App.nodes[-1].placeNode(App.canvas)

    def placeChildNode(node: Node, xpos, ypos):
        node.placeNode(App.canvas, xpos, ypos)
        node.id = App.idCount
        App.idCount += 1
        App.nodes.append(node)
        App.make_draggable(node)

    def removeNode():
        App.cancel = False
        frame = tk.Frame(App.workSpace)
        text = tk.StringVar()
        text.set("select the starting block")
        label = tk.Label(App.canvas, textvariable=text,
                         background="#c7c7c7", height=1, width=1000, font=("Arial", 18))
        App.canvas.bind("<Button-3>", App.cancelFunc)

        App.rootNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateRootNode)
        label.pack()
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda: label.destroy())
            return

        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>", None)

        if App.rootNode.blockType == Node.STARTBLOCK or App.rootNode.blockType == Node.ENDBLOCK:
            messagebox.showwarning(
                "Deletion Error", "Cannot delete start or end block")
            return
        
        if App.rootNode.blockType == Node.NEWFORLOOP or App.rootNode.blockType == Node.NEWWHILELOOP:
            loopEndNode = App.rootNode.loopEndNode
            for node in loopEndNode.nextNode:
                node.lastNode.remove(loopEndNode)
                node.removeConnector(App.canvas, loopEndNode)
            for node in loopEndNode.lastNode:
                node.nextNode.remove(loopEndNode)
                node.removeConnector(App.canvas, loopEndNode)
            App.nodes.remove(loopEndNode)
            loopEndNode.deleteConnectors(App.canvas)
            App.canvas.delete(loopEndNode.window)

        if App.rootNode.blockType == Node.LOOPENDBLOCK:
            parentNode = App.rootNode.parentLoop
            for node in parentNode.nextNode:
                node.lastNode.remove(parentNode)
                node.removeConnector(App.canvas, parentNode)
            for node in parentNode.lastNode:
                node.nextNode.remove(parentNode)
                node.removeConnector(App.canvas, parentNode)
            App.nodes.remove(parentNode)
            parentNode.deleteConnectors(App.canvas)
            App.canvas.delete(parentNode.window)


        for node in App.rootNode.nextNode:
            node.lastNode.remove(App.rootNode)
            node.removeConnector(App.canvas, App.rootNode)
        for node in App.rootNode.lastNode:
            node.nextNode.remove(App.rootNode)
            node.removeConnector(App.canvas, App.rootNode)
        App.nodes.remove(App.rootNode)
        App.rootNode.destroy()
        App.rootNode.deleteConnectors(App.canvas)
        App.canvas.delete(App.rootNode.window)

    def make_draggable(node: Node):
        node.widget.bind("<Button-1>", App.on_drag_start)
        node.widget.bind("<B1-Motion>", App.on_drag_motion)
        node.widget._node = node

    def on_drag_motion(event: tk.Event):
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

        App.canvas.move(event.widget._node.window, x, y)
        event.widget._node.connect(App.canvas)

    def on_drag_start(event: tk.Event):
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
        App.canvas.bind("<Button-3>", App.cancelFunc)

        App.rootNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateRootNode)
            if (node.blockType == Node.NEWFORLOOP or node.blockType == Node.NEWWHILELOOP):
                node.loopEndNode.widget.bind(
                    "<ButtonRelease-1>", App.locateRootNode)
            elif (node.blockType == Node.NEWIFBLOCK):
                node.trueBranchNode.widget.bind(
                    "<ButtonRelease-1>", App.locateRootNode)
                node.falseBranchNode.widget.bind(
                    "<ButtonRelease-1>", App.locateRootNode)
        label.pack()
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda: label.destroy())
            return

        text.set("select the ending block")
        App.nextNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateNextNode)
            if (node.blockType == Node.NEWFORLOOP or node.blockType == Node.NEWWHILELOOP):
                node.loopEndNode.widget.bind(
                    "<ButtonRelease-1>", App.locateNextNode)
            elif (node.blockType == Node.NEWIFBLOCK):
                node.trueBranchNode.widget.bind(
                    "<ButtonRelease-1>", App.locateNextNode)
                node.falseBranchNode.widget.bind(
                    "<ButtonRelease-1>", App.locateNextNode)
        frame.wait_variable(App.waitFlag)

        # cancel check
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda: label.destroy())
            return

        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
            if (node.blockType == Node.NEWFORLOOP or node.blockType == Node.NEWWHILELOOP):
                node.loopEndNode.widget.bind("<ButtonRelease-1>", None)
            elif (node.blockType == Node.NEWIFBLOCK):
                node.trueBranchNode.widget.bind("<ButtonRelease-1>", None)
                node.falseBranchNode.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>", None)

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
        App.canvas.bind("<Button-3>", App.cancelFunc)

        App.rootNode = None
        App.waitFlag.set(0)
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", App.locateRootNode)
        label.pack()
        frame.wait_variable(App.waitFlag)

        # cancel
        if App.cancel:
            text.set("canceled")
            label.after(500, lambda: label.destroy())
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
            label.after(500, lambda: label.destroy())
            return

        label.destroy()
        for node in App.nodes:
            node.widget.bind("<ButtonRelease-1>", None)
        App.canvas.bind("<Button-3>", None)

        if App.nextNode == App.rootNode:
            messagebox.showwarning('Same Block Unlinking',
                                   "Please do not unlink a block by itself")
            return

        if App.nextNode in App.rootNode.nextNode:
            App.rootNode.nextNode.remove(App.nextNode)
            App.rootNode.removeConnector(App.canvas, App.nextNode)
        if App.nextNode in App.rootNode.lastNode:
            App.rootNode.lastNode.remove(App.nextNode)
            App.nextNode.removeConnector(App.canvas, App.rootNode)
        if App.rootNode in App.nextNode.nextNode:
            App.nextNode.nextNode.remove(App.rootNode)
            App.nextNode.removeConnector(App.canvas, App.rootNode)
        if App.rootNode in App.nextNode.lastNode:
            App.nextNode.lastNode.remove(App.rootNode)
            App.rootNode.removeConnector(App.canvas, App.nextNode)

    def run():
        for node in App.nodes:
            if node.blockType == Node.STARTBLOCK:
                startNode = node
            if node.blockType == Node.ENDBLOCK:
                node.initVarDict = App.variables.copy()
                node.varReference = App.variables
        App.console.show()
        App.console.reset()
        startNode.run(App.variables, App.console)

    def new():
        for node in App.nodes:
            node.destroy()
            node.deleteConnectors(App.canvas)
        App.canvas.delete("all")
        App.nodes = []
        App.variables = {}
        App.idCount = 0
        App.currentChartName = None

        App.initialize()

    def exportToJSON():
        result = {}

        result['nodes'] = {}
        result['variables'] = App.variables.copy()

        serializer = nodeSerializer.NodeSerializer(App.canvas)
        for node in App.nodes:
            # use node serializers
            nodeDict = {}
            match node.blockType:
                case Node.SETVARIABLE:
                    nodeDict = serializer.setVariableSe(node)
                case Node.CHANGEVARIABLE:
                    nodeDict = serializer.changeVariableSe(node)
                case Node.NEWIFBLOCK:
                    nodeDict = serializer.ifBlockSe(node)
                case Node.NEWWHILELOOP:
                    nodeDict = serializer.whileLoopSe(node)
                case Node.NEWFORLOOP:
                    nodeDict = serializer.forLoopSe(node)
                case Node.IFTRUEBLOCK | Node.IFFALSEBLOCK:
                    nodeDict = serializer.textNodeSe(node)
                case Node.LOOPENDBLOCK:
                    nodeDict = serializer.loopEndSe(node)
                case Node.INPUTBLOCK:
                    nodeDict = serializer.inputSe(node)
                case Node.OUTPUTBLOCK:
                    nodeDict = serializer.outputSe(node)
                case Node.STARTBLOCK:
                    nodeDict = serializer.startSe(node)
                case Node.ENDBLOCK:
                    nodeDict = serializer.endSe(node)
                case _:
                    raise Exception("Node of unexpected type detected")

            result["nodes"][node.id] = nodeDict

        return result

    def saveScreen():
        def close_event():
            screen.destroy()
            screen.update()

        chartName = tk.StringVar()

        screen = tk.Toplevel()
        screen.title("Save As...")
        screen.geometry("300x200+200+150")
        screen.resizable(False, False)
        screen.protocol("WM_DELETE_WINDOW", close_event)

        instruction = tk.Label(
            screen, text="Enter the name for the flowchart", wraplength=300, font=("Arial", 13))
        instruction.pack(pady=(30, 15))

        nameInput = tk.Entry(screen, font=("Arial", 13),
                             textvariable=chartName, width=30)
        nameInput.pack(pady=15)

        def confirm():
            screen.destroy()
            screen.update()

        def end():
            chartName.set("-1")
            screen.destroy()
            screen.update()

        decide = tk.Button(screen, text="Save",
                           command=confirm, font=("Arial", 13))
        decide.pack(side=LEFT, padx=(60, 0))

        cancel = tk.Button(screen, text="Cancel",
                           command=end, font=("Arial", 13))
        cancel.pack(side=RIGHT, padx=(0, 60))

        screen.wait_window(screen)

        return chartName

    def saveAs():
        fileName = App.saveScreen().get()
        if fileName == "-1":
            return
        fileName = fileName.replace(" ", "_")
        if not is_valid_filename(fileName):
            messagebox.showwarning(
                "Invalid Flowchart Name", "Invalid flowchart name. Flowchart name should not contain any special characters.")
            App.saveAs()
            return
        filePath = f"./saves/{fileName}.json"
        if os.path.isfile(filePath):
            confirmBox = tk.messagebox.askquestion('Replace File', f'The flowchart with name {fileName} already exists, would you like to replace existing file?',
                                                   icon='warning')
            if confirmBox == 'yes':
                App.saveToExisting(fileName)
                return
            else:
                App.saveAs()
                return

        fileDict = App.exportToJSON()
        with open(f"./saves/{fileName}.json", "w", encoding="utf8") as file:
            json.dump(fileDict, file, indent=4, ensure_ascii=False)

        App.currentChartName = fileName
        App.root.title("Flowchart Builder - "+fileName)

    def saveToExisting(fileName: str):
        if not fileName:
            App.saveAs()
            return
        fileDict = App.exportToJSON()
        with open(f"./saves/{fileName}.json", "w", encoding="utf8") as file:
            json.dump(fileDict, file, indent=4, ensure_ascii=False)

    def openOld():
        chartName = App.openMenu().get()

        if chartName == "-1":
            return
        
        App.new()

        nodesDict: dict = {}
        varDict = {}
        with open(f"./saves/{chartName}.json") as jsonFile:
            chartDict = json.load(jsonFile)
            nodesDict = chartDict['nodes']
            varDict = chartDict['variables']

        constructor = nodeConstructor.NodeConstructor(
            App.canvas, varDict, App.placeChildNode)

        nodeIDs = list(nodesDict.keys())
        nodeIDs.sort()

        for id in nodeIDs:
            nodeDict = nodesDict[id]
            node = None
            match nodeDict['blockType']:
                case Node.SETVARIABLE:
                    node = constructor.setVariableCon(nodeDict, id)
                case Node.CHANGEVARIABLE:
                    node = constructor.changeVariableCon(nodeDict, id)
                case Node.NEWIFBLOCK:
                    node = constructor.ifBlockCon(nodeDict, id)
                case Node.NEWFORLOOP:
                    node = constructor.forLoopCon(nodeDict, id)
                case Node.NEWWHILELOOP:
                    node = constructor.whileLoopCon(nodeDict, id)
                case Node.IFTRUEBLOCK:
                    parentNodeId = int(nodeDict['lastNode'][0])
                    App.canvas.move(App.nodes[parentNodeId].trueBranchNode.window,nodeDict['x'],nodeDict['y']-280)
                    for nodeId in nodeDict['nextNode']:
                        App.nodes[parentNodeId].trueBranchNode.nextNode.append(nodeId)
                    continue
                case Node.IFFALSEBLOCK:
                    parentNodeId = int(nodeDict['lastNode'][0])
                    App.canvas.move(App.nodes[parentNodeId].falseBranchNode.window,nodeDict['x']-300,nodeDict['y']-280)
                    for nodeId in nodeDict['nextNode']:
                        App.nodes[parentNodeId].falseBranchNode.nextNode.append(nodeId)
                    continue
                case Node.LOOPENDBLOCK:
                    parentNodeId = nodeDict['parentLoop']
                    App.canvas.move(App.nodes[parentNodeId].loopEndNode.window,nodeDict['x']-100,nodeDict['y']-300)
                    for nodeId in nodeDict['nextNode']:
                        App.nodes[parentNodeId].loopEndNode.nextNode.append(nodeId)
                    for nodeId in nodeDict['lastNode']:
                        App.nodes[parentNodeId].loopEndNode.lastNode.append(nodeId)
                    continue
                case Node.INPUTBLOCK:
                    node = constructor.inputCon(nodeDict, id)
                case Node.OUTPUTBLOCK:
                    node = constructor.outputCon(nodeDict, id)
                case Node.STARTBLOCK:
                    App.canvas.move(App.nodes[0].window,nodeDict['x'],nodeDict['y'])
                    for nodeId in nodeDict['nextNode']:
                        App.nodes[0].nextNode.append(nodeId)
                    continue
                case Node.ENDBLOCK:
                    App.canvas.move(App.nodes[1].window,nodeDict['x']-200,nodeDict['y'])
                    for nodeId in nodeDict['lastNode']:
                        App.nodes[1].lastNode.append(nodeId)
                    continue
                case _:
                    raise Exception("Unexpected node type detected")
            App.make_draggable(node)
            App.nodes.append(node)
            if nodeDict['blockType'] == Node.NEWIFBLOCK:
                App.idCount+=1
                node.placeNode(App.canvas)
                App.canvas.move(node.window, nodeDict['x']-50, nodeDict['y'])
            if nodeDict['blockType'] == Node.NEWWHILELOOP or nodeDict['blockType'] == Node.NEWFORLOOP:
                App.idCount+=1
                node.placeNode(App.canvas)
                App.canvas.move(node.window, nodeDict['x'], nodeDict['y'])

        for node in App.nodes:
            index = 0
            for n in node.lastNode:
                nId = n
                if type(nId) == int or type(nId) == str:
                    node.lastNode[index] = App.nodes[int(nId)]
            index = 0
            for n in node.nextNode:
                nId = n
                if type(nId) == int or type(nId) == str:
                    node.nextNode[index] = App.nodes[int(nId)]
        for node in App.nodes:
            node.connect(App.canvas)

        App.idCount = int(nodeIDs[-1])+1
        App.root.title("Flowchart Builder - "+chartName)
        App.currentChartName = chartName

    def openMenu():
        def close_event():
            screen.destroy()
            screen.update()

        chartName = tk.StringVar()

        screen = tk.Toplevel()
        screen.title("Open Flowchart")
        screen.geometry("500x500+200+150")
        screen.resizable(False, False)
        screen.protocol("WM_DELETE_WINDOW", close_event)

        instruction = tk.Label(
            screen, text="Select the flowchart you wish to open", wraplength=300, font=("Arial", 13))
        instruction.pack(pady=(15, 0))

        chartListWrapper = tk.LabelFrame(screen)
        selectWrapper = tk.LabelFrame(screen)

        chartListSpace = tk.Canvas(chartListWrapper)
        chartListSpace.pack(side=LEFT, fill=BOTH, expand=True)

        yScrollBar = tk.Scrollbar(
            chartListWrapper, orient="vertical", command=chartListSpace.yview)
        yScrollBar.pack(side=RIGHT, fill="y")

        chartListSpace.configure(yscrollcommand=yScrollBar.set)

        chartListFrame = tk.Frame(chartListSpace)
        frameId = chartListSpace.create_window(
            (0, 0), window=chartListFrame, anchor="nw")

        def configureSpace(e):
            chartListSpace.itemconfig(frameId, width=e.width)
            chartListSpace.configure(
            scrollregion=chartListSpace.bbox("all"))
        chartListSpace.bind("<Configure>", configureSpace)

        chartListWrapper.pack(fill="both", expand=True, padx=10, pady=10)
        selectWrapper.pack(fill="both", expand=True, padx=10, pady=10)

        lastChartLabel = tk.Label()

        def selectChart(e: tk.Event):
            nonlocal lastChartLabel
            lastChartLabel.config(bg="SystemButtonFace")
            e.widget.config(bg="#98b2d4")
            chartName.set(e.widget.cget("text"))
            lastChartLabel = e.widget

        charts = []
        for chart in os.listdir("./saves"):
            if chart.endswith(".json"):
                charts.append(chart)
        for chart in charts:
            label = tk.Label(chartListFrame, text=chart.removesuffix(
                '.json'), borderwidth=1, relief="solid", anchor="w", font=("Arial", 13))
            label.pack(fill="x", expand=True, side=TOP, anchor="w")
            label.bind("<Button-1>", lambda e: selectChart(e))

        def confirm():
            screen.destroy()
            screen.update()

        def end():
            chartName.set("-1")
            screen.destroy()
            screen.update()

        decide = tk.Button(selectWrapper, text="Open",
                           command=confirm, font=("Arial", 13))
        decide.pack(side=LEFT, padx=(60, 0))

        cancel = tk.Button(selectWrapper, text="Cancel",
                           command=end, font=("Arial", 13))
        cancel.pack(side=RIGHT, padx=(0, 60))

        screen.wait_window(screen)

        return chartName

    def about():
        messagebox.showinfo('About', 'What do you expect of a test program?')

    def initialize():
        App.root.title("Flowchart Builder")
        App.root.geometry("1200x760+100+100")
        App.root.resizable(False, False)

        start = StartBlock(App.canvas)
        start.id = App.idCount
        App.idCount += 1
        end = EndBlock(App.canvas)
        end.id = App.idCount
        App.idCount += 1
        App.nodes.append(start)
        App.nodes.append(end)
        start.placeNode(App.canvas)
        end.placeNode(App.canvas)
        App.make_draggable(start)
        App.make_draggable(end)

    def menu():
        menubar = tk.Menu(App.root, background='#fff', foreground='black',
                          activebackground='white', activeforeground='black')
        file = tk.Menu(menubar, tearoff=0,
                       background='#fff', foreground='black')
        file.add_command(label="New", command=App.new)
        file.add_command(label="Open", command=App.openOld)
        file.add_command(
            label="Save", command=lambda: App.saveToExisting(App.currentChartName))
        file.add_command(label="Save as", command=App.saveAs)
        file.add_command(label="Exit", command=App.root.quit)
        menubar.add_cascade(label="File", menu=file)

        help = tk.Menu(menubar, tearoff=0)
        help.add_command(label="About", command=App.about)
        menubar.add_cascade(label="Help", menu=help)

        App.root.config(menu=menubar)

    def widgets():

        App.toolBox.pack(side=LEFT, expand=True, fill=BOTH)
        App.workSpace.pack(expand=True, fill=BOTH)
        App.canvas.pack_propagate(False)

        # add scrollbars
        App.hbar.pack(side="bottom", fill="x")
        App.hbar.config(command=App.canvas.xview)
        App.vbar.pack(side="right", fill="y")
        App.vbar.config(command=App.canvas.yview)
        # scroll region set to all so all objects follow
        App.canvas.config(xscrollcommand=App.hbar.set,
                          yscrollcommand=App.vbar.set, scrollregion=(0, 0, 2000, 2000))
        # setting up scrolling binding
        App.canvas.bind_all("<MouseWheel>", lambda e: App.canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))
        # pack after setting up scrollbars
        App.canvas.pack(expand=True, fill=BOTH, side="left")

        addButton = tk.Button(App.toolBox, text="add",
                              command=App.addNode, height=5, width=22)
        addButton.grid(column=0, row=0, padx=20, pady=20, rowspan=1)

        removeButton = tk.Button(
            App.toolBox, text="remove", height=5, width=22, command=App.removeNode)
        removeButton.grid(column=0, row=1, padx=20, pady=10, rowspan=1)

        linkButton = tk.Button(App.toolBox, text="link", height=5, width=22,
                               command=App.link)
        linkButton.grid(column=0, row=2, padx=20, pady=10, rowspan=1)

        unlinkButton = tk.Button(App.toolBox, text="unlink", height=5, width=22,
                                 command=App.unlink)
        unlinkButton.grid(column=0, row=3, padx=20, pady=10, rowspan=1)

        runButton = tk.Button(App.toolBox, text="run",
                              height=10, width=22, command=lambda: App.run())
        runButton.grid(column=0, row=4, padx=20, pady=20, rowspan=2)


try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

finally:
    App.initialize()
    App.menu()
    App.widgets()
    mainloop()
