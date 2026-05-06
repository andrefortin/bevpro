#!/usr/bin/env node
// screenshot.js <site_dir> <output_path>
// Screenshots a generated FieldLaunch site (serves dist/ via temp HTTP server)

const path = require('path');
const fs = require('fs');
const http = require('http');
const { execSync } = require('child_process');

const siteDir = process.argv[2];
const outputPath = process.argv[3];

if (!siteDir || !outputPath) {
  console.error('Usage: node screenshot.js <site_dir> <output_path>');
  process.exit(1);
}

// Prefer dist/ (built), fall back to root index.html
const distDir = path.join(siteDir, 'dist');
const serveDir = fs.existsSync(path.join(distDir, 'index.html')) ? distDir : siteDir;

const puppeteerPath = path.resolve(__dirname, '../../app/node_modules/puppeteer');
const puppeteer = require(puppeteerPath);

function findFreePort() {
  return new Promise((resolve, reject) => {
    const srv = http.createServer();
    srv.listen(0, '127.0.0.1', () => {
      const port = srv.address().port;
      srv.close(() => resolve(port));
    });
    srv.on('error', reject);
  });
}

function startServer(dir, port) {
  // Use Python's http.server — universally available
  const { spawn } = require('child_process');
  const proc = spawn('python3', ['-m', 'http.server', String(port), '--directory', dir], {
    stdio: 'pipe',
    detached: false,
  });
  return proc;
}

(async () => {
  const port = await findFreePort();
  const server = startServer(serveDir, port);

  // Wait for server to be ready
  await new Promise(r => setTimeout(r, 800));

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
    headless: 'new',
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'networkidle0', timeout: 20000 });
    // Wait for React to paint
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({
      path: outputPath,
      type: 'jpeg',
      quality: 82,
      clip: { x: 0, y: 0, width: 1280, height: 900 },
    });
    console.log(outputPath);
  } finally {
    await browser.close();
    server.kill();
  }
})().catch(e => {
  console.error('screenshot failed:', e.message);
  process.exit(1);
});
