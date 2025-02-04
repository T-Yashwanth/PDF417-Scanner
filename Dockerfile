# Use an official Python slim base image.
FROM python:3.9-slim

# Install Java (OpenJDK) and any other necessary system packages.
RUN apt-get update && \
    apt-get install -y default-jre && \
    rm -rf /var/lib/apt/lists/*

# Set a working directory inside the container.
WORKDIR /app

# Copy the rest of your application code into the container.
COPY . .
# Copy the requirements file and the setup.py file for your local package
#COPY requirements.txt setup.py src/ ./

# Optionally, copy any other files needed for installation here if required
# COPY other_required_file ./

# Install the Python dependencies (now installation will find setup.py)
RUN pip install --no-cache-dir -r requirements.txt



# Expose the port that will be used by your hosting environment.
EXPOSE ${PORT}

# Run Gunicorn to serve your Flask application.
#CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "wsgi:app"]
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} wsgi:app"