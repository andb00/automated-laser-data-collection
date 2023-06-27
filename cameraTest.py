import cv2
import os
from PIL import Image
from PIL.TiffTags import TAGS

from vimba import *

# Configure settings on Vimba Viewer

# Allow 16-bit 
# Mono12 packed and/or Mono16
# Check if images are 16 bit

# Makes a directory to store images
directory = 'data_collection'
os.mkdir(directory)

# Call for camera to be used
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()

    with cams[0] as cam:

        # Camera will capture images for the number of iterations inputted by user
        
        # Activating ChunkMode will allow to grab specific metadata
        chunks = cam.get_feature_by_name("ChunkModeActive")
        chunks.set(True)

        # Format of image will initially be set to Mono12Packed
        pixel_format = cam.get_feature_by_name("PixelFormat")
        pixel_format.set("Mono12Packed")

        for ctr in range(3):
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono16)

            # Image captured by camera will be stored in directory
            save_path = os.path.join(directory, '{}.tiff'.format(ctr + 1))
            cv2.imwrite(save_path, frame.as_opencv_image())

        # open the image
        image = Image.open("data_collection/1.tiff")

        # extracting the exif metadata
        exifdata = image.getexif()

        info_dict = {
            "Filename": image.filename,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1),

        }

        for label, value in info_dict.items():
            print(f"{label:25}: {value}")

        # looping through all the tags present in exifdata
        for tagid in exifdata:
            # getting the tag name instead of tag id
            tagname = TAGS.get(tagid, tagid)

            # passing the tagid to get its respective value
            value = exifdata.get(tagid)

            # printing the final result
            print(f"{tagname:25}: {value}")

        exposure = cam.get_feature_by_name("ExposureTimeAbs")
        exposure.set(15000)
        print("Exposure %17s %.1f" % (":", exposure.get()))
