# hw11.py
# Derrell Dunn
# Math 5364
# This is where we're getting the fancy graphics stuff we need.
from Tkinter import *
from copy import deepcopy
from collections import OrderedDict

# Define Readability constants
LIVE_CELL = 1  # Living cell
DEAD_CELL = 0  # Dead cell
LEFT_WRAP_EDGE = -1  # leftmost edge of array
RIGHT_WRAP_EDGE = 43  # rightmost edge of array
TOP_ROWWRAP_EDGE = -1  # top row of array
BOTTOM_ROWWRAP_EDGE = 22  # bottom row of array
TOP_ROW = 0
BOTTOM_ROW = 21
LEFT_COLUMN = 0
RIGHT_COLUMN = 42

##################################
###### Game of Life class.  ######
##################################
class GOL:
    def __init__(self, filename):
        self.board = {}
        self.rows = 0
        self.cols = 0
        self.generation = 1
        try:
            infile = open(filename, "r")
        except:
            print "Could not open file '%s' for reading!" % (filename)
            return
        i = 0  # This will be the index of the row we're currently reading from file.
        for line in infile:
            thisRow = line.strip() # Removing trailing newline character.
            N = len(thisRow)
            # Bookkeeping: the grid size will be the minimum necessary
            # to accomodate all of the nonempty lines.
            if N > self.cols:
                self.cols = N
            if N > 0:
                self.rows = i+1
                
            for j in range(N):
                self.board[i, j] = DEAD_CELL
                if thisRow[j] == '1':
                    self.board[i, j] = LIVE_CELL
            i += 1
        infile.close()

    def neighbors(self, row, column):
        # Write this function, as described in the assignment file.
        # It should return the number of live neighbors of the
        # cell self.board[i,j].

        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        maxrow, maxcolumn = 21, 42
  
        count = 0
        for f in sorted(set(self.board)):
            print(f)
            # if ()
        working_copy = OrderedDict((key, self.board[key]) for key in sorted(self.board))
        modified_copy = deepcopy(working_copy)
        '''
        i_s = range(1, 11)
        x_s = range(1, 11)
        # x_s = range(11, 1, -1) # Also works
        d = dict([(i_s[index], x_s[index],) for index in range(len(i_s))])
        '''
        for rowes, coles in working_copy.iterkeys():
            if rowes is BOTTOM_ROW:
                  print 'this is the value {} corresponding to row{} column {}'.format(working_copy[rowes,coles], rowes,
                                                                                       coles)
                  modified_copy[TOP_ROWWRAP_EDGE,coles]= working_copy[rowes, coles]
            if rowes is TOP_ROW:
                print 'this is the value {} corresponding to row{} column {}'.format(working_copy[rowes, coles], rowes,
                                                                                     coles)
                modified_copy[BOTTOM_ROWWRAP_EDGE, coles] = working_copy[rowes, coles]
            if coles is RIGHT_COLUMN:
                print 'this is the value {} corresponding to row{} column {}'.format(working_copy[rowes, coles], rowes,
                                                                                     coles)
                modified_copy[rowes, LEFT_WRAP_EDGE] = working_copy[rowes, coles]
            if coles is LEFT_COLUMN:
                print 'this is the value {} corresponding to row{} column {}'.format(working_copy[rowes, coles], rowes,
                                                                                     coles)
                modified_copy[rowes, RIGHT_WRAP_EDGE] = working_copy[rowes, coles]
        for rws, colms in modified_copy.iterkeys():
            print 'this is the MOdified {} corresponding to row{} column {}'.format(modified_copy[rws, colms], rws,
                                                                                 colms)
        #Sort again for efficiency
        modified_copy = OrderedDict((key, modified_copy[key]) for key in sorted(modified_copy))
        print 'Sorted FINAL copy'
        for f in modified_copy:
            print f
        #Let's look for living neighbors!!
        for offset in offsets:
            r = row + offset[0]
            c = column + offset[1]
            if (0 <= r < maxrow) and (0 <= c < maxcolumn) and modified_copy[row, column] == LIVE_CELL:
                count += 1
        return count

    def  nextGeneration(self):
        # Write this function, as described in the assignment file.
        # leave this next line at the end of this function;
        # it's how we keep track of the generation we're 
        # on so we can report it on the screen, but that's all it's used for.
        newboard = deepcopy(self)
        row = 3
        column = 4
        GOL.neighbors(newboard, row, column)
        print 'after call to neighbors'
        self.generation += 1


    def numRows(self):
        return self.rows

    def numCols(self):
        return self.cols

    def isAlive(self, row, col):
        if (row>=0) and (row<self.rows) and (col>=0) and (col<self.cols):
            if self.board[row,col] is LIVE_CELL:
                return True
        return False

    def generation(self):
        return self.generation


#####################################################
## Do not change anything below here!! Feel free   ##
## to read it if you want to see the overall logic ##
## of the whole program, though.                   ##
#####################################################
class Plot:
    master = Tk()
    def __init__(self):
        self.canvasW = 800
        self.canvasH = 600
        self.w = Canvas(self.master, width=self.canvasW, height=self.canvasH)
        self.w.pack()


    def update_screen(self):
        self.master.update_idletasks()


    def clear_screen(self, color):
        # First destroy the previous canvas widget to free up the
        # associated memory.
        self.w.destroy()
        self.w = Canvas(self.master, width=self.canvasW, height=self.canvasH)
        self.w.pack()
        # Now fill the entire screen with a solid color
        self.w.create_rectangle(0,0,self.canvasW-1,self.canvasH-1,fill=color)


    def draw_grid(self, rowHeights, columnWidths, color):
        W = self.canvasW
        H = self.canvasH
        # First draw the vertical lines
        c=1
        while (c < W):
            self.w.create_line(c,0,c,H-1,fill=color)
            c += columnWidths
        # Now the horizontal
        r=0
        while (r<H):
            self.w.create_line(0,r,W-1,r,fill=color)
            r += rowHeights


    def label_screen(self, color, label):
        self.w.create_text(0, 0, text=label,anchor="nw",fill=color) 


    def plotPoint(self,x, y, color):
        self.w.create_rectangle(x-0.5, y-0.5, x+0.5, y+0.5, fill=color,outline=color)


    def plotCell(self, r, c, height, width,color):
        padW = 0.1*width
        padH = 0.1*height
        self.w.create_oval(c*width+padW, r*height+padH, (c+1)*width-padW, (r+1)*height-padH, fill=color,outline=color)


    def pixelW(self):
        # Gives the width of each pixel in Cartesian coordinates.
        return (self.BR_x - self.TL_x)/float(self.cavasW)


    def pixelH(self):
        # Gives the height of each pixel in Cartesian coordinates.
        return (self.TR_y - self.BL_y)/float(self.canvasH)


    def canvas_width(self):
        return self.canvasW


    def canvas_height(self):
        return self.canvasH


    def canvas_to_cartesian(self, pixelX, pixelY):
        # Returns Cartesian coordinates associated with (a corner of)
        # the given pixel.
        x = self.TL_x + (self.BR_x - self.TL_x)*pixelX/float(self.canvasW)
        y = self.BR_y + (self.TL_y - self.BR_y)*pixelY/float(self.canvasH)
        return [x,y]


########################################################
def colorFromRGB(r, g, b):
    # R, G, B are floating point numbers between 0 and 1 describing
    # the intensity level of the Red, Green and Blue components.
    X = [int(r*255), int(g*255), int(b*255)]
    for i in range(3):
        if X[i]<0:
            X[i] = 0
        if X[i]>255:
            X[i]=255
    color = "#%02x%02x%02x"%(X[0],X[1],X[2])
    return color


#####################################################
def drawScreen(n):
    # This function redraws the Game of Life screen. If n=0,
    # the screen is just drawn once. But if n > 0, we will
    #      (1) update the GOL once,
    #      (2) redraw the screen,
    # and repeat these steps n-1 more times (e.g., n times total).

    w = myPlot.canvas_width()
    h = myPlot.canvas_height()

    r = G.numRows()
    c = G.numCols()
    if (r <=0) or (c <=0):
        return # There's nothing to draw!

    # Figure out how wide each row and column should be to
    # fit nicely in the window.
    rowheight = h/r
    colwidth  = w/c
    aliveColor = colorFromRGB(1.0, 1.0, 1.0)
    deadColor = colorFromRGB(0.0, 0.0, 0.0)
    gridColor = colorFromRGB(0,0,1.0)

    done = False
    updates = 0
    while not(done):
        if (updates < n):
            G.nextGeneration()
            updates += 1
        myPlot.clear_screen(deadColor)
        myPlot.draw_grid(rowheight, colwidth, gridColor)
        for i in range(r):
            for j in range(c):
                if G.isAlive(i,j):
                    myPlot.plotCell(i, j, rowheight, colwidth, aliveColor)
        myPlot.update_screen()
    
        # Draw the generation label on the screen.
        genColor = colorFromRGB(1.0, 0.5, 0.5)
        myPlot.label_screen(genColor, "Generation: "+str(G.generation))
        if updates >= n:
            done = True
    

###########################################
### Entry point. Execution begins here. ###
###########################################
G = GOL("input.txt") # Load the input file.

myPlot = Plot() # This creates an object which holds the canvas widget that we draw on.

# These functions create two buttons with 'callback' functions; that is,
# when the buttons are clicked, the specified functions will be called.
Button(text="Advance 1 generation", command=lambda:drawScreen(1)).pack()
Button(text="Advance 10 generations", command=lambda:drawScreen(10)).pack()

drawScreen(0) # Draw the first generation.

# Cede control to the function mainloop(). That function just waits for
# events such as mouse clicks and handles them appropriately. The only things
# we've told it how to handle are clicks on the two buttons we created, so
# it won't do much else besides look for clicks on those buttons.
mainloop()
