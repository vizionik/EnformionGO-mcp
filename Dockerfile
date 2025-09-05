# Use a slim Python base image
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN /bin/bash -c "uv pip install --system -r <(uv pip compile pyproject.toml --output-file=-)"

# --- Final Stage ---
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
