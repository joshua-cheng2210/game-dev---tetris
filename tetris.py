import turtle, random

SCALE = 32 #Controls how many pixels wide each grid square is

class Game:
    '''
Purpose: the tetris game
Instance variables: 
    self.active = the block of squares
    self.occupied = a list of all the blocks that has been spawned
    self.arranged_occupied = a list of all the squares arranged in terms of the rows
    self.eliminate_row = a list of row that is to be eliminated
    self.check_rotate = a list to  just check if all the squares in the blcok can be rotated
    self.score = the points for the game. 4 points for every square spawned. 10 points for every row that has been eliminated
    self.occupied_check = if any squares in the block is the same with any of the squares in self.occupied list
Methods: 
    self.gameloop = bring the block down by 1 unit every 300 mili sec
    self.move_left = move the block to the left
    self.move_right = move the block to the right
    self.move_down = move the block to the lowest possible height for self.valid == True
    self.rotate = to rotate the block by 90 degree clockwise
    self.valid = to check if the black exits the border or collides with other previous blocks
    self.game_over = to check if the game is over and return the score if so
    self.line_elimination = eliminate the line if it is filled iwth squares
'''

    def __init__(self):
        #Setup window size based on SCALE value.
        turtle.setup(SCALE*12+20, SCALE*22+20)

        #Bottom left corner of screen is (-1.5,-1.5)
        #Top right corner is (10.5, 20.5)
        turtle.setworldcoordinates(-1.5, -1.5, 10.5, 20.5)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        #Ensure turtle is running as fast as possible
        turtle.hideturtle()
        turtle.delay(0)
        turtle.speed(0)
        turtle.tracer(0, 0)

        #Draw rectangular play area, height 20, width 10
        turtle.bgcolor('black')
        turtle.pencolor('white')
        turtle.penup()
        turtle.setpos(-0.525, -0.525)
        turtle.pendown()
        for i in range(2):
            turtle.forward(10.05)
            turtle.left(90)
            turtle.forward(20.05)
            turtle.left(90)
        
        self.active = Block()
        self.occupied = []
        self.arranged_occupied = []
        for row in range(25):
            self.arranged_occupied.append([[], [], [], [], [], [], [], [], [], []])
        self.eliminate_row = []
        self.check_rotate = []
        self.score = 4
        print(f"Current Score: 4")

        turtle.ontimer(self.gameloop, 300)
        turtle.onkeypress(self.move_left, 'Left')
        turtle.onkeypress(self.move_right, 'Right')
        turtle.onkeypress(self.move_down, 'Down')
        turtle.onkeypress(self.rotate, 'space')
        turtle.update()
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        if self.valid(0, -1) == True:
            self.active.move(0, -1)
            turtle.update()
            turtle.ontimer(self.gameloop, 300)
        else:
            self.line_elimination()
            if self.game_over() == False:
                self.score += 4
                print("+4")
                print(f"Current Score: {self.score}")
                self.active = Block()
                turtle.ontimer(self.gameloop, 300)
            else:
                turtle.onkeypress(None, 'Left')
                turtle.onkeypress(None, 'Right')
                turtle.onkeypress(None, 'Down')
                turtle.onkeypress(None, 'space')
                print("Game Over!!")

    def move_left(self):
        if self.valid(-1, 0) == True:
            self.active.move(-1, 0)
            turtle.update()

    def move_right(self):
        if self.valid(1, 0) == True:
            self.active.move(1, 0)
            turtle.update()

    def move_down(self):
        while self.valid(0, -1) == True:
            self.active.move(0, -1)
        turtle.update()

    def rotate(self):
        # the first index of the Block() is the centre point // block of rotation
        for ssquare in self.active.squares:
            print(ssquare, end = "")
        print(" >>> ", end = "")

        for ssquares in self.active.squares[1:]:
            if ssquares.ycor() == self.active.squares[0].ycor():
                dx = self.active.squares[0].xcor() - ssquares.xcor()
                try:
                    if self.arranged_occupied[self.active.squares[0].ycor() + dx][self.active.squares[0].xcor()] == [] and 0 <= self.active.squares[0].xcor() <= 9 and 0 <= self.active.squares[0].ycor() + dx <= 19:
                        self.check_rotate.append(1)
                except:
                    None

            elif ssquares.xcor() == self.active.squares[0].xcor():
                dy = ssquares.ycor() - self.active.squares[0].ycor()
                try:
                    if self.arranged_occupied[self.active.squares[0].ycor()][self.active.squares[0].xcor() + dy] == [] and 0 <= self.active.squares[0].xcor() + dy <= 9 and 0 <= self.active.squares[0].ycor() <= 19:
                        self.check_rotate.append(2)
                except:
                    None

            else:
                dx = self.active.squares[0].xcor() - ssquares.xcor()
                dy = ssquares.ycor() - self.active.squares[0].ycor()
                try:
                    if self.arranged_occupied[self.active.squares[0].ycor() + dx][self.active.squares[0].xcor() + dy] == [] and 0 <= self.active.squares[0].xcor() + dy <= 9 and 0 <= self.active.squares[0].ycor() + dx <= 19:
                        self.check_rotate.append(3)
                except:
                    None

        print(f"{self.check_rotate} >>>", end = "")

        if len(self.check_rotate) == 3:
            for ssquares in self.active.squares[1:]:
                if ssquares.ycor() == self.active.squares[0].ycor():
                    dx = self.active.squares[0].xcor() - ssquares.xcor()
                    ssquares.goto(self.active.squares[0].xcor(), self.active.squares[0].ycor() + dx)
                elif ssquares.xcor() == self.active.squares[0].xcor():
                    dy = ssquares.ycor() - self.active.squares[0].ycor()
                    ssquares.goto(self.active.squares[0].xcor() + dy, self.active.squares[0].ycor())
                else:
                    dx = self.active.squares[0].xcor() - ssquares.xcor()
                    dy = ssquares.ycor() - self.active.squares[0].ycor()
                    ssquares.goto(self.active.squares[0].xcor() + dy, self.active.squares[0].ycor() + dx)
        
        self.check_rotate = []

        for ssquare in self.active.squares:
            print(ssquare, end = "")
        print()
                
    def valid(self, dx, dy):
        for shapes in self.active.squares:
            xxx = shapes.xcor() + dx
            yyy = shapes.ycor() + dy
           # check if any squares exit the borders, if so, update the self.occupied list and return False
            if yyy < 0 or xxx < 0 or xxx > 9:
                if yyy < 0:
                    self.occupied.append(self.active)

                    try:
                        if self.occupied[-1] == self.occupied[-2]:
                            self.occupied.pop(-1)
                    except:
                        None

                    for row in range(25):
                            self.arranged_occupied.append([[], [], [], [], [], [], [], [], [], []])
                    for bblocks in self.occupied:
                        for ssquare in bblocks.squares:
                            self.arranged_occupied[ssquare.ycor()][ssquare.xcor()] = ssquare
                return False

            #check if any of the squares collide with the position of previous squares
            for bblock in self.occupied:
                for occ in bblock.squares:
                    if occ.xcor() == xxx and occ.ycor() == yyy:
                        self.occupied.append(self.active)

                        try:
                            if self.occupied[-1] == self.occupied[-2]:
                                self.occupied.pop(-1)
                        except:
                            None

                        for row in range(25):
                            self.arranged_occupied.append([[], [], [], [], [], [], [], [], [], []])
                        for bblocks in self.occupied:
                            for ssquare in bblocks.squares:
                                self.arranged_occupied[ssquare.ycor()][ssquare.xcor()] = ssquare
                        return False
        return True

    def game_over(self):
        for bblocks in self.occupied:
            for ssquares in bblocks.squares:
                if ssquares.ycor() > 19:
                    return True
        return False

    def line_elimination(self):
        # transfer the blocks of squares into an specific arrangement
        for bblocks in self.occupied:
            for ssquare in bblocks.squares:
                self.arranged_occupied[ssquare.ycor()][ssquare.xcor()] = ssquare

        # eliminate the row of complete squares
        for row in range(len(self.arranged_occupied)):
            if [] not in self.arranged_occupied[row]:
                self.eliminate_row.append(row)
                self.score += 10
                print("Nice!")
                print(f"Current Score: {self.score}")
                for ssquare in range(len(self.arranged_occupied[row])):
                    if type(self.arranged_occupied[row][ssquare]) == Square:
                        self.arranged_occupied[row][ssquare].goto(-1, -1)
                        self.arranged_occupied[row][ssquare] = []

        # move the squares in the row above the eliminted row by (0, -1)
        for eli in self.eliminate_row:
            for row in self.arranged_occupied[eli:]:
                for ssquares in row:
                    if type(ssquares) == Square:
                        ssquares.goto(ssquares.xcor(), ssquares.ycor() - 1)        
        self.eliminate_row = []

        # update the arranged occupied list
        self.arranged_occupied = []
        for row in range(25):
            self.arranged_occupied.append([[], [], [], [], [], [], [], [], [], []])
        for bblocks in self.occupied:
            for ssquare in bblocks.squares:
                self.arranged_occupied[ssquare.ycor()][ssquare.xcor()] = ssquare

class Square(turtle.Turtle):
    '''
Purpose: to make the squares of the block
Instance variables: 
    None
Methods:
    __repr__ = is just to print the coordinate of the square
'''

    def __init__(self, x, y, color):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.shapesize(SCALE/20)
        self.speed(0)
        self.fillcolor(color)
        self.pencolor("gray")
        self.penup()
        self.goto(x, y)
    
    def __repr__(self):
        return f"({self.xcor()}, {self.ycor()})"

class Block:
    '''
Purpose: a number of squares
Instance variables: 
    self.squares = the making of the block
Methods: 
    move = to move the block to dx and dy coordinate
'''

    def __init__(self):
        random_blocks = [
        [Square(5, 21, "cyan"), Square(3, 21, "cyan"), Square(4, 21, "cyan"), Square(6, 21, "cyan")],
        [Square(5, 21, "red"), Square(4, 22, "red"), Square(4, 21, "red"), Square(6, 21, "red")],
        [Square(4, 21, "yellow"), Square(3, 21, "yellow"), Square(5, 21, "yellow"), Square(5, 22, "yellow")],
        [Square(5, 21, "seagreen1"), Square(4, 22, "seagreen1"), Square(4, 21, "seagreen1"), Square(5, 22, "seagreen1")],
        [Square(5, 21, "green"), Square(6, 22, "green"), Square(4, 21, "green"), Square(5, 22, "green")],
        [Square(4, 21, "pink"), Square(3, 22, "pink"), Square(5, 21, "pink"), Square(4, 22, "pink")],
        [Square(5, 21, "orange"), Square(5, 22, "orange"), Square(4, 21, "orange"), Square(6, 21, "orange")]
        ]
        self.squares = random.choice(random_blocks)

    def move(self, dx, dy):
        for shapes in self.squares:
            shapes.goto(dx + shapes.xcor(), dy + shapes.ycor())

if __name__ == '__main__':
    Game()
