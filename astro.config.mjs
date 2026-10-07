// @ts-check
import { defineConfig } from 'astro/config';

import mdx from '@astrojs/mdx';

import cloudflare from '@astrojs/cloudflare';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.jasosal.com',
  integrations: [mdx(), sitemap({ filter: (p) => !/\/(admin|print)\//.test(p) })],
  adapter: cloudflare(),
  redirects: {
    '/es-home.html': '/es/',
    '/es-articles.html': '/es/articles/',
    '/es-author.html': '/es/author/',
    '/es-ebook.html': '/es/ebook/',
    '/es-ebook-chapter-01.html': '/es/ebook/01-what-can-industrial-design-teach/',
    '/home.html': '/',
    '/articles.html': '/articles/',
    '/author.html': '/author/',
    '/ebook.html': '/ebook/',
    '/ebook-chapter-01.html': '/ebook/01-what-can-industrial-design-teach/',
    '/ebook/es-ebook.html': '/es/ebook/'
  }
});