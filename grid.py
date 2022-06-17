import math


# grab_center_index -> [row_index, col_index]
# array_grab_center_index -> start at left top
array_grab_center_index = [[[1,1]],[[1.5,1.5],[1.5,0.5],[0.5,1.5],[1.5,1.5]],[[1,1.5],[1.5,1]],[[1,1.5],[1.5,1]],[[0.5,2],[2,0.5]],[[1.5,2.5],[2.5,0.5],[0.5,0.5],[0.5,1.5]],[[1.5,0.5],[0.5,0.5],[0.5,2.5],[2.5,1.5]]]
# array_grab_center_index -> start at block center    index start at 0 for computer\
# -0.5 because move from left top to block center has +0.5 by default, so minus 0.5 to let it equal the previous indexes list
pixel_grab_center_index_zero = [[[int(xy - 0.5) if not (xy - 0.5) % 1 else (xy - 0.5) for xy in coordinate] for coordinate in shape] for shape in array_grab_center_index]
# array_grab_center_index -> start at block center    index start at 1 for human
# pixel_grab_center_index_one = [[[int(xy - 0.5 + 1) if not (xy - 0.5 + 1) % 1 else (xy - 0.5 + 1) for xy in coordinate] for coordinate in shape] for shape in array_grab_center_index]
pixel_grab_center_index_one = [[[int(2 * xy) for xy in coordinate] for coordinate in shape] for shape in array_grab_center_index]

# pixel_head_index -> start at block center    index start at 0 for computer
pixel_head_index = [[[0,0.5]],[[0,1],[1,1],[1,1],[1,0]],[[0.5,0],[0,0.5]],[[0.5,0],[0,0.5]],[[0,0],[0,0]],[[1,0],[2,1],[0,2],[0,0]],[[1,2],[0,1],[0,0],[2,0]]]

# current position use pixel_grab_center_index_zero to calculate location of the object
# current position use pixel_head_index to calculate direction of the object

# target position use pixel_grab_center_index_one to calculate location of the object
# target position use board vector to calculate direction of the object


def array_to_pixel(idx, centers, index_list, rotation):
    pixel_index = index_list[idx][rotation]
    assert len(pixel_index) == 2, "Unexpected pixel_index length."
    if isinstance(pixel_index[0], int) and isinstance(pixel_index[1], int):
        pixel_center = centers[pixel_index[0]][pixel_index[1]]
        return pixel_index, [round(pixel, 2) for pixel in pixel_center]
    else:
        # two xy coordinates -> 2*2 2d list
        pixel_center_index = [[None] * 2 for _ in range(2)]
        for index, xy in enumerate(pixel_index):
            if isinstance(xy, int):
                for i in range(len(pixel_center_index)):
                    pixel_center_index[i][index] = pixel_index[index]
            else:
                pixel_center_index[0][index] = math.floor(pixel_index[index])
                pixel_center_index[1][index] = math.ceil(pixel_index[index])
        pixel_center_row = 0
        pixel_center_col = 0
        for neighbor in pixel_center_index:
            pixel_center_row += centers[neighbor[0]][neighbor[1]][0]
            pixel_center_col += centers[neighbor[0]][neighbor[1]][1]
        pixel_center = [round(pixel_center_row/2, 2), round(pixel_center_col/2,)]
        return pixel_index, pixel_center
        
        
def shape_property(idx, rotation, centers):
    grab_center_pixel = None
    head_pixel = None

    grab_center_index, grab_center_pixel = array_to_pixel(idx, centers, pixel_grab_center_index_zero, rotation)
    head_pixel_index, head_pixel = array_to_pixel(idx, centers, pixel_head_index, rotation)
    print(f'vec(head_pixel, grab_center_pixel): ({head_pixel}, {grab_center_pixel})')

    return grab_center_pixel, head_pixel