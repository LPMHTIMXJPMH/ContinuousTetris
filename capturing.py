import cv2 as cv
import time

import methods
import Contours
import config
import init

board_box = init.corners

cap = cv.VideoCapture(0)
while(True):
    t2 = time.time()
    ret, src = cap.read()
    shapes = []
    for idx in range(len(config.hsv)):
        print('===============================================')
        print('\nIndexing shape')
        hsv, res = methods.hsv(src, config.hsv[idx][0], config.hsv[idx][1])
        windows = "index is" + str(idx)
        contours = Contours.findCnt(hsv, config.thresh)
        assert len(contours) > 0; f"Warning! No contour detected at idx = {idx}"
        detected = Contours.contour_property(idx, contours, board_box['left_bottom'])
        if detected is not None: 
            shapes.append(detected)  
            print("\nshape",detected.index ) 
            print("distance:",detected.distance)
            print("angle:",detected.angle)
                
    t3 = time.time()
    print('t3 - t2', t3 - t2)  

    colored = Contours.where_to_draw
    cv.imshow('colored counter', colored)
    cv.waitKey()   

    cv.destroyAllWindows()