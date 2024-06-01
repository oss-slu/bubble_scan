# How to run the Dockerfiles separately?
**This is to run the flask and react servers separately for testing purposes. We need to use the docker-compose yml file to run both components.**

**Also, make sure all the docker files are in the root directory. Render yml file is used to test the app public availability on the render website.**

### Prerequisites
You need to have the below files in the root directory:
- flask.Dockerfile
- react.Dockerfile
- docker-compose.yml

### Docker Compose Setup
1. Make sure you are in the bubble_scan base directory
```
cd bubble_scan
```
2. Open Docker and make sure it is open when running the Dockerfiles
3. Type the command below into the git terminal

```
docker-compose up --build
```
4. Check the Docker window to see the bubble_scan container
5. Start up the program and click on the server to see the results

### Handling Multi-Platform Issues
To make sure the dependencies were compatible across different platforms, 'node_modules' is rebuilt inside the Docker container

The docker-compose.yml file configured port mappings for the server and client to allow local access.

