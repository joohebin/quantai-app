/**
 * QuantAI Electron 预加载脚本
 * 安全地暴露 Node.js API 到渲染进程
 */
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // 获取 API 地址
  getApiBase: () => ipcRenderer.invoke('get-api-base'),

  // 获取版本
  getVersion: () => ipcRenderer.invoke('get-version'),

  // 显示原生通知
  showNotification: (title, body) => ipcRenderer.send('show-notification', { title, body }),

  // 保存文件
  saveFile: (defaultPath, content) => ipcRenderer.invoke('save-file', { defaultPath, content }),

  // 打开外部链接
  openExternal: (url) => ipcRenderer.send('open-external', url),

  // 监听菜单导航事件
  onMenuNav: (callback) => ipcRenderer.on('menu-nav', (_e, page) => callback(page)),

  // 监听紧急平仓
  onEmergencyCloseAll: (callback) => ipcRenderer.on('emergency-close-all', callback),

  // 监听更新通知
  onUpdateAvailable: (callback) => ipcRenderer.on('update-available', callback),
  onUpdateDownloaded: (callback) => ipcRenderer.on('update-downloaded', callback),
  installUpdate: () => ipcRenderer.send('install-update'),

  // 平台信息
  platform: process.platform,
  isElectron: true,
});
