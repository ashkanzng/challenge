#FROM ubuntu:14.04
# Use an official Python runtime as a parent image
#FROM python:2.7-slim
FROM python:2.7

# Set the working directory to /app
WORKDIR /APP

# Copy the current directory contents into the container at /app
ADD . /APP

# Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y mysql-client

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME MYChalanges

# Run app.py when the container launches
CMD ["python", "server.py"]


