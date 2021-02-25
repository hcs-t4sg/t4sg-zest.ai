# set base image (host OS)
FROM python:3.7-alpine

# set the working director in the container
WORKDIR /code

# set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

# copy the flask server file of the local src directory to the working directory
COPY app.py .

CMD ["flask", "run"]