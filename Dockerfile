# ─────────────────────────────────────────────────────────────
# Finovo Backend — Production Dockerfile
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc and enable unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# ─── Build stage: install Python deps ─────────────────────
FROM base AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─── Runtime stage ────────────────────────────────────────
FROM base AS runtime

# Create a non-root user
RUN groupadd -r finovo && useradd -r -g finovo -d /app -s /sbin/nologin finovo

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Collect static files (uses whitenoise in production)
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Fix permissions
RUN chown -R finovo:finovo /app

USER finovo

# Expose Gunicorn port
EXPOSE 8000

# Health check — ALB also does its own but this helps Docker orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/')" || exit 1

# Start Gunicorn with the config file
CMD ["gunicorn", "core.wsgi:application", "--config", "gunicorn.conf.py"]
