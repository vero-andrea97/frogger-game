#
#   Template for SAMS: Programming
#   Final Project: Frogger
#
#   frogger.py
#
#   
#   WRITTEN BY: (Veronica A. Gutierrez) & (vagutier)
#

from Tkinter import *
from random import randint


######################
######################
# Events
######################
######################

# Reacts to key presses.  Tests the state of the game, then accepts
# appropriate keys.
def keyPressed(event):
    key = event.keysym
    if canvas.data.state == "game":
        if key in ["Up","Down","Left","Right"] and not canvas.data.paused:
            moveFrog(key)
        if key == "p":
            canvas.data.paused = not canvas.data.paused
    elif canvas.data.state == "splash":
        if key == "space":
            canvas.data.state = "game"
    if key == "r":
        init()
    redrawAll()

######################
# Game Functions
######################

############################################################
############################################################
############################################################
#                        TASK   2                          #
############################################################
############################################################
############################################################

# Returns True if the player's current position corresponds to a location in
# board which represents a "goal", and False otherwise.
def frogInGoal():
    if canvas.data.pos[0] == 0 and canvas.data.pos[1] == 1:
        return True
    elif canvas.data.pos[0] == 0 and canvas.data.pos[1] == 4:
        return True
    elif canvas.data.pos[0] == 0 and canvas.data.pos[1] == 7:
        return True
    elif canvas.data.pos[0] == 0 and canvas.data.pos[1] == 10:
        return True
    elif canvas.data.pos[0] == 0 and canvas.data.pos[1] == 13:
        return True
    else:
        return False

# Returns True if the player's current postion is a location where the player
# will die, and False otherwise.  The player will die if a car is occupying
# the same space, or if the player is standing on a board location with water
# and no lily pad or log is occupying the same space.
def frogDies():
    row = canvas.data.pos[0]
    col = canvas.data.pos[1]
    if canvas.data.board[row][col] == "frog":
        canvas.data.lives -= 1
        return True
    elif canvas.data.board[row][col] == "water":
        for lily in canvas.data.lilies:
            if lily[0] == row and lily[1] == col:
                return False
        for logs in canvas.data.logs:
            if logs[0] == row and logs[1] == col:
                return False
        else:
            return True
    elif canvas.data.board[row][col] == "road":
        for cars in canvas.data.cars:
            if cars[0] == row and cars[1] == col:
                return True
    else:
        return False

# Moves the player one space in the given direction, if movement is possible.
# Tests to see if the player has entered a board space representing a "goal"
# or if the player dies, and updates the game and values as necessary.
def moveFrog(direction):      
    if direction == "Up" and canvas.data.pos[0] > 0:
        canvas.data.pos[0] -= 1
    elif direction == "Down" and canvas.data.pos[0] < canvas.data.rows - 1:
        canvas.data.pos[0] += 1
    elif direction == "Left" and canvas.data.pos[1] > 0:
        canvas.data.pos[1] -= 1
    elif direction == "Right" and canvas.data.pos[1] < canvas.data.cols - 1:
        canvas.data.pos[1] += 1

    if frogInGoal() == True:
        row = canvas.data.pos[0]
        col = canvas.data.pos[1]
        canvas.data.board[row][col] = "frog"
        canvas.data.pos[0] = 12
        canvas.data.pos[1] = 7
        if fullBoard() == True:
            beatLevel()
        
    if frogDies() == True:
        canvas.data.pos[0] = 12
        canvas.data.pos[1] = 7
        canvas.data.lives -= 1
        if canvas.data.lives == 0:
            gameOver()   
    pass

############################################################
############################################################
############################################################
#                        TASK   W                          #
############################################################
############################################################
############################################################

# Moves each of the floating logs one space in the direction of their motion.
# If the player is standing on the log, also moves the player.
def moveLogs():
    dfrog = None
    for log in canvas.data.logs:
        if log[2] == "Right":
            dcol = 1
        else:
            dcol = -1
        if canvas.data.pos == [log[0], log[1]]:
            # player is standing on this log
            dfrog = log[2]
        log[1] += dcol
        log[1] %= canvas.data.cols
        # allows wrap-around
    if dfrog != None:
        # player is on a log that moved
        moveFrog(dfrog)

# Moves each of the floating lily pads on space in the direction of their
# motion.  If the player is standing on the lily pad, also moves the player.
def moveLilies():
    dfrog = None
    for lily in canvas.data.lilies:
        if lily[2] == "Right":
            dcol = 1
        else:
            dcol = -1
        if canvas.data.pos == [lily[0], lily[1]]:
            # player is standing on this lily pad
            dfrog = lily[2]
        lily[1] += dcol
        lily[1] %= canvas.data.cols
        # allows wrap-around
    if dfrog != None:
        # player is standing on a lily pad that moved
        moveFrog(dfrog)


# Moves each of the cars one space in the direction of their motion.
def moveCars():
    for car in canvas.data.cars:
        if car[2] == "Right":
            car[1] += 1
        else:
            car[1] -= 1
        car[1] %= canvas.data.cols
        # allows wrap-around

        
# Advance to the next level.  Updates level,delay, and lives, and then
# reinitializes all other values.  On level 4, ends the game.
def beatLevel():
    if canvas.data.level == 4:
        canvas.data.state = "win"
    else:
        level = canvas.data.level
        delay = canvas.data.delay
        lives = canvas.data.lives
        init()
        canvas.data.level = level+1
        canvas.data.delay = delay - 100
        canvas.data.lives = lives
        canvas.data.state = "game"

# Changes the game state to "lose" so that the game over screen will be drawn.
def gameOver():
    canvas.data.state = "lose"


# Returns True if there are no empty "goal" spaces remaining on the board, and
# False otherwise.
def fullBoard():
    for row in canvas.data.board:
        for x in row:
            if x=="goal":
                return False
    return True


# Moves cars, lily pads, and logs.  Must test if the player dies because a
# car may have moved onto the player's location.
def updateGame():
    moveCars()
    moveLilies()
    moveLogs()
    if frogDies():
        canvas.data.pos = [12, 7]
        canvas.data.lives -= 1
        if canvas.data.lives == 0:
            gameOver()

# Updates the game if necessary, then calls timerFired after canvas.data.delay
# milliseconds.
def timerFired():
    if not canvas.data.paused:
        updateGame()
    delay = canvas.data.delay
    redrawAll()
    canvas.after(delay, timerFired)



######################
######################
# Drawing
######################
######################


# Draws each log in canvas.data.logs.
def drawLogs():
    size = canvas.data.cellSize
    for log in canvas.data.logs:

        row = log[0]
        col = log[1]
        x1 = col*size
        x2 = x1+size
        y1 = row*size+size/5
        y2 = y1+(size/5)*3
        w = 0
        color = canvas.data.colors["log"]
        canvas.create_rectangle(x1,y1,x2,y2,fill=color, width = w)

# Draws each lily pad in canvas.data.lilies.       
def drawLilies():
    size = canvas.data.cellSize
    for lily in canvas.data.lilies:
        row = lily[0]
        col = lily[1]
        x1 = col*size
        x2 = x1+size
        y1 = row*size
        y2 = y1+size
        w = 1
        color = canvas.data.colors["lily"]
        color2 = canvas.data.colors["water"]
        canvas.create_oval(x1+2,y1+2,x2-2,y2-2,fill=color, width = 0)
        canvas.create_polygon(x1,y1+7,x1+size/2-5,y1+size/2,x1,y2-7, \
                              fill=color2, width = 0)


# Draws each car in canvas.data.cars.
def drawCars():
    size = canvas.data.cellSize
    tenth = size/10
    for car in canvas.data.cars:
        row = car[0]
        col = car[1]
        x1 = col*size
        x2 = x1+size
        y1 = row*size
        y2 = y1+size
        w = 1
        canvas.create_rectangle(x1+tenth,y1+size/5,x2-tenth,y2-size/5, \
                                fill=car[3], width = 0)
        canvas.create_rectangle(x1+tenth,y1+tenth,x1+3*tenth,y1+2*tenth, \
                                fill = "black")
        canvas.create_rectangle(x2-3*tenth,y1+tenth,x2-tenth,y1+2*tenth, \
                                fill = "black")
        canvas.create_rectangle(x1+tenth,y2-2*tenth,x1+3*tenth,y2-tenth, \
                                fill = "black")
        canvas.create_rectangle(x2-3*tenth,y2-2*tenth,x2-tenth,y2-tenth, \
                                fill = "black")

# Draws the player.
def drawFrog(row, col):
    size = canvas.data.cellSize
    x1 = col*size+size/4
    x2 = x1+size/2
    y1 = row*size + size/4
    y2 = y1+size/2
    w = 1
    canvas.create_oval(x1+3,y1,x2-3,y2,fill="green", width = 0)
    # front legs
    canvas.create_line(x1-2,y1+7,(x1+x2)/2,(y1+y2)/2,fill="green", width=4)
    canvas.create_line(x2+2,y1+7,(x1+x2)/2,(y1+y2)/2,fill="green", width=4)
    # back legs
    canvas.create_line(x1-1,y2-6,(x1+x2)/2,y2-2,fill="green",width=5)
    canvas.create_line(x2+1,y2-6,(x1+x2)/2,y2-2,fill="green",width=5)
    # feet: top left, top right, bottom left, bottom right
    canvas.create_line(x2+2,y1+8,x2+2,y1+4,fill="green", width = 4)
    canvas.create_line(x1-2,y1+8,x1-2,y1+4,fill="green", width = 4)
    canvas.create_line(x1-3,y2-6,x1-3,y2-10,fill="green", width = 4)
    canvas.create_line(x2+3,y2-6,x2+3,y2-10,fill="green", width = 4)
    canvas.create_oval(x1+5,y1+3,x1+8,y1+6,fill="black")
    canvas.create_oval(x2-8,y1+3,x2-5,y1+6,fill="black")

def drawFrogs():
    board = canvas.data.board
    pos = canvas.data.pos
    drawFrog(pos[0],pos[1])
    for col in range(len(board[0])):
        if board[0][col] == "frog":
            drawFrog(0,col)
            
# Draws the text displaying lives, levels, and pause on the bottom of the
# screen.
def drawData():
    livesMessage= "Lives: %d" % canvas.data.lives
    canvas.create_text(canvas.data.width/9, canvas.data.height-25, \
                       anchor = CENTER, fill = "white", text = livesMessage, \
                       font = "Helvetica 25 bold")
    levelMessage = "Level: %d" % canvas.data.level
    canvas.create_text(canvas.data.width*9/10, canvas.data.height-25, \
                       anchor = CENTER, fill = "white", text = levelMessage, \
                       font = "Helvetica 25 bold")
    if canvas.data.paused:
        canvas.create_text(canvas.data.width/2, canvas.data.height-25, \
                           anchor = CENTER, fill = "white", text = "PAUSED", \
                           font = "Helvetica 25 bold")

# Draws the splash screen at the start of the game.
def drawSplash():
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height, \
                            fill = "black")
    canvas.create_text(canvas.data.width/2,canvas.data.height/5, \
                       anchor = CENTER, text = "FROGGER", \
                       font = "Courier 50 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/6*3, \
                       text = "Use arrow keys to move, 'p' to pause", \
                       font = "Helvetica 30 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/6*4, \
                       text = "Try to reach the white squares", \
                       font = "Helvetica 30 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/6*5, \
                       text = "Press 'space' to start", \
                       font = "Helvetica 30 bold", fill = "white")

# Draws the winning game over screen.
def drawWin():
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height, \
                            fill = "black")
    canvas.create_text(canvas.data.width/2,canvas.data.height/4, \
                       anchor = CENTER, text = "GAME OVER!", \
                       font = "Courier 50 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/3, \
                       anchor = CENTER, text = "YOU WON", \
                       font = "Courier 50 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/3*2, \
                       text = "Press 'r' to restart", \
                       font = "Helvetica 30 bold", fill = "white")

# Draws the losing game over screen.    
def drawLose():
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height, \
                            fill = "black")
    canvas.create_text(canvas.data.width/2,canvas.data.height/4, \
                       anchor = CENTER, text = "GAME OVER!", \
                       font = "Courier 50 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/3, \
                       anchor = CENTER, text = "YOU LOST", \
                       font = "Courier 50 bold", fill = "white")
    canvas.create_text(canvas.data.width/2,canvas.data.height/3*2, \
                       text = "Press 'r' to restart", \
                       font = "Helvetica 30 bold", fill = "white")

# Draws a black rectangle behind the board.
def drawBackground():
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height, \
                            fill="black")    



############################################################
############################################################
############################################################
#                        TASK   1                          #
############################################################
############################################################
############################################################


# Given a row and column, draws a square representing the current value at
# row and column in canvas.data.board.
def drawCell(row, col):
    x = canvas.data.board[row][col]
    color = canvas.data.colors[x]
    canvas.create_rectangle(col*canvas.data.cellSize, row*canvas.data.cellSize, col*canvas.data.cellSize + canvas.data.cellSize, row*canvas.data.cellSize + canvas.data.cellSize, fill = color)
    pass

# Loops through all the indexes of row and column in canvas.data.board, and
# calls drawCell with each row and column.
def drawBoard():
    #canvas.data.board
    for row in range (canvas.data.rows):
        for col in range (canvas.data.cols):
            drawCell(row, col)
    pass

# Draws everything in the game state.
def drawGame():
    drawBackground()
    drawBoard()
    drawLogs()
    drawCars()
    drawLilies()
    drawFrogs()
    drawData()
    pass


############################################################
############################################################
############################################################
#                        TASK   1                          #
############################################################
############################################################
############################################################


# Erase everything, then draw to the screen based on the current game state.
def redrawAll():
    canvas.delete(ALL)
    if canvas.data.state == "splash":
        drawSplash()
    elif canvas.data.state == "win":
        drawWin()
    elif canvas.data.state == "lose":
        drawLose()
    elif canvas.data.state == "game":
        drawGame()
    else:
        pass



######################    
######################
# Init
######################
######################

# Create an array of all cars in the level.  Each car is represented as a list
# of [row, column, direction, color].
def createCars():
    cars = [[10,0,"Right"],[10,1,"Right"],[10,7,"Right"],[10,8,"Right"],
            [10,4,"Right"],[10,11,"Right"],
            [9,1,"Left"],[9,4,"Left"],[9,7,"Left"],[9,10,"Left"],[9,13,"Left"],
            [8,6,"Right"],[8,7,"Right"],[8,8,"Right"],[8,9,"Right"],
            [8,10,"Right"],[8,11,"Right"],
            [7,4,"Left"],[7,5,"Left"],[7,6,"Left"],[7,10,"Left"],[7,11,"Left"],
            [7,0,"Left"]            
           ]
    colors = ["red","orange","yellow","cadet blue","magenta","cyan"]
    for car in cars:
        car.append(colors[randint(0,len(colors)-1)])
    return cars

# Create an array of all logs in the level.  Each log is represented as a list
# of [row, column, direction].
def createLogs():
    return [[1,0,"Right"],[1,1,"Right"],[1,2,"Right"],
            [1,6,"Right"],[1,7,"Right"],
            [1,11,"Right"],[1,12,"Right"],

            [3,8,"Right"],[3,9,"Right"],[3,10,"Right"],[3,11,"Right"],
            [3,1,"Right"],[3,2,"Right"],[3,3,"Right"],

            [4,4,"Left"],[4,5,"Left"],[4,6,"Left"],
            [4,10,"Left"],[4,11,"Left"],
            [4,0,"Left"],[4,1,"Left"]
           ]

# Create an array of all lily pads in the level.  Each lily pad is represented
# as a list of [row, column, direction].
def createLilies():
    return [[5,0,"Right"],[5,1,"Right"],
            [5,5,"Right"],[5,6,"Right"],
            [5,10,"Right"],[5,11,"Right"],
            
            [2,1,"Left"],[2,2,"Left"],[2,3,"Left"],
            [2,8,"Left"],[2,9,"Left"],[2,10,"Left"]
           ]

                        
#Returns starting board, represented as 2D list
def createBoard():
    board = [['water','goal','water','water','goal','water','water','goal', \
              'water', 'water','goal','water','water','goal','water'],
             ['water']*15,
             ['water']*15,
             ['water']*15,
             ['water']*15,
             ['water']*15,
             ['dirt']*15,
             ['road']*15,
             ['road']*15,
             ['road']*15,
             ['road']*15,
             ['road']*15,
             ['dirt']*15,]
    return board

# Creates a dictionary where board elements map to the color of the element.
def createColors():
    d = dict()
    d["goal"] = "white"
    d["water"] = "navy"
    d["dirt"] = "brown"
    d["road"] = "gray19"
    d["frog"] = "white"
    d["log"] = "saddle brown"
    d["lily"] = "darkgreen"
    return d

#Set initial game values
def init():
    canvas.data.rows = 13
    canvas.data.cols = 15
    canvas.data.cellSize = 50
    canvas.data.startPos = [12, 7]
    canvas.data.pos = canvas.data.startPos

    canvas.data.board = createBoard()
    canvas.data.lilies = createLilies()
    canvas.data.cars = createCars()
    canvas.data.logs = createLogs()
    canvas.data.colors = createColors()

    canvas.data.level = 1
    canvas.data.lives = 100
    canvas.data.delay = 700
    canvas.data.state = "splash"
    canvas.data.paused = True



######################
######################
# Run
######################
######################

# Creates global canvas and canvas.data.struct.  Initializes starting values
# and begins timerFired loop.
def run():
    global canvas
    root = Tk()
    canvas = Canvas(root, width=750, height=700)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width = 750
    canvas.data.height = 700
    init()
    root.bind("<Key>", keyPressed)
    timerFired()
    root.mainloop()
    
run()
