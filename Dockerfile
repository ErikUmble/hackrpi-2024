# Use the official Python image with a specific version
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disk
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current directory to the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port 9000 for the Flask app
EXPOSE 9000

ENV GOOGLE_APPLICATION_CREDENTIALS=able-81a4e-e694abda18d2.json

# Command to run the Flask app
CMD ["python", "backend/server.py", "--host=0.0.0.0", "--port=9000"]