import tetris
import numpy as np
import time
import json

t1 = time.time()
tetris = tetris.Tetris()
t2 = time.time()
tetris.autoPlay()
t3 = time.time()
print("Mission Accomplished")
print("Remained",tetris.remained)
print(tetris.current)
print("")
t4 = time.time()
print('t - t: ',t2 - t1)
print('t - t: ',t3 - t2)
print('t - t: ',t4 - t3)
print("tetris.go")
tetris.go = np.reshape(np.array(tetris.go), (-1,4))
print(tetris.go)
print(tetris.current)
json_go = json.dumps(tetris.go.tolist())
with open('python_json.json', 'w') as f:
    json.dump(json_go, f)