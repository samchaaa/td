
### to do ###

# make baddies class
# make towers class
# make towers shoot different ascii for different angles
# make towers set first priority
# make set towers mode
# 

import csv
import copy
import time
from msvcrt import getch
import os
import math

class Game:
    
    def __init__(self, map_path):
    
        self.map = self.read_map(map_path)
        self.path = self.get_path()
        self.cl = [19, 6]
        self.baddies = {}
        self.n_baddies = 5
        self.towers = {
            0: {
                'r': 7, 
                'c': (12, 7)
            },
            1: {
                'r': 3, 
                'c': (24, 14)
            }
            
        }
        
    def read_map(self, map_path):
    
        map_ = []
        with open(map_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                map_.append(row)
                
        return map_
    
    def get_path(self):
        
        # get start pos
        for y, row in enumerate(self.map):
            if self.map[y][0] == '═':
                path = [(0, y)]
                break
        c = path[-1]
        up_last = False
        down_last = False
        right_last = False
        left_last = False

        while True:
            if c[0] == len(self.map[0])-1:
                break
            if self.map[c[1]-1][c[0]] not in ['', 'x'] and down_last == False:
                path.append((c[0], c[1]-1))
                up_last = True
                down_last = False
                left_last = False
                right_last = False
                c = (c[0], c[1]-1)
                continue
            if self.map[c[1]+1][c[0]] not in ['', 'x'] and up_last == False:
                path.append((c[0], c[1]+1))
                down_last = True
                up_last = False
                left_last = False
                right_last = False
                c = (c[0], c[1]+1)
                continue
            if self.map[c[1]][c[0]+1] not in ['', 'x'] and left_last == False:
                path.append((c[0]+1, c[1]))
                up_last = False
                down_last = False
                right_last = True
                left_last = False
                c = (c[0]+1, c[1])
                continue
            if self.map[c[1]][c[0]-1] not in ['', 'x'] and right_last == False:
                path.append((c[0]-1, c[1]))
                up_last = False
                down_last = False
                right_last = False
                left_last = True
                c = (c[0]-1, c[1])
                continue
                
        return path
    
    def render(self):
    
        temp_map = copy.deepcopy(self.map)
        
        # if cursor is 24, 2:5 (play), highlight
        # if cursor is 24, 8:13 (build), highlight
        if self.cl[0] == 24 and (self.cl[1] >= 2 and self.cl[1] <= 5):
            temp_map[24][1], temp_map[24][6] = '[', ']'
        elif self.cl[0] == 24 and (self.cl[1] >= 8 and self.cl[1] <= 12):
            temp_map[24][7], temp_map[24][13] = '[', ']'
        else:
            # else plot cursor
            temp_map[self.cl[0]][self.cl[1]] = '╬'
            
        for x in self.baddies.keys():
            if self.baddies[x][0] > 0 and self.baddies[x][1] > 0:
                temp_map[self.baddies[x][1]][self.baddies[x][0]] = '$'
        
        # plot towers
        for x in self.towers.keys():
            temp_map[self.towers[x]['c'][1]][self.towers[x]['c'][0]] = '%'
        
            for y in self.baddies.keys():
                x_dist = abs(self.baddies[y][0] - self.towers[x]['c'][0])
                y_dist = abs(self.baddies[y][1] - self.towers[x]['c'][1])
                if math.sqrt((x_dist*x_dist) + (y_dist*y_dist)) < self.towers[x]['r']:
                # if x_dist < self.towers[x]['r'] or y_dist < self.towers[x]['r']:
                    
                    q = sorted([self.baddies[y][0], self.towers[x]['c'][0]])
                    w = sorted([self.baddies[y][1], self.towers[x]['c'][1]])
                    
                    for e in range(q[0]+1, q[1]):
                        for f in range(w[0]+1, w[1]):
                            # if 
                            temp_map[f][e] = '░'
                
                    print('attack')
        # calc baddie dist
        
        
        for row in temp_map:
            for z in row:
                print(z.ljust(2), end='')
            print()
            
        return
    
    def wait(self):
    
        while True:
            keycode = ord(getch())
            # escape (?)
            if keycode == 27:
                break
            # enter key
            elif keycode == 13:
                if self.cl[0] == 24 and (self.cl[1] >= 2 and self.cl[1] <= 5):
                    self.play()
                    print('play mode')
                    continue
                if self.cl[0] == 24 and (self.cl[1] >= 8 and self.cl[1] <= 12):
                    self.render()
                    print('build mode')
                    continue
                else:
                    # prompt
                    d = input(">")
            elif keycode == 224:
                keycode = ord(getch())
                if keycode == 80:
                    loc_mod = (1, 0)
                elif keycode == 72:
                    loc_mod = (-1, 0)
                elif keycode == 75:
                    loc_mod = (0, -1)
                elif keycode == 77:
                    loc_mod = (0, 1)
    
            os.system("cls")
            self.cl[0] += loc_mod[0]
            self.cl[1] += loc_mod[1]

            self.render()
            # can print status stuff here, otherwise resumes loop until break
        
        return
            
    def play(self):
    
        # populate self.baddies
        for x in range(self.n_baddies):
            self.baddies[x] = (-10, -10)
        
        # update baddie loc, then call self.render()
        for cd in range(70):

            for x in range(self.n_baddies):
                # for each iteration, plot a baddie on the map, if '' skip
                self.baddies[x] = self.path[cd-(2*x)]
            
            os.system('cls')
            self.render()
            time.sleep(.05)
    
        return
            
        
game = Game('td map - Sheet4 (1).csv')
game.wait()

    
    
    
    
    
    