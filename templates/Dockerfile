# Use official Python image
FROM python:3.13-slim

WORKDIR /app

COPY . /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Default command (can be overridden)
CMD ["python", "app.py"]