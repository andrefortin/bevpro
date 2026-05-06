#!/usr/bin/env node
/**
 * ci-test.js — Regression test for a generated FieldLaunch site.
 * Usage: node ci-test.js <site_dir> [--base-url <url>]
 *
 * Checks:
 *  - index.html exists
 *  - window.SITE_CONFIG is present and parseable
 *  - Page title is set (not empty/placeholder)
 *  - Hero section renders (h1 or first heading visible)
 *  - No JS errors on load
 *  - Screenshot saved to <site_dir>/ci-screenshot.jpg
 *
 * Exits 0 on pass, 1 on failure. Prints JSON results to stdout.
 */

const path = require('path');
const fs = require('fs');
const http = require('http');
const { spawn } = require('child_process');

const args = process.argv.slice(2);
const siteDir = args[0];
const baseUrlFlag = args.indexOf('--base-url');
const baseUrl = baseUrlFlag !== -1 ? args[baseUrlFlag + 1] : null;

if (!siteDir) {
  console.error('Usage: node ci-test.js <site_dir> [--base-url <url>]');
  process.exit(1);
}

const puppeteerPath = path.resolve(__dirname, '../../app/node_modules/puppeteer');
const puppeteer = require(puppeteerPath);

function findFreePort() {
  return new Promise((resolve, reject) => {
    const srv = http.createServer();
    srv.listen(0, '127.0.0.1', () => { const p = srv.address().port; srv.close(() => resolve(p)); });
    srv.on('error', reject);
  });
}

const results = { passed: [], failed: [], screenshot: null };

function pass(name) { results.passed.push(name); }
function fail(name, reason) { results.failed.push({ name, reason }); }

(async () => {
  // Static checks
  const indexPath = path.join(siteDir, 'index.html');
  if (!fs.existsSync(indexPath)) {
    fail('index.html exists', 'File not found');
    console.log(JSON.stringify({ ...results, ok: false }));
    process.exit(1);
  }
  pass('index.html exists');

  const html = fs.readFileSync(indexPath, 'utf8');
  const hasConfig = /window\.SITE_CONFIG\s*=\s*\{/.test(html);
  if (hasConfig) pass('window.SITE_CONFIG present');
  else fail('window.SITE_CONFIG present', 'Not found in index.html');

  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  const titleText = titleMatch ? titleMatch[1].trim() : '';
  if (titleText && titleText !== 'FieldLaunch Site') pass('page title set');
  else fail('page title set', `Got: "${titleText}"`);

  // Browser checks
  const distDir = path.join(siteDir, 'dist');
  const serveDir = fs.existsSync(path.join(distDir, 'index.html')) ? distDir : siteDir;
  let serverProc = null;
  let siteUrl = baseUrl;

  if (!siteUrl) {
    const port = await findFreePort();
    serverProc = spawn('python3', ['-m', 'http.server', String(port), '--directory', serveDir], { stdio: 'pipe' });
    await new Promise(r => setTimeout(r, 800));
    siteUrl = `http://127.0.0.1:${port}/`;
  }

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
    headless: 'new',
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });

    const jsErrors = [];
    page.on('pageerror', e => jsErrors.push(e.message));
    page.on('console', msg => {
      if (msg.type() === 'error') jsErrors.push(msg.text());
    });

    await page.goto(siteUrl, { waitUntil: 'networkidle0', timeout: 20000 });
    await new Promise(r => setTimeout(r, 1200));

    // Check for heading
    const heading = await page.evaluate(() => {
      const h = document.querySelector('h1,h2,[class*="hero"] h2,[class*="headline"]');
      return h ? h.textContent?.trim() : null;
    });
    if (heading) pass(`heading visible: "${heading.slice(0, 60)}"`);
    else fail('heading visible', 'No h1/h2 found in rendered page');

    // Check for contact info
    const hasPhone = await page.evaluate(() => {
      return /\d{3}[-.\s]\d{3}[-.\s]\d{4}/.test(document.body.innerText);
    });
    if (hasPhone) pass('phone number visible');
    else fail('phone number visible', 'No phone pattern found');

    // JS errors
    const criticalErrors = jsErrors.filter(e =>
      !e.includes('favicon') && !e.includes('net::ERR') && !e.includes('Failed to load resource')
    );
    if (criticalErrors.length === 0) pass('no JS errors');
    else fail('no JS errors', criticalErrors.slice(0, 3).join('; '));

    // Screenshot
    const ssPath = path.join(siteDir, 'ci-screenshot.jpg');
    await page.screenshot({ path: ssPath, type: 'jpeg', quality: 80 });
    results.screenshot = ssPath;
    pass('screenshot captured');

  } finally {
    await browser.close();
    if (serverProc) serverProc.kill();
  }

  const ok = results.failed.length === 0;
  console.log(JSON.stringify({ ...results, ok }));
  process.exit(ok ? 0 : 1);
})().catch(e => {
  fail('browser launch', e.message);
  console.log(JSON.stringify({ ...results, ok: false }));
  process.exit(1);
});
