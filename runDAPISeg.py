from CellDIVE_Seg import CellDIVESeg
from CellDIVE_IO import CellDIVE_IO
import cv2
import time
import sys
import numpy as np


imName = sys.argv[1]
outputName = sys.argv[2]
paramPatch = int(sys.argv[3])

img = cv2.imread(imName, -1)
height, width = img.shape
tsSeg = 255 * np.ones((height, width))

CDS = CellDIVESeg()
CDIO_ts = CellDIVE_IO()

dpIM = CDIO_ts.ReadPTiffLevel(imName, [0])

t1 = time.time()
print('Start prediction')
DS = CDS.mlNucSeg(dpIM[0], paramPatch, tsSeg, modelfName='./models/unet_models/nuc_seg_unet_model_48_sp.h5')
t2 = time.time()
print('Prediction time:', t2-t1)

print(DS)

cv2.imwrite(outputName, DS.astype('uint8'))
