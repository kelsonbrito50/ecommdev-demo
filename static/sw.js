/**
 * ECOMMDEV Service Worker
 * Strategy:
 *   - Static assets  → Cache-First (serve from cache, update in background)
 *   - API routes     → Network-First (fresh data, fallback to cache)
 *   - Everything else → Network-First with cache fallback
 */

const CACHE_VERSION = 'v1';
const STATIC_CACHE  = `ecommdev-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `ecommdev-dynamic-${CACHE_VERSION}`;

// Static assets to pre-cache on install
const PRECACHE_URLS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/img/logo.png',
  '/static/img/icon.png',
  '/offline/',
];

// URL prefixes that are considered API routes → Network-First
const API_PREFIXES = ['/api/', '/webhook/'];

// URL prefixes that are considered static assets → Cache-First
const STATIC_PREFIXES = ['/static/'];

// ─── Install ──────────────────────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      // Pre-cache critical assets; ignore failures (e.g. /offline/ may not exist yet)
      return Promise.allSettled(
        PRECACHE_URLS.map((url) => cache.add(url).catch(() => null))
      );
    })
  );
  // Activate the new SW immediately without waiting for old clients to close
  self.skipWaiting();
});

// ─── Activate ─────────────────────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== DYNAMIC_CACHE)
          .map((key) => caches.delete(key))
      )
    )
  );
  // Take control of all open clients immediately
  self.clients.claim();
});

// ─── Fetch ────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle same-origin GET requests
  if (request.method !== 'GET' || url.origin !== self.location.origin) {
    return; // Let the browser handle non-GET and cross-origin requests normally
  }

  const path = url.pathname;

  if (API_PREFIXES.some((prefix) => path.startsWith(prefix))) {
    // ── Network-First for API ────────────────────────────────────────────────
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
  } else if (STATIC_PREFIXES.some((prefix) => path.startsWith(prefix))) {
    // ── Cache-First for static assets ───────────────────────────────────────
    event.respondWith(cacheFirst(request, STATIC_CACHE));
  } else {
    // ── Network-First for HTML pages ────────────────────────────────────────
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
  }
});

// ─── Strategy: Cache-First ────────────────────────────────────────────────────
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) {
    // Serve from cache; revalidate in the background
    refreshCache(request, cacheName);
    return cached;
  }
  return fetchAndCache(request, cacheName);
}

// ─── Strategy: Network-First ──────────────────────────────────────────────────
async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    // Last resort: return a minimal offline response
    return new Response('Você está offline. Tente novamente mais tarde.', {
      status: 503,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────────────
async function fetchAndCache(request, cacheName) {
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
  }
  return response;
}

function refreshCache(request, cacheName) {
  fetch(request)
    .then((response) => {
      if (response.ok) {
        caches.open(cacheName).then((cache) => cache.put(request, response));
      }
    })
    .catch(() => {
      // Silently ignore background refresh failures
    });
}
