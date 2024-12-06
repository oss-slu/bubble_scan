#!/bin/bash

# Create the static directory
mkdir -p ServerCode/application/static

# Move to bubblescan-client directory and build frontend
cd bubblescan-client
npm install
npm run build
cp -r dist/* ../ServerCode/application/static/

# Go back to main directory, activate Python environment, and install dependencies
cd ..
cd ServerCode
python -m venv venv  # Use python3 for virtual environment creation in bash

source venv/bin/activate

echo "Checking for and uninstalling pathlib package..."
pip uninstall -y pathlib 2>/dev/null || echo "pathlib was not found, skipping."

pip install --no-cache-dir -r requirements.txt
pip install werkzeug
pip install flask
pip install pyinstaller
pip install opencv-python

pip uninstall -y pathlib 2>/dev/null || echo "pathlib was not reinstalled."

echo "Building macOS binary..."

CODESIGN=""
# Check if running in GitHub workflow
if [[ -n "$GITHUB_ACTIONS" ]]; then
    # Running in GitHub workflow
    security create-keychain -p actions build.keychain
    security default-keychain -s build.keychain
    security unlock-keychain -p actions build.keychain
    security set-keychain-settings -lut 3600 build.keychain

    echo "$MACOS_CERTIFICATE" | base64 --decode > certificate.p12
    security import certificate.p12 \
          -k build.keychain \
          -P "$MACOS_CERTIFICATE_PWD" \
          -T /usr/bin/codesign

    CODESIGN="--codesign-identity 'Developer ID Application: Ekaterina Holdener (V4Q7X7HV6L)'"
fi

pyinstaller --onefile $(CODESIGN) --windowed --name BubbleScan-macOS --add-data "application/static:static" --add-data "application/logging.conf:." --add-data "BubbleScan_AI:BubbleScan_AI" --hidden-import=cv2 --hidden-import=flask --hidden-import=werkzeug --hidden-import=fitz application/AppServer.py

# Deactivate the virtual environment
deactivate

# Go back to main directory and copy static files to dist directory
#cd ..
#mkdir -p ServerCode/dist  # Ensure dist directory exists
#cp -r ServerCode/application/static ServerCode/dist

# Verify build outputs
#echo "Build outputs:"
#ls -l ServerCode/dist
