# Stage 2: Build Flask Application
FROM python:latest AS flask-builder

WORKDIR /app/flask

# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3-venv libgl1-mesa-glx \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Poppler
RUN apt-get update && apt-get install -y poppler-utils

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask

# Debugging: List contents of /app/flask directory
RUN ls -la /app/flask

# Delete existing venv
RUN rm -rf venv

# Continue building the image
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt"

# Reinstall requirements without cache
RUN pip uninstall -y -r requirements.txt && pip install -r requirements.txt --no-cache-dir

# Stage 3: Final Image
FROM python:latest

WORKDIR /app

# Install libgl1-mesa-glx
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy built Flask app from previous stage
COPY --from=flask-builder /app/flask /app

# Expose ports
EXPOSE 5001

# Run Flask app
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && /app/venv/bin/python /app/AppServer.py"]