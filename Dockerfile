# Python image
FROM python:3.12-slim


# Install FFmpeg and system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project
COPY . .

# RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 
EXPOSE 8000

# Run on Gunicorn
CMD ["gunicorn", "transcodenexus.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]