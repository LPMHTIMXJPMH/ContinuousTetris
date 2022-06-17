import sys
import numpy as np
import cv2 as cv
sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import methods

# turn programming distance into visual distance
def direvative_per_board_unit(lefttop, rightbottom, width = 10, height = 14):
    derivative_x = (rightbottom[0] - lefttop[0]) / width / 2
    derivative_y = (rightbottom[1] - lefttop[1]) / height / 2
    return derivative_y, derivative_x

def orient(corners):
    left_bottom_to_top = [t - b for t, b in zip(corners['left_top'],corners['left_bottom'])]
    right_bottom_to_top = [t - b for t, b in zip(corners['right_top'],corners['right_bottom'])]
    top_minus_bottom = [xy / 2 for xy in [left + right for left, right in zip(left_bottom_to_top, right_bottom_to_top)]]
    # Turn Y axis from downward for upward
    top_minus_bottom[1] = -top_minus_bottom[1]
    return top_minus_bottom

def draw_box(where_to_draw, box):
    for point in box:
        methods.draw_text(where_to_draw, str(point), (point[0]-20,point[1]))
    # draw minimal size bounding corners
    methods.draw(where_to_draw, [box],(225,75,225),2)

def target(go_steps, on_board_direction_list, pixel_grab_center_index_one, box_left_top_y, box_left_top_x, direvative_y, direvative_x):
    steps_num = len(go_steps)
    # if use deque data structure
    if steps_num // 4 == 34:
        pixel_grab_centers = []
        for i in range(steps_num):
            x       =   go_steps.pop()
            y       =   go_steps.pop()
            rotation=   go_steps.pop()
            index   =   go_steps.pop()

            angle = on_board_direction_list[rotation]

            # left_top_to_center and position y and x index begin at 1
            y = y*2 + pixel_grab_center_index_one[index][rotation][0] 
            x = x*2 + pixel_grab_center_index_one[index][rotation][1] 
            pixel_y = box_left_top_y + direvative_y * y
            pixel_x = box_left_top_x + direvative_x * x

            # shape index and rotation index begin at 0
            pixel_grab_centers.append(      index      )
            pixel_grab_centers.append(      rotation   )
            pixel_grab_centers.append(round(angle, 2)  )
            pixel_grab_centers.append(      y          )
            pixel_grab_centers.append(      x          )
            pixel_grab_centers.append(round(pixel_y, 2))
            pixel_grab_centers.append(round(pixel_x, 2)) 







def rectangle(img, corners, width, height):
    left_top_right_top = np.array(corners['right_top']) - np.array(corners['left_top'])
    left_top_left_bottom = np.array(corners['left_bottom']) - np.array(corners['left_top'])

    right_bottom_left_bottom = np.array(corners['right_bottom']) - np.array(corners['left_bottom'])
    right_bottom_right_top = np.array(corners['right_bottom']) - np.array(corners['right_top'])
 
    d1 = np.sqrt(np.square(left_top_right_top[0]) + np.square(left_top_right_top[1]))
    d2 = np.sqrt(np.square(left_top_left_bottom[0]) + np.square(left_top_left_bottom[1]))
    d3 = np.sqrt(np.square(right_bottom_left_bottom[0]) + np.square(right_bottom_left_bottom[1]))
    d4 = np.sqrt(np.square(right_bottom_right_top[0]) + np.square(right_bottom_right_top[1]))

    block_size = (d1 + d2 + d3 + d4)/(2*(width + height))
    # assert block_size is not None, print('board corners distance : ', d1, d2, d3, d4)



    line_color = (100,150,200)
    # avoid divided by zero
    if abs(left_top_right_top[1]) > 0.01 and \
        abs(left_top_left_bottom[0]) > 0.01 and \
        abs(right_bottom_left_bottom[1]) > 0.01 and \
        abs(right_bottom_right_top[0]) > 0.01: 

        x_bias = ((left_top_left_bottom[0] + right_bottom_right_top[0])/2)/height
        dy = ((left_top_left_bottom[1] + right_bottom_right_top[1])/2)/height

        dx = ((left_top_right_top[0] + right_bottom_left_bottom[0])/2)/width
        y_bias = ((left_top_right_top[1] + right_bottom_left_bottom[1])/2)/width
        for i in range(height+1):
            cv.line(img, (int(corners['left_top'][0]+i*x_bias), int(corners['left_top'][1]+i*dy)), (int(corners['right_top'][0]+i*x_bias), int(corners['right_top'][1]+i*dy)), line_color, 2)
        for i in range(width+1):
            cv.line(img, (int(corners['left_top'][0]+i*dx), int(corners['left_top'][1]+i*y_bias)), (int(corners['left_bottom'][0]+i*dx), int(corners['left_bottom'][1]+i*y_bias)), line_color, 2)
        # cv.imshow('Drawing Borad', img)
        # cv.waitKey()
    else:
        block_size = int(block_size)
        left_x = int(corners['left_top'][0])
        right_x = int(corners['right_top'][0])
        top_y = int(corners['left_top'][1])
        bottom_y = int(corners['left_bottom'][1])
        for i in range(height+1):
            cv.line(img, (left_x, top_y+i*block_size), (right_x, top_y+i*block_size), line_color, 2)
        for i in range(width+1):
            cv.line(img, (left_x+i*block_size, top_y), (left_x+i*block_size, bottom_y), line_color, 2)
        # cv.imshow('Drawing Borad', img)
        # cv.waitKey()
    return block_size