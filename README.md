**vimbaCamera**
Project for Vimba Camera automation

Connecting Camera:

**PC-Beamage**
For creating beam profiles for the laser diodes and collimating lenses. 
Set up:
              1. Before opening the PC-Beamage software. Make sure the camera is plugged in. 
              RECOMMENDED: Plug the camera into a hi-speed USB port.
              2. From the start-up menu. Choose the name of the camera device. The software should
              detect the camera automatically and show up as an option on the start-up menu. 
              3. Adjust the camera accordingly for the image capture.
              4. Then to capture and save the image, click "Save Current Image" and from the drop-menu,
              Choose the desired image format. 
              Recommended: Save the image as a .bmg file and as a .txt file.

              Additional Information:
              The display of the image can be changed if you look at the bottom of the window. For our project we used both 3D                 and 2D. Display to check the image for adjustments. The image should be centered. The software should let you zoom               in and out of the image which helps in adjustments.


            
              
      
**Arcus Technology Software**
This software allows you to configure the Rotating Phase Plate. 

Other names: ACE-SXE Software or SOFT-EXE-ACE-SXE-230

Set up:
              1. Before opening the application, connect the camera to the PC. RECOMMENDED: Use a high-speed
              USB port.
              2. From the start-up menu of the software, click USB and choose the device. 
              3. The main window will open and you will be able to configure the settings. Click "Enable" checkbox to 
              access the camera. 
              * Make sure PC-Beamage is close and any applications that can interfere with the software. RECOMMENDED:
              Unplug any connections from the ports except for the Rotary Phase Plate to ensure the program runs smoothly. 
              The program can still run while other devices are connected but might make the software run slow. 
              4. In the "Control" section, you are able to access the Phase Plate. To double check if the connection
              of the camera is successful, you can press either "JOG-" or "JOG+".
              5. To synchronize the Rotating Phase Plate with a camera, you can calculate the steps you need with fps
              the camera.
              6. To have more control of the device, you can develop and use a code to configure the settings. 
              You can enter the code in the "Text Program" Section
              EXAMPLE: 

              
                      HSPD=1000
                      LSPD=100
                      ACC=300
                      EO=1
                      V1=0
                      V2=0
                      WHILE V1 < 960
                        XV2
                        DELAY=65
                        V2=V2+10
                        V1=V1+1
                      ENDWHILE
                      END

                      
 *This code was used for an experiment. This was used to synchronize with a camera that will 
  capture 960 images. The fps used was 20. 
*The manual contains all the code syntax and functions for the software.


              7. You can save your code and use it later. 
              8. After inputting your code, make sure to "compile", "download", and "Upload".
              9. This will allow you to run the code.
              10. After each run, make sure in the "STATUS" section that the "Postion" is at zero, or reset. 
              11. If you need to use another application or want to stop the access to the rotor device, click
              "Enable" and make sure the box is unchecked. 
              

             










                      

