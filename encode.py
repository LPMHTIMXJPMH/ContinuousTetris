import numpy as np
import math

# rotate on anti-clock direction 
def rotate(input_piece, n_times = 1):
    #for y coordinate,downforward is positive
    # (rows, cols) = input_piece.shape
    rows = len(input_piece)
    cols = len(input_piece[0])
    
    if n_times == 0:
        return input_piece
    if n_times == 1:
        rotated = np.zeros((cols, rows), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[cs][rows-rs-1] = input_piece[rs][cs]
    if n_times == 2:
        rotated = np.zeros((rows, cols), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[rows-rs-1][cols-cs-1] = input_piece[rs][cs]
    if n_times == 3:
        rotated = np.zeros((cols, rows), dtype = np.uint8)
        for rs in range(rows):
            for cs in range(cols):
                rotated[cols - cs -1][rs] = input_piece[rs][cs]

    return rotated

pieces = [[[1, 1],[1, 1]],[[0, 2, 0],[2, 2, 2]],[[0, 3, 3],[3, 3, 0]],[[4, 4, 0],[0, 4, 4]],[[5, 5, 5, 5]],[[0, 0, 6],[6, 6, 6]],[[7, 0, 0],[7, 7, 7]]]

rotation_nums = [1, 4, 2, 2, 2, 4, 4]

matches = dict()
for index, rotation_num in enumerate(rotation_nums):
    for rot in range(rotation_num):
        matches[str(index) + str(rot)] = np.array(rotate(pieces[index], n_times = rot), dtype = bool)

def match(idx, sample_result, threshold = 5):
    index = str(idx)
    sample_result = [[z if z > threshold else 0 for z in row] for row in sample_result]
    sample_result = np.array(sample_result, dtype = bool)

    for rotation in range(rotation_nums[idx]):
        rotation_str = str(rotation)
        if np.array_equal(matches[index + rotation_str], sample_result):
            print(f'Successfully matched the shape! The shape is {pieces[idx]} rotate for {rotation} time/times')
            return rotation

    # dynamic threshold
    sample_result_one_dimension = sample_result.flatten()
    sample_result_one_dimension = sorted(sample_result_one_dimension, reverse = True)
    fourth_threshold = sample_result_one_dimension[4]
    sample_result = [[z if z > fourth_threshold else 0 for z in row] for row in sample_result]
    sample_result = np.array(sample_result, dtype = bool)

    for rotation in range(rotation_nums[idx]):
        rotation_str = str(rotation)
        if np.array_equal(matches[index + rotation_str], sample_result):
            return rotation
    else:
        print(f"Error!, Boolean Sampling Result Failed To Match Any Shape!:\n{sample_result} at index:\n{idx}")
        print('Considering envroment background noise Or \nAdjusting sampling threshold to the shapes contour! ')
        return None