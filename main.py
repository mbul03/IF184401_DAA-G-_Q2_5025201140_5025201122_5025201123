from tokenize import Number
from gui import *
from state import *
from functions import *

startState = ['_', '_', '_', '_', '_', '_', '_', '_', '_']

maxPlayer, minPlayer = 'X', 'O'
bestScore = 0

def main():

    root = tk.Tk()
    App(root, (500, 500)).pack(side="top", fill="both", expand=True)
    root.mainloop()
    return


if __name__ == "__main__":
    main()