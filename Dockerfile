FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libicu-dev \
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies including Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Alternatively, install Gunicorn directly here if not in requirements.txt
RUN pip install gunicorn

# Expose port 8000 for Gunicorn (as it's serving on 8000)
EXPOSE 8000

# Define environment variable for Python to run in unbuffered mode (helpful for logging)
ENV PYTHONUNBUFFERED=1

# Default command is defined in docker-compose.yml
CMD ["gunicorn", "your_module_name:app", "--bind", "0.0.0.0:8000"]
