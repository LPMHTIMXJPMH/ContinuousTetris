import numpy as np

hsv = np.zeros((7,2,3),dtype = np.uint8)

hsv[0] = np.array([[0,110,153],[19,240,255]])   # 90 block O

hsv[1] = np.array([[0,104,41],[8,167,252]])     # 360 block T

hsv[2] = np.array([[77,117,107],[93,211,194]])   # 180 block S
hsv[3] = np.array([[93,109,114],[109,184,255]])  # 180 block Z

hsv[4] = np.array([[169,159,0],[176,255,225]])  # 180 block I

hsv[5] = np.array([[23,32,165],[60,73,255]])     # 360 block L
hsv[6] = np.array([[112,33,109],[137,180,213]])  # 360 block J



thresh = (4000, 8000)
Thresh = (200000, 400000)

kx = 0.48309179
bx = -179.36643

ky = -0.492
by = 484.60632689