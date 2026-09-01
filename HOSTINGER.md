# Mettre le site en ligne sur Hostinger

Ce site est 100% statique (HTML/CSS/JS, aucun serveur, aucune base de données, aucun build à faire). Il fonctionne tel quel sur n'importe quel hébergement Hostinger (Premium, Business, Cloud...).

## Méthode 1 — Gestionnaire de fichiers (le plus simple)

1. Connectez-vous à **hPanel** (panneau Hostinger).
2. Allez dans **Sites web** → choisissez votre site → **Gérer**.
3. Ouvrez le **Gestionnaire de fichiers** (File Manager).
4. Ouvrez le dossier **`public_html`**.
5. Supprimez les fichiers qui s'y trouvent déjà (souvent un `index.html` par défaut, `default.php`, etc.) — sauf si vous savez que vous en avez besoin.
6. Cliquez sur **Importer / Upload**, sélectionnez le fichier `doxha-church-site.zip`.
7. Une fois l'upload terminé, faites un clic droit sur le zip → **Extraire** (Extract), directement dans `public_html`.
8. Supprimez le fichier `.zip` une fois extrait (optionnel, pour faire le ménage).
9. Votre site est en ligne immédiatement à l'adresse de votre domaine.

**Important** : les fichiers doivent être directement dans `public_html` (pas dans un sous-dossier `public_html/doxha-church-site/`). Si l'extraction crée un sous-dossier, déplacez tout son contenu à la racine de `public_html`.

## Méthode 2 — FTP (FileZilla ou autre client FTP)

1. Dans hPanel, récupérez vos identifiants FTP : **Sites web** → **Gérer** → **Fichiers** → **Comptes FTP**.
2. Connectez-vous avec FileZilla (ou un autre client FTP) : hôte, nom d'utilisateur, mot de passe, port 21.
3. Naviguez jusqu'au dossier `public_html` sur le serveur.
4. Glissez-déposez tout le contenu du dossier décompressé (index.html, css/, js/, assets/, ressources/, etc.) directement dans `public_html`.

## Structure du site (doit rester intacte)

```
public_html/
├── index.html
├── fonctionnalites.html
├── cas-usage.html
├── ressources.html
├── tarifs.html
├── a-propos.html
├── contact.html
├── connexion.html
├── inscription.html
├── css/
│   ├── style.css
│   └── devices.css
├── js/
│   └── main.js
├── assets/
│   └── favicon.svg
└── ressources/
    ├── guide-gestion-eglise-moderne.pdf
    ├── guide-dimes-et-offrandes.pdf
    └── guide-multi-campus.pdf
```

## Nom de domaine

Si votre domaine est déjà géré chez Hostinger, il pointe automatiquement vers `public_html` — rien d'autre à faire. Si votre domaine est ailleurs, pointez ses enregistrements DNS (A / CNAME) vers Hostinger depuis hPanel → **Domaines** → **DNS**.

## Formulaires (contact, connexion, inscription)

Les formulaires du site sont actuellement statiques (démo front-end uniquement, aucune donnée n'est envoyée). Pour qu'ils envoient réellement des emails ou créent des comptes, il faudra les connecter à un service (formulaire PHP simple compatible Hostinger, Formspree, ou votre futur backend applicatif).
