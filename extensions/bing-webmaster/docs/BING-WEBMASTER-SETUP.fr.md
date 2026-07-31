> **Langue :** Français | [English](BING-WEBMASTER-SETUP.md)

# Outils Bing Webmaster + configuration de l'extension IndexNow

## Ce que ça te donne

1. **API Bing Webmaster Tools** : liens entrants, statistiques d’exploration et données de recherche
mots clés, et comparaison de liens concurrents via
`scripts/bing_webmaster.py` (déjà expédié avec powehi-seo-geo).
2. ** Soumission d'URL IndexNow** pour Amazon, Bing, Naver, Seznam.cz,
Yandex, et Yeep via `scripts/indexnow_submit.py`.
3. Une compétence `seo-bing` unifiée qui dirige la bonne commande à la
script droit.

## Installation

```bash
./extensions/bing-webmaster/install.sh
.\extensions\bing-webmaster\install.ps1
```

Vous serez invité à :

- Clé API Bing Webmaster Tools (https://www.bing.com/webmasters/api)
- IndexNow clé hôte (toute chaîne de 32 caractères au hasard)
- IndexNow keyLocation URL (doit servir le fichier clé à cette URL)

Les deux groupes peuvent être laissés en blanc si vous n'en voulez qu'un. L'installateur
écrit seulement l'env vars que vous fournissez.

## Liste de contrôle de configuration IndexNow

1. Generate a key: `openssl rand -hex 32`
2. Save the key to a file at the **root** of your site, named `<key>.txt`,
   served at `https://example.com/<key>.txt`. The file body is the key.
3. Run:
   ```
   /powehi-seo bing verify-indexnow
   ```
   The verifier fetches your keyLocation URL and confirms the body
   matches the key, the #1 onboarding mistake.

## Référence Microsoft Copilot

Microsoft Copilot tire des citations de l'index Bing. Pages que
Ils ne sont pas à Bing. IndexNow notifie la participation
moteurs sur les URL modifiées et peut accélérer la découverte, mais il ne
garantie vitesse d'indexation.

## Désinstaller

```bash
./extensions/bing-webmaster/uninstall.sh
```

PowerShell manual removal:
```powershell
Remove-Item -Recurse -Force "$HOME\.claude\skills\powehi-seo-bing"
notepad "$HOME\.claude\settings.json"
```

Dans `settings.json`, supprimer `BING_WEBMASTER_API_KEY`, `INDEXNOW_KEY` et
`INDEXNOW_KEY_LOCATION` à partir de l'objet de niveau supérieur `env`.
