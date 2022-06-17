import numpy as np
import sys

sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import methods

def sample(box, edge, dense = 5):
    assert dense % 2, "dense should be odd number"
    room = dense - 1
    short, long = sorted(edge)[0], sorted(edge)[1]
    
    corners = methods.rect_corner(box)
    left_top = corners['left_top']
    right_top = corners['right_top']
    left_bottom = corners['left_bottom']
    right_bottom = corners['right_bottom']

    amount = ( long * short * room * room + (long+short) * room + 1) * 2
    grid = np.zeros(amount)

    left_right = ( np.linalg.norm([r - l for r, l in zip(right_top,left_top)]) + np.linalg.norm([r - l for r, l in zip(left_bottom,right_bottom)]) ) / 2
    top_bottom = ( np.linalg.norm([t - b for t, b in zip(left_top,left_bottom)]) + np.linalg.norm([t - b for t, b in zip(right_top,right_bottom)]) ) / 2

    standing = True if top_bottom > left_right else False
    if standing:
        D = ( ( (right_top[0] - left_top[0]) + (right_bottom[0] - left_bottom[0]) ) / 2 / short + ( (left_bottom[1] - left_top[1]) + (right_bottom[1] - right_top[1]) ) / 2 / long ) / 2
        grid = grid.reshape( long*room + 1, short*room + 1, 2 )
    else:
        D = ( ( (right_top[0] - left_top[0]) + (right_bottom[0] - left_bottom[0]) ) / 2 / long + ( (left_bottom[1] - left_top[1]) + (right_bottom[1] - right_top[1]) ) / 2 / short ) / 2
        grid = grid.reshape( short*room + 1, long*room + 1, 2 )
    d = D / room
    dx = 0
    dy = 0
    if standing:
        ROW, COL = long, short
    else:
        ROW, COL = short, long
    # x
    grid[..., 0, 0] = np.linspace(left_top[0], left_bottom[0], ROW*room+1)
    for _ in range(COL*room):
        grid[..., _+1, 0] = grid[..., _, 0] + d * 0.995

    # y
    grid[0, ..., 1] = np.linspace(left_top[1], right_top[1], COL*room+1)
    for _ in range(ROW*room):
        grid[_+1, ..., 1] = grid[_, ..., 1] + d * 0.99
    
    centers = np.zeros((ROW, COL, 2))
    for index_row, row in enumerate(grid):
        if (index_row - room//2) % room == 0:
            for index_col, row_col in enumerate(row):
                if (index_col - room//2) % room == 0:
                    centers[(index_row - room//2) // room, (index_col - room//2) // room] = row_col
    return grid, [ROW, COL], centers