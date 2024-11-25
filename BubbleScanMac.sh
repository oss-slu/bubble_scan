#!/bin/bash

# macOS-specific build script for BubbleScan

# Step 1: Create the static directory
mkdir -p ServerCode/application/static

# Step 2: Build the frontend
echo "Building frontend..."
cd bubblescan-client
npm install
npm run build
cp -r dist/* ../ServerCode/application/static/

# Step 3: Return to the ServerCode directory
cd ..
cd ServerCode

# Step 4: Set up and activate Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv

# Activate the virtual environment
if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
else
    echo "Failed to activate the virtual environment. Exiting..."
    exit 1
fi

# Step 5: Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip uninstall -y pathlib 2>/dev/null || echo "pathlib was not found, skipping."
pip install --no-cache-dir -r requirements.txt
pip install pyinstaller

# Step 6: Build macOS binary
echo "Building macOS binary with PyInstaller..."
pyinstaller --onefile --name BubbleScan-macOS \
    --add-data "application/static:static" \
    --hidden-import=fitz application/AppServer.py

# Step 7: Deactivate the virtual environment
deactivate

# Step 8: Copy static files to dist directory
echo "Copying static files to dist directory..."
cd ..
mkdir -p ServerCode/dist
cp -r ServerCode/application/static ServerCode/dist

# Step 9: Verify build outputs
echo "Build outputs:"
ls -l ServerCode/dist

echo "macOS build script completed successfully!"
