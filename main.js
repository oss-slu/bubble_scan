const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

function createWindow() {
    try {
        mainWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: true,
            },
        });
        mainWindow.loadURL('http://127.0.0.1:5000');
    } catch (error) {
        console.error("Failed to create window:", error);
    }
}


app.whenReady().then(() => {
    // Start the Flask server as a subprocess
    flaskProcess = spawn('python', ['ServerCode/application/AppServer.py']); 

    flaskProcess.stdout.on('data', (data) => {
        console.log(`Flask: ${data}`);
        if (data.toString().includes("Running on http://127.0.0.1:5000")) {
            // Only create the Electron window once Flask confirms it's running
            createWindow();
        }
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`Flask error: ${data}`);
    });

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            if (flaskProcess) flaskProcess.kill();
            app.quit();
        }
    });
});

