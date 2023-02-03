import cv2
import numpy as np
import csv


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
    
# def save_to_csv(img_name, radiuses, areas):
#     """
#     write stats to csv file
#     """
#     header = ["object_id", "radius [μm]", "area [μm^2]", "number of particles"]
#     mean_values = ["mean", np.mean(radiuses), np.mean(areas), len(areas)]
#     f = open(img_name + ".csv", 'w')

#     writer = csv.writer(f)
    
#     writer.writerow(header)
#     writer.writerow(mean_values)

#     object_id  = list(range(len(areas)))
#     for row in zip(object_id, radiuses, areas):
#         writer.writerow(row)

    f.close()
    
def getSize(path, threshold, physical_width_of_view, physical_height_of_view):
    """
    Args
    
    Return
    """
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img_orig = img.copy()
    pixels_per_metric_height = img.shape[0]/physical_height_of_view
    pixels_per_metric_width = img.shape[1]/physical_width_of_view
    
    # blurring
    #img = cv2.GaussianBlur(img, (3, 3), 0)
    
    # take single channel for thresholding
    img_channel = img[:,:,2]
    ret, binary  = cv2.threshold(img_channel,threshold, 255, cv2.THRESH_BINARY_INV)
    #binary = cv2.adaptiveThreshold(img_channel, threshold, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)

    # get objects from thresholded image
    output = cv2.connectedComponentsWithStats(binary, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    
    # get measurements of objects
    physical_radiuses = []
    physical_areas = []
        
    # get radius and area
    for i in range(1, len(stats)-1):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        physical_width = w / pixels_per_metric_width
        physical_height = h / pixels_per_metric_height
        radius =  getParticleRadius(physical_width, physical_height)
        area = getParticleArea(radius)
        physical_radiuses.append(radius)
        physical_areas.append(area)
        #draw bbox
        cv2.rectangle(img, (x,y), (x+w, y+h), color=(0,0,255), thickness=1)
        
    #draw centroid
    for c in centroids:
        x = int(c[0])
        y = int(c[1])
        cv2.circle(img, (x,y), radius=1, color=(0, 0, 255), thickness=-1)
        
    stats = "mean area: " + str(np.mean(physical_areas)) + " mean radius: " + str(np.mean(physical_radiuses))
    print(stats)
    # cv2.putText(img, text=stats, org=(5, 40), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)

    # # save to file
    # img_name = path.split(".", 1)[0]
    # save_to_csv(img_name, physical_radiuses, physical_areas)
    
    # show output
    binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    images_concat = np.concatenate((img_orig, img), axis=0)
    # show image
    cv2.imshow("Particle detection", images_concat)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    

path = "A16.bmp"
"A16, A25, A26, A36, A46"

image_width = 3
image_height = 1

physical_width_of_view = inch_to_mm(image_width)
physical_height_of_view = inch_to_mm(image_height)
threshold = 155
getSize(path, threshold, physical_width_of_view, physical_height_of_view)

