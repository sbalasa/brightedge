# Base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the working directory
COPY . .

# Change the working directory to brightedge
WORKDIR /app/brightedge

# Run the spider and format the output file
CMD scrapy crawl brightedge -o output.json && black -l 80 output.json && cat output.json
