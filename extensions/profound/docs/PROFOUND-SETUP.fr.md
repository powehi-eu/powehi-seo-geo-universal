> **Langue :** Français | [English](PROFOUND-SETUP.md)

# Configuration de l'extension profonde

Profound (https://tryprofound.com) trace les mentions de marque sur les LLM comme
une série chronologique — le complément de l'échantillonnage SE Ranking à la demande.

## Installation

```bash
./extensions/profound/install.sh        # Linux / macOS
.\extensions\profound\install.ps1       # Windows
```

Stocke `PROFOUND_API_KEY` dans `~/.claude/settings.json` env bloc, mode 0o600.

## Vérifier

```
/powehi-seo profound citations "Powehi Universal SEO"
```

## Désinstaller

```bash
./extensions/profound/uninstall.sh
```

## Quand utiliser Profound contre SE Ranking

Utiliser Profound Utiliser SE Ranking
- Oui.
Analyse des tendances (dérision de la mention de marque hebdomadaire)
ChatGPT + Perplexité couverture profonde
Alertes sur le changement de taux de citation

Les deux sont complémentaires, pas redondants. Installez les deux pour l'IA complète
couverture de visibilité; installer un si budget-contraire.
