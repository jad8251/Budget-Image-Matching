# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:20:03 2018

@author: Jason Durek
"""

import random
import time

import numpy as np
import cv2
import argparse

def main():
#    start = time.time()
    img1 = cv2.imread('Places365_val_00000061.jpg')
    img2 = cv2.imread('Places365_Lval_00000061.jpg')
    heightO, widthO, _  = img1.shape
    img2 = cv2.resize(img2, (widthO,heightO), interpolation = cv2.INTER_AREA)
    
    start = time.time()
    #Start SIFT detector
    orb = cv2.ORB_create()
    
    #Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    
#    Create BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    #Match Descriptors
    matches = bf.match(des1,des2)
    totalDist = 0
    numMatches = len(matches)
    for match in matches:
        totalDist += match.distance
    print("Number of matches is {}".format(numMatches))
    print(totalDist)
    
    #Attempt to determine if the images are matches, or if we've simply found 
    #a subimage within the larger one.
    
    ctr = 0
    #Compute keypoints between the two
    for i in range(heightO):
        for j in range(widthO):
            #Make a comparision, do nothing with it
            if(img1[i][j][1] == img2[i][j][1]):
                #Can't print, just increment our counter
                ctr += 1


    end = time.time()
    print(end-start)
    return
    
main()
