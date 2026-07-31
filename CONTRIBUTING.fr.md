> **Langue :** Français | [English](CONTRIBUTING.md)

# Contribution à powehi-seo-geo

Merci pour votre intérêt à contribuer! Voici comment s'impliquer.

## Signaler des bogues

Ouvrir un [GitHub Issue](https://github.com/powehi-eu/powehi-seo-geo-universal/issues) avec:

- Votre version OS et Python
- La sortie d'erreur complète (copie depuis le terminal)
- La commande ou l'étape qui a échoué
- L'URL que vous analysiez (le cas échéant)

## Caractéristiques suggérées

Utiliser [GitHub Discussions](https://github.com/powehi-eu/powehi-seo-geo-universal/discussions) pour des idées et des questions de fonctionnalités.

## Demandes de tirage

1. Fourche le dépôt
2. Créer une branche de fonctionnalités (`git checkout -b feature/my-feature`)
3. Faites vos changements
4. Tester avec un exemple d'URL avant de soumettre
5. Soumettre un PR avec une description claire de ce qui a changé et pourquoi

### Configuration du développement

#### Option A: Installation locale

```bash
git clone https://github.com/YOUR_USERNAME/powehi-seo-geo.git
cd powehi-seo-geo
bash install.sh
```

#### Option B: Espaces de codes GitHub / conteneurs de code VS Dev

Un `.devcontainer/devcontainer.json` est inclus afin que vous puissiez développer sans aucun
installation locale. Deux chemins :

- ** Espaces de codes GitHub** : cliquez sur **Code -> Espaces de codes -> Créer un espace de code sur
principal** sur la page GitHub de la repo. Vous obtenez un Python entièrement provisionné 3.12
environnement avec `requirements.txt` installé et Playwright + Chrome
Prêt, dans environ 60 secondes.
- **VS Code Conteneurs à distance**: avec l'extension [Dev Conteneurs ](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
installé, cloner le repo localement puis exécuter **Conteneurs Dev: Réouvrir dans
Conteneur** de la palette de commandes.

Les deux chemins utilisent la même image (`mcr.microsoft.com/devcontainers/python:3.12`)
et post-créer la commande (`pip install -r requirements.txt && dramaturge
installer le chrome'). Aucune configuration supplémentaire n'est nécessaire non plus.

### Lignes directrices

- Tous les scripts Python doivent afficher JSON pour Claude Code pour analyser
- Les scripts Shell doivent utiliser `set -euo pipefail` pour la sécurité
- Les fichiers SKILL.md doivent rester en dessous de 500 lignes
- Les fichiers de référence devraient être concentrés et inférieurs à 200 lignes
- Suivez le nom de kebab pour tous les répertoires et fichiers
- Gardez une dépendance minimale

### Style de code

- Python : suivre les 8 conventions du PPE. Utilisez `ruff check` ou `flake8` pour le lintage avant de soumettre
- Shell: Utiliser `set -euo pipefail` et citer toutes les variables
- Marquage : garder les lignes sous 120 caractères lorsque cela est pratique

## Extensions communautaires (Pro Hub Challenge)

Powehi Universal SEO accepte les extensions communautaires grâce aux défis et aux PR.
v1.9.0 5 demandes de contestation intégrées et v1.9.7 ont ajouté 9 appels communautaires
demandes de 7 contributeurs. Voir [CONTRIBUTORS.md](CONTRIBUTORS.md) pour
des crédits complets.

Pour soumettre une extension communautaire :
1. Construisez votre compétence/agent/script suivant les modèles de cette repo
2. Conserver SKILL.md sous 500 lignes, références sous 200 lignes
3. Tous les scripts de saisie d'URL doivent passer par `scripts/url_safety.py` — le calque canonique SSRF / DNS (`validate_url()`, `safe_requests_session()`); ne jamais récupérer une URL fournie par l'utilisateur sans elle. (`google_auth.py` est un cycle de vie en jeton OAuth seulement — pas un garde SSRF.)
4. Inclure `original_author` dans vos métadonnées SKILL.md
5. Soumettre un PR ou un poste dans le [AI Marketing Hub](https://www.skool.com/ai-marketing-hub)
