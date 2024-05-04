FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
 nodejs \
 npm \
 curl \
 wget \
 poppler-utils

# Stage 1: Build Flask Application
# Install system dependencies
#RUN apt-get update \
#    && apt-get install -y nodejs \
#    && apt-get install -y npm \
#    && apt-get install -y python3 libgl1-mesa-glx \
#    && apt-get install -y poppler-utils

#    && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y poppler-utils && apt-get install -y supervisor

RUN npm install -g npm

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask

# Install npm dependencies
RUN pip install -r /app/flask/requirements.txt
RUN pip install gunicorn

COPY bubblescan-client /app
RUN npm install
RUN npm install cors

#COPY service_script.conf /app

# Expose ports
EXPOSE 5001
EXPOSE 5173

CMD gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app --daemon & npm run dev 

#CMD ["supervisord","-c","/app/service_script.conf"]
