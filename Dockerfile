#FROM ubuntu:14.04


# Use an official Python runtime as a parent image
#FROM python:2.7-slim
FROM python:2.7

# Set the working directory to /app
WORKDIR /APP

# Copy the current directory contents into the container at /app
ADD . /APP

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update && apt-get install -y mysql-client

# Make port 80 available to the world outside this container
EXPOSE 8085

# Define environment variable
ENV NAME Chalanges

# Run app.py when the container launches

CMD ["python", "server.py"]
#CMD ["/bin/bash","setup.sh"]

