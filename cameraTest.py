import cv2
import os
from tkinter import *
from PIL import Image
from PIL.TiffTags import TAGS
from vimba import *
from datetime import datetime

# Allow 16-bit
# Mono12 packed


# Function for closing GUI window
def close():
    tkWindow.quit()


# Creates date and time for the name of the directory
now = datetime.now()
directory = now.strftime("%m-%d-%Y %H-%M-%S")

# Creates GUI window
tkWindow = Tk()
tkWindow.geometry('300x200')
tkWindow.title("Summer 2023 Rotation Phase")

# Text entries for exposure, gain, frame rate, wavelength, beam size, region,
# and step size
exposure_prompt = Label(tkWindow, text="Exposure")
exposure_input = Entry(tkWindow)

gain_prompt = Label(tkWindow, text="Gain")
gain_input = Entry(tkWindow)

frame_rate_prompt = Label(tkWindow, text="Frame Rate")
frame_rate_input = Entry(tkWindow)

wavelength_prompt = Label(tkWindow, text="Wavelength")
wavelength_input = Entry(tkWindow)

beam_size_prompt = Label(tkWindow, text="Beam Size")
beam_size_input = Entry(tkWindow)

region_prompt = Label(tkWindow, text="Region")
region_input = Entry(tkWindow)

step_size_prompt = Label(tkWindow, text="Step Size")
step_size_input = Entry(tkWindow)

# The submit button will close the window
submitButton = Button(tkWindow, text="Submit", command=close)

# Formatting of the text entries
exposure_prompt.grid(row=0, column=0)
exposure_input.grid(row=0, column=1)

gain_prompt.grid(row=1, column=0)
gain_input.grid(row=1, column=1)


frame_rate_prompt.grid(row=2, column=0)
frame_rate_input.grid(row=2, column=1)

wavelength_prompt.grid(row=3, column=0)
wavelength_input.grid(row=3, column=1)

beam_size_prompt.grid(row=4, column=0)
beam_size_input.grid(row=4, column=1)

region_prompt.grid(row=5, column=0)
region_input.grid(row=5, column=1)

step_size_prompt.grid(row=6, column=0)
step_size_input.grid(row=6, column=1)

submitButton.grid(row=7, column=1)

tkWindow.mainloop()


directory += "_" + wavelength_input.get() + "nm_r_" + region_input.get() + " " + beam_size_input.get()
try:
    os.mkdir(directory)

except FileExistsError:
    print("File already exists. Delete the file and try again.")
    exit(1)

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

        for ctr in range(960):
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono16)

            # Image captured by camera will be stored in directory
            save_path = os.path.join(directory, '{}.tiff'.format(ctr + 1))
            cv2.imwrite(save_path, frame.as_opencv_image(), [259, 1])

        # finish = time.perf_counter()
        # open the image
        image = Image.open(f"{directory}/1.tiff")
        image.tag[37000] = int(wavelength_input.get())
        image.tag[270] = str(beam_size_input.get())
        image.tag[271] = int(region_input.get())
        image.tag[272] = int(step_size_input.get())
        image.save(f"{directory}/1.tiff", tiffinfo=image.tag)

        # extracting the exif metadata
        exifdata = image.getexif()

        info_dict = {
            "Filename": image.filename,
            "Image Format": image.format,
            "Wavelength": str(image.tag[37000]).replace("(", "").replace(")", "").replace(",", ""),
            "Beam Size": str(image.tag[270]).replace("(", "").replace(")", "").replace(",", "")
            .replace('\'', '').replace('\'', ''),
            "Region": str(image.tag[271]).replace("(", "").replace(")", "").replace(",", ""),
            "Step Size": str(image.tag[272]).replace("(", "").replace(")", "").replace(",", "")
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
        frame_rate.set(frame_rate_input.get())
        print("Frame Rate %15s %f" % (":", frame_rate.get()))

        ip_address = cam.get_feature_by_name("GevCurrentIPAddress")
        print("IP Address %15s %d" % (":", ip_address.get()))

