# --- Build Stage ---
FROM python:3.13-slim-bookworm AS builder

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy application files
COPY . .

# --- Final Stage ---
FROM python:3.13-slim-bookworm

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd --create-home appuser

# Copy installed dependencies from builder stage
COPY --from=builder /app /app

# Add the venv to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Change ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]