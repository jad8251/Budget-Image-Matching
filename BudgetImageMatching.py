# -*- coding: utf-8 -*-
"""
Initial draft of budget-image matching program

Created on Sun Mar 18 13:57:17 2018

@author: Jason Durek
"""
import numpy as np
import cv2
import argparse

def histMatch():
    return

def edgeMatch():
    return

def morphMatch():
    return

def comboMatch():
    return


#Central function, designed to handle bulk of logic
#This includes resizing smaller image to match larger
def main(imgI, imgII, method, sens):
    #Check to make sure we can access both images
    imgOne = cv2.imread(imgI,0)
    imgTwo = cv2.imread(imgII,0)
    if imgOne is None:
        print("Failed to read first image provided.")
        if imgTwo is None:
            print("Failed to read second image provided.")
        return
    elif imgTwo is None:
        print("Failed to read second image provided.")
        return
    
    #Images were correctly read in; Determine which one is smaller,
    #Then scale it up to match the size of the larger one.
    
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
