import cv2 as cv
import numpy as np
import math
import sys
import time

sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import methods
import sampling
import encode
import grid
'''
def centroid(box):
    X = 0
    Y = 0
    for (x, y) in box:
        X += x
        Y += y
    return [X//4, Y//4]
'''
def minRec(contour):
    contours_poly = cv.approxPolyDP(contour, 3, True)
    minRec = cv.minAreaRect(contours_poly)
    box = np.int0(cv.boxPoints(minRec))
    #box = cv.boxPoints(minRec)
    return minRec, box


def findCnt(src, threshold):
    contours, _ = cv.findContours(src, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    selected_cnt = []
    for cnt in contours:
        area = int(cv.contourArea(cnt))
        if area > threshold[0] and area < threshold[1]:
            selected_cnt.append(cnt)

    return selected_cnt


def sample_inside_contour(grids, height_width, contour):
    result = np.zeros((height_width[0], height_width[1]), dtype = np.uint8)
    for index_row_grid, row in enumerate(grids):
        if index_row_grid % 4:
            for index_col_grid, col in enumerate(row):
                if index_col_grid % 4:
                    sample_point = grids[index_row_grid, index_col_grid]
                    if cv.pointPolygonTest(contour, sample_point, True) > 0:
                        result[index_row_grid // 4][index_col_grid // 4] += 1
    return result

def contour_property(where_to_draw, idx, contours):
    cnt_prop = []
    for contour in contours:
        minrec, box_points = minRec(contour)
        #centroids.append(centroid(box_points))

        draw_minRec = [box_points]
        methods.draw(where_to_draw, draw_minRec,(125,175,25),2)

        (___, __), (width, height), angle = minrec
        ratio = width/height
        if ratio < 1:
            ratio = 1 / ratio
        
        edge = [len(encode.pieces[idx]), len(encode.pieces[idx][0])]
        grids, object_height_width, sampling_centers= sampling.sample(box_points, edge)
        # draw samping grids
        draw_grid = grids.reshape(-1,2)
        for _ in draw_grid:
            cv.circle(where_to_draw, (int(math.ceil(_[0])), int(math.ceil(_[1]))), 1, (255,255,255),-1)
        

        sampling_result = sample_inside_contour(grids, object_height_width, contour)
        print('\n< sampling result >')
        print(sampling_result)

        # index = sorted(np.argpartition(result, -4)[-4:])
        # index = np.insert(index, 0, height_width[0])
        # numpy to python list
        # index = [x for x in index]

        rotation = encode.match(idx, sampling_result)
        center, head = grid.shape_property(idx, rotation, sampling_centers)
        cv.circle(where_to_draw, (int(center[0]), int(center[1])), 4, (125, 75, 125), -1)
        cv.circle(where_to_draw, (int(head[0]), int(head[1])), 4, (75, 225, 125), -1)
        vector = [h - c for h, c in zip(head, center)]
        angle_max180 = methods.vector_angle(vector)
        if vector:
            if vector[0]:
                if vector[0] < 0:
                    angle_max180 = 360 - angle_max180
        cnt_prop.append([idx, angle_max180, center])

    if len(cnt_prop):
        return cnt_prop
    else:
        print("Error at fn contour property :: fn encode.match(idx, sampling_result, sampling_centers)")
        return [[None]]