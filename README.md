# Doxha Church — Site web

Site vitrine (marketing/SaaS) pour Doxha Church, logiciel professionnel de gestion d'église. Design premium et corporate, inspiré des standards Apple / Stripe / Notion / Sage.

## Structure

```
.
├── index.html            Accueil (hero, fonctionnalités, stats, CTA)
├── fonctionnalites.html  Fonctionnalités détaillées
├── tarifs.html           Tarifs (Free / Pro / Business) + comparatif + FAQ
├── a-propos.html         Vision, mission, valeurs, histoire, carrières
├── contact.html          Formulaire de contact + informations support
├── connexion.html        Page de connexion
├── inscription.html      Page de création de compte
├── css/style.css         Design system (couleurs, typo, composants)
├── js/main.js            Interactions (menu mobile, accordéon FAQ, reveal au scroll, toggle tarifs)
└── assets/favicon.svg    Favicon (monogramme "D")
```

Aucune dépendance de build : HTML/CSS/JS statiques, prêts à déployer tels quels (Netlify, Vercel, GitHub Pages, ou tout hébergeur statique).

## Design system

- **Couleurs** : blanc / gris clair (`--gray-50…900`), bleu profond (`--blue-500…700`), noir/bleu nuit (`--navy-900`), accent doré (`--gold-500`), accent néon/teal (`--teal-400`).
- **Typographie** : [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts), avec repli sur SF Pro / Segoe UI / Roboto.
- **Composants réutilisables** : boutons (`.btn-primary/secondary/ghost/gold`), cartes fonctionnalités, cartes tarifs, tableau comparatif, FAQ accordéon, bannière CTA, formulaires, mockup produit en CSS pur.

## Développement local

Ouvrez simplement `index.html` dans un navigateur, ou servez le dossier avec un serveur statique :

```bash
python3 -m http.server 8080
```

## Notes

- Les formulaires (contact, connexion, inscription) sont statiques côté front (aucun backend n'est branché) : ils affichent un message de confirmation à la soumission. À connecter à votre backend / service d'emailing (Formspree, Resend, API interne…) en production.
- Les visuels de "mockup produit" sont réalisés en CSS pur (pas de captures d'écran réelles) — à remplacer par de vraies captures du logiciel dès qu'elles sont disponibles.
