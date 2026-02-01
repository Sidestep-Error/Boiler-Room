# ==== Build ====
FROM python:3.11-alpine AS builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# ==== Runtime ====
FROM python:3.11-alpine

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy app code from builder stage
COPY --from=builder /app .

# Expose the port
EXPOSE 8080

# Create non-root user
RUN adduser -D appuser
USER appuser

# Command to run the app
CMD ["python", "app.py"]

