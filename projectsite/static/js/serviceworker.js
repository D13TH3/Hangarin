self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('projectsite-cache-v1').then(function(cache) {
          return cache.addAll([
               '/',
               '/static/css/bootstrap.min.css',
               '/static/css/fontawesome.min.css',
               '/static/css/custom.css', 
               '/static/js/custom.js',
              
        
            ]);
        })
    );
});
self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
           return response || fetch(e.request);
        })
    );
});