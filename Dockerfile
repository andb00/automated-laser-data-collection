FROM python:latest
COPY cameraTest.py .
ADD VimbaPython-master .
COPY requirements.txt ./
RUN pip install opencv-python numpy
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
COPY . .
CMD ["python", "./cameraTest.py"]
