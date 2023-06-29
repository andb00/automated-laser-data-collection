import cv2
import os
from tkinter import *
from PIL import Image
from PIL.TiffTags import TAGS
from vimba import *
from datetime import datetime


# Configure settings on Vimba Viewer
# Allow 16-bit
# Mono12 packed

# Function for closing GUI window
def close():
    tkWindow.quit()


now = datetime.now()
directory = now.strftime("%m-%d-%Y %H-%M-%S")


# Will attempt to create directory and notify when if one has already been created
try:
    os.mkdir(directory)

except FileExistsError:
    print("File already exists. Delete the file and try again.")
    exit(1)

# Creates GUI window
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title("Vimba Viewer")

# Text entries for exposure, gamma, and gain
exposure_prompt = Label(tkWindow, text="Enter Exposure")
exposure_input = Entry(tkWindow)
gain_prompt = Label(tkWindow, text="Enter gain")
gain_input = Entry(tkWindow)

# The submit button will close the window
submitButton = Button(tkWindow, text="Submit", command=close)

# Formatting of the text entries
exposure_prompt.grid(row=0, column=0)
exposure_input.grid(row=0, column=1)

gain_prompt.grid(row=1, column=0)
gain_input.grid(row=1, column=1)

submitButton.grid(row=3, column=1)

tkWindow.mainloop()

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
            cv2.imwrite(save_path, frame.as_opencv_image(), [259, 1])

        # open the image
        image = Image.open(f"{directory}/1.tiff")

        # extracting the exif metadata
        exifdata = image.getexif()

        info_dict = {
            "Filename": image.filename,
            "Image Format": image.format,
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
        exposure.set(exposure_input.get())
        print("Exposure %17s %.1f" % (":", exposure.get()))

        gain = cam.get_feature_by_name("Gain")
        gain.set(gain_input.get())
        print("Gain %21s %.1f" % (":", gain.get()))

        frame_rate = cam.get_feature_by_name("AcquisitionFrameRateAbs")
        print("Frame Rate %15s %f" % (":", frame_rate.get()))

        ip_address = cam.get_feature_by_name("GevCurrentIPAddress")
        print("IP Address %15s %d" % (":", ip_address.get()))
