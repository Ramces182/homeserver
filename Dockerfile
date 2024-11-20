# Use Python as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files to the container
COPY . /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy the crontab file to the container
COPY crontab /etc/cron.d/email-cron

# Set permissions for the cron file
RUN chmod 0644 /etc/cron.d/email-cron

# Apply the cron job
RUN crontab /etc/cron.d/email-cron

# Make the script executable
RUN chmod +x /app/email.py

# Start cron in the foreground
CMD ["cron", "-f"]