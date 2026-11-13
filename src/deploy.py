d='aura3/'; s=open(d+'aura-demo.html').read()
i=s.index('<div class="bgwash"')
head=s[:i].replace('<meta charset="utf-8">\n','').replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
body=s[i:]
top='''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#FCF0EC">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="AURĀ">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<script>window.AURA_APP = true;</script>
'''
open('deploy/aura/index.html','w').write(top+head+'</head>\n<body>\n'+body+'\n</body>\n</html>\n')
open('deploy/aura/manifest.webmanifest','w').write('''{
  "name": "AURĀ · Aromaterapia botánica",
  "short_name": "AURĀ",
  "description": "Demo de AURĀ: aceites esenciales, biblioteca 3D, rituales, conocimiento botánico y Olia.",
  "lang": "es",
  "start_url": "./#inicio",
  "scope": "./",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#FCF0EC",
  "theme_color": "#FCF0EC",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
open('deploy/aura/sw.js','w').write('''/* AURĀ · funcionamiento sin conexión. Cambia VERSION cada vez que subas una nueva index.html. */
const VERSION = 'aura-v14';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).then(res => { const cp = res.clone(); caches.open(VERSION).then(c => c.put('./index.html', cp)); return res; }).catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(r).then(hit => {
    const net = fetch(r).then(res => { if (res.ok || res.type === 'opaque') { const cp = res.clone(); caches.open(VERSION).then(c => c.put(r, cp)); } return res; }).catch(() => hit);
    return hit || net;
  }));
});
''')
