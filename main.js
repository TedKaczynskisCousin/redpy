const { app, BrowserWindow, session } = require('electron')
const path = require('path')

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })
  mainWindow.webContents.session.enableNetworkEmulation({ offline: true })
  mainWindow.loadURL('https://www.meter.net/ping-test/')

  // mainWindow.webContents.openDevTools()
}



app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit 
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})


// code.