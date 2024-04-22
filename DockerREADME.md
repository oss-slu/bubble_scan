# How to run Dockerfiles

1. Make sure you are in the bubble_scan base directory
```
cd bubble_scan
```
2. Open Docker and make sure it is open when running the Dockerfiles
3. Type this command into the git terminal

```
docker-compose up --build
```
4. Check the Docker window to see the bubble_scan container
5. Start up the program and click on the server to see the results

# Server Dockerfile Configuration

Set a working directory inside the container called /app
```
WORKDIR /app
```
Install system dependencies
```
RUN apt-get update \
    && apt-get install -y python3-venv libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
```
Exposed port 5001 for the Flask server
```
EXPOSE 5001
```
Copy the Flask application code into the image
```
COPY ServerCode/application /app/flask
Configured the container to run the Flask application
```
Run Flask app
```
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && /app/venv/bin/python /app/AppServer.py"]
```
# Client Dockerfile Configuration
Set another working directory for the client
```
WORKDIR /app
```
Copy package.json and package-lock.json for the npm install
```
COPY bubblescan-client/package*.json ./
```

Installed the dependencies 
```
RUN npm install
```
Copy the React application code into the image
```
COPY bubblescan-client .
```
Exposed port 5173
```
EXPOSE 5173
```
Start React Vite development server
```
CMD ["npm", "run", "dev"]
```
# Handling Multi-Platform Issues
To make sure the dependencies were compatible across different platforms, 'node_modules' is rebuilt inside the Docker container

# Docker Compose
The docker-compose.yml file configured port mappings for both the server and client to allow local access


