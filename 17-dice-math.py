import random # type: ignore
from blessed import Terminal
import winsound


DIE_AMMOUNT: int = 5
TERM_SIZE: tuple = (100, 50) #(Width, Height)
D1 = """
+-------+
|       |
|   O   |
|       |
+-------+"""

D2 = ["""
+-------+
| O     |
|       |
|     O |
+-------+""",
"""
+-------+
|     O |
|       |
| O     |
+-------+"""]

D3 = ["""
+-------+
| O     |
|   O   |
|     O |
+-------+""",
"""
+-------+
|     O |
|   O   |
| O     |
+-------+"""]

D4 = """
+-------+
| O   O |
|       |
| O   O |
+-------+"""

D5 = """
+-------+
| O   O |
|   O   |
| O   O |
+-------+"""

D6 = ["""
+-------+
| O O O |
|       |
| O O O |
+-------+""",
"""
+-------+
| O   O |
| O   O |
| O   O |
+-------+"""]


def randomRectanglePositionsInBoard(
    rectWidth : int,
    rectHeight : int,
    rectAmmount : int,
    boardWidth : int,
    boardHeight : int
    ) -> list[list[int]]:
    """
    Returns a list of coordinates [x,y], that are the top-left corners of found valid rectangles
    """
    while True:
        triesToReset = 200
        coordinates = []
        while triesToReset > 0:
            triesToReset -= 1
            isValid = True
            for _ in range(rectAmmount):
                newCoord = [random.randint(0, boardWidth - rectWidth - 1), random.randint(0, boardHeight - rectHeight - 1)]
                coordinates.append(newCoord)
            for i in range(rectAmmount):
                for j in range(i + 1 ,rectAmmount):
                    if abs(coordinates[i][0] - coordinates[j][0]) < rectWidth or abs(coordinates[i][1] - coordinates[j][1]) < rectHeight:
                        isValid = False
                        break
                if not isValid:
                    break
            if isValid:
                return coordinates


def main():
    term = Terminal()
    inp = ""
    with term.hidden_cursor(), term.fullscreen():
        while not inp.startswith("q"):

            print(term.home + term.on_black + term.clear)
            #Draw green board
            for i in range(TERM_SIZE[0]):
                for j in range(TERM_SIZE[1]):
                    print(term.move_xy(i, j) + term.white_on_green + " ", end="")
            #Draw board border
            for i in range(TERM_SIZE[0]):
                print(term.move_xy(i, 0) + "-", end= "")
                print(term.move_xy(i, TERM_SIZE[1] -1) + "-", end= "")
            for j in range(1, TERM_SIZE[1] - 1):
                print(term.move_xy(0, j) + "|", end= "")
                print(term.move_xy(TERM_SIZE[0] -1, j) + "|", end= "")
            print(term.move_xy(0, 0) + "+", end= "")
            print(term.move_xy(0, TERM_SIZE[1] - 1) + "+", end= "")
            print(term.move_xy(TERM_SIZE[0] - 1, 0) + "+", end= "")
            print(term.move_xy(TERM_SIZE[0] - 1, TERM_SIZE[1] - 1) + "+", end= "")
            #Find valid dice positions, dice are 9x5 chars each
            coordinates = randomRectanglePositionsInBoard(9, 5, DIE_AMMOUNT, TERM_SIZE[0] - 2, TERM_SIZE[1] - 2)
            #Roll dice
            dice = []
            index = 0
            for _ in range(DIE_AMMOUNT):
                dice.append(random.randint(1, 6))
            #Pick correct die to print, then print it for all rolled dice
            for die in dice:
                dieToPrint = ""
                if die == 1:
                    dieToPrint = D1
                elif die == 2:
                    dieToPrint = D2[random.randint(0, 1)]
                elif die == 3:
                    dieToPrint = D3[random.randint(0, 1)]
                elif die == 4:
                    dieToPrint = D4
                elif die == 5:
                    dieToPrint = D5
                else:
                    dieToPrint = D6[random.randint(0, 1)]
                printThis = dieToPrint.split("\n")
                #Print die
                for i in range(5 + 1): #5 is height of die
                    print(term.move_xy(coordinates[index][0], coordinates[index][1] + i) + term.black_on_white + printThis[i], end="")
                index += 1
            print(flush=True)
            #Dice sound
            winsound.PlaySound("diceroll.wav", 0)
            #Move cursor and ask for input
            print(term.move_xy(0, TERM_SIZE[1]) + "Enter total:")
            inp = input()
            if inp.isdecimal():
                total = 0
                for die in dice:
                    total += die
                if total == int(inp):
                    winsound.PlaySound("goodbeep.wav", 0)
                else:
                    winsound.PlaySound("badbeep.wav", 0)
            elif inp not in (u"q", u"Q"):
                winsound.PlaySound("badbeep.wav", 0)








if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("BOOP")