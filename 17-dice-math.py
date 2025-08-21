import random # type: ignore
from blessed import Terminal
import winsound
import time
from pathlib import Path

DIE_MIN: int = 2 #Minimum dice
DIE_MAX: int = 5 #Maximum dice (If set too high in relation to board size program will hang or be very slow)
TERM_SIZE: tuple = (101, 50) #(Width, Height)
TIME_LIMIT: float = 60.0 
POINT_REWARD: int = 5 #Correct answer reward
POINT_PENALTY: int = 2 #Points lost when giving wrong answer
POINT_COMBO_REWARD: int = 7 #How many points are awarded every combo
POINT_COMBO_THRESHOLD: int = 3 #Correct answers in row to award combo

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


def bubblesortDiceMath(arr : list) -> list[str]:
    if len(arr) <= 1:
        return arr

    #make list sortable
    arrCopy = arr[:-1].copy()
    k = 0
    for string in arrCopy:
        m = string.find(",")
        arrCopy[k] = int(string[1:m])
        k += 1


    j = len(arr) - 2

    while j > 0:
        for i in range(j):
            if arrCopy[i] < arrCopy[i+1]:
                arrCopy[i], arrCopy[i+1] = arrCopy[i+1], arrCopy[i]
                arr[i], arr[i+1] = arr[i+1], arr[i]
        j -= 1

    return arr


def saveScore(scoreToSave : int) -> None:
    scoreList = [] #For sorting
    currentPath = Path(__file__).parent
    scoreFileLocation = currentPath / "scores.txt"
    print("Enter name:")
    name = input("> ")
    #Read/Create file if none exists
    writeThis = (scoreToSave, name)
    with open(scoreFileLocation, "a") as f:
        f.write(str(writeThis) + "\n")
    #Scores are stored as such: (score, 'name')
    with open(scoreFileLocation) as f:
        for line in f:
            scoreList.append(line)
        bubblesortDiceMath(scoreList)
    with open(scoreFileLocation, "w") as f:
        for line in scoreList:
            f.write(line)



def main():
    term = Terminal()
    inp = ""
    pointTotal: int = 0
    currentCombo: int = 0
    timerStart = time.time()
    #Draw start menu
    with term.hidden_cursor(), term.fullscreen():
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

            #Draw title
            print(term.move_xy((TERM_SIZE[0] // 2) - 8, 2) + term.white_on_black + term.bold + " 17-dice-math.py ", end="")
            print(term.move_xy((TERM_SIZE[0] // 2) - 8, 3) + " Add up the dice ", end="")
            #Draw score board background, 21 characters wide, 23 tall
            for i in range(1, 24):
                print(term.move_xy((TERM_SIZE[0] // 2) - 10, 5+i) + " "*21, end="")
            #Draw text on scoreboard
            currentPath = Path(__file__).parent
            scoreFileLocation = currentPath / "scores.txt"
            scoreList = []
            print(term.move_xy((TERM_SIZE[0] // 2) - 5, 6) + "TOP SCORES" ,end="")
            #Only need up to 20 scores
            with open(scoreFileLocation) as f:
                for line in f:
                    if len(scoreList[:-1]) > 20:
                        break
                    scoreList.append(line)
            for i in range(len(scoreList)):
                #(66, 'Emilia')
                position = str(i+1) + "."
                name = scoreList[i]
                m = name.find(",")
                #Last name on score board doesn't contain \n
                name = name[m+3:-3]
                #Check if name is too long
                if len(position) + len(name) > 21:
                    name = name[:21-len(position)]
                print(term.move_xy((TERM_SIZE[0] // 2) - 10, 8+i) + position + name, end="")
            #If there are less than 20 scores
            if len(scoreList) < 20:
                for i in range(len(scoreList), 21):
                    print(term.move_xy((TERM_SIZE[0] // 2) - 10, 8+i) + str(i) + "." ,end="")
            #Draw start message
            print(term.move_xy((TERM_SIZE[0] // 2) - 10, 31) + "Press ENTER to start." ,end="")





            input()

    #Game loop
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
            dieAmmount = random.randint(DIE_MIN, DIE_MAX)
            coordinates = randomRectanglePositionsInBoard(9, 5, dieAmmount, TERM_SIZE[0] - 2, TERM_SIZE[1] - 2)
            #Roll dice
            dice = []
            index = 0
            for _ in range(dieAmmount):
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
            #Move cursor and ask for input, print remaining time
            elapsedTime = time.time() - timerStart
            print(term.move_xy(0, TERM_SIZE[1]) + "Time Remaining: ", end="")
            if elapsedTime > TIME_LIMIT:
                print("0.00")
            else:
                print(str(round(TIME_LIMIT - round(time.time() - timerStart, 2), 2)))
            print("Enter Total:")
            inp = input("> ")
            elapsedTime = time.time() - timerStart
            if inp.isdecimal() and elapsedTime <=TIME_LIMIT:
                total = 0
                for die in dice:
                    total += die
                if total == int(inp):
                    winsound.PlaySound("goodbeep.wav", 0)
                    pointTotal += POINT_REWARD
                    currentCombo += 1
                    if currentCombo % POINT_COMBO_THRESHOLD == 0:
                        winsound.PlaySound("combo.wav", 0)
                        pointTotal += POINT_COMBO_REWARD
                else:
                    winsound.PlaySound("badbeep.wav", 0)
                    pointTotal -= POINT_PENALTY
            elif inp not in (u"q", u"Q"):
                winsound.PlaySound("badbeep.wav", 0)
            #Ask to retry
            if elapsedTime > TIME_LIMIT:
                print("Game over! You got {} points! Save score? (y/n)".format(pointTotal))
                inp = input("> ")
                if inp.startswith("y") or inp.startswith("Y"):
                    saveScore(pointTotal)
                print("Try again? (y/n)")
                inp = input("> ")
                if inp.startswith("y") or inp.startswith("Y"):
                    inp = ""
                    pointTotal: int = 0
                    currentCombo: int = 0
                    timerStart = time.time()
                else:
                    inp = "q"








if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("BOOP")
