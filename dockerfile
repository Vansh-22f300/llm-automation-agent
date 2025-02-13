# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy application files
COPY app.py /app/

# Install dependencies
RUN pip install flask requests

# Expose the API port
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
