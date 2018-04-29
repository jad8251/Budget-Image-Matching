# -*- coding: utf-8 -*-
"""
Initial draft of budget-image matching program

Created on Sun Mar 18 13:57:17 2018

@author: Jason Durek
@author: Connor Coval
@author: Chris Grate
"""
import random
import time

import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt

"""NOTES: edgeMatch and morphMatch do not account for color; They generate pure
black/white images, absolute binary with nothing in between. This means
images with only the color scales shifted around equally could still report 
the same edges.
"""

def histMatch(imgOne, imgTwo, mode):
    #Use color histograms (Homework 1) to determine matchup
    #Determine the difference by directly comparing each bin
    if mode == "rand":
        return 
        
    else:
        
        #Hold current time (when function is run - hence the start time)
        startTime = time.time()
        #Use color histograms (Homework 1) to determine matchup
        color = ('b','g','r')
        
        #Create color histogram for each image, from iterating through each pixel
        #value - produces a 256x1 array of pixel values.


        #Commented out, used for testing purposes of getting a histogram
        #equalized version of both images - would just have to change
        #name of output file, and the image you're equalizing
        #img_hsv = cv2.cvtColor(imgTwo,cv2.COLOR_BGR2HSV)
        #img_hsv[:,:,2] = cv2.equalizeHist(img_hsv[:,:,2])
        #img_eq = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        #newfile = '.test2'+ '_hsveq.jpg'
        #cv2.imwrite(newfile,img_eq)
  
        for x,y in enumerate (color):
            histOne = cv2.calcHist([imgOne],[x],None,[256],[0,256])
            histTwo = cv2.calcHist([imgTwo],[x],None,[256],[0,256])

            #Create and show the histogram for Image 1
            plt.figure(1)
            plt.subplot(211)
            plt.plot(histOne,color = y)
            plt.xlim([0,256])

            #Create and show the histogram for image 2
            plt.figure(2)
            plt.subplot(212)
            plt.plot(histTwo,color = y)
            plt.xlim([0,256])
        plt.show()

        #256 is the size of the histogram lists.

        #The number of differences found between the histogram lists
        #And their intesity counts
        diffCount = 0
        for x in range(0,256):
            if(histOne[x] != histTwo[x]):
                diffCount+=1
            else:
                continue

        #Hold the current time (after the function has performed its actions)
        endTime = time.time()

    #Calculate the total time taken for function to perform its tasks
    elapsedTime = endTime - startTime
        
    #Hold the diffrence percentage, essentially the percentage of pixel values
    #between the two images that were different between the histograms.
    diffPercent = ((diffCount/256)*100)
    print("Histogram Matching - Difference count: ",+diffCount)
    print("Histogram Matching - Percentage Difference: ",+ diffPercent)

def edgeMatch(imgOne, imgTwo, mode):
    #Feed the images through Canny Edge Detector provided by cv2
    #Sizeorder is so we can determine which one was upscaled for some comparision logic
    #TODO; Think about how to cope with possible edge shifts based on the rescaling
    
    #Create Canny Edge images
    cannyOne = cv2.Canny(imgOne, 100, 200)
    cannyTwo = cv2.Canny(imgTwo, 100, 200)
    
#    cv2.imshow("Canny ImgOne", cannyOne)
#    cv2.imshow("Canny ImgTwo", cannyTwo)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    height, width, _ = imgOne.shape
    print("Height:{} \t Width:{}".format(height,width))
    
    if mode == "rand":
        percentVal = .2
        print("Generating random points for Edge Detector...")
        totalPoints = height * width * percentVal #Need to research how many should be sampled
        rPts = randPoints(height,width, totalPoints)
        totalDiff = 0
        for point in rPts:
            pX, pY = point
            #print("Img1:{} \t Img2:{}".format(cannyOne[pX,pY], cannyTwo[pX,pY]))
            if(cannyOne[pX,pY] != cannyTwo[pX,pY]):
                
                totalDiff += 1
        print("Number of points sampled: {}, which is {}% of points".format(totalPoints,
              percentVal*100))
        print("Edge Random Sample- Difference count:{}".format(totalDiff))
        print("Edge Random Sample- Percentage Diff:{}".format(totalDiff/totalPoints))
        return totalDiff
    
    #Experimental mode- We pick random points, create a new image from those
    #And feed it to Canny Edge
    elif mode == "exp":
        print("Running experimental Edge comparision: Random sample before Canny")
        percentVal = .002 #2 in a thousand points randomly chosen
        #The percentage for this mode is far lower, due to it pulling points around it
        
        numPoints = (int)(height * width * percentVal)
        #Creating temporary sub-images
        blankImg1 = np.zeros((5,5,3), np.uint8)
        blankImg2 = np.zeros((5,5,3), np.uint8)
        rPts = randPoints(height, width, numPoints)
        i = 0
        totalDiff = 0
        totalPoints = 0
        modTotal = 0
        for point in rPts:
            pX, pY = point
            for k in range(5):
                for l in range(5):
                    if(pX + k - 2 < 0):
                        blankImg1[k,l] = 0
                        blankImg1[k,l] = 0
                    elif(pX + k - 2 >= height):
                        blankImg1[k,l] = 0
                        blankImg2[k,l] = 0
                    elif(pY + l - 2 < 0):
                        blankImg1[k,l] = 0
                        blankImg2[k,l] = 0
                    elif(pY + l - 2 >= width):
                        blankImg1[k,l] = 0
                        blankImg2[k,l] = 0
                    else:
                        blankImg1[k,l] = imgOne[(pX + k - 2),(pY + l - 2)]
                        blankImg2[k,l] = imgTwo[(pX + k - 2),(pY + l - 2)]
            #Feed the resulting images into Canny
            expCan1 = cv2.Canny(blankImg1, 100,200)
            expCan2 = cv2.Canny(blankImg2, 100,200)
            #Compare these small-images for accuracy
            
            for x in range(5):
                for y in range(5):
                    totalPoints += 1
                    if(expCan1[x,y] == 255 and expCan2[x,y] == 255):
                        modTotal += 1
                        continue
                    if(expCan1[x,y] != expCan2[x,y]):
                        totalDiff += 1
                        modTotal += 1
        #cv2.imshow("Canny Expermental 1", expCan1)
        #cv2.imshow("Canny Expermental 2", expCan2)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        percPt = totalPoints / (modTotal*1.0)
        
        
        
        print("Number of points sampled: {}, which is {}% of points".format(totalPoints, 
              format(percPt,'.3f')))
        print("Expermental Random Edge - Difference count:{}".format(modTotal))
        print("Expermental Random Edge- Percentage Diff:{}".format(totalDiff * 1.0/modTotal))
        
        return
    
    
    else:
        print("Passing over entire image for Edge Comparision...")
        totalDiff = 0
        modTotal = 0
        for i in range(height):
            for j in range(width):
#                print(i,j)
                if(cannyOne[i,j] == 255 and cannyTwo[i,j] == 255):
                    modTotal += 1
                    continue #Black matching black is no useful ifnormation
                if(cannyOne[i,j] != cannyTwo[i,j]):
                    totalDiff += 1
                    modTotal += 1
        print(modTotal)
        print("Edges Different points: {}".format(totalDiff))
        print("Total Difference %wise: {}".format(totalDiff/(modTotal*1.0)))
        return totalDiff #Change to the % Accuracy? Could be worth looking into.


def morphMatch(imgOne, imgTwo, mode):
    #Pass the image into cv2 morphology (Similar to HW3, minus the detection)
    #Just apply the cv2.morphology ex
    #Could generate a list of contours, but that's probably not needed- we can
    #just compare the black/white image, similar to the Canny Edge result.
    #This makes it easier to just separate into a binary-choice on if it matches or not
    if mode == "rand":
        #Build histogram using only randomly selected points
        return
    else:
        #unfinished implementation, generating list of contours (but doesn't actually compare them)
        img1_gray = cv2.cvtColor(imgOne, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(imgTwo, cv2.COLOR_BGR2GRAY)
        img1_bw = cv2.adaptiveThreshold(img1_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1)
        img2_bw = cv2.adaptiveThreshold(img2_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1)
        contours1, _ = cv2.findContours(img1_bw.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(img2_bw.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
    rImgTwo = cv2.resize(imgTwo, (widthO,heightO), interpolation = cv2.INTER_AREA)
    hT, wT, _ = imgTwo.shape
    hTR, wTR, _ = rImgTwo.shape
    print("Dimensions of images: \n"
          "\tImage One:\t\t {} by {}\n"
          "\tImage Two:\t\t {} by {}\n"
          "\tResized Image Two:\t {} by {}\n".format(heightO, widthO, hT, wT, hTR,wTR)
          )
    
    #Creates Blurred images for testing
    blurOne = cv2.blur(imgOne, (3,3))
    blurTwo = cv2.blur(rImgTwo, (3,3))
    
    #Feed in the images into the code we have handy
    cv2.imshow("ImgOne", imgOne)
    cv2.imshow("ImgTwo", imgTwo)
    cv2.imshow("Scaled ImgTwo", rImgTwo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #sumSquaresMatch(imgOne, rImgTwo, "Normal")
    
    
    start = time.time()
    histMatch(imgOne,rImgTwo,"Normal")
    end = time.time()
    print("Elapsed Time HistMatch: " ,end-start)
    print()

    
    start = time.time()
    edgeMatch(imgOne, rImgTwo, "Normal")
    end = time.time()
    print("Elapsed Time EdgeMatch: " ,end-start)
    print()
    
#    start = time.time()
#    edgeMatch(imgOne, rImgTwo, "rand")
#    end = time.time()
#    print(end-start)

#    start = time.time()
#    edgeMatch(imgOne, rImgTwo, "exp")
#    end = time.time()
#    print(end-start)
    
    print("\nBlurred Image to Edge func\n")
    start = time.time()
    edgeMatch(blurOne, blurTwo, "Normal")
    end = time.time()
    print("Elapsed Time EdgeMatch (Blurred): ",end-start)
    print()
    
#    print("")
#    start = time.time()
#    edgeMatch(blurOne, blurTwo, "rand")
#    end = time.time()
#    print(end - start)

#    start = time.time()
#    edgeMatch(blurOne, blurTwo, "exp")
#    end = time.time()
#    print(end-start)
    
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
