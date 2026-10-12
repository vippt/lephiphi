const CACHE_NAME = 'baocao-v1';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

// Bắt buộc phải có listener fetch để trình duyệt công nhận SW hợp lệ
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
