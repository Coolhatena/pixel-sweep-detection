import sys
import cv2 as cv
import numpy as np
import time

global LOW, UPP

LOW = np.array([0,0,0])
UPP = np.array([180,255,255])

if True:
    cv.namedWindow('FILTER MARKERS')

    def min_hue(MINHUE):
        LOW[0] = MINHUE
        msk = cv.inRange(hsv, LOW, UPP)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)

    def min_sat(MINSAT):
        LOW[1] = MINSAT
        msk = cv.inRange(hsv, LOW, UPP)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)

    def min_bri(MINBRI):
        LOW[2] = MINBRI
        msk = cv.inRange(hsv, LOW, UPP)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)

    def max_hue(MAXHUE):
        UPP[0] = MAXHUE
        msk = cv.inRange(hsv, LOW, UPP)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)

    def max_sat(MAXSAT):
        UPP[1] = MAXSAT
        msk = cv.inRange(hsv, LOW, UPP)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)

    def max_bri(MAXBRI):
        UPP[2] = MAXBRI
        msk = cv.inRange(hsv, LOW, UPP)
        msk_NOT = cv.bitwise_not(msk)
        filtered = cv.bitwise_and(src,src, mask= msk)
        cv.imshow('FILTER',filtered)


cv.createTrackbar('MIN_HUE', 'FILTER MARKERS' , 0, 180, min_hue)
cv.createTrackbar('MIN_SAT', 'FILTER MARKERS' , 0, 255, min_sat)
cv.createTrackbar('MIN_BRI', 'FILTER MARKERS' , 0, 255, min_bri)

cv.createTrackbar('MAX_HUE', 'FILTER MARKERS' , 180, 180, max_hue)
cv.createTrackbar('MAX_SAT', 'FILTER MARKERS' , 255, 255, max_sat)
cv.createTrackbar('MAX_BRI', 'FILTER MARKERS' , 255, 255, max_bri)

camera_id = 0
cap = cv.VideoCapture(0)

while not cap.isOpened():
    time.sleep(.5)
    cap = cv.VideoCapture(0)

while True:
    src = cv.imread("./img_8.jpg")
    #cv.imshow('src1',src)
    
    cv.imshow('FILTER',src)

    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)

    msk = cv.inRange(hsv, LOW, UPP)
    filtered = cv.bitwise_and(src,src, mask= msk)
    cv.imshow('FILTER',filtered)

##    cv.imshow('SOURCE IMAGE',src)

    key = cv.waitKey(1)
    if key == (ord('b')):
        print('Exit...')
        break

##cv.waitKey(0)
cv.destroyAllWindows()



cv.waitKey(0)
cv.destroyAllWindows()
