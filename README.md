# Budget-Image-Matching
Computer Vision Project using lower-cost methods to test trying to match images of different resolutions (Similar to Google's Image Search).

This is a Python 2 program using the Open CV Library (CV2) to implement image matching using less resource-intensitive methods compared to a more full-featured matching program. This also includes attempts to improve performance further by relying on statistics to determine tradeoffs on quality for speed. 

This tests 4 main methods in two ways; Full Scan and Random Sampling.
These methods are as follows
  1) Color Histogram Matching
  2) Edge Detection Matching
  3) Morphology Matching
  4) Sum of Squared Pixel Differences
  
The program takes in two images (Filepaths to images), a Method argument, a sensitivity argument, and a Mode argument. 
Method just picks which of the above to use, while Sensitivity is an optional argument that allows for less-than perfect matches to be flagged as matching images due to the nature of how the images are resized. Mode alternates between full scans of the images or random samplings of identical locations in both images after matching their resolutions. 

Currently, we scale the smaller image up to the larger one to avoid loosing information from the image, along with having the sensitivity because we don't know how the images were scaled to a different size. Some parts might be a slightly different color, which has to be considered when deciding if it's a match or close enough to be a match. 
