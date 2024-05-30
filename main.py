from tkinter import messagebox,Tk #for creating small dialogue box
import pygame
import sys

window_width=720
window_height=720

window=pygame.display.set_mode((window_width,window_height))

columns=30
rows=30

box_width=window_width//columns
box_height=window_height//rows
grid=[]
queue=[]
path=[]
class Box:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.start=False
        self.wall=False
        self.target=False
        self.queued=False
        self.visited=False
        self.neighbours=[]
        self.prior=None

    def draw(self,win,color):
        pygame.draw.rect(win,color,(self.x*box_width,self.y*box_height,box_width-2,box_height-2))

    def set_neighbours(self):
        if self.x>0:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x<columns-1:
            self.neighbours.append(grid[self.x+1][self.y])
        
        if self.y>0:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y<rows-1:
            self.neighbours.append(grid[self.x][self.y+1])

#create grid
for i in range(columns):
    arr=[]
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

#set neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box=grid[0][0]
start_box.start=True
start_box.visited=True
queue.append(start_box)

def main():

    begin_search=False
    target_box_set=False
    searching=True
    target_box=None
     
    while True:
        

        for event in pygame.event.get():  #for closing the window
            #quit window
            if(event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            
            #mouse contraol
            elif event.type==pygame.MOUSEMOTION:
                x=pygame.mouse.get_pos()[0]
                y=pygame.mouse.get_pos()[1]
                #draw wall
                if event.buttons[0]:
                    i=x//box_width
                    j=y//box_height
                    grid[i][j].wall=True
                #set target
                if event.buttons[2] and not target_box_set:
                    i=x//box_width
                    j=y//box_height
                    target_box=grid[i][j]
                    target_box.target=True
                    target_box_set=True
            #start Dijkstra Algo
            if event.type==pygame.KEYDOWN and target_box_set:
                begin_search=True

        
        if begin_search:
            if len(queue)>0 and searching:
                current_box=queue.pop(0)
                current_box.visited=True

                if current_box==target_box:
                    searching=False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for nex in current_box.neighbours:
                        if not nex.queued and not nex.wall:
                            nex.queued=True
                            nex.prior = current_box
                            queue.append(nex)

            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Path Found!")
                    searching=False
                



        window.fill((0,0,0)) #for coloring the window black (R,G,B)

        for i in range(columns):
            for j in range(rows):
                box=grid[i][j]
                box.draw(window,(161,204,209))
                
                if box.queued:
                    box.draw(window,(82,255,121))
                if box.visited:
                    box.draw(window,(160,132,232))
                if box in path:
                    box.draw(window,(159,13,127))
                if box.start:
                    box.draw(window,(0,148,0))
                if box.wall:
                    box.draw(window,(53,21,93))
                if box.target:
                    box.draw(window,(253,0,127))
                

        pygame.display.flip() #for updating the display

main()