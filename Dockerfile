# Gunakan image python resmi sebagai base image
FROM python:3.9-slim

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Buat direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt ke direktori kerja di dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh isi direktori kerja lokal ke direktori kerja di dalam container
COPY . /app/

# Perintah untuk menjalankan aplikasi
CMD ["python", "kuso.py"]
