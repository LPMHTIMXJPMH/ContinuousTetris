import cv2 as cv

import methods
import Contours
import config
import board
import sampling
import math

cap = cv.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
capture = cap.isOpened()
print('cap.isOpend()', capture)
cv.namedWindow('Window')
while(True):
    ret, frame = cap.read()
    # frame = methods.blur(frame)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    board_hsv, res = methods.hsv(frame)

    board_cnt = Contours.findCnt(board_hsv, config.Thresh)
    num = len(board_cnt)
    assert num == 1,"error on finding board contour in Countours.findCnt()"
    ''''''
    # filling contour/contours(Board contour) black to speed up?
    # cv.drawContours(src, board_cnt, -1, color=(0, 0, 0), thickness=cv.FILLED)
    # findCnt() usually return a 2d list contain multiple contours
    # In this case, only one board contour:[[board_contour]][0]
    board_cnt = board_cnt[0]
    methods.draw(frame, board_cnt, obv = 4)

    minRec, board_box = Contours.minRec(board_cnt)
    print('board_box <-> board corners\n', board_box)
    board.draw_box(frame, board_box)
    corners = methods.rect_corner(board_box)
    print('corners ', corners)

    grid, object_height_width, sampling_centers= sampling.sample(board_box, [14,10], dense = 3)
    # draw samping grid
    draw_grid = grid.reshape(-1,2)
    for _ in draw_grid:
        cv.circle(frame, (int(math.ceil(_[0])), int(math.ceil(_[1]))), 1, (255,255,255),-1)

    cv.imshow('original image', frame)
    if cv.waitKey(1) & 0XFF == ord('q'):
        break
    ''''''
cap.release()
cv.destroyAllWindows()
