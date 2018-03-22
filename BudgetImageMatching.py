# -*- coding: utf-8 -*-
"""
Initial draft of budget-image matching program

Created on Sun Mar 18 13:57:17 2018

@author: Jason Durek
"""
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
    return

def morphMatch(imgOne, imgTwo, mode):
    #Pass the image into cv2 morphology (Similar to HW3 I suppose)
    return

def sumSquares(imgOne, imgTwo, mode):
    #Process the image and determine how much difference exists between the two in terms of raw
    #pixel information. 
    
    return

def comboMatch(imgOne, imgTwo, mode):
    return


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
    rImgTwo = cv2.resize(imgTwo, (heightO,widthO))
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
