/**
 * QuantAI Electron 主进程
 * Windows + macOS 桌面客户端
 */
const { app, BrowserWindow, Menu, shell, ipcMain, dialog, Tray, nativeImage } = require('electron');
const path = require('path');
const { autoUpdater } = require('electron-updater');

// ─────────── 配置 ───────────
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
const API_BASE = process.env.QUANTAI_API || 'http://localhost:8000';

let mainWindow = null;
let tray = null;

// ─────────── 防止多实例 ───────────
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

// ─────────── 创建主窗口 ───────────
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    title: 'QuantAI - 智能量化交易',
    backgroundColor: '#0a0e1a',
    show: false,   // 先隐藏，加载完再显示
    frame: true,
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: !isDev,   // 开发模式关闭安全策略，方便调试
    },
    icon: getIcon(),
  });

  // 加载前端
  const frontendPath = path.join(__dirname, '..', '..', 'index.html');
  mainWindow.loadFile(frontendPath);

  // 加载完成后显示窗口（避免白屏闪烁）
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDev) {
      mainWindow.webContents.openDevTools({ mode: 'detach' });
    }
  });

  // 拦截外部链接，在系统浏览器中打开
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  mainWindow.on('close', (e) => {
    if (process.platform === 'darwin') {
      // macOS: 关闭窗口不退出 app
      if (!app.isQuitting) {
        e.preventDefault();
        mainWindow.hide();
      }
    }
  });

  mainWindow.on('closed', () => { mainWindow = null; });
}

// ─────────── 托盘图标 ───────────
function createTray() {
  const iconPath = getIcon();
  tray = new Tray(nativeImage.createFromPath(iconPath));
  tray.setToolTip('QuantAI 量化交易');
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: '打开 QuantAI', click: () => { mainWindow?.show(); mainWindow?.focus(); } },
    { label: 'API 状态', click: () => shell.openExternal(`${API_BASE}/health`) },
    { type: 'separator' },
    { label: '退出', click: () => { app.isQuitting = true; app.quit(); } }
  ]));
  tray.on('double-click', () => { mainWindow?.show(); mainWindow?.focus(); });
}

// ─────────── 菜单 ───────────
function buildMenu() {
  const isMac = process.platform === 'darwin';
  const template = [
    ...(isMac ? [{
      label: 'QuantAI',
      submenu: [
        { role: 'about', label: '关于 QuantAI' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide', label: '隐藏 QuantAI' },
        { role: 'hideOthers', label: '隐藏其他' },
        { type: 'separator' },
        { role: 'quit', label: '退出 QuantAI' }
      ]
    }] : []),
    {
      label: '文件',
      submenu: [
        {
          label: '导出报告',
          accelerator: 'CmdOrCtrl+E',
          click: () => mainWindow?.webContents.send('menu-export-report')
        },
        { type: 'separator' },
        isMac ? { role: 'close', label: '关闭窗口' } : { role: 'quit', label: '退出' }
      ]
    },
    {
      label: '查看',
      submenu: [
        { role: 'reload', label: '刷新' },
        { role: 'forceReload', label: '强制刷新' },
        { type: 'separator' },
        { role: 'resetZoom', label: '重置缩放' },
        { role: 'zoomIn', label: '放大', accelerator: 'CmdOrCtrl+=' },
        { role: 'zoomOut', label: '缩小' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: '全屏' },
        ...(isDev ? [
          { type: 'separator' },
          { role: 'toggleDevTools', label: '开发者工具' }
        ] : [])
      ]
    },
    {
      label: '交易',
      submenu: [
        {
          label: '行情大屏',
          accelerator: 'CmdOrCtrl+1',
          click: () => mainWindow?.webContents.send('menu-nav', 'market')
        },
        {
          label: 'AI 助手',
          accelerator: 'CmdOrCtrl+2',
          click: () => mainWindow?.webContents.send('menu-nav', 'ai')
        },
        {
          label: '持仓管理',
          accelerator: 'CmdOrCtrl+3',
          click: () => mainWindow?.webContents.send('menu-nav', 'positions')
        },
        {
          label: '策略中心',
          accelerator: 'CmdOrCtrl+4',
          click: () => mainWindow?.webContents.send('menu-nav', 'strategies')
        },
        { type: 'separator' },
        {
          label: '紧急全部平仓',
          accelerator: 'CmdOrCtrl+Shift+X',
          click: async () => {
            const { response } = await dialog.showMessageBox(mainWindow, {
              type: 'warning',
              buttons: ['取消', '确认全部平仓'],
              defaultId: 0,
              cancelId: 0,
              title: '紧急平仓确认',
              message: '⚠️ 确定要一键平掉所有持仓吗？',
              detail: '此操作不可撤销，将按市价平掉所有当前持仓。'
            });
            if (response === 1) mainWindow?.webContents.send('emergency-close-all');
          }
        }
      ]
    },
    {
      label: '帮助',
      submenu: [
        {
          label: 'API 文档',
          click: () => shell.openExternal(`${API_BASE}/docs`)
        },
        {
          label: '检查更新',
          click: () => autoUpdater.checkForUpdatesAndNotify()
        },
        { type: 'separator' },
        {
          label: '关于 QuantAI',
          click: async () => {
            await dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: '关于 QuantAI',
              message: 'QuantAI 量化交易平台',
              detail: `版本：${app.getVersion()}\nPowered by AI\n© 2026 QuantAI`,
              buttons: ['确定']
            });
          }
        }
      ]
    }
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

// ─────────── IPC 消息处理 ───────────
function setupIPC() {
  // 获取 API 地址
  ipcMain.handle('get-api-base', () => API_BASE);

  // 获取 App 版本
  ipcMain.handle('get-version', () => app.getVersion());

  // 原生通知
  ipcMain.on('show-notification', (_event, { title, body }) => {
    const { Notification } = require('electron');
    new Notification({ title, body }).show();
  });

  // 下载/保存文件
  ipcMain.handle('save-file', async (_event, { defaultPath, content }) => {
    const { filePath } = await dialog.showSaveDialog(mainWindow, {
      defaultPath,
      filters: [{ name: 'CSV Files', extensions: ['csv'] }, { name: 'All Files', extensions: ['*'] }]
    });
    if (filePath) {
      const fs = require('fs');
      fs.writeFileSync(filePath, content, 'utf8');
      return { success: true, path: filePath };
    }
    return { success: false };
  });

  // 打开外部链接
  ipcMain.on('open-external', (_event, url) => shell.openExternal(url));
}

// ─────────── 工具函数 ───────────
function getIcon() {
  const assetsDir = path.join(__dirname, '..', 'assets');
  if (process.platform === 'win32') return path.join(assetsDir, 'icon.ico');
  if (process.platform === 'darwin') return path.join(assetsDir, 'icon.icns');
  return path.join(assetsDir, 'icon.png');
}

// ─────────── App 生命周期 ───────────
app.whenReady().then(async () => {
  buildMenu();
  createMainWindow();
  createTray();
  setupIPC();

  // macOS: 点击 Dock 图标重新显示窗口
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    } else {
      mainWindow?.show();
    }
  });

  // 生产环境自动检查更新
  if (!isDev) {
    autoUpdater.checkForUpdatesAndNotify();
  }
});

app.on('window-all-closed', () => {
  // macOS 不关闭进程
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  app.isQuitting = true;
});

// 更新事件
autoUpdater.on('update-available', () => {
  mainWindow?.webContents.send('update-available');
});

autoUpdater.on('update-downloaded', () => {
  mainWindow?.webContents.send('update-downloaded');
});

ipcMain.on('install-update', () => {
  autoUpdater.quitAndInstall();
});
