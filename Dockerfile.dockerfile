# syntax=docker/dockerfile:1
FROM python:3.7-alpine

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements.txt file and install Python packages
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files into the container
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the Flask application port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run"]
