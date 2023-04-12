
import cv2 
from  picamera import PiCamera
import time
from time import sleep 

camera = PiCamera()
camera.start_preview()
sleep(40)
# camera.stop_preview()
# camera.close()
# time.sleep(5)
camera.capture("/home/pi/Pictures/image8.jpg")
camera.stop_preview()
print("DONE.")
img=cv2.imread("/home/pi/Pictures/image8.jpg")
print('shape of image',img.shape)
crop= img[:,50:1870]
cv2.imshow('TEST',crop)
cv2.waitKey(0)

