import numpy as np
import torch

pieces = [[[1, 1],[1, 1]],[[0, 2, 0],[2, 2, 2]],[[0, 3, 3],[3, 3, 0]],[[4, 4, 0],[0, 4, 4]],[[5, 5, 5, 5]],[[0, 0, 6],[6, 6, 6]],[[7, 0, 0],[7, 7, 7]]]

board_width,board_height = 7,8

def index_of(piece):
    return int(np.sum(piece)/4) - 1

def rotate(input_piece,n_times):
    i = [x[:] for x in input_piece]
    
    for _ in range(n_times):
        rows = len(i)
        cols = len(i[0])
        r = [[0]*rows for _ in range(cols)]
        
        for rs in range(rows):
            for cs in range(cols):
                #for y coordinate,downforward is positive
                r[cs][rows-rs-1] = i[rs][cs]
                # Or r[cs][rs] = i[rows-rs-1][cs]
        i = r
    return i


class Tetris:
    def __init__(self):
        self.reset()   
    def reset(self):
        self.remained = [2]*7
        self.current_step = 0        
        self.MissionAccomplished = False           
        self.current = np.array([[0]*board_width for r in range(board_height)])
        self.go = []
        self.choices = np.array([None] * 14)
    
    # Make sure new adding piece and previous pieces attach in y direction by using numpy diff()
    def attach(self,p,x,heights):
        wid = len(p[0])
        # board heights difference
        pattern = list(np.diff(heights[x:x+wid]))
        if wid == 1:#can't use numpy diff() though because shape '\'
            return [heights[x],x]
        # pd -> piece border shape height difference ie [[0, 3, 3],[3, 3, 0]]->[1,0,0]->[0-1=-1,0-0=0]->[-1,0]
        pd = list(np.diff(self.heights(p = p, wid = wid)))
        if pattern == pd:
            # check if piece[0][0] position is None
            if p[0][0]:
                y = heights[x]
            elif p[1][0]:
                y = heights[x]-1
            else:
                y = heights[x]-2
            #return suitable position for adding piece attatch other pieces
            return [y,x]
        
    # return board empty "height" in y direction
    # or return piece "height"
    def heights(self,p, wid = board_width):
        heights = [board_height]*wid
        if wid == board_width:
            reverse = np.transpose(p[::-1])
        else:
            reverse = np.transpose(p)
        for idx,col in enumerate(reverse):
            for i,e in enumerate(col):
                if e != 0:
                    heights[idx] = i
                    break

        return np.array(heights)
        
    
    # add piece to board, only non-zero element in piece array will be added
    def board_add_pieces(self, adding_piece, y, x, board, real = False):
        a = adding_piece
        idx = index_of(a)
        if real:
            self.remained[idx] = self.remained[idx] - 1
            b = board
        else:
            b = board.copy()
        for r in range(len(a)):
            for c in range(len(a[r])):
                if a[r][c]:
                    row = y + r
                    col = x + c
                    b[row, col] = a[r][c]
        return b
    
    def draw_back(self, i, r, y, x):
        b = rotate(pieces[i], n_times = r)
        self.remained[i] = self.remained[i] + 1
        for r in range(len(b)):
            for c in range(len(b[r])):
                if b[r][c]:
                    row = y + r
                    col = x + c       
                    self.current[row, col] = 0
        return self.current
        
    # check if piece over border in y direction
    def y_border(self,p_length,y,min_y):
        end_y = y + p_length
        if end_y > board_height or end_y > min_y+5:
            return True
        else:
            return False
    
    def pity(self,state, remained, choice):
        print(state)
        pity = False
        print(remained)
        if len(self.next_steps(state, remained)) < sum(remained):
            pity = True
        return pity 

    # find all possible next step in a single step
    def next_step(self,state):
        next_step = {}
        heights = board_height - self.heights(state.copy())
        x = np.argmin(heights)
        for i,e in enumerate(self.remained):
            if e > 0:
                if i == 0:
                    rot = 1
                elif i == 2 or i == 3 or i == 4:
                    rot = 2
                else:
                    rot = 4
                
                p = pieces[i]
                for r in range(rot):
                    yxs = self.attach(p,x,heights)
                    if yxs:
                        colli = self.y_border(len(p),yxs[0],int(np.min(heights)))
                        if not colli:
                            choice = (i,r,yxs[0],x)
                            state = self.board_add_pieces(p, yxs[0], x, self.current)
                            next_step[choice] = state
                    p = rotate(p,n_times = 1)
        return next_step    
    
    # self.choices[14 - sum(self.remained)]
    def autoPlay(self):
        self.MissionAccomplished = False
        new = False
        while not (self.MissionAccomplished):
            print(self.remained)
            print(self.current)
            play = self.next_step(self.current)
            l = len(play)
            if self.choices[14 - sum(self.remained)] is None:
                self.choices[14 - sum(self.remained)] = l
            if self.choices[14 - sum(self.remained)]:
                choices, states = zip(*play.items())
                choice = choices[self.choices[14 - sum(self.remained)] - 1]
                state = self.board_add_pieces(rotate(pieces[choice[0]], n_times = choice[1]), choice[2], choice[3], self.current, real = True)
                for _ in range(4):
                    self.go.append(choice[_])
                if sum(self.remained) == 0:
                    self.MissionAccomplished = True
            else:
                print('draw it back')
                p_x = self.go.pop()
                p_y = self.go.pop()
                p_r = self.go.pop()
                p_i = self.go.pop()
                state = self.draw_back(p_i,p_r,p_y,p_x)
                self.choices[14 - sum(self.remained)] -= 1
                r = 14 - sum(self.remained)
                self.choices[r+1:] = None
        if not sum(self.remained):
            self.MissionAccomplished = True
            
tetris = Tetris()
tetris.autoPlay()
print("Mission Accomplished")
print("Remained",tetris.remained)
print(tetris.current)