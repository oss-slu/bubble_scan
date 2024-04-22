# Stage 2: Build Flask Application
FROM python:latest AS flask-builder

WORKDIR /app/flask

# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask

# Debugging: List contents of /app/flask directory
RUN ls -la /app/flask

# Continue building the image
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt"

# Uninstall PyMuPDF if it's already installed
RUN pip uninstall -y PyMuPDF

# Install PyMuPDF
RUN pip install PyMuPDF

# Stage 3: Final Image
FROM python:latest

WORKDIR /app

# Copy built Flask app from previous stage
COPY --from=flask-builder /app/flask /app

# Expose ports
EXPOSE 5001 5713

# Run Flask app
CMD ["./venv/bin/python", "AppServer.py"]