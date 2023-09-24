# Droplet Measurement and Analysis Using Image Processing for Insecticide Spray
### About the Project
1. The professionals at the Anastasia Mosquito Control District (AMCD) are experts in providing environmental-friendly mosquito control services, community education, and scientific research on mosquito-borne diseases for St. Johns County, St. Augustine, FL. AMCD carries out insecticide testing to measure, droplet count and diameter spectrum values (DV0.5, DV0.1, and DV0.9).
2. Particle droplet size and count of insecticides are essential parameters to determine the amount of insecticide needed to cover an intended target area. Diameter volume spectrum values such as DV0.5, DV0.1, and DV0.9 describe the application an insecticide is suitable for and its susceptibility to spray drift.
3. The current tool i.e., Artium PDI TK1 Droplet Analyzer used to calculate the droplet size, count and diameter volume spectrum parameters at the AMCD could be time consuming, costly, and tedious to use. It is an expensive benchtop tool which can only test sample slides indoors, consequently, it does not give instantaneous results.
4. Around 60 slides need to be tested after each insecticide testing, which takes atleast 3-4 hours according to the experts at the AMCD. Collecting the slides from the field and testing indoors, requires heavy labour. There is a need to create a system which could make this process more efficient.
5. The system proposed is a user-oriented, Internet of Things (IoT) based cost-effective portable tool to give a real-time droplet size and diameter spectrum measurement using image processing for insecticide spray.

### Hardware tools used
>Raspberry pi 4B+, HQ camera, Pimoroni Microscopic lens.

### Software tools used
>Python, OpenCV, Visual Studio Code, Linux distribution, VNC Viewer. 

### Inbuilt Libraries
1. **PiCamera**: Take multiple images using Raspberry Pi with a delay to create an image pipeline.  Allows taking images of the multiple insecticide slides at once in real-time.
2. **Numpy**: Basic numpy functions like np.mean, np.concatenate, np.zeros, np.pi, np.sort, np.unique applied in the algorithm.

3. **OpenCV**: 
   1. **Threshold**: Separate foreground from background using Global Thresholding with a value 155.
   2. **Contour**: Contour pixels using cv2.findContours which were labeled using watershed algorithm. 
   3. **Enclosing Method**: Circle, Rectangle; Used to mark the contoured droplets on the image.
      
4. **Distance Transform, Peak_local_max**: Using the distance transform the distance between each foreground and nearest background pixel is calculated, from this matrix the peak_local_max selects the maximum values with a minimum distance of 5 pixels as set in this algorithm. This was specifically used to avoid under/over-segmentation due the small droplet size [1-150um] of the insecticide spray.   
6. **Watershed**: The threshold image was used to make a mask to label the background pixels as ‘0’ and ‘255’ to allocate memory for the labeled region.
7. **CSV**: Store and display the calculated parameters such as, Droplet Count, DV0.5, DV0.1, and DV0.9, Relative Span.
8. **Matplotlib**: Achieved similar output format as the current tool used at AMCD by plotting histogram and analyzing the Volume Median Diameter (DV0.5).

### Functions created
1.	**inch_to_mm**: The actual image size is in inches and the droplets are to be measured in micrometers (um). For scaling purposes, a function was created to convert inches to um.
2.	**getParticleRadius**:  Variables calculated using connected component analysis were used to get individual droplet radius. This radius was used to calculate droplet diameters. 
3.	**particle_detection**: The main function of the algorithm, takes in path of the image, its physical widht and height in um, enclosing method, the minimum distance to output the number of droplets recognized and labels to create an appropriate mask for contouring. 
4.	**get_vmd**: the median of the list of diameters used to calculate DV0.5, DV0.1, and DV0.9.
5.	**plot_vmd**: Plotted vertical lines to represent DV0.5, DV0.1, and DV0.9 on a histogram for number of droplets vs a range droplet diameters to replicate the output histogram obtained from the current AMCD tool.

### Results
The algorithm developed was first applied on images obtained from the AMCD. These are images **A16, A25, A26, A36, A46**. The processed and contoured output after applying the algorithm can be seen in output_A16-46. The consolidated calculated parameters for droplet count, diameter spectrum values and relative span is as seen in the **output_A16-46.csv** file. Once tested on the images from AMCD, this algorithm was run on an image pipeline with 3 different insecticide spray slide images taken by the Raspberry Pi camera for real-time testing. The input images are **image1, 2,3** . The output images **output_image1,2,3** are able to  **replicate the images** obtained from the current tool used at the AMCD. **Instanteneous output** is obtained and stored in the **output_realtime.csv**. 


### Reliability of the system  <br>
Now that the system worked as whole from taking images to calculating mathematical parameters, there was a need to check the reliability of the system. 
To test the reliability of this Droplet Analysis and Measurement device a single water sensitive card was sprayed with water. An image of the same slide was taken thrice using the PiCamera pipeline as shown in **image 8,9,10** . The algorithm was applied to the images in a loop.The processed and contoured output images output_image8,9,10 are added. The results for number of particles, diameter volume spectrum values and relative span are **quite similar** as proved in the **output_reliability.csv** file. This proves that the results obtained from the droplet analyzer are **reliable** .

### Achievements 
1.	Unlike the current tool used at the AMCD, this droplet analyzer can be operated **remotely**. The results can be stored and viewed from multiple systems using the **VNC Viewer**. This **reduces** the need for heavy labor and time for analysis.
2.	As this is a **portable** tool, it can be taken to the field for capturing real time images of insecticide slides and obtain instant output.
3.	As the hardware is IoT based the installation and setup is **cost effective**. This system can be easily replicated to create **multiple nodes**. 
4.	As the software is open source, this system can be easily **commercialized**.

### Contact 
> Email: riyadesai54@gmail.com <br>
>  [Linkedin](https://www.linkedin.com/in/riya-paragkumar-desai-a805a0181)




