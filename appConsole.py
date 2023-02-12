import tkinter as tk
from tkinter import ttk, messagebox

class AppConsole:

    def __init__(self) -> None:

        self.screen = tk.Toplevel()
        self.screen.title("Flowchart Console")
        self.screen.geometry("500x780+1350+100")
        self.screen.resizable(False, False)
        self.screen.protocol("WM_DELETE_WINDOW", self.hide)

        self.printerWrapper = tk.LabelFrame(self.screen)
        self.trackerWrapper = tk.LabelFrame(self.screen)
        self.inputWrapper = tk.LabelFrame(self.screen)

        # Printer setup
        self.printerSpace = tk.Canvas(self.printerWrapper)
        self.printerSpace.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.printerScrollBar = tk.Scrollbar(
            self.printerWrapper, orient="vertical", command=self.printerSpace.yview)
        self.printerScrollBar.pack(side=tk.RIGHT, fill="y")

        self.printerSpace.configure(yscrollcommand=self.printerScrollBar.set)
        
        self.printerFrame = tk.Frame(self.printerSpace, bg="white")
        printerFrameId = self.printerSpace.create_window(
            (0, 0), window=self.printerFrame, anchor="nw")
        
        self.printerFrameInitHeight = self.printerFrame.winfo_height()
        
        # Tracker setup
        self.trackerSpace = tk.Canvas(self.trackerWrapper)
        self.trackerSpace.pack(side="left",fill="both",expand=True)

        self.trackerScrollBar = tk.Scrollbar(
            self.trackerWrapper, orient="vertical", command=self.trackerSpace.yview)
        self.trackerScrollBar.pack(side="right", fill="y")

        self.trackerSpace.configure(yscrollcommand=self.trackerScrollBar.set)
        
        self.trackerFrame = tk.Frame(self.trackerSpace)
        trackerFrameId = self.trackerSpace.create_window(
            (0, 0), window=self.trackerFrame, anchor="nw")
        
        self.trackerFrameInitHeight = self.trackerFrame.winfo_height()
        self.trackerFrame.grid_columnconfigure(0,weight=1)
        self.trackerFrame.grid_columnconfigure(1,weight=1)

        varLabel = tk.Label(self.trackerFrame, text="Variable", font=("Arial", 13), anchor="w")
        valueLabel = tk.Label(self.trackerFrame, text="Value", font=("Arial", 13), anchor="w")

        varLabel.grid(row=0, column=0, sticky="we")
        valueLabel.grid(row=0, column=1, sticky="we")
        
        # Input setup
        self.inputText = tk.StringVar(self.inputWrapper)
        self.inputFlag = tk.BooleanVar(self.inputWrapper)
        self.inputFlag.set(False)

        self.inputFrame = tk.Frame(self.inputWrapper)
        self.inputFrame.pack(fill="both",expand=True)

        self.inputLabel = tk.Label(self.inputFrame,font=("Arial",13), text="Input Here", anchor="w")
        self.inputLabel.grid(row=0,column=0, sticky="wens", padx=8, pady=4)

        self.inputBox = tk.Entry(self.inputFrame, font=("Arial",13), textvariable=self.inputText)
        self.inputBox.grid(row=1,column=0, sticky="wens", padx=8, pady=(0,8))

        enterPhoto = tk.PhotoImage(file = "./assets/enter.png")
        enterPhoto = enterPhoto.subsample(10,10)
        self.inputButton = tk.Button(self.inputFrame,image=enterPhoto, command=lambda:self.inputFlag.set(True))
        self.inputButton.image = enterPhoto
        self.inputButton.grid(row=0,column=1, padx=(0,4), pady=8, rowspan=2, sticky="ns")

        self.inputFrame.grid_columnconfigure(0,weight=9)
        self.inputFrame.grid_columnconfigure(1,weight=1)
        self.inputFrame.grid_rowconfigure(0,weight=1)
        self.inputFrame.grid_rowconfigure(1,weight=3)
        
        
        def configureFrame(e):
            self.printerSpace.itemconfig(printerFrameId, width=e.width)
            self.trackerSpace.itemconfig(trackerFrameId, width=e.width)
            self.printerSpace.configure(
            scrollregion=self.printerSpace.bbox("all"))
            self.trackerSpace.configure(
            scrollregion=self.trackerSpace.bbox("all"))
        self.printerSpace.bind("<Configure>", configureFrame)

        self.printerWrapper.pack(fill="both", expand=True, padx=10, pady=10)
        self.trackerWrapper.pack(fill="both", expand=True, padx=10, pady=10)
        self.inputWrapper.pack(fill="both", expand=True, padx=10, pady=10)

        self.printList:list[tk.Label] = []
        self.trackerList:list[tuple[str,tk.Label,tk.Label]] = []

        self.trackerCount = 1 # so that row starts from 1

        self.hide()

    def show(self):
        self.screen.deiconify()

    def hide(self):
        self.screen.withdraw()

    def reset(self):
        for widget in self.printerFrame.winfo_children():
            widget.destroy()
        for widget in self.trackerFrame.winfo_children():
            widget.destroy()

        varLabel = tk.Label(self.trackerFrame, text="Variable", font=("Arial", 13), anchor="w")
        valueLabel = tk.Label(self.trackerFrame, text="Value", font=("Arial", 13), anchor="w")

        varLabel.grid(row=0, column=0, sticky="we")
        valueLabel.grid(row=0, column=1, sticky="we")
        
        self.printList = []
        self.printerFrame.config(height=self.printerFrameInitHeight)
        self.printerSpace.configure(scrollregion=self.printerSpace.bbox("all"))

        self.trackerList = []
        self.trackerFrame.config(height=self.trackerFrameInitHeight)
        self.trackerSpace.configure(scrollregion=self.trackerSpace.bbox("all"))

    def print(self, text):
        label = tk.Label(self.printerFrame, text=text, anchor="w", font=("Arial", 13))
        separator = ttk.Separator(self.printerFrame, orient="horizontal")
        self.printList.append(label)

        label.pack(fill="x", expand=True, side="top")
        separator.pack(fill="x")

        self.printerSpace.configure(scrollregion=self.printerSpace.bbox("all"))

    def addVariableTrack(self, variable:str, varDict:dict):
        for var in self.trackerList:
            if variable == var[0]:
                self.refresh(varDict)
                return
        varLabel = tk.Label(self.trackerFrame, text=variable, font=("Arial", 13), anchor="w")
        valueLabel = tk.Label(self.trackerFrame, text=varDict[variable], font=("Arial", 13), anchor="w")
        varSet = (variable, varLabel, valueLabel)
        self.trackerList.append(varSet)

        varLabel.grid(row=self.trackerCount, column=0, sticky="we")
        valueLabel.grid(row=self.trackerCount, column=1, sticky="we")
        self.trackerCount+=1

    def input(self, variable:str, varDict:dict):
        self.inputText.set("")
        self.inputFlag.set(False)
        self.inputLabel.config(text="Please enter the value for variable: "+variable)
        result = self.waitInput()

        match varDict[variable]:
            case int():
                try:
                    varDict[variable] = int(result)
                except ValueError:
                    messagebox.showwarning("Invalid Input Type",f"The variable: {variable} is of type integer. Your input: {result} is not an integer. Please input again")
                    self.input(variable,varDict)
                    return
            case float():
                try:
                    varDict[variable] = float(result)
                except ValueError:
                    messagebox.showwarning("Invalid Input Type",f"The variable: {variable} is of type float. Your input: {result} is not a float number. Please input again")
                    self.input(variable,varDict)
                    return
            case str():
                varDict[variable] = result
            case _:
                raise Exception("Unexpected variable type detected")
        
        self.inputLabel.config(text="Variable: "+variable+" successfully updated")
        self.inputText.set("")
            
    def waitInput(self) -> str:
        self.inputButton.wait_variable(self.inputFlag)
        result = self.inputText.get()
        return result

    def refresh(self, varDict:dict):
        varList = list(varDict.keys())
        for var in varList:
            updated = False
            for varSet in self.trackerList:
                if var == varSet[0]:
                    varSet[2].config(text=varDict[var])
                    updated = True
                    break
            if not updated:
                self.addVariableTrack(var,varDict)