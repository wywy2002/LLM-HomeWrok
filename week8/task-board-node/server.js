const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3001;
const BASE_DIR = __dirname;
const DATA_DIR = path.join(BASE_DIR, 'data');
const DATA_FILE = path.join(DATA_DIR, 'tasks.json');
const HTML_FILE = path.join(BASE_DIR, 'index.html');

function ensureStore() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, JSON.stringify({ nextId: 1, tasks: [] }, null, 2));
}

function readStore() {
  ensureStore();
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
}

function writeStore(store) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(store, null, 2));
}

function sendJson(res, status, payload) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(payload));
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(HTML_FILE, 'utf8'));
    return;
  }

  if (url.pathname === '/api/tasks' && req.method === 'GET') {
    const store = readStore();
    sendJson(res, 200, store.tasks);
    return;
  }

  if (url.pathname === '/api/tasks' && req.method === 'POST') {
    const payload = await parseBody(req);
    if (!payload.title || !String(payload.title).trim()) {
      sendJson(res, 400, { error: 'title is required' });
      return;
    }
    const store = readStore();
    const task = {
      id: store.nextId++,
      title: String(payload.title).trim(),
      details: String(payload.details || '').trim(),
      completed: false,
    };
    store.tasks.unshift(task);
    writeStore(store);
    sendJson(res, 201, task);
    return;
  }

  if (url.pathname.startsWith('/api/tasks/')) {
    const id = Number(url.pathname.split('/').pop());
    const store = readStore();
    const index = store.tasks.findIndex((task) => task.id === id);
    if (index === -1) {
      sendJson(res, 404, { error: 'task not found' });
      return;
    }

    if (req.method === 'PUT') {
      const payload = await parseBody(req);
      if (!payload.title || !String(payload.title).trim()) {
        sendJson(res, 400, { error: 'title is required' });
        return;
      }
      store.tasks[index] = {
        id,
        title: String(payload.title).trim(),
        details: String(payload.details || '').trim(),
        completed: Boolean(payload.completed),
      };
      writeStore(store);
      sendJson(res, 200, store.tasks[index]);
      return;
    }

    if (req.method === 'DELETE') {
      store.tasks.splice(index, 1);
      writeStore(store);
      res.writeHead(204);
      res.end();
      return;
    }
  }

  sendJson(res, 404, { error: 'not found' });
});

server.listen(PORT, () => {
  console.log(`Task Board Node server running at http://127.0.0.1:${PORT}`);
});
