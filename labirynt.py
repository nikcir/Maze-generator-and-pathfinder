import pygame
import numpy as np
from random import randint
import os
import json
import heapq
from time import sleep

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
PURPLE = (128, 0, 128)

class Main:
    def __init__(self):
        self.running = True
        
        self.numbox = 100
        self.width = 800
        self.height = 800
        self.togglelines = False
        
        self.boxdim = self.width//self.numbox
        self.neig = [       (-1, 0),
                  (0, -1),           (0, 1),
                             (1, 0)]
        self.load = input("load/generate/test/path l/g/t/p: ")
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("lab")

        if self.load in ("g","t"):
            self.allmap = {}
            self.create_grid()
        elif self.load in ("l", "p"):
            self.loader()

        if self.load == "p":
            self.speed = input("select drawing speed: steps/intant/turbo: (s/i/t): ")
            self.findpath()
        else:
            self.run()

    def create_grid(self):
        gridd = [0]*self.numbox**2
        self.grid = np.reshape(gridd,(self.numbox,self.numbox))
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                if y%2==0:
                    self.grid[x][y]=1
                elif x%2==0:
                    self.grid[x][y]=1
                else:
                    self.grid[x][y]=0
                    self.allmap[(x,y)] = (x,y)
    
    def draw_grid(self):
        self.screen.fill(WHITE)
        for x in range(self.numbox):
            for y in range(self.numbox):
                if self.grid[x][y]==1:
                    color = BLUE
                elif self.grid[x][y]==2:
                    color = RED
                elif self.grid[x][y]==3:
                    color = GREEN
                elif self.grid[x][y]==4:
                    color = PURPLE
                else:
                    color = BLACK

                rect = pygame.Rect(x*self.boxdim, y*self.boxdim, self.boxdim, self.boxdim)
                pygame.draw.rect(self.screen, color, rect)

                if self.togglelines:
                    pygame.draw.rect(self.screen, WHITE, rect, 1)

    def check_neibourhhs(self,x,y):
        open_values = []
        for e,f in self.neig:
            try:
                if self.grid[e+x][f+y] == 0:
                    if self.allmap[(x+e,y+f)] in open_values:
                        return
                    else:
                        open_values.append(self.allmap[(x+e,y+f)])
            except:
                pass
        if len(open_values)>=2:
            self.grid[x][y] = 0
            for value in open_values[1:]:
                self.update_mapvalues(open_values[0],value)
            
    
    def choose_rand(self):
        return randint(0,self.numbox-1)

    def update_mapvalues(self,new,old):
        for key, value in self.allmap.items():
            if value == old:
                self.allmap[key] = new

    def saver(self):
        if self.load=="t":
            return
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir,"data", "matrix_data.json")
        if self.load=="g":

            savedata = {
                "matrix":self.grid.tolist(),
                "numbox":self.numbox,
                "width" :self.width,
                "height":self.height
            }
            
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(savedata, f, indent=4)


    def loader(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir,"data", "matrix_data.json")
        with open(file_path, "r", encoding="utf-8") as f:
            loaddata = json.load(f)

        self.numbox = loaddata["numbox"]
        self.width = loaddata["width"]
        self.height = loaddata["height"]
        self.grid = np.array(loaddata["matrix"])


    def generator(self):
        self.check_neibourhhs(self.choose_rand(),self.choose_rand())

    

    def dijkstra(self, start=tuple, goal=tuple):
        
        distances = { (x, y): float("inf") for x in range(self.numbox) for y in range(self.numbox) if self.grid[x][y] != 1 }
        previous = { (x, y): None for (x, y) in distances }
        distances[start] = 0

        #priority que
        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current == goal:
                break 

            if current_dist > distances[current]:
                continue  

            cx, cy = current
            for dx, dy in self.neig:  
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.numbox and 0 <= ny < self.numbox:
                    if self.grid[nx][ny] != 1: 
                        new_dist = current_dist + 1 
                        if new_dist < distances[(nx, ny)]:
                            distances[(nx, ny)] = new_dist
                            previous[(nx, ny)] = current
                            heapq.heappush(pq, (new_dist, (nx, ny)))

        path = []
        if goal in previous and distances[goal] != float("inf"):
            node = goal
            while node is not None:
                path.insert(0, node)
                node = previous[node]
        else:
            print("Goal not reachable")

        return path



    def run(self):
        if self.load in ("l", "p"):
            self.loader()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            

            if self.load in ("t","g"):
                self.generator()

            # elif self.load=="p":
            #     # print(self.dijkstra((1,1),(13,1)))
            #     for e in self.dijkstra((1,1),(13,1)):
            #         self.grid[e] = 2

            self.draw_grid()
            pygame.display.flip()
            # self.clock.tick(60)
        pygame.quit()
        self.saver()

    def findpath(self):
        Running = True
        while Running:
            self.loader()
            while True:
                start = (randint(0,self.numbox-1),randint(0,self.numbox-1))
                if self.grid[start] == 0:
                    break
            while True:
                end = (randint(0,self.numbox-1),randint(0,self.numbox-1))
                if self.grid[end] == 0:
                    break
            self.grid[start], self.grid[end] = 3,4

            path = self.dijkstra(start,end)
            for e in path:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Running = False
                        break
                if e != start:
                    self.grid[e] = 2

                    if self.speed == "s":
                        self.draw_grid()
                        pygame.display.flip()
            self.draw_grid()
            pygame.display.flip()
            # self.clock.tick(60)
            if self.speed == "i":
                sleep(0.5)


            # for e in path:
            #     if e != start:
            #         self.grid[e] = 2
            # for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             Running = False
            #             break

        pygame.quit()

if __name__ == "__main__":
    Main()



