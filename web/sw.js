// Keeps the clock running when the network drops. Only active over https or on localhost.
// The Pages workflow replaces CACHE with a per-commit name, so devices pick up new versions.
var CACHE = 'litclock-v1';
var FILES = [
  './',
  'index.html',
  'quotes.js',
  'fonts/LinLibertine_Rah.ttf',
  'fonts/LinLibertine_RBah.ttf',
  'fonts/LinLibertine_RIah.ttf'
];

self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) { return cache.addAll(FILES); }));
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; })
      .map(function (k) { return caches.delete(k); }));
  }));
});

// network first, so updates show up; fall back to the cache when offline
self.addEventListener('fetch', function (event) {
  event.respondWith(
    fetch(event.request).then(function (response) {
      var copy = response.clone();
      caches.open(CACHE).then(function (cache) { cache.put(event.request, copy); });
      return response;
    }).catch(function () {
      return caches.match(event.request);
    })
  );
});
