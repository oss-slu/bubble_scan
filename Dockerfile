FROM --platform=linux/arm64 nikolaik/python-nodejs:python3.12-nodejs22

WORKDIR /app

# Stage 1: Build Flask Application
# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3-venv libgl1-mesa-glx \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Poppler
#RUN apt-get update && apt-get install -y poppler-utils

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask

# Debugging: List contents of /app/flask directory
RUN ls -la /app/flask

RUN /bin/bash -c "pip install --upgrade pip \
    && pip install -r /app/flask/requirements.txt \
    && pip install gunicorn"

# Expose ports
EXPOSE 5001

#RUN gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app&

# Stage 2: Build React Application
# Copy package.json and package-lock.json for npm install
COPY bubblescan-client/package*.json /app

# Install npm dependencies
RUN npm install

# Update npm
RUN npm install -g npm

# Install npm cors
RUN npm install cors

# Copy the React application code into the image
COPY bubblescan-client /app

# Expose port for React Vite development server
EXPOSE 5173

# Start React Vite development server
#CMD ["npm", "run", "dev"]

CMD gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app & npm run dev
#CMD npm run dev