FROM nikolaik/python-nodejs:latest

WORKDIR /app

# Stage 1: Build Flask Application
# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3-venv libgl1-mesa-glx \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y poppler-utils && apt-get install -y supervisor

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask
#COPY bubblescan-client/package*.json /app
COPY bubblescan-client /app
COPY service_script.conf /app

# Install npm dependencies
RUN /bin/bash -c "pip install --upgrade pip \
    && pip install -r /app/flask/requirements.txt \
    && pip install gunicorn"

RUN npm install -g npm
RUN npm install
RUN npm install cors

# Expose ports
EXPOSE 5001
EXPOSE 5173

#RUN gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app&

# Stage 2: Build React Application
# Copy package.json and package-lock.json for npm install



# Install npm cors

# Copy the React application code into the image

# Expose port for React Vite development server

# Start React Vite development server
#CMD ["npm", "run", "dev"]

#CMD gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app & npm run dev
#CMD npm run dev

CMD ["supervisord","-c","/app/service_script.conf"]
