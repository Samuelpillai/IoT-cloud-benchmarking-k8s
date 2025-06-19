# Use Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the pythin script into the container
COPY load_generator.py /app/

# Install required Python dependencies
RUN pip install --no-cache-dir requests

# Expose a port
EXPOSE 30000

# Set environment variable for default port
ENV TARGET_PORT="http://localhost:30000/primecheck"
ENV FREQUENCY=1

# Command to run the load generator script
CMD ["python", "load_generator.py"]