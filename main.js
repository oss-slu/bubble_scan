const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let flaskProcess;

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
        },
    });
    win.loadURL('http://127.0.0.1:5000');  // Flask server URL
}

app.whenReady().then(() => {
    // Start Flask server as a subprocess
    flaskProcess = spawn('python', ['ServerCode/application/AppServer.py']);  

    flaskProcess.stdout.on('data', (data) => {
        console.log(`Flask: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`Flask error: ${data}`);
    });

    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Ensure Flask process is killed when Electron quits
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        if (flaskProcess) flaskProcess.kill();
        app.quit();
    }
});
