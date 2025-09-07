# ===== Продакшен базовый образ =====
FROM python:3.12.10-slim AS base

# Update packages and install build dependencies
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	build-essential \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY config/ /app/config/
COPY fsm/ /app/fsm/
COPY keyboards/ /app/keyboards/
COPY lexicon/ /app/lexicon/
COPY middlewares/ /app/middlewares/
COPY routers/ /app/routers/
COPY services/ /app/services/
COPY utils/ /app/utils/
COPY main.py .

# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Test stage
FROM base AS test-stage

# Install testing dependencies
RUN pip install --no-cache-dir pytest pytest-asyncio

# Launch tests
CMD ["pytest"]
