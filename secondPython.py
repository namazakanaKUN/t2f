#time to frame convert app
import tkinter as tk
import math as m
frameList = []

window = tk.Tk()
window.geometry("500x500")
window.title("Time to Frame")
explaintText = tk.Label(text=("This app is convertion Time to Frame"), width=40, height=5)
explaintText.pack()

def showList():
    frameSet = set(frameList)
    print("----- Frame list -----")
    for elements in frameSet:
        print(elements)

def showResult(result):
    resultText = tk.Label(text=result, name="resultText")
    resultText.pack_forget()
    resultText.pack()

def timeCalc(minute,second,FPS):
    totalSecond = int(minute)*60 + int(second)
    Frame = int(totalSecond) * int(FPS)
    result = str(Frame) + "Farme"
    showResult(result)
    frameList.append(result)


def main():
    showListButton = tk.Button(text="Show frame list",command=showList)

    text1 = tk.Label(text="Input the FPS")
    entryFPS = tk.Entry()

    text2 = tk.Label(text="Input the minute")
    entryMinute = tk.Entry()

    text3 = tk.Label(text="Input the second")
    entrySecond = tk.Entry()

    convertButton = tk.Button(text="Start convert", command=lambda: timeCalc(entryMinute.get(), entrySecond.get(), entryFPS.get()))
    
    
    showListButton.pack()
    text1.pack()
    entryFPS.pack()
    text2.pack()
    entryMinute.pack()
    text3.pack()
    entrySecond.pack()
    convertButton.pack()
    window.mainloop()
main()