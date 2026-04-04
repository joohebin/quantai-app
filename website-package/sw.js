// QuantAI Service Worker - PWA 离线缓存
const CACHE_NAME = 'quantai-v3';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json'
];

// 安装：预缓存核心资源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// 请求拦截：网络优先，降级走缓存
self.addEventListener('fetch', event => {
  // API 请求不走缓存
  if (event.request.url.includes('/api/')) return;

  event.respondWith(
    fetch(event.request)
      .then(resp => {
        // 更新缓存
        const clone = resp.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return resp;
      })
      .catch(() => caches.match(event.request))
  );
});
