import numpy as np
from collections import deque
import pickle

import base
pieces = base.pieces
board_height = base.board_height
board_width = base.board_width


def index_of(piece):
    return int(np.sum(piece)/4) - 1

def rotate(input_piece, n_times = 1):
    #for y coordinate,downforward is positive
    # (rows, cols) = input_piece.shape
    rows = len(input_piece)
    cols = len(input_piece[0])
    
    if n_times == 0:
        return input_piece
    if n_times == 1:
        rotated = np.zeros((cols, rows), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[cs][rows-rs-1] = input_piece[rs][cs]
    if n_times == 2:
        rotated = np.zeros((rows, cols), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[rows-rs-1][cols-cs-1] = input_piece[rs][cs]
    if n_times == 3:
        rotated = np.zeros((cols, rows), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[cols - cs -1][rs] = input_piece[rs][cs]

    return rotated

######################################
######################################
class Tetris:
    def __init__(self):
        self.amount = 35
        self.remained = [5]*7
        self.step = 0        
        self.play = [None] * 34
        self.MissionAccomplished = False           
        self.current = np.zeros((board_height, board_width), dtype = np.uint8)
        self.go_steps = deque()
        self.choices = np.array([None] * 34)
    
    # Make sure new adding piece and previous pieces attach in y direction by using numpy diff()
    def attach(self,p,x,heights):
        wid = len(p[0])
        # board heights difference
        pattern = list(np.diff(heights[x:x+wid]).astype(np.uint8))
        if wid == 1:#can't use numpy diff() though because shape '\'
            return [heights[x],x]
        # pd -> piece border shape height difference ie [[0, 3, 3],[3, 3, 0]]->[1,0,0]->[0-1=-1,0-0=0]->[-1,0]
        pd = list(np.diff(self.heights(p = p, wid = wid).astype(np.uint8)))
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
        return np.array(heights, dtype = np.uint8)

    
    # add piece to board, only non-zero element in piece array will be added
    def board_add_pieces(self, adding_piece, y, x, board, real = False):
        a = adding_piece
        idx = index_of(a)
        if real:
            self.step += 1
            self.remained[idx] -= 1
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
        self.step -= 1
        self.remained[i] += 1
        b = rotate(pieces[i], n_times = r)
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

    # find all possible next step in a single step
    def next_step(self, state):
        next_step = []
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
                            next_step.append([i,r,yxs[0],x])
                    p = rotate(p,n_times = 1)
        return next_step    
    
    
    # def next_step_verbose(self,state):
    #         next_step = {}
    #         heights = board_height - self.heights(state.copy())
    #         for x in range(board_width):
    #             for i,e in enumerate(self.remained):
    #                 if e > 0:
    #                     if i == 0:
    #                         rot = 1
    #                     elif i == 2 or i == 3 or i == 4:
    #                         rot = 2
    #                     else:
    #                         rot = 4
                        
    #                     p = pieces[i]
    #                     for r in range(rot):
    #                         yxs = self.attach(p,x,heights)
    #                         if yxs:
    #                             colli = self.y_border(len(p),yxs[0],int(np.min(heights)))
    #                             if not colli:
    #                                 choice = (i,r,yxs[0],x)
    #                                 state = self.board_add_pieces(p, yxs[0], x, self.current)
    #                                 next_step[choice] = state
    #                         p = rotate(p,n_times = 1)
    #         return next_step 

    # self.choices[35 - sum(self.remained)]
    
    def autoPlay(self):
        self.MissionAccomplished = False

        while not (self.MissionAccomplished):
            if self.play[self.step] is None:
                self.play[self.step] = self.next_step(self.current)
            self.choices[self.step] = len(self.play[self.step]) if self.play[self.step] else 0
            if self.choices[self.step]:
                choice = self.play[self.step][self.choices[self.step]-1]
                self.board_add_pieces(rotate(pieces[choice[0]], n_times = choice[1]), choice[2], choice[3], self.current, real = True)
                self.go_steps.append(choice[0])
                self.go_steps.append(choice[1])
                self.go_steps.append(choice[2])
                self.go_steps.append(choice[3])
                if self.step == 34:
                    self.MissionAccomplished = True
                    self.go_steps_array = np.array(self.go_steps).reshape(-1,4)
            else:
                p_x = self.go_steps.pop()
                p_y = self.go_steps.pop()
                p_r = self.go_steps.pop()
                p_i = self.go_steps.pop()
                self.draw_back(p_i,p_r,p_y,p_x)
                self.play[self.step].pop()
                self.choices[self.step] -= 1
                self.choices[self.step+1] = None
                self.play[self.step+1] = None
            
    def save_go_steps_array(self, where = 'tetris_array/index_rotation_y_x_array.pickle'):
        with open(where, 'wb') as f:
            print(f'"self.go_steps_array_array" with data type {type(self.go_steps_array)} saved at {where}')
            pickle.dump(self.go_steps_array, f)
    def save_go_steps(self, where = 'tetris_array/index_rotation_y_x_deque.pickle'):
        with open(where, 'wb') as f:
            print(f'"self.go_steps" with data type {type(self.go_steps)} saved at {where}')
            pickle.dump(self.go_steps, f)
    def save_current(self, where = 'tetris_array/board_self_current.pickle'):
        with open(where, 'wb') as f:
            print(f'"self.current" with data type {type(self.current)} saved at {where}')
            pickle.dump(self.current, f)