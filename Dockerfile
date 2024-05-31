FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
 nodejs \
 npm \
 curl \
 wget \
 poppler-utils

RUN npm install -g npm

# Copy the Flask application code into the image
COPY ServerCode/application /app/flask
# Install npm dependencies
RUN pip install -r /app/flask/requirements.txt
RUN pip install gunicorn

COPY bubblescan-client /app
RUN npm install
RUN npm install cors

RUN npm run build
RUN cp -r dist/ flask/static/
#COPY dist flask/static

# Expose ports
EXPOSE 5001

CMD gunicorn --bind 0.0.0.0:5001 --chdir flask AppServer:app & npm run dev

#CMD ["supervisord","-c","/app/service_script.conf"]