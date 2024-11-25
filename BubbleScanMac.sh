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

# Step 5: Install dependencies with robust error handling
echo "Installing dependencies with robust error handling..."

# Upgrade pip and essential tools
pip install --upgrade pip setuptools wheel

# Iterate over each package in requirements.txt and install it individually
while read -r package || [[ -n "$package" ]]; do
    echo "Installing $package..."
    pip install "$package" --no-cache-dir || echo "Failed to install $package. Continuing with the next package..."
done < requirements.txt

# Install additional tools like PyInstaller
echo "Installing PyInstaller and checking additional packages..."
pip install pyinstaller --no-cache-dir

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
