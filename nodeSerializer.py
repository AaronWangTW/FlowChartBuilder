import node
import tkinter as tk


class NodeSerializer:

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    def setVariableSe(self, node: node.SetVariable) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['lastVarName'] = node.lastVarName
        result['typeChoice'] = node.typeChoice.get()
        result['value'] = node.value.get()
        result['varName'] = node.varName.get()

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def changeVariableSe(self, node: node.ChangeVariable) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['firstVar'] = node.firstVar.get()
        result['typeChoice'] = node.typeChoice.get()
        result['value'] = node.value.get()
        result['operator'] = node.operator.get()

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def ifBlockSe(self, node: node.NewIfBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['firstValue'] = node.firstValue.get()
        result['operator'] = node.operator.get()
        result['secondType'] = node.secondType.get()
        result['secondValue'] = node.secondValue.get()
        result['trueBranchNode'] = node.trueBranchNode.id
        result['falseBranchNode'] = node.falseBranchNode.id

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def forLoopSe(self, node: node.NewForLoop) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['iterator'] = node.iterator.get()
        result['operator'] = node.operator.get()
        result['initValue'] = node.initValue.get()
        result['targetValue'] = node.targetValue.get()
        result['modifier'] = node.modifier.get()
        result['changeValue'] = node.changeValue.get()
        result['loopEndNode'] = node.loopEndNode.id

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def whileLoopSe(self, node: node.NewWhileLoop) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['var'] = node.var.get()
        result['operator'] = node.operator.get()
        result['targetType'] = node.targetType.get()
        result['targetValue'] = node.targetValue.get()
        result['loopEndNode'] = node.loopEndNode.id

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def textNodeSe(self, node: node.TextNode) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def loopEndSe(self, node: node.LoopEndBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['parentLoop'] = node.parentLoop.id

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def inputSe(self, node: node.InputBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['inputCount'] = node.inputCount
        result['inputVars'] = []
        for var in node.inputVars:
            result['inputVars'].append(var.get())

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def outputSe(self, node: node.OutputBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['outputCount'] = node.outputCount
        result['outputs'] = []
        for var in node.outputs:
            result['outputs'].append(var.get())
        result['outputType'] = node.outputType.get()

        result['nextNode'] = []
        result['lastNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result

    def startSe(self, node: node.StartBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['nextNode'] = []
        for n in node.nextNode:
            result['nextNode'].append(n.id)
        return result

    def endSe(self, node: node.EndBlock) -> dict:
        result = {}
        pos = self.canvas.bbox(node.widget._node.window)
        result['x'] = pos[0]
        result['y'] = pos[1]
        result['blockType'] = node.blockType

        result['lastNode'] = []
        for n in node.lastNode:
            result['lastNode'].append(n.id)
        return result
