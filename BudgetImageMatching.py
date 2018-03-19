# -*- coding: utf-8 -*-
"""
Initial draft of budget-image matching program

Created on Sun Mar 18 13:57:17 2018

@author: Jason Durek
"""

def histMatch():
    return

def edgeMatch():
    return

def morphMatch():
    return

def comboMatch():
    return





if __name__ == '__main__':
    import sys
    if(len(sys.argv) == 2):
        #Special check for if user puts in help
        if(sys.argv[1] == "help"):
            print("Usage: --.py imageFile1 imageFile2 method [-sensitivity]")
            print("Available methods:")
            print("\thist - Use color histograms to create approximations")
            print("\tedge - Use edge detection to narrow down features and compare general locations")
            print("\tmorph - Use morphology to transform image and find objects and general locations")
            print("Sensitivity tweaks the treshold for determining if an image matches.")
            print("\tScales from 0 to 100- 0 is Always match, 100 is Exact match, 75 means 25% or less differences between is match. By default, this is 90")    
    elif(len(sys.argv) > 5 or len(sys.argv) < 4):
        print("Usage: --.py imageFile1 imageFile2 method [-sensitivity]")
    else:
        #Execute actual code
        print("Executing code")