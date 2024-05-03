FROM nikolaik/python-nodejs:latest

WORKDIR /app

# Stage 1: Build Flask Application
# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3-venv libgl1-mesa-glx \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y poppler-utils && apt-get install -y supervisor
RUN npm install -g npm

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask
# Install npm dependencies
RUN /bin/bash -c "pip install --upgrade pip \
    && pip install -r /app/flask/requirements.txt \
    && pip install gunicorn"

COPY bubblescan-client /app
RUN npm install
RUN npm install cors

#COPY service_script.conf /app

# Expose ports
EXPOSE 5173
EXPOSE 5001

#RUN gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app&

# Stage 2: Build React Application
# Copy package.json and package-lock.json for npm install



# Install npm cors

# Copy the React application code into the image


# Start React Vite development server
CMD gunicorn --bind localhost:5001 --chdir flask AppServer:app --daemon & npm run dev --network=host 
#CMD npm run dev

#CMD ["supervisord","-c","/app/service_script.conf"]
