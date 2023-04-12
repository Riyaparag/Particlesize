import cv2
import numpy as np
import csv
from  picamera import PiCamera
import time
from time import sleep 


camera = PiCamera()
camera.start_preview()
sleep(5)
# camera.stop_preview()
# camera.close()
# time.sleep(5)
camera.capture("/home/pi/particle_test/particle/image8.jpg")
camera.stop_preview()
path = '/home/pi/particle_test/particle/image8.jpg'



# print('shape of image',img.shape)
# crop= image[:,50:1870]
# cv2.imshow('TEST',crop)


img = cv2.imread(path, cv2.IMREAD_COLOR)
img_orig = img.copy()

def inch_to_mm(x):
    return x * 25400
def getParticleArea(radius):
    return np.pi * radius**2

def getParticleRadius(width, height):
    """
    """
    if width == 0:
        return height/2
    elif height == 0:
        return width/2
    else:
        return (height+width)/4

image_width = 3
image_height = 1
physical_width_of_view = inch_to_mm(image_width)
physical_height_of_view = inch_to_mm(image_height)
pixels_per_metric_height = img.shape[0]/physical_height_of_view
pixels_per_metric_width = img.shape[1]/physical_width_of_view
    
#     # blurring
#     #img = cv2.GaussianBlur(img, (3, 3), 0)
threshold = 155
#     # take single channel for thresholding
img_channel = img[:,:,2]
ret, binary  = cv2.threshold(img_channel,threshold, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('TEST',binary)
# cv2.waitKey(0)
# binary = cv2.adaptiveThreshold(img_channel, threshold, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)

#     # get objects from thresholded image
binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
output = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
(numLabels, labels, stats, centroids) = output
print(output)
    
#     # get measurements of objects
physical_radiuses = []
physical_areas = []
        
#     # get radius and area
for i in range(1, len(stats)-1):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
        #draw bbox
img= cv2.rectangle(img, (x,y), (x+w, y+h), color=(0,0,255), thickness=1)

physical_width = w / pixels_per_metric_width
physical_height = h / pixels_per_metric_height
radius =  getParticleRadius(physical_width, physical_height)
area = getParticleArea(radius)
physical_radiuses.append(radius)
physical_areas.append(area)
    

        
#     #draw centroid
for c in centroids:
    x = int(c[0])
    y = int(c[1])
you= cv2.circle(img, (x,y), radius=1, color=(0, 0, 255), thickness=-1)


        
stats = "mean area: " + str(np.mean(physical_areas)) + " mean radius: " + str(np.mean(physical_radiuses))
print(stats)

images_concat = np.concatenate((img_orig, img), axis=0)
    # show image
cv2.imshow("Particle detection", images_concat)
cv2.waitKey(0) 


