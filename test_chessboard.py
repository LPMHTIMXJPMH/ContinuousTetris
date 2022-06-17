import cv2 as cv


cap = cv.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
capture = cap.isOpened()
print('cap.isOpend()', capture)
cv.namedWindow('Window')
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
while(True):
    ret, frame = cap.read()
    # frame = methods.blur(frame)
    # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (9, 6))

    if ret == True:
        print('\n')
        corners = cv.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        counter = 0
        for corner in corners:
            
            if not counter % 9:
                print('\n')
            counter += 1
            print('corner', corner)
        cv.drawChessboardCorners(frame, (9,6), corners, ret)
        cv.imshow('original image', frame)
        if cv.waitKey(1) & 0XFF == ord('q'):
            break
    print('\n\n')

cap.release()
cv.destroyAllWindows()
