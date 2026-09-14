// Generates the real "download the book so far" PDFs (EN + ES) from the
// actual built static site: a cover page plus every currently published
// chapter, printed with a real headless browser and merged into one file.
// Runs automatically after `npm run build` via the "postbuild" script.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer';
import { PDFDocument } from 'pdf-lib';

const ROOT = path.resolve(import.meta.dirname, '..', 'dist', 'client');
const PORT = 4173;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
};

function startServer() {
  const server = createServer(async (req, res) => {
    try {
      let urlPath = decodeURIComponent(req.url.split('?')[0]);
      if (urlPath.endsWith('/')) urlPath += 'index.html';
      if (!path.extname(urlPath)) urlPath += '/index.html';
      const filePath = path.join(ROOT, urlPath);
      if (!filePath.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
      const data = await readFile(filePath);
      const ext = path.extname(filePath);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      res.end(data);
    } catch {
      res.writeHead(404);
      res.end('Not found');
    }
  });
  return new Promise((resolve) => server.listen(PORT, () => resolve(server)));
}

// Chrome's print-to-PDF embeds images at their full source resolution
// regardless of how small they're displayed, which blew past Cloudflare's
// 25 MiB asset limit (source photos are 1.5-2MB each, 14+ of them per
// chapter). Re-encode every rendered <img> to ~2x its on-page CSS size at
// JPEG quality 0.72 via canvas before printing — same visual result at a
// fraction of the size.
async function compressImages(page) {
  await page.evaluate(() => {
    document.querySelectorAll('img[loading="lazy"]').forEach((img) => img.removeAttribute('loading'));
  });
  await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('img'));
    await Promise.all(imgs.map((img) => (img.complete ? Promise.resolve() : img.decode().catch(() => {}))));
  });
  const handles = await page.$$('img');
  for (const handle of handles) {
    await handle.evaluate((img) => {
      if (!img.complete || !img.naturalWidth) return;
      const targetW = Math.min(img.naturalWidth, Math.min(900, Math.max(1, Math.round(img.clientWidth * 1.6))));
      if (targetW >= img.naturalWidth) return;
      const scale = targetW / img.naturalWidth;
      const canvas = document.createElement('canvas');
      canvas.width = targetW;
      canvas.height = Math.round(img.naturalHeight * scale);
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      img.src = canvas.toDataURL('image/jpeg', 0.6);
    });
    await handle.dispose();
  }
}

async function printPage(page, url) {
  await page.goto(url, { waitUntil: 'networkidle0' });
  await compressImages(page);
  return page.pdf({ printBackground: true, format: 'A4' });
}

async function mergePdfs(buffers) {
  const merged = await PDFDocument.create();
  for (const buf of buffers) {
    const doc = await PDFDocument.load(buf);
    const pages = await merged.copyPages(doc, doc.getPageIndices());
    pages.forEach((p) => merged.addPage(p));
  }
  return merged.save();
}

const EDITIONS = [
  {
    lang: 'en',
    outFile: 'thinking-in-products-building-systems-current.pdf',
    routes: ['/print/cover/', '/ebook/01-what-can-industrial-design-teach/'],
  },
  {
    lang: 'es',
    outFile: 'pensar-en-productos-construir-sistemas-actual.pdf',
    routes: ['/es/print/portada/', '/es/ebook/01-what-can-industrial-design-teach/'],
  },
];

async function main() {
  if (!existsSync(ROOT)) {
    console.error(`[generate-pdf] build output not found at ${ROOT} — run "npm run build" first.`);
    process.exit(1);
  }

  const downloadsDir = path.join(ROOT, 'downloads');
  mkdirSync(downloadsDir, { recursive: true });

  const server = await startServer();
  const browser = await puppeteer.launch({
    headless: true,
    protocolTimeout: 300000,
    args: ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const [page] = await browser.pages();

  try {
    for (const edition of EDITIONS) {
      const buffers = [];
      for (const route of edition.routes) {
        const url = `http://localhost:${PORT}${route}`;
        buffers.push(await printPage(page, url));
      }
      const merged = await mergePdfs(buffers);
      const outPath = path.join(downloadsDir, edition.outFile);
      await (await import('node:fs/promises')).writeFile(outPath, merged);
      console.log(`[generate-pdf] wrote ${outPath} (${(merged.length / 1024).toFixed(0)} KB, ${edition.routes.length} source pages)`);
    }
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch((err) => {
  console.error('[generate-pdf] failed:', err);
  process.exit(1);
});
