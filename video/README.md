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

## Voix off + musique

Le dossier `audio/` contient de quoi régénérer la bande son (voix off française + musique de fond), 100% générée localement (aucun service externe, aucun contenu tiers réutilisé) :

- `audio/segments.json` — le script de la voix off, phrase par phrase, avec le timestamp de départ de chacune (synchronisé sur la timeline de la vidéo).
- `audio/make_music.py` — génère une musique originale (nappes, pulsation, carillons) en pure synthèse (numpy), sans échantillon ni piste existante.

Régénérer la bande son :
```bash
# 1. Voix off (nécessite espeak-ng + mbrola-fr, ex: apt-get install -y mbrola mbrola-fr1 mbrola-fr4)
cd video/audio
python3 - <<'PY'
import json, subprocess
for s in json.load(open('segments.json')):
    subprocess.run(['espeak-ng', '-v', 'mb-fr4', '-s', '150', '-p', '48', s['text'], '-w', f"{s['id']}.wav"], check=True)
PY

# 2. Musique
python3 make_music.py   # -> music.wav

# 3. Mixer voix + musique avec adelay/amix + sidechaincompress (voir historique de session pour la commande ffmpeg complète)

# 4. Incruster l'audio sur la vidéo
ffmpeg -y -i promo-video.mp4 -i mixed_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest doxha-church-promo-audio.mp4
```

**Limite connue** : la voix off utilise `espeak-ng`/`mbrola`, un moteur de synthèse vocale libre et 100% hors-ligne — la qualité est correcte mais reste synthétique, pas un vrai comédien voix ni une voix neuronale premium (type ElevenLabs), car aucun service de ce type n'était accessible depuis cet environnement. Pour un rendu plus proche d'une pub Apple, il est recommandé de remplacer `mixed_audio.wav` par un enregistrement studio réel avant diffusion finale.
