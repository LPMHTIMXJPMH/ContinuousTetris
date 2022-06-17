import cv2 as cv
import time
import sys

sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import methods
import Contours
import config
import init
from encode import pieces


where_to_draw = init.where_to_draw
board_corners = init.corners
pixel_grab_centers = init.target_pixel_grab_centers

before = time.time()
src = init.src
shapes = []
for idx in range(len(config.hsv)):
    hsv, res = methods.hsv(src, config.hsv[idx][0], config.hsv[idx][1])
    contours = Contours.findCnt(hsv, config.thresh)
    if len(contours) > 0 and len(contours) < 6: #f"Warning! No contour detected at idx = {idx}"
        for contour in contours:
            methods.draw(where_to_draw, contour, obv = 4)
        after_find_cnt = time.time()
        shape_prop = Contours.contour_property(where_to_draw, idx, contours)
        if len(shape_prop):
            shapes.append(shape_prop)
            print(f'\n[Reporting] < {len(contours)} of shape{idx} object detected >    < Showing thier contour property: >')
            print(shape_prop,'\n')
        else:
            shapes.append([idx, None, [None, None]]*5)
            print(f'Warning! The specific kind of shape object {pieces[idx]}not detected?!')
            print('"operation": shapes.append([idx, None, [None, None], [None, None]])  has been executed !')
            print('Please check "previous step": shape_prop = Contours.contour_property(where_to_draw, idx, contours)')
    else:
        print('No this kind of shape detected.')
        shapes.append([idx, None, [None, None]]*5)
after = time.time()
print('Time cost after detect all at once: ', after - before)  
cv.imshow('where_to_draw', where_to_draw)
cv.waitKey()

left_bottom = board_corners['left_bottom']
print(left_bottom)
# pixel_grab_centers
# shapes
robot = []
for shape_index, shape in enumerate(shapes):
    target_index = 0
    for single_index, current in enumerate(shape):
        single = []
        target = pixel_grab_centers[shape_index*5+target_index if shape_index*5+target_index < 34 else 0]
        if current[0] is not None:
            print('INDEX : ', current[0])
            single.append(current[0])

        if target[2] and current[1]:
            print('current angle  ', round(current[1],2))
            single.append(round(current[1],2))
            print('target angle  ', round(target[2],2))
            single.append(round(target[2],2))
            angle = target[2] - current[1]
            print('delta angle  ', round(angle,2))
            
        if target[5] and target[6] and current[2]:
            target_y = target[5]
            target_x = target[6]
            current_x = current[2][0]
            current_y = current[2][1]
            single.append([current_x,current_y])
            single.append([target_x,target_y])
            print('target_y  ',target_y)
            print('target_x  ', target_x)
            print('current_y  ',current_y)
            print('current_x  ',current_x)


            target_xy_mm = methods.linear(x = target_x, y = target_y)
            current_xy_mm = methods.linear(x = current_x, y = current_y)
            # single.append(current_xy_mm)
            # single.append(target_xy_mm)

            # print('target_xy_mm\n',target_xy_mm)
            # print('current_xy_mm\n', current_xy_mm)
            
        print('')
        robot.append(single)
        target_index += 1

print('robot  length :    ', len(robot))