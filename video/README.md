# Vidéo promo Doxha Church

`promo-video-source.html` est la source de la vidéo publicitaire (~28s, style Apple/keynote). C'est une page HTML autonome qui réutilise le CSS réel du site (`css/devices.css` + `css/style.css`) et enchaîne des scènes en plein écran (1920×1080) via une timeline JS (`setTimeout`).

## Régénérer la vidéo (MP4)

1. Servir le site à la racine du dépôt, par ex. :
   ```
   python3 -m http.server 8099 --directory .
   ```
2. Enregistrer la page en vidéo avec Playwright (résolution 1920×1080, ~29s) :
   ```js
   const { chromium } = require('playwright');
   const browser = await chromium.launch();
   const context = await browser.newContext({
     viewport: { width: 1920, height: 1080 },
     recordVideo: { dir: 'out/', size: { width: 1920, height: 1080 } },
   });
   const page = await context.newPage();
   await page.goto('http://localhost:8099/video/promo-video-source.html', { waitUntil: 'load' });
   await page.waitForTimeout(28500);
   await context.close();
   ```
   Cela produit un fichier `.webm` (VP8).
3. Convertir en `.mp4` (H.264, plus compatible) avec un ffmpeg complet (le ffmpeg fourni par Playwright est une build minimale sans H.264) :
   ```
   ffmpeg -y -i input.webm -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium -movflags +faststart doxha-church-promo.mp4
   ```

## Modifier le contenu

Toute la timeline (durées, textes, scènes) est dans le `<script>` en bas du fichier HTML — variable `timeline`. Les scènes sont des `<section class="scene" id="sX">` ; les couleurs et cartes réutilisent les classes du design system du site.
