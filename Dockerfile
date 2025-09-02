FROM python:3.14-rc-alpine3.21

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir gunicorn  # Ensure gunicorn is installed

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Use a lightweight production server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]