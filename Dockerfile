# set base image (host OS)
FROM python:3.7

# copy requirements.txt and install Python requirements
COPY requirements.txt .
RUN python -m pip install pip-tools && pip-sync

# copy the app itself
COPY application.py .
COPY app/ ./app
