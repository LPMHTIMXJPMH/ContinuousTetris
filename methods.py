import cv2 as cv
import numpy as np
import math
import sys

sys.path.insert(1, '/home/xjyhc/Tetris (2)/tetris_pixel')
import config

# v0 vector = [0:x, 1:y] by default
def vector_angle(v1, v0 = [0, 1]):
    if v1 == [None, None] or v0 == [None, None] or v1 == None or v0 == None:
        return None
    else:
        v1 = v1 / np.linalg.norm(v1)
        v0 = v0 / np.linalg.norm(v0)

    radian = np.arccos(np.clip(np.dot(v1, v0), -1.0, 1.0))
    angle = (radian / 3.1415926 * 180)
    return  angle
    
def random_color():
    return np.random.randint(low = 0, high = 255, size = 3).tolist()


def rect_corner(box):
    assert len(box), "box is empty"
    corners = dict()

    x = np.array(sorted(box, key = lambda x:x[0])).tolist()
    y = np.array(sorted(box, key = lambda x:x[1])).tolist()
    for i in x[:2]:
        if i in y[:2]:
            corners['left_top'] = i
    for i in x[:2]:
        if i in y[2:]:
            corners['left_bottom'] = i
    for i in x[2:]:
        if i in y[:2]:
            corners['right_top'] = i
    for i in x[2:]:
        if i in y[2:]:
            corners['right_bottom'] = i
    if "left_top" not in corners and "right_bottom" not in corners:
        assert x[0] in y[2:] and x[1] in y[2:], "Error! Unexpected!"
        corners['left_top'] = x[0]
        corners['right_bottom'] = x[-1]  
        corners['left_bottom'] = x[1]   
        corners['right_top'] = y[0]
    if "left_bottom" not in corners and "right_top" not in corners:
        assert x[0] in y[:2] and x[1] in y[:2], "Error! Unexpected!"
        corners['left_bottom'] = x[0]
        corners['right_top'] = x[-1]        
        corners['left_top'] = x[1]
        corners['right_bottom'] = y[-1]        
    return corners

'''
def ratio(corners):
    lt = corners['left_top']
    lb = corners['left_bottom']
    rt = corners['right_top']
    rb = corners['right_bottom']
'''
    

def hsv(src,lower = np.array([59,179,51]),higher = np.array([88,255,190])):
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, higher)
    res = cv.bitwise_and(src,src, mask= mask)
    return mask, res


def arithmetic(src,src2,option):
    if option == 'bitwise_not':
        arithmetic = cv.bitwise_not(src)
    elif option == 'bitwise_or':
        arithmetic = cv.bitwise_or(src, src2, mask = None)
    elif option == 'bitwise_and':
        arithmetic = cv.bitwise_and(src,src,mask = src2)
    elif option == 'bitwise_xor':
        arithmetic = cv.bitwise_xor(src,src2)
    elif option == 'add_weighted':
        pass
    elif option == 'absdiff':
        pass
    else:
        pass
    return arithmetic


def morphological(src,option,kernel = np.ones((3,3),np.uint8)):
    if option == 'erosion':
        morphological = cv.erode(src,kernel,iterations = 1)
    if option == 'dilation':
        morphological = cv.dilate(src,kernel,iterations = 1)
    if option == 'opening':
        morphological = cv.morphologyEx(src,cv.MORPH_OPEN,kernel)
    if option == 'closing':
        morphological = cv.morphologyEx(src,cv.MORPH_CLOSE,kernel)
    if option == 'top_hat':#It is the difference between dilation and erosion of an image.
        morphological = cv.morphologyEx(src,cv.MORPH_GRADIENT,kernel)
    if option == 'black_hat':
        morphological = cv.morphologyEx(src,cv.MORPH_TOPHAT,kernel)

    return morphological


def blur(src, gaussian_kernel=3, kernel = 2):
    blur = cv.GaussianBlur(src,(gaussian_kernel,gaussian_kernel),0)
    blur = cv.blur(blur,(kernel,kernel))
    blur = cv.bilateralFilter(blur,9,75,75)
    return blur


def threshold(src):
    th2 = cv.adaptiveThreshold(src,255,\
        cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)

    th3 = cv.adaptiveThreshold(src,255,\
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    return th2,th3


def canny(src, threshold=30):
    canny_output = cv.Canny(src, threshold, threshold * 2)
    return canny_output


def draw(src,cnt,color = (125,125,0),obv = 1):
    # print('len(cnt)   ', len(cnt))
    cv.drawContours(src,cnt,-1,color,obv)


def draw_text(src,text,org,fontScale=0.4,color=(25,25,255),thickness=1):
    return cv.putText(src, text, [int(xy) for xy in org], cv.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness, cv.LINE_AA)


def moment(contour):
    contour_moment = cv.moments(contour)
    if contour_moment['m10'] and contour_moment['m00'] and contour_moment['m01'] and contour_moment['m00']:
        x = contour_moment['m10']/contour_moment['m00']
        y =  contour_moment['m01']/contour_moment['m00']
        return (x,y)
    else:
        return (None,None)


# rotate on anti-clock direction 
def rotate(input_piece,n_times = 1):
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

    
def rotate_vec(vec, rotation):
    x = vec[0]
    y = vec[1]
    x = math.cos(rotation) * x - math.sin(rotation) * y
    y = math.sin(rotation) * x + math.cos(rotation) * y
    return [x, y]


def linear(**kwargs):
    for key, value in kwargs.items():
        if key == 'x':
            x = config.kx * value + config.bx
        if key == 'y':
            y = config.ky * value + config.by
    return [x, y]