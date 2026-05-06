#!/usr/bin/env node
/**
 * audit.js <site_dir> <output_json_path> [output_html_path]
 *
 * Runs Google Lighthouse against a generated FieldLaunch site.
 * Spins up python3 -m http.server, audits, tears down.
 *
 * Outputs a JSON summary (scores + top opportunities) to output_json_path.
 * Optionally writes the full HTML report to output_html_path.
 */

const path = require('path');
const fs = require('fs');
const http = require('http');
const { spawn } = require('child_process');

const siteDir = process.argv[2];
const outputJson = process.argv[3];
const outputHtml = process.argv[4] || null;

if (!siteDir || !outputJson) {
  console.error('Usage: node audit.js <site_dir> <output_json> [output_html]');
  process.exit(1);
}

const distDir = path.join(siteDir, 'dist');
const serveDir = fs.existsSync(path.join(distDir, 'index.html')) ? distDir : siteDir;

const lighthousePath = path.resolve(__dirname, '../../app/node_modules/lighthouse');
const lighthouse = require(lighthousePath);
const chromeLauncher = require(path.resolve(__dirname, '../../app/node_modules/chrome-launcher'));

function findFreePort() {
  return new Promise((resolve, reject) => {
    const srv = http.createServer();
    srv.listen(0, '127.0.0.1', () => { const p = srv.address().port; srv.close(() => resolve(p)); });
    srv.on('error', reject);
  });
}

(async () => {
  const port = await findFreePort();
  const serverProc = spawn('python3', ['-m', 'http.server', String(port), '--directory', serveDir], {
    stdio: 'pipe',
  });
  await new Promise(r => setTimeout(r, 800));

  const chrome = await chromeLauncher.launch({
    chromePath: '/usr/bin/google-chrome',
    chromeFlags: ['--headless', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  });

  try {
    const runnerResult = await lighthouse(`http://127.0.0.1:${port}/`, {
      logLevel: 'error',
      output: outputHtml ? ['json', 'html'] : ['json'],
      onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
      port: chrome.port,
    });

    const lhr = runnerResult.lhr;
    const categories = lhr.categories;

    // Extract top opportunities (audits that failed)
    const opportunities = Object.values(lhr.audits)
      .filter(a => a.score !== null && a.score < 1 && a.details?.type === 'opportunity')
      .sort((a, b) => (a.score ?? 1) - (b.score ?? 1))
      .slice(0, 8)
      .map(a => ({
        id: a.id,
        title: a.title,
        description: a.description?.split('.')[0] + '.',
        score: Math.round((a.score ?? 0) * 100),
        displayValue: a.displayValue || null,
      }));

    // Extract diagnostics that failed
    const diagnostics = Object.values(lhr.audits)
      .filter(a => a.score !== null && a.score < 1 && a.details?.type === 'table')
      .sort((a, b) => (a.score ?? 1) - (b.score ?? 1))
      .slice(0, 6)
      .map(a => ({
        id: a.id,
        title: a.title,
        score: Math.round((a.score ?? 0) * 100),
        displayValue: a.displayValue || null,
      }));

    const summary = {
      url: `http://127.0.0.1:${port}/`,
      fetchedAt: new Date().toISOString(),
      scores: {
        performance: Math.round((categories.performance?.score ?? 0) * 100),
        accessibility: Math.round((categories.accessibility?.score ?? 0) * 100),
        bestPractices: Math.round((categories['best-practices']?.score ?? 0) * 100),
        seo: Math.round((categories.seo?.score ?? 0) * 100),
      },
      opportunities,
      diagnostics,
    };

    fs.writeFileSync(outputJson, JSON.stringify(summary, null, 2));

    if (outputHtml && runnerResult.report) {
      const reports = Array.isArray(runnerResult.report) ? runnerResult.report : [runnerResult.report];
      const htmlReport = reports.find(r => r.startsWith('<!DOCTYPE') || r.startsWith('<')) || reports[1];
      if (htmlReport) fs.writeFileSync(outputHtml, htmlReport);
    }

    console.log(JSON.stringify(summary));
  } finally {
    await chrome.kill();
    serverProc.kill();
  }
})().catch(e => {
  console.error('lighthouse audit failed:', e.message);
  process.exit(1);
});
