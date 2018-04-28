# Dockerfile for batchcutencode

FROM ubuntu:16.04
#FROM python:3.6


WORKDIR /app

ADD src/ /app/

RUN apt-get update && apt-get install -y ffmpeg handbrake-cli python3 python3-pyinotify

# Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python3", "batchcutencode.py"]
