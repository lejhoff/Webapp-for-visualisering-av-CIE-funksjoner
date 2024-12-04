# Use the official python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application to the working directory
COPY . .

# Expose the port the app runs on inside the container
EXPOSE 8000

# Run the application
CMD ["sanic", "cieapi:api", "--host=0.0.0.0", "--port=8000", "--workers=4"]
