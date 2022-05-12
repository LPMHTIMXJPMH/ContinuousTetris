import tetris
import json
import os
import numpy as np
import shutil

empty = tetris.Tetris()
state = empty.current
next_steps = empty.next_step_verbose(state)
print("next_steps")
print(next_steps)

root = './first'
if os.path.exists(root):
    shutil.rmtree(root)
os.mkdir(root)
for key, value in next_steps.items():
    file = str(key)
    dir = root
    path = dir + '/' + file
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    step_json = json.dumps(np.array(key).tolist())
    state_json = json.dumps(value.tolist())
    print('\n', step_json, '\n')
    json_file = path + '/' + str(key) + '.json'
    with open(json_file, 'w') as f:
        print(f"The json file named {file} is created!")
        json.dump(step_json + state_json, f)