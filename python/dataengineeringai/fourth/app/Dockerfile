
# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY . .

# Expose the Flask server port
EXPOSE 5000

# Start the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
