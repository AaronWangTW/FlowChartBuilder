import node
import tkinter as tk


class NodeConstructor:

    def __init__(self, canvas: tk.Canvas, varDict: dict, placeChild) -> None:
        self.canvas = canvas
        self.varDict = varDict
        self.placeChild = placeChild

    def setVariableCon(self, nodeDict: dict, id: int) -> node.SetVariable:
        result = node.SetVariable(self.canvas, self.varDict)
        result.id = id
        result.placeNode(self.canvas)
        self.canvas.move(result.window, nodeDict['x'], nodeDict['y'])

        result.lastVarName = nodeDict['lastVarName']
        result.typeChoice.set(nodeDict['typeChoice'])
        result.value.set(nodeDict['value'])
        result.varName.set(nodeDict['varName'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def changeVariableCon(self, nodeDict: dict, id: int) -> node.ChangeVariable:
        result = node.ChangeVariable(self.canvas, self.varDict)
        result.id = id
        result.placeNode(self.canvas)
        self.canvas.move(result.window, nodeDict['x'], nodeDict['y'])

        result.firstVar.set(nodeDict['firstVar'])
        result.typeChoice.set(nodeDict['typeChoice'])
        result.value.set(nodeDict['value'])
        result.operator.set(nodeDict['operator'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def ifBlockCon(self, nodeDict: dict, id: int) -> node.NewIfBlock:
        result = node.NewIfBlock(self.canvas, self.varDict, self.placeChild)
        result.id = id

        result.firstValue.set(nodeDict['firstValue'])
        result.operator.set(nodeDict['operator'])
        result.secondType.set(nodeDict['secondType'])
        result.secondValue.set(nodeDict['secondValue'])

        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def forLoopCon(self, nodeDict: dict, id: int) -> node.NewForLoop:
        result = node.NewForLoop(self.canvas, self.varDict, self.placeChild)
        result.id = id

        result.iterator.set(nodeDict['iterator'])
        result.operator.set(nodeDict['operator'])
        result.initValue.set(nodeDict['initValue'])
        result.targetValue.set(nodeDict['targetValue'])
        result.modifier.set(nodeDict['modifier'])
        result.changeValue.set(nodeDict['changeValue'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def whileLoopCon(self, nodeDict: dict, id: int) -> node.NewWhileLoop:
        result = node.NewWhileLoop(self.canvas, self.varDict, self.placeChild)
        result.id = id

        result.var.set(nodeDict['var'])
        result.operator.set(nodeDict['operator'])
        result.targetType.set(nodeDict['targetType'])
        result.targetValue.set(nodeDict['targetValue'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def textNodeCon(self, nodeDict: dict, id:int) -> node.TextNode:
        result = node.TextNode(self.canvas,nodeDict['blockType'])
        result.id = id
        result.placeNode(self.canvas,nodeDict['x'],nodeDict['y'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def loopEndCon(self, nodeDict: dict, id:int) -> node.LoopEndBlock:
        result = node.LoopEndBlock(self.canvas,nodeDict['parentLoop'])
        result.id = id
        result.placeNode(self.canvas)
        self.canvas.move(result.window,nodeDict['x'],nodeDict['y'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def inputCon(self, nodeDict: dict, id:int) -> node.InputBlock:
        result = node.InputBlock(self.canvas,self.varDict)
        result.id = id
        result.placeNode(self.canvas)
        self.canvas.move(result.window,nodeDict['x'],nodeDict['y'])

        result.inputCount = nodeDict['inputCount']
        count = 0
        for var in nodeDict['inputVars']:
            if count == 0:
                result.initVar.set(var)
                continue
            result.addInput()
            result.inputVars[-1].set(var)

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    def outputCon(self, nodeDict: dict, id:int) -> node.OutputBlock:
        result = node.OutputBlock(self.canvas,self.varDict)
        result.id = id
        result.placeNode(self.canvas)
        self.canvas.move(result.window,nodeDict['x'],nodeDict['y'])

        result.outputCount = nodeDict['outputCount']
        count = 0
        for var in nodeDict['outputs']:
            if count == 0:
                result.initOutput.set(var)
                continue
            result.addInput()
            result.outputs[-1].set(var)
        result.outputType.set(nodeDict['outputType'])

        for nodeId in nodeDict['nextNode']:
            result.nextNode.append(nodeId)
        for nodeId in nodeDict['lastNode']:
            result.lastNode.append(nodeId)

        return result

    # def startCon(self, nodeDict: dict, id:int) -> node.StartBlock:
    #     result = node.StartBlock(self.canvas)
    #     result.id = id
    #     result.placeNode(self.canvas)
    #     self.canvas.move(result.window,nodeDict['x'],nodeDict['y'])

    #     for nodeId in nodeDict['nextNode']:
    #         result.nextNode.append(nodeId)

    #     return result

    # def endCon(self, nodeDict: dict, id:int) -> node.EndBlock:
    #     result = node.EndBlock(self.canvas)
    #     result.id = id
    #     result.placeNode(self.canvas)
    #     self.canvas.move(result.window,nodeDict['x'],nodeDict['y'])

    #     for nodeId in nodeDict['lastNode']:
    #         result.lastNode.append(nodeId)

    #     return result
