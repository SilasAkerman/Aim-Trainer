from aimGame import Game, Target
import tkinter as tk

root = tk.Tk()
root.title("AimTrainer")

def createGame():
     Practice = Game(targetAmountSlider.get(), targetDelaySlider.get()/1000, targetSizeSlider.get())
     Practice.play()

targetSizeLabel = tk.Label(root, text="Target Size")
targetSizeLabel.pack()
targetSizeSlider = tk.Scale(root, from_=5, to=100, orient=tk.HORIZONTAL)
targetSizeSlider.pack()

targetAmountLabel = tk.Label(root, text="Target Amount")
targetAmountLabel.pack()
targetAmountSlider = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL)
targetAmountSlider.pack()

targetDelayLabel = tk.Label(root, text="Target Delay (ms)")
targetDelayLabel.pack()
targetDelaySlider = tk.Scale(root, from_=0, to=2000, orient=tk.HORIZONTAL)
targetDelaySlider.pack()

gameButton = tk.Button(root, text="Create Game", command=createGame)
gameButton.pack()


root.mainloop()