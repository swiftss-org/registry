# Set base image (host OS)
FROM python:3.7

# Copy requirements.txt and install Python requirements
COPY requirements.txt .
RUN python -m pip install pip-tools && pip-sync

# Copy the app and static files into the container
COPY application.py .
COPY app/ ./app
COPY static/ ./static
COPY templates/ ./templates

# Run Flask
ENV FLASK_APP="application.py"
CMD [ "flask" , "run","--host=0.0.0.0" ]