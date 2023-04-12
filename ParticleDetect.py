import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2

from  picamera import PiCamera
import time
from time import sleep 

camera = PiCamera() 
camera.start_preview()
sleep(10)
# camera.stop_preview()
# camera.close()
# time.sleep(5)
camera.capture("/home/pi/particle_test/particle/image8.jpg")
camera.stop_preview()



camera.start_preview()
sleep(10)
# camera.stop_preview()
# camera.close()
# time.sleep(5)
camera.capture("/home/pi/particle_test/particle/image9.jpg")
camera.stop_preview()
print("Images captured.")

# camera.start_preview()
# sleep(30)
# # camera.stop_preview()
# # camera.close()
# # time.sleep(5)
# camera.capture("/home/pi/particle_test/particle/image10.jpg")
# camera.stop_preview()
# print("DONE.")




def inch_to_mm(x):
    return x * 25400

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

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

def write_header(file_name):
    header = ["image_name", "number of particles", "dv01", "dv05", "dv09", "relative span"]
    f = open(file_name, 'w')
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()
    
def save_add_to_csv(file_name, image_name, dvs, radiuses):
    """
    write stats to csv file
    """
    relative_span = (dvs[2]- dvs[0]) / dvs[1]
    values = [image_name, len(radiuses), dvs[0], dvs[1], dvs[2], relative_span]
    f = open(file_name, 'a')
    writer = csv.writer(f)
    writer.writerow(values)
    f.close()

def save_to_csv(img_name, radiuses, dvs, areas):
    """
    write stats to csv file
    """
    relative_span = (dv09- dv01) / dv05
    header = ["object_id", "radius [μm]", "area [μm^2]", "number of particles", "dv01", "dv05", "dv09", "realtive span"]
    mean_values = ["mean", np.mean(radiuses), np.mean(areas), len(areas), dvs[0], dvs[1], dvs[2], relative_span]
    f = open(img_name + ".csv", 'w')

    writer = csv.writer(f)
    
    writer.writerow(header)
    writer.writerow(mean_values)

    object_id  = list(range(len(areas)))
    for row in zip(object_id, radiuses, areas):
        writer.writerow(row)

    f.close()
    
    
def get_vmd(radiuses):
    diameters = list(map(lambda n: n+n, radiuses))
    n_particles = len(diameters)
    sorted_diameters = np.sort(diameters)
    dv01 = sorted_diameters[int(0.1*n_particles)]
    dv05 = sorted_diameters[int(0.5*n_particles)]
    dv09 = sorted_diameters[int(0.9*n_particles)]
    print("DV01: ", dv01)
    print("DV05: ", dv05)
    print("DV09: ", dv09)

    return dv01, dv05, dv09

def plot_vmd(name, dv01, dv05, dv09, radiuses):
    diameters = list(map(lambda n: n+n, radiuses))
    fig, ax = plt.subplots()
    bins = list(range(0, 700, 25))
    plt.hist(diameters, bins = "auto")
    plt.xlabel("Droplet Diameter")
    plt.ylabel("Number of particles")
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    
    xpos = (dv01+abs(xmin))/(xmax+abs(xmin))
    plt.axvline(x = dv01, color = 'r',label = 'DV 0.1')
    plt.text(xpos, 1.02, str(dv01)[0:4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    xpos = (dv05+abs(xmin))/(xmax+abs(xmin))    
    plt.axvline(x = dv05, color = 'r',label = 'DV 0.5')
    plt.text(xpos, 1.02, str(dv05)[0:5], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
    
    xpos = (dv09+abs(xmin))/(xmax+abs(xmin))
    plt.axvline(x = dv09, color = 'r',label = 'DV 0.9')
    plt.text(xpos, 1.02, str(dv09)[0:5], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
    
    fig.savefig(name)

def particle_detection(path, physical_width_of_view, physical_height_of_view, min_distance= 5, enclosing_method = "circle"):
    image = cv2.imread(path)
    pixels_per_metric_height = image.shape[0]/physical_height_of_view
    pixels_per_metric_width = image.shape[1]/physical_width_of_view

    # thresholding
    channel = image[:,:,2]
    thresh = cv2.threshold(channel, 155, 255,cv2.THRESH_BINARY_INV)[1]
    
    D = ndimage.distance_transform_edt(thresh)
    
    localMax = peak_local_max(D, indices=False, min_distance=min_distance,labels=thresh)
    
    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then appy the Watershed algorithm
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    
    
    labels = watershed(-D, markers, mask=thresh)
   
    
    print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

    # get measurements of objects
    physical_radiuses = []
    radiuses_bbox = []
    radiuses_circle = []
    physical_areas = []

    #loop over the unique labels returned by the Watershed
    # algorithm
    for label in np.unique(labels):
        # if the label is zero, we are examining the 'background'
        # so simply ignore it
        if label == 0:
            continue
        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(thresh.shape, dtype="uint8")
        mask[labels == label] = 255

        # detect contours in the mask and grab the largest one
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
       
        # save stats
        if enclosing_method == "circle":
             # get and draw circle enclosing the object
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 0, 255), 1)
            physical_width = 2*radius / pixels_per_metric_width
            physical_height = 2*radius / pixels_per_metric_height
            radius = (physical_width + physical_height) / 4
        else:
             # get and draw bounding rectangle
            x,y,w,h = cv2.boundingRect(mask)
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 1)
            physical_width = w / pixels_per_metric_width
            physical_height = h / pixels_per_metric_height
            radius =  getParticleRadius(physical_width, physical_height)
        
        physical_radiuses.append(radius)
        #area =  getParticleArea(radius_circle)
        #physical_areas.append(area)
        
    # prepare output
    dv01, dv05, dv09 = get_vmd(physical_radiuses)
    dvs = [dv01, dv05, dv09]

    # segmentated image
    output_img = image #np.concatenate((image, image2), axis=0) # to display image side by side
    
    return output_img, dvs, physical_radiuses


# path of folder of images
root_path = "/home/pi/particle_test/particle/"
# image names
images = ["image8.jpg","image9.jpg"]
# name of csv file
file_name = "output.csv"
# write header into csv file
write_header(root_path + file_name)
# set physical width and height of the image in [mm], use  inch_to_mm() if in inch
physical_width_of_view = inch_to_mm(3)
physical_height_of_view =inch_to_mm(1)

# parameters
min_distance = 5
enclosing_method = "circle" # "circle" or "bbox"

# loop through images
for image_name in images:
    print("[PROCESS] ", image_name)
    imgae_name_without_filename = image_name.split(".", 1)[0]
    image_path = root_path + image_name
    # perform particle detection
    img_output, dvs, radiuses = particle_detection(image_path, physical_width_of_view, physical_height_of_view, 
            min_distance= min_distance, enclosing_method = enclosing_method)

   
    # save image with markers to file
    cv2.imwrite(root_path + "output_" + image_name, img_output)
    dv01, dv05, dv09 = dvs
    # plot histogram
    plot_vmd(root_path + "histogram_" + imgae_name_without_filename, dv01, dv05, dv09, radiuses)
    
    # show image
    dsize = (img_output.shape[1]//2, img_output.shape[0]//2)
    show_img = cv2.resize(img_output, dsize, interpolation = cv2.INTER_AREA)
    cv2.imshow("Output", show_img)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    # save stats to csv file
    save_add_to_csv(root_path + file_name, image_name, dvs, radiuses)



