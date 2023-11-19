# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR .

# Copy the app.py file into the container at /app
COPY app.py /app/

# Create a directory to hold video files within the container
RUN mkdir /app/videos

# Copy the Traffic1.mp4 and Traffic2.mp4 files into the container at /app/videos
COPY Traffic1.mp4 /app/videos/
COPY Traffic2.mp4 /app/videos/

# Install any needed dependencies specified in requirements.txt
RUN pip install opencv-python-headless numpy ultralytics

# Run app.py when the container launches
CMD ["python", "app.py"]
