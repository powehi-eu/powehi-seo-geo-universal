> **Langue :** Français | [English](UNLIGHTHOUSE-SETUP.md)

# Configuration de l'extension Unlighthouse

[Unlighthouse](https://unlighthouse.dev) est une page multi-page sous licence MIT
Coureur de phare qui produit un seul rapport agrégé. Pas d'API
quota, pas d'identification, pas de sortie de réseau au-delà de la cible.

## Installation

```bash
./extensions/unlighthouse/install.sh
.\extensions\unlighthouse\install.ps1
```

L'installateur:

1. Vérifie Python 3 + Node 18+.
2. Préchauffe `unlighthouse@0.13.5` via `npx --yes`.
3. Copie la compétence `seo-unlighthouse` dans `~/.claude/skills/`.

Pas de clés API, pas de mutation de settings.json.

## Vérifier

```
/powehi-seo unlighthouse https://example.com --max-routes 5
```

## Quand utiliser Unlighthouse vs PageSpeed Insights

Utiliser Unlighthouse
- Oui.
Site a 100s de pages et vous voulez chaque audité
Hors ligne / environnement restreint Données de champ des utilisateurs réels de Chrome (CrUX)
Contrôle de régression dirigé par l'IC après déploiement
Libéré / sans problème de quota

PSI utilise des données de champ CrUX lorsque disponibles (utilisateurs réels); Unlighthouse
effectue localement des tests de laboratoire de phare. Pour une mesure fiable du VCT
sur le trafic de production, préfèrent PSI / CrUX.

## Désinstaller

```bash
./extensions/unlighthouse/uninstall.sh
```
