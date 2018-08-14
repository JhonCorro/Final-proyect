import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path of working folder on Disk
src_path = "C:/Users/user/Pictures/"
d=0 # Slice image counter

def ocr(img):# Apply OCR for character recognition

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string((img))

    return result

#Function that process images
def analyzer(img):

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 57,2)  # (57,2) for sliced number #1.


    #cv2.imwrite(src_path + "thres.png", img)  # imagen thresh

    #Write results on a file
    f = open('resultados.txt', 'a')
    f.write('\n' + (ocr(img)))
    f.close()

# Function to divide image into images with the relevant data
def divide_images (img,d):
    c=0#Frame Counter
    ImgVector = list()# Declaring array
    ImgVector.append(img[90:175, 600:900])#Add sliced image into an array
    # cv2.imshow('Display', img)#[90:175, 600:900]) #For test

    #Traversing images in vector, applying image processing and write them on path
    for frame in ImgVector:
        analyzer(ImgVector[c]) #Apply Image processing
        cv2.imwrite(src_path + "/crop%d_%d.jpg" %(c,d), ImgVector[c])# write file with frame and slice counter
        c = c + 1
    return d+1 #Increase global frame counter


#Function that separate video frames| (path of video, path of frame storage, slice image counter)
def extractImages(pathin, pathout,d):
    count = 0# Frame counter for limit frame quantity
    vidcap = cv2.VideoCapture(pathin)#Capture video from path
    success,image = vidcap.read()#validating frames
    #success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))# Limiting frame quantity, count*Milliseconds
      success,image = vidcap.read()#Frame Status
      if not success:# If frame is not successful break loop
          break
      print ('Read a new frame: ', success)#Print if frame reading was successful
      d=divide_images(image,d) # Save Frame counter to pass to main code and global d variable
      cv2.imwrite( pathout + "/frame%d.jpg" % count, image)# save frame as JPEG file
      count = count + 1#Increase frame counter



"""MAIN"""

print ('--- Start recognize text from image ---')
d=(extractImages(src_path + "prueba.mov", src_path ,d))#Select video
print ("------ Done -------")