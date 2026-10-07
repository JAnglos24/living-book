import { chromium } from 'file:///D:/symbios_global_core/node_modules/playwright/index.mjs';

const pages = [
  'https://iliriaviveros.com/',
  'https://www.jasosal.com/',
  'https://www.jasosal.com/es/',
  'https://www.jasosal.com/es/ebook/05-digital-materials-apis-data-and-constraints/',
];
const files = [
  'https://iliriaviveros.com/robots.txt',
  'https://iliriaviveros.com/sitemap-index.xml',
  'https://iliriaviveros.com/sitemap-0.xml',
  'https://www.jasosal.com/robots.txt',
  'https://www.jasosal.com/sitemap-index.xml',
  'https://www.jasosal.com/sitemap-0.xml',
];

const browser = await chromium.launch({ channel: 'chrome' });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' });
const page = await ctx.newPage();

for (const u of pages) {
  const r = await page.goto(u + '?nocache=' + Date.now(), { waitUntil: 'domcontentloaded' });
  const d = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    title: document.title,
    canonical: document.querySelector('link[rel=canonical]')?.href ?? 'MISSING',
    ogImage: document.querySelector('meta[property="og:image"]')?.content ?? 'MISSING',
    robotsMeta: document.querySelector('meta[name=robots]')?.content ?? '(none)',
    ldjson: document.querySelectorAll('script[type="application/ld+json"]').length,
  }));
  console.log(`\n[${r.status()}] ${u}\n`, d);
}

for (const u of files) {
  const r = await ctx.request.get(u + '?nocache=' + Date.now());
  const t = await r.text();
  const locs = (t.match(/<loc>/g) || []).length;
  console.log(`\n[${r.status()}] ${u}  ${locs ? locs + ' <loc>' : ''}\n${locs ? '' : t.slice(0, 200)}`);
}
await browser.close();
