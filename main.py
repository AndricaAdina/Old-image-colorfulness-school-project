"""
resources:
https://www.pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/
https://www.tutorialkart.com/opencv/python/opencv-python-get-image-size/#gsc.tab=0

"""

import cv2 as cv
import numpy as np
import os
from imutils import build_montages

# Function used to determine the color level of an image
def ColorfulnessOfImage(image):

    # split the image into its respective components (RGB)
    (R, G, B) = cv.split(image.astype("float"))  
    rg = np.absolute(R - G)                      # compute rg = R - G
    yb = np.absolute(0.5 * (R + G) - B)          # compute yb = 0.5 * (R + G) - B

    # compute the mean and standard deviation of both `rg` and `yb`
    rb_mean = np.mean(rg)                       
    rb_std = np.std(rg)                         
    yb_mean = np.mean(yb)                       
    yb_std = np.std(yb)                         

    # combine the mean and standard deviations
    stdRoot = np.sqrt((rb_std ** 2) + (yb_std ** 2))  
    meanRoot = np.sqrt((rb_mean ** 2) + (yb_mean ** 2))  

    # derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)           

# Path where the program selects images
folder = "images/"                              
images = os.listdir(folder)

# List to store images from the selected folder
ImagesList = []                                    

# Read all images from the folder
for i in images:                                
    img = cv.imread(folder + i)
    d = img.shape
    h = img.shape[0]
    w = img.shape[1]

    if (w >= 1200 and h >= 1024):
        img = cv.resize(img, (0, 0), None, 0.5, 0.5)  # Resize images to desired dimensions
        C = ColorfulnessOfImage(img)
        # afișează scorul de culoare pe imagine
        cv.putText(img, "{:.2f}".format(C), (40, 40), cv.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), 3)
        ImagesList.append((img,C))

# Sort images based on color level
ImagesList = sorted(ImagesList, key = lambda x : x[1], reverse= True)

# Check if there is at least one image that meets the criteria
if ImagesList:

    # Get the most colorful image
    mostColor = ImagesList[0][0]

    # Display the most colorful image
    cv.imshow("Most colorful image", mostColor)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("No images meet the resolution threshold.")
    