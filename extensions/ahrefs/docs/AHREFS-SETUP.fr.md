> **Langue :** Français | [English](AHREFS-SETUP.md)

# Configuration de l'extension Ahrefs

Câbles de la [`@ahrefs/mcp@0.0.11`](https://www.npmjs.com/package/@ahrefs/mcp)
serveur dans votre session Claude Code afin que la compétence `seo-ahrefs` puisse appeler
données Ahrefs en direct.

## Installation

```bash
./extensions/ahrefs/install.sh        # Linux / macOS
.\extensions\ahrefs\install.ps1       # Windows PowerShell
```

L'installateur:

1. Vérifie que Python 3 + Node 18+ sont sur `$PATH`.
2. Prompts pour votre jeton API Ahrefs (l'entrée est cachée).
3. Préchauffe le paquet `@ahrefs/mcp@0.0.11` npm via `npx --yes`
L'appel MCP ne passe pas 10 secondes de téléchargement.
4. Copie `skills/seo-ahrefs/SKILL.md` dans `~/.claude/skills/powehi-seo-ahrefs/`.
5. Atomically écrit `mcpServers.ahrefs` dans `~/.claude/settings.json`
avec votre jeton dans le bloc `env`. Le fichier de paramètres est `chmod 0o600`
après la fusion (même durcissement que le jeton OAuth).

## Vérifier

Ouvrez une nouvelle session Claude Code et demandez :

```
/powehi-seo ahrefs metrics https://example.com
```

Si vous voyez "Ahrefs MCP non connecté", le paquet npm n'est pas encore mis en cache.
Relancez l'installateur pour préchauffer ou exécutez manuellement `npx --yes --package=@ahrefs/mcp@0.0.11 mcp --help`.

## Jeton rotatif

```bash
./extensions/ahrefs/install.sh   # re-runs the prompt; overwrites the env entry
```

Le script de fusion de Python est idempotent — re-running remplace seulement le
`mcpServers.ahrefs.env.AHREFS_API_TOKEN` valeur, laissant le reste de
`settings.json` intact.

## Désinstaller

```bash
./extensions/ahrefs/uninstall.sh    # removes the skill + clears the MCP entry
```

## Modèle de coût

Ahrefs frais par "unité". Une unité couvre la plupart des paramètres lus (domaine
métriques, données de rétrolien) à 1 unité chacune; les paramètres globaux coûtent plus cher. Les
`scripts/dataforseo_costs.py` suivi des coûts expédié avec powehi-seo-geo
généralise les fournisseurs — voir l'extension DataForSEO
`references/cost-tiers.md` pour le modèle de préréglage budgétaire
câblage Ahrefs comptabilité.

## Dépannage

Symptômes Cause Correction
- Oui.
L'installateur n'a pas saisi l'entrée.
Exécuter avec Internet; l'installateur préchauffe mais le cache a besoin de réseau.
401 de n'importe quelle commande `/powehi-seo ahrefs *`.
