> **Langue :** Français | [English](BANANA-SETUP.md)

# Guide de configuration de l'extension de banane

## Clé de l'API Google AI

1. Allez à [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Créer une clé API"
4. Copier la clé. Vous en aurez besoin pendant l'installation

** Limites des niveaux libres :**
- Vérifier les limites actuelles dans Google AI Studio avant le travail par lots

## Configuration du serveur ## MCP

L'installateur le configure automatiquement. Si vous devez le configurer manuellement,
Ajouter à `~/.claude/settings.json` :

```json
{
  "mcpServers": {
    "nanobanana-mcp": {
      "command": "npx",
      "args": ["-y", "@ycse/nanobanana-mcp@1.1.1"],
      "env": {
        "GOOGLE_AI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Scripted setup helper:
```bash
powehi-seo-geo run --extension banana setup_mcp.py --key YOUR_KEY
```

## Installation de vérification

Run the validation script:
```bash
powehi-seo-geo run --extension banana validate_setup.py
```

Ou vérifiez manuellement :
1. Le fichier `ls ~/.claude/skills/powehi-seo-image-gen/SKILL.md`:skill existe
2. Le fichier `ls ~/.claude/agents/seo-image-gen.md`:agent existe
3. `grep nanobanana ~/.claude/settings.json`:MCP configuré

## Questions communes

### "Les outils MCP ne sont pas disponibles"
- Redémarrer Claude Code après l'installation de l'extension
- Vérifier que votre clé API est valide sur [aistudio.google.com](https://aistudio.google.com)
- Vérifiez que `~/.claude/settings.json` a l'entrée nanobanana-mcp

### Taux limité (429)
- Vérifiez les limites actuelles de free-tier dans Google AI Studio
- Attendez 60 secondes et réessayez
- Pour les opérations par lots, ajouter des retards entre les demandes

### Erreur "IMAGE SAFETY"
- Le filtre de sécurité a signalé votre prompt (souvent un faux positif)
- Claude proposera des alternatives reformulées automatiquement
- Déclencheurs communs : certaines descriptions de couleurs, scénarios implicites
- Voir la section sur la reformulation de sécurité `references/prompt-engineering.md`

### "Node.js version trop ancienne"
- Nécessite Node.js 20+
- Mise à jour via nvm: `nvm install 20 && nvm use 20`
- Ou télécharger depuis [nodejs.org](https://nodejs.org/)

### Les images générées n'apparaissent pas
- Répertoire de sortie par défaut : `~/Documents/nanobanana_generated/`
- Vérifiez le chemin retourné par Claude après génération
- Vérifier l'espace disque disponible

## ImageMagick (facultatif)

Pour post-traitement (conversion WebP, culture, enlèvement de fond):

```bash
# Ubuntu/Pop!_OS
sudo apt install imagemagick

# Verify
magick --version
```

Si `magick` (v7) n'est pas disponible, les scripts reviennent à `convert` (v6).
