# Use the official Python image from the Docker Hub
FROM --platform=linux/amd64 python:3.10.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 80 for the Flask application
EXPOSE 80

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application in production mode on port 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]