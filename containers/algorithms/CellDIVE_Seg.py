import numpy as np
import os
import cv2
import json
import pickle
from learning_helpers import Traditional_ML
import subprocess



class CellDIVESeg:
    def __init__(self):
        self.tissueSegModel = None
        self.DLFeats = False
        self.learningMethod = Traditional_ML()


    def loadTissueModel(self, modelfName):
        filename, file_extension = os.path.splitext(modelfName)
        jFname = filename + '.json'

        if file_extension == '.sav':
            with open(jFname) as jFile:
                jData = json.load(jFile)
                self.learningMethod.classifierType = jData['classifier_type']
                self.DLFeats = jData['DLFeatures']
                self.learningMethod.model = pickle.load(open(modelfName, 'rb'))
        else:
            self.learningMethod.classifierType = 3
            self.DLFeats = 0
            self.learningMethod.LoadModelCNNModel(modelfName)


    # Initial version using wavelet-based segmentation
    def nucSegmentation(self, img, tissueMask, patchSize):

        s = img.shape
        if patchSize > s[0] or patchSize > s[1]:
            print('Patch size is too large')
            return None

        outIm = img * 0
        outIm = outIm.astype('uint32')
        # exec for nuc seg
        exeName = 'nucseg/itkWaveletNucleiSegmentationTest.exe '
        exeArgs = 'tempN.tif tempNS.tif '+ str(3) + ' ' + str(5) + ' ' + str(2) + ' ' + str(1)
        cmmd = exeName + exeArgs

        currMaxLab = 0;
        print(s[0],s[1])


        for i in range(0,s[0],patchSize):
            i2 = min(i+patchSize,s[0])
            for j in range(0, s[1], patchSize):
                j2 = min(j + patchSize, s[1])

                print(i,i2,j,j2)

                tM = tissueMask[i:i2,j:j2]
                if np.max(tM) == 0:
                    # no tissue
                    continue
                dP = img[i:i2,j:j2]
                #dP[tM == 0] = 0

                # write to a temp image and run nuc seg exec
                cv2.imwrite('tempN.tif',dP)
                subprocess.check_call(cmmd)

                # read nuc seg results
                dPS = cv2.imread('tempNS.tif',-1)
                dPS = dPS.astype('uint32')

                # add prev max lab and insert to the final image
                dPS[dPS>0] = dPS[dPS>0] + currMaxLab
                currMaxLab = np.max(dPS)
                outIm[i:i2, j:j2] = dPS

        return outIm

    # ML/DL-based segmentation
    def mlNucSeg(self, img, patchSize, tissueMask, modelfName=None):

        # load the model if it is not already loaded
        if modelfName is not None:
            self.loadTissueModel(modelfName)

        s = img.shape
        if patchSize > s[0] or patchSize > s[1]:
            print('Patch size is too large')
            return None


        outIm = img * 0
        outIm = outIm.astype('uint8')

        currMaxLab = 0;
        print(s[0], s[1])

        kernel = np.ones((5, 5), np.uint8)

        for i in range(0, s[0], patchSize):
            i2 = min(i + patchSize, s[0])
            for j in range(0, s[1], patchSize):
                j2 = min(j + patchSize, s[1])

                print(i, i2, j, j2)

                tM = tissueMask[i:i2, j:j2]
                if np.max(tM) == 0:
                    # no tissue
                    continue

                dP = img[i:i2, j:j2]

                # Call the inference/prediction function, which depends on the type of the model
                if self.learningMethod.classifierType == 3:  # TF CNN
                    dPS = self.learningMethod.predict_CNN_pixel_level(dP)
                else:
                    dPS = self.learningMethod.predict_pixel_level([dP/255], self.DLFeats, None)

                dPS[dPS == 3] = 255
                dPS[dPS < 255] = 0
                dPS = cv2.morphologyEx(dPS, cv2.MORPH_OPEN, kernel)
                dPS = cv2.morphologyEx(dPS, cv2.MORPH_CLOSE, kernel)

                outIm[i:i2, j:j2] = dPS

        _, outIm = cv2.connectedComponents(outIm)

        return outIm


    # Post-processing maybe needed to separate nuclei that were not separated by the DL method
    def SegPostProcess(self, mask, distance=None, SZ=21):
        from scipy import ndimage as ndi
        from skimage.feature import peak_local_max
        from skimage.segmentation import watershed

        if distance is None:
            distance = ndi.distance_transform_edt(mask)

        local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((SZ, SZ)), labels=mask)
        markers = ndi.label(local_maxi)[0]
        labels = watershed(-distance, markers, mask=mask, watershed_line=False)

        return labels


    def ExtractTissue(self, img, modelfName=None):

        # load the model if it is not already loaded
        if modelfName is not None:
            self.loadTissueModel(modelfName)


        if img.max()>255:
            img = img/255

        # Call the inference/prediction function, which depends on the type of the model
        if self.learningMethod.classifierType == 3:  # TF CNN
            mask_predict = self.learningMethod.predict_CNN_pixel_level([img])
        else:
            mask_predict = self.learningMethod.predict_pixel_level([img], self.DLFeats,None)

        mask_predict[mask_predict==1] = 255
        mask_predict[mask_predict<255] = 0

        # We need to remove any parts of adjacent tissues by applying the following steps
        # 1- Perform connected componenets analysis

        # Perform the operation
        _, labels = cv2.connectedComponents(mask_predict.astype('uint8'))


        if np.max(labels) > 1:
            #exclude labels touching the edge
            mx = len(np.where(labels == 1)[0])
            indMax = 1
            for j in range(2,np.max(labels)+1):
                if len(np.where(labels == j)[0]) > mx:
                    mx = len(np.where(labels == j)[0])
                    indMax = j*1

            I1 = np.concatenate([labels[0,:],labels[-1,:],labels[:,-1], labels[:,0]])
            I1 = np.unique(I1)
            if len(I1)>0:
                for i in range(0, len(I1)):
                    if(I1[i] != indMax):
                        mask_predict[labels == I1[i]] = 0

        return mask_predict




