import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs';
import path from 'path';

puppeteer.use(StealthPlugin());

const USERNAME = 'anglos84@gmail.com';
const PASSWORD = 'L30noR$H2302198#';

(async () => {
    console.log('Iniciando sincronización de artículos de LinkedIn...');
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    
    // Login
    console.log('Iniciando sesión...');
    await page.goto('https://www.linkedin.com/login');
    await page.type('#username', USERNAME);
    await page.type('#password', PASSWORD);
    await page.click('[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle2' });
    
    // Go to Articles
    console.log('Navegando a los artículos...');
    await page.goto('https://www.linkedin.com/in/josé-angel-sosa-lópez-2568683a/recent-activity/articles/', { waitUntil: 'networkidle2' });
    
    // Wait for the articles to load
    await page.waitForSelector('.profile-creator-shared-feed-update__container', { timeout: 15000 }).catch(() => console.log("No se encontraron artículos o tardó demasiado"));
    
    // Scroll down to load more (optional)
    for(let i = 0; i < 3; i++) {
        await page.evaluate(() => window.scrollBy(0, document.body.scrollHeight));
        await new Promise(r => setTimeout(r, 2000));
    }

    const articles = await page.evaluate(() => {
        let results = [];
        let items = document.querySelectorAll('.profile-creator-shared-feed-update__container');
        for (let item of items) {
            let titleEl = item.querySelector('.break-words.update-components-article__title');
            let linkEl = item.querySelector('a.app-aware-link');
            let dateEl = item.querySelector('.visually-hidden');
            let descEl = item.querySelector('.update-components-article__description');
            
            if (titleEl && linkEl) {
                results.push({
                    title: titleEl.innerText.trim(),
                    link: linkEl.href.split('?')[0],
                    date: dateEl ? dateEl.innerText.trim() : 'Reciente',
                    desc: descEl ? descEl.innerText.trim() : ''
                });
            }
        }
        return results;
    });

    console.log(`Se encontraron ${articles.length} artículos.`);
    
    if(articles.length > 0) {
        // Build HTML
        let htmlContent = '';
        for(let art of articles) {
            htmlContent += `
    <article class="article">
      <span class="date">${art.date}</span>
      <div>
        <h2><a href="${art.link}">${art.title}</a></h2>
        <p>${art.desc}</p>
      </div>
      <a class="go" href="${art.link}">Read on LinkedIn ↗</a>
    </article>
`;
        }

        // Replace in articles.astro
        const updateFile = (filePath, lang) => {
            const fullPath = path.resolve(filePath);
            let content = fs.readFileSync(fullPath, 'utf8');
            const regex = /<section class="list">\s*<div class="wrap">([\s\S]*?)<\/div>\s*<\/section>/;
            
            let replacedHtml = htmlContent;
            if (lang === 'es') {
                replacedHtml = replacedHtml.replace(/Read on LinkedIn ↗/g, 'Leer en LinkedIn ↗');
            }

            let newContent = content.replace(regex, `<section class="list">\n  <div class="wrap">\n${replacedHtml}  </div>\n</section>`);
            fs.writeFileSync(fullPath, newContent, 'utf8');
            console.log(`Archivo ${filePath} actualizado.`);
        };

        updateFile('./src/pages/articles.astro', 'en');
        updateFile('./src/pages/es/articles.astro', 'es');
    }

    await browser.close();
    console.log('Sincronización terminada.');
})();
