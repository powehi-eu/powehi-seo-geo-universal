> **Langue :** Français | [English](SERANKING-SETUP.md)

# Configuration de l'extension du classement SE

L'API de SE Ranking expose les données traditionnelles SEO (SERP, backlinks,
En ce qui concerne les systèmes de gestion de l'information, il convient de noter que les systèmes de gestion de l'information et de gestion de l'information ne sont pas compatibles avec le marché intérieur.

## Installation

```bash
./extensions/seranking/install.sh        # Linux / macOS
.\extensions\seranking\install.ps1       # Windows
```

L'installateur invite à une clé API (entrée cachée), copie
`SKILL.md` dans `~/.claude/skills/powehi-seo-seranking/`, et écrit
`env.SERANKING_API_KEY` dans `~/.claude/settings.json` avec le mode 0o600.

## Obtenez une clé API

https://seranking.com/api.html — la tarification est basée sur une unité; la visibilité AI
coûtent ~5 unités par requête (1 par plate-forme).

## Vérifier

```
/powehi-seo seranking ai-visibility "Powehi Universal SEO"
```

Résultats escomptés: pourcentages par plateforme (ChatGPT, Gemini, Perplexité,
Aperçus AI, mode AI) avec des notes de confiance de taille d'échantillon.

## Clé tournante

Re-exécuter l'installateur ; il écrase `env.SERANKING_API_KEY` atomiquement
(tempfile + remplacer) sans toucher à d'autres paramètres.

## Désinstaller

```bash
./extensions/seranking/uninstall.sh
```
