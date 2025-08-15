# -------------------------------
# messaging_app/Dockerfile
# -------------------------------

# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libpq-dev \
    libsystemd-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy project files
COPY . /app/

# 7. Expose port (default Django runs on 8000)
EXPOSE 8000

# 8. Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
