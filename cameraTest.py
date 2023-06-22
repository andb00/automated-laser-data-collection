import cv2
import os

from vimba import *

# Configure settings on Vimba Viewer
# Allow 16-bit 
# Mono12 packed

# Makes a directory to store images
directory = 'data_collection'
os.mkdir(directory)

# Prompts user to input number of images to capture
# iterations = int(input("Enter the number of iterations for the camera to take pictures: "))

# Call for camera to be used
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()

    with cams[0] as cam:

        # Camera will capture images for the number of iterations inputted by user
        for ctr in range(3):
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono16)

            # Image captured by camera will be stored in directory
            save_path = os.path.join(directory, '{}.tiff'.format(ctr + 1))
            cv2.imwrite(save_path, frame.as_opencv_image())


# Program will notify it has completed image capturing
print("Program successful!")
