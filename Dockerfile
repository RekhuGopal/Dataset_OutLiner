# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY stock_price_outlier_detection.py stock_price_outlier_detection.py

# Set the entry point for the Docker container
ENTRYPOINT ["python", "stock_price_outlier_detection.py"]

# Define default arguments for the script
CMD ["data", "output", "--num_files", "1"]