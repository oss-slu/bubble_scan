# How to run Dockerfiles

1. Make sure you are in the bubble_scan base directory
```
cd bubble_scan
```
2. Open docker and make sure it is open when running the Dockerfiles
3. Type this command into the git terminal

```
docker-compose up --build
```
4. Check Docker window to see bubble_scan container
5. Start up the program and click on the server to see the results

# Server Dockerfile Configuration

Set a working directory inside the container called /app
```
WORKDIR /app
```
Used pip to install the dependencies inside 'requirements.txt'
```
RUN pip install Flask
RUN pip install -r mockapp/requirements.txt
```
Exposed port 5000 for the Flask server
```
EXPOSE 5000
```
Defined environment variables to specify entry point
```
ENV FLASK_APP=application/AppServer.py
ENV FLASK_RUN_HOST=0.0.0.0
```
Configured the container to run the Flask application
```
CMD ["flask", "run"]
```

# Client Dockerfile Configuration
Set another working directory for the client
```
WORKDIR /app
```
Installed the dependencies 
```
RUN npm install
```
Ran a build script to compile the code
```
RUN npm run build
```
Used a multi-stage build where the final stage started with an Nginx base image to serve the static files efficiently
```
FROM nginx:alpine as production-stage
```
Copied the output of the build process into Nginx's serving directory
```
COPY --from=build-stage /app/dist /usr/share/nginx/html
```
Exposed port 80
```
EXPOSE 80
```
Configured Nginx to start when the container boots
```
CMD ["nginx", "-g", "daemon off;"]
```
# Handling Multi-Platform Issues
To make sure the dependencies were compatable across different platforms, 'node_modules' is rebuilt inside the Docker container

# Docker Compose
The docker-compose.yml file configured port mappings for both the server and client to allow local access


