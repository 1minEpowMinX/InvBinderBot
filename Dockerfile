FROM python:3.12.10-slim

# Update the package list and install any necessary dependencies
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	build-essential \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY config/ /app/config/
COPY fsm/ /app/fsm/
COPY keyboards/ /app/keyboards/
COPY lexicon/ /app/lexicon/
COPY middlewares/ /app/middlewares/
COPY routers/ /app/routers/
COPY services/ /app/services/
COPY utils/ /app/utils/
COPY main.py .

# Make sure the entrypoint script is executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]
