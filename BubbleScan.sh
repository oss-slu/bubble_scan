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
python3 -m venv venv  # Use python3 for virtual environment creation in bash

# Check if running on Windows or Linux/macOS and activate environment accordingly
if [[ -f "venv/bin/activate" ]]; then
    # Linux/macOS
    source venv/bin/activate
elif [[ -f "venv/Scripts/activate" ]]; then
    # Windows
    source venv/Scripts/activate
else
    echo "Failed to find the activate script for the virtual environment."
    exit 1
fi

# Uninstall pathlib if it exists in the virtual environment
echo "Checking for and uninstalling pathlib package..."
pip uninstall -y pathlib 2>/dev/null || echo "pathlib was not found, skipping."

# Install dependencies from requirements.txt while ensuring pathlib is not reinstalled
pip install --no-cache-dir -r requirements.txt

# Check again to ensure pathlib is uninstalled
pip uninstall -y pathlib 2>/dev/null || echo "pathlib was not reinstalled."

# Run PyInstaller
pyinstaller --onefile \
    --paths=./ \
    --add-data "BubbleScan_AI:BubbleScan_AI" \
    --add-data "application:application" \
    --add-data "application/static:static" \
    --hidden-import=fitz \
    application/AppServer.py


# Deactivate the virtual environment
deactivate

# Go back to main directory and copy static files to dist directory
cd ..
mkdir -p ServerCode/dist  # Ensure dist directory exists
cp -r ServerCode/application/static ServerCode/dist
