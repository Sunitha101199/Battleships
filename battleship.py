"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random
import math

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["numShips"] = 5
    data["cellSize"] = data["boardSize"]/data["rows"]
    # data["compGrid"] = []
    # data["userGrid"] = []
    data["compGrid"] = addShips(emptyGrid(data["rows"], data["cols"]),data["numShips"])
    data["userGrid"] = emptyGrid(data["rows"], data["cols"])#changed test.testShip()
    # addShips(data["compGrid"], data["numShips"])
    data["tempShips"] = []#emptyGrid(data["rows"], data["cols"])
    data["numUserShips"] = 0
    return

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userGrid"], True)
    drawGrid(data, compCanvas, data["compGrid"], False)
    drawShip(data, userCanvas, data["tempShips"])
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    [row,col] = getClickedCell(data,event)
    if board == "user":
        # print(data["tempShips"])
        clickUserBoard(data,row,col)
    if board == "comp":
        runGameTurn(data,row,col)
    pass

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    gridRows=[]
    for i in range(rows):
        gridCols=[]
        gridRows.append(gridCols)
        for j in range(cols):
            gridCols.append(EMPTY_UNCLICKED)#append
    return gridRows

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    rows,cols = random.randint(1,8), random.randint(1,8)
    orientation = random.randint(0,1)
    if orientation==0:
        ship = [[rows-1,cols],[rows,cols],[rows+1,cols]]
    else:
        ship = [[rows,cols-1],[rows,cols],[rows,cols+1]]
    return ship

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count = 0
    for i in range(len(ship)):
        row,col = ship[i][0],ship[i][1]
        if grid[row][col] == EMPTY_UNCLICKED:
            count = count+1
    return count == len(ship)

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    currentShips = 0
    while currentShips < numShips:
        ship = createShip()
        if checkShip(grid,ship):
            currentShips +=1
            for j in range(len(ship)):
                grid[ship[j][0]][ship[j][1]] = SHIP_UNCLICKED
    return grid

'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col] == SHIP_UNCLICKED:
                canvas.create_rectangle(col*data["cellSize"], row*data["cellSize"], (col*data["cellSize"])+data["cellSize"], (row*data["cellSize"])+data["cellSize"], fill="yellow")
            elif grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(col*data["cellSize"], row*data["cellSize"], (col*data["cellSize"])+data["cellSize"], (row*data["cellSize"])+data["cellSize"], fill="red")
            elif grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(col*data["cellSize"], row*data["cellSize"], (col*data["cellSize"])+data["cellSize"], (row*data["cellSize"])+data["cellSize"], fill="white")
            else:
                canvas.create_rectangle(col*data["cellSize"], row*data["cellSize"], (col*data["cellSize"])+data["cellSize"], (row*data["cellSize"])+data["cellSize"], fill="blue")
    if showShips == False and grid[row][col] == SHIP_UNCLICKED:
        canvas.create_rectangle(col*data["cellSize"], row*data["cellSize"], (col*data["cellSize"])+data["cellSize"], (row*data["cellSize"])+data["cellSize"], fill="blue") 
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    rows = []
    rows = [(ship[col][1]) for col in range(len(ship))]
    rows.sort()
    if rows[0]+1 == rows[1] and rows[1]+1 == rows[2]:
        return True
    return False

'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    cols = []
    cols = [(ship[col][1]) for col in range(len(ship))]
    cols.sort()
    if cols[0]+1 == cols[1] and cols[1]+1 == cols[2]:
        return True
    return False

'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    row = math.floor(event.y / data["cellSize"])
    col = math.floor(event.x / data["cellSize"])
    return [row, col]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for position in range(len(ship)):
        canvas.create_rectangle(ship[position][1]*data["cellSize"], ship[position][0]*data["cellSize"], (ship[position][1]*data["cellSize"])+data["cellSize"], (ship[position][0]*data["cellSize"])+data["cellSize"], fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) == 3:
        if checkShip(grid, ship):
            if isVertical(ship) or isHorizontal(ship):
                return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    temp = data["tempShips"]
    if shipIsValid(data["userGrid"], data["tempShips"]):
        for j in temp:
            data["userGrid"][j[0]][j[1]] = SHIP_UNCLICKED
                # addShips(data["userGrid"], data["numShips"])
        data["numUserShips"]+=1
    else:
        print("Error: Ship is not Valid")
    data["tempShips"] = []
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["numUserShips"] == data["numShips"]:
        print("Start playing the game!")
        return
    if [row, col] in data["tempShips"]:
        return
    data["tempShips"].append([row,col])
    if len(data["tempShips"]) == 3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED and player == "user":
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == SHIP_UNCLICKED and player == "comp":
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED and player == "user":
        board[row][col] = EMPTY_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED and player == "comp":
        board[row][col] = EMPTY_CLICKED
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["compGrid"][row][col] == SHIP_CLICKED or data["compGrid"][row][col] == EMPTY_CLICKED:
        return
    updateBoard(data,data["compGrid"],row,col,"user")
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    return

'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    return


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    ## Finally, run the simulation to test it manually ##
    # runSimulation(500, 500)
    test.testUpdateBoard()
