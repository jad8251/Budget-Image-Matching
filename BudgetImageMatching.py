# -*- coding: utf-8 -*-
"""
Initial draft of budget-image matching program

Created on Sun Mar 18 13:57:17 2018

@author: Jason Durek
"""
import random

import numpy as np
import cv2
import argparse

def histMatch(imgOne, imgTwo, mode):
    #Use color histograms (Homework 1) to determine matchup
    #Determine the difference by directly comparing each bin
    return

def edgeMatch(imgOne, imgTwo, mode):
    #Feed the images through Canny Edge Detector provided by cv2
    #Sizeorder is so we can determine which one was upscaled for some comparision logic
    #TODO; Think about how to cope with possible edge shifts based on the rescaling
    
    #Create Canny Edge images
    cannyOne = cv2.Canny(imgOne, 100, 200)
    cannyTwo = cv2.Canny(imgTwo, 100, 200)
    
    cv2.imshow("Canny ImgOne", cannyOne)
    cv2.imshow("Canny ImgTwo", cannyTwo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    height, width, _ = imgOne.shape
    
    if mode == "rand":
        percentVal = .2
        print("Generating random points for Edge Detector...")
        totalPoints = height * width * percentVal #Need to research how many should be sampled
        rPts = randPoints(height,width, totalPoints)
        totalDiff = 0
        for point in rPts:
            pX, pY = point
            if(cannyOne[pX,pY] != cannyTwo[pX,pY]):
                totalDiff += 1
        print("Number of points sampled: {}, which is {}%".format(totalPoints,
              percentVal*100))
        print("Edge Random Sample- Difference count:{}".format(totalDiff))
        print("Edge Random Sample- Percentage Diff:{}".format(totalDiff/totalPoints))
    else:
        print("Passing over entire image for Edge Comparision...")
        totalDiff = 0
        for i in range(height):
            for j in range(width):
                if(cannyOne[i,j] != cannyTwo[i,j]):
                    totalDiff += 1
        print("Edges Different points: {}".format(totalDiff))
        print("Total Difference %wise: {}".format(totalDiff/(height*width*1.0)))
    return

def morphMatch(imgOne, imgTwo, mode):
    #Pass the image into cv2 morphology (Similar to HW3 I suppose)
    return

def sumSquaresMatch(imgOne, imgTwo, mode):
    #Process the image and determine how much difference exists between the two in terms of raw
    #pixel information. 
    if mode == "rand":
        print("Generating random points and comparing...")
    else:
        print("Passing over entire image...")
        height, width, _ = imgOne.shape
        totalDiff = 0
        for i in range(height):
            for j in range(width):
                #Compare the difference between the images at coordinates
                currDiff = 0.0
                rDiff = abs(int(imgOne[i,j][0]) - int(imgTwo[i,j][0]))
                gDiff = abs(int(imgOne[i,j][1]) - int(imgTwo[i,j][1]))
                bDiff = abs(int(imgOne[i,j][2]) - int(imgTwo[i,j][2]))
                currDiff += rDiff + bDiff + gDiff
                #Not sure how to really judge "different colors"
                #if currDiff > 10:
                totalDiff += currDiff

        print("Total Difference: {}".format(totalDiff/255/3))
    return

def comboMatch(imgOne, imgTwo, mode):
    return


#Helper function- takes in dimensions of image and a count for # of points
#Returns list of tuples (x,y), each which are likely unique.
#Idea- duplicate point check in set(), which is O(1) lookup time
def randPoints(height, width, count):
    coords = set()
    randPoints = []
    i = 0
    while i < count:
        x = random.randrange(height)
        y = random.randrange(width)
        if (x,y) in coords: continue
        randPoints.append((x,y))
        coords.add((x,y))
        i += 1
    return randPoints


#Central function, designed to handle bulk of logic
#This includes resizing smaller image to match larger
def main(imgI, imgII, method, sens):
    #Check to make sure we can access both images
    imgOne = cv2.imread(imgI)
    imgTwo = cv2.imread(imgII)
    if imgOne is None:
        print("Failed to read {}.".format(imgI))
        if imgTwo is None:
            print("Failed to read {}.".format(imgII))
        return
    elif imgTwo is None:
        print("Failed to read {}.".format(imgII))
        return
    
    #Images were correctly read in; Resize one of the images so both are the same size
    #Need to determine which way to scale (Discuss as group? Mabye ask Professor for advice)
    
    #temporary code to resize the 2nd image to the dimensions of the 1st image, regardless of
    #whichever was larger to begin with.
    heightO, widthO, _  = imgOne.shape
    #TODO: Consider how cv2.resize interpolation argument should be utilized
    #Using INTER_AREA for the time being, as the others had some noticable jags on edges
    #From simply eyeballing the two images side by side
    rImgTwo = cv2.resize(imgTwo, (heightO,widthO), interpolation = cv2.INTER_AREA)
    hT, wT, _ = imgTwo.shape
    hTR, wTR, _ = rImgTwo.shape
    print("Dimensions of images: \n"
          "\tImage One:\t\t {} by {}\n"
          "\tImage Two:\t\t {} by {}\n"
          "\tResized Image Two:\t {} by {}\n".format(heightO, widthO, hT, wT, hTR,wTR)
          )
    
    #Feed in the images into the code we have handy
    cv2.imshow("ImgOne", imgOne)
    cv2.imshow("Scaled ImgTwo", rImgTwo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    sumSquaresMatch(imgOne, rImgTwo, "Normal")
    edgeMatch(imgOne, rImgTwo, "rand")
    
    return

#Parsing function to sift through args provided and ensue it's valid
def argParser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('fileOne',
                help = ('First file to use for comparision'))
    parser.add_argument('fileTwo',
                help = ('Second file to use for comparision'))
    parser.add_argument('method',
                help = ('Method to use in order to decide if files are a match.\n'
                        '\tAvailable methods are as follows\n'
                                
                        ))
    parser.add_argument('-sens','--sensitivity', required = False,
                help = ('Optional way to change how strict the matching is.'
                        'By default, it needs 90%% confidence to match.'))
    
    args = parser.parse_args()
    if args.sensitivity:
        main(args.fileOne, args.fileTwo, args.method, args.sensitivity)
    else:
        main(args.fileOne, args.fileTwo, args.method, 90)
    return

#TODO: Revamp argv checks to be easier to extend, probalby argparse
if __name__ == '__main__':
    argParser()
#    
