# set base image (host OS)
FROM python:3.8

# set the working director in the container
WORKDIR /code

# set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

EXPOSE 5000

CMD ["flask", "run"]