import time

if __name__ == '__main__':
    import tetris
else:
    import tetris_array.tetris as tetris
# gogogo
tetris = tetris.Tetris()
begin = time.time()
tetris.autoPlay()
end = time.time()

# report process
print("Mission Accomplished")
print("Remained",tetris.remained)
print(tetris.current)
print('time cost: ',end - begin)
print(tetris.go_steps_array)

# save go steps
where_to_save = 'tetris_array/index_rotation_y_x_deque.pickle'
tetris.save_go_steps(where_to_save)
where_to_save = 'tetris_array/index_rotation_y_x_array.pickle'
tetris.save_go_steps_array(where_to_save)
where_to_save = 'tetris_array/board_self_current.pickle'
tetris.save_current(where_to_save)







'''
########################################
# instore index rotation y x separately#
########################################
steps = dict()
indexes = ""
rotations = ""
ys = ""
xs = ""
for i in range(len(tetris.go_steps)):
    #  9 -> 09
    # 11 -> 11
    indexes = indexes+str(tetris.go_steps[i][0]) if tetris.go_steps[i][0] > 9 else indexes+'0'+str(tetris.go_steps[i][0])
    rotations +='0'+str(tetris.go_steps[i][1])
    ys = ys+str(tetris.go_steps[i][2])if tetris.go_steps[i][2] > 9 else ys+'0'+str(tetris.go_steps[i][2])
    xs +='0'+str(tetris.go_steps[i][3])

steps['indexes'] = indexes
steps['rotations'] = rotations
steps['ys'] = ys
steps['xs'] = xs
print(steps)

# dump string into json file
json_steps = json.dumps(steps)
with open('json/steps_dict.json', 'w') as file:
    json.dump(json_steps, file)
    '''