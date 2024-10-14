#!/bin/bash
# create a static directory in the application server
# front-end files will be placed there
mkdir -p ServerCode/application/static

# generate front-end files
cd bubblescan-client
npm run build

# copy front-end files to the application server
cp -r dist/* ../ServerCode/application/static

# start the app
cd ../ServerCode
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python application/AppServer.py
