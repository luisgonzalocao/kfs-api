# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to start FastAPI with Uvicorn
CMD ["uvicorn", "kfs.main:app", "--host", "0.0.0.0", "--port", "8000"]
