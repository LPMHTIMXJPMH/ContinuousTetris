import cv2 as cv
import numpy as np
import sys
import os
import time
import pickle

sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import board
import methods
import Contours
import config
import grid

image_path = 'tetris_pixel/frame1.jpg'
before = time.time()
where_to_draw =  np.zeros( [ 1080, 1920 ,3], dtype = np.uint8 )
board_height = 14
board_width = 10

src = cv.imread(image_path)
assert src is not None, "Image has not been read!"
print('size')
print(len(src))
print('len(src[0])', len(src[0]))
# cv.imshow('original image', src)
# cv.waitKey()

###########################################
# Calculate board position and direction #
###########################################
board_hsv, res = methods.hsv(src)
# cv.imshow('board_hsv', board_hsv)
# cv.waitKey()
board_cnt = Contours.findCnt(board_hsv, config.Thresh)
num = len(board_cnt)
assert num == 1,"error on finding board contour in Countours.findCnt()"
# filling contour/contours(Board contour) black to speed up?
# cv.drawContours(src, board_cnt, -1, color=(0, 0, 0), thickness=cv.FILLED)
# findCnt() usually return a 2d list contain multiple contours
# In this case, only one board contour:[[board_contour]][0]
board_cnt = board_cnt[0]
methods.draw(where_to_draw, board_cnt, obv = 4)

minRec, board_box = Contours.minRec(board_cnt)
print('board_box <-> board corners\n', board_box)
board.draw_box(where_to_draw, board_box)
corners = methods.rect_corner(board_box)
print('corners ', corners)
board_vector = board.orient(corners)
direvative_y, direvative_x = board.direvative_per_board_unit(corners['left_top'], corners['right_bottom'])

board_corners_vector_unit_size = []
# find board contour property: board corners coordinates, board vector
block_size = board.rectangle(where_to_draw, corners, board_width, board_height)
board_corners_vector_unit_size.append(corners)
board_corners_vector_unit_size.append(board_vector)
board_corners_vector_unit_size.append(block_size)
where = 'tetris_pixel/board_corners_vector_unit_size.pickle'
with open(where, 'wb') as f:
    print(f'"self.go_steps" with data type {type(board_corners_vector_unit_size)} saved at {where}')
    pickle.dump(board_corners_vector_unit_size, f)
print('########## BOARD PROPERTY ##########')
print('Board Location point =>   ', corners['left_bottom'])
print('Board orientation =>    {}'.format(board_vector))
print('A single board unit block in pixel size (block_size) =>   ', block_size)
print('\n')


# READ TETRIS GO STEPS AND BOARD CURRENT STATUS
gone = os.path.isfile('tetris_array/index_rotation_y_x_deque.pickle') 
if not gone:
    sys.path.insert(1, 'C:/Users/NvWa/Desktop/新建文件夹/tetris_array')
    import tetris_array.go

from collections import deque
with open('tetris_array/index_rotation_y_x_deque.pickle', 'rb') as f:
    go_steps = pickle.load(f)
    print('type(go_steps):    ', type(go_steps))
assert isinstance(go_steps, deque), 'Tetris steps data file has been read wrongly!'

with open('tetris_array/index_rotation_y_x_array.pickle', 'rb') as f:
    go_steps_array = pickle.load(f)
    print('type(go_steps_array):    ', type(go_steps_array))
assert isinstance(go_steps_array, np.ndarray), 'Tetris steps data file has been read wrongly!'

with open('tetris_array/board_self_current.pickle', 'rb') as f:
    board_final_self_current = pickle.load(f)
    print('type(board_final_self_current):    ', type(board_final_self_current))
assert isinstance(board_final_self_current, np.ndarray), 'Board self_current data file has been read wrongly!'
print('board_final_self_current\n', board_final_self_current)


##################################################
# Calculate tetris target position and direction #
##################################################
total_on_board_direction = 4
# target direction <= Use Angle || Not Radian
on_board_direction_dict = {}
on_board_direction_list = [None] * total_on_board_direction

for i in range(total_on_board_direction):
    target_angle = round(methods.vector_angle(board_vector) + i * 90, 3) # degree
    on_board_direction_dict[str(i)] = target_angle
    on_board_direction_list[i] = target_angle

print('on_board_direction_dict :    ', on_board_direction_dict)

# target position <= Use Pixel || Not mili-Meter

box_left_top_y = corners['left_top'][1]
box_left_top_x = corners['left_top'][0]
target_pixel_grab_centers = []
# coordinate (0, 0) => move from left top {python array style} to unit center {human-life-style}
steps_num = len(go_steps) // 4
assert steps_num == 34, "Go steps Error."
for i in range(steps_num):
    x       =   go_steps.pop()
    y       =   go_steps.pop()
    rotation=   go_steps.pop()
    index   =   go_steps.pop()

    angle = on_board_direction_list[rotation]

    # left_top_to_center and position y and x index begin at 1
    pixel_y = box_left_top_y + direvative_y * y
    pixel_x = box_left_top_x + direvative_x * x

    # shape index and rotation index begin at 0
    target_pixel_grab_centers.append(      index      )
    target_pixel_grab_centers.append(      rotation   )
    target_pixel_grab_centers.append(round(angle, 2)  )
    target_pixel_grab_centers.append(      y          )
    target_pixel_grab_centers.append(      x          )
    target_pixel_grab_centers.append(round(pixel_y, 2))
    target_pixel_grab_centers.append(round(pixel_x, 2))   


target_pixel_grab_centers = [target_pixel_grab_centers[i:i+7] for i in range(0, len(target_pixel_grab_centers), 7)]
target_pixel_grab_centers = sorted(target_pixel_grab_centers, key = lambda x : x[0])

after = time.time()
print(f'Initialization cost {after - before} seconds.')
# for pixel_grab_center in target_pixel_grab_centers:
#     print('\n[init_pixel_grab_center]', pixel_grab_center)