FROM python:3.12-slim  
WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set environment variables
ENV DATABASE_URL="postgresql+asyncpg://postgres:082004@34.50.80.190:5432/feedback"
ENV PYTHONUNBUFFERED=1  

# Copy application code
COPY . /app

# Expose the port
EXPOSE 8080

# Start the application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
