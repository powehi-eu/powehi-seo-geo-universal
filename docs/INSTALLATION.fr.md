> **Langue :** Français | [English](INSTALLATION.md)

# Guide d'installation

## Préalables

- **Python 3.10+** avec pip
- **Git** pour le clonage du dépôt
- **Claude Code CLI** installé et configuré

Facultatif:
- **Playwright Chrome** - install.sh tente cela automatiquement; la défaillance est non fatale; nécessaire uniquement pour le rendu SPA et les captures d'écran

## Installation rapide

### Installation du plugin (Claude Code 1.0.33+)

Le chemin recommandé. À l'intérieur de Claude Code:

```
/plugin marketplace add powehi-eu/powehi-seo-geo-universal
/plugin install powehi-seo-geo@powehi-universal-seo-geo
/powehi-seo setup
```

L'installation du plugin n'exécute pas les gestionnaires de paquets. `/powehi-seo setup` est un explicite,
étape de fourniture unique qui écrit l'environnement virtuel et le navigateur seulement
aux données du plugin persistant de Claude. Utilisez `/powehi-seo doctor` pour une vérification en lecture seule.

### Installation manuelle (Unix, macOS, Linux)

```bash
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
bash powehi-seo-geo/install.sh
```

Examen à l'époque:

```bash
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh > install.sh
cat install.sh        # review
bash install.sh       # run when satisfied
rm install.sh
```

### Installation manuelle (Windows, PowerShell)

```powershell
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
powershell -ExecutionPolicy Bypass -File powehi-seo-geo\install.ps1
```

Le chemin Windows utilise `git clone` plutôt que `irm | iex` parce que les propres garde-corps de sécurité de Claude Code drapeau piped distant-script exécution. Inspectez `install.ps1` avant de courir.

## Installation manuelle

1. **Cluner le dépôt**

```bash
git clone https://github.com/powehi-eu/powehi-seo-geo-universal.git
cd powehi-seo-geo
```

2. **Démarrer l ' installateur**

```bash
./install.sh
```

3. **Vérifier l'exécution gérée**

L'installateur délègue la dépendance et la fourniture de chrome au même moment
utilisé par toutes les compétences. Il crée `~/.claude/skills/powehi-seo/.venv/` et ne tombe jamais
retour à l'installation globale ou du paquet utilisateur.

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo doctor
```

Si la configuration du noyau a échoué, réexécutez l'installateur inspecté. Si seulement le chrome a échoué,
l'installateur signale un résultat dégradé et une analyse brute reste disponible.

## Chemins d'installation

L'installateur copie les fichiers vers :

Composante
C'est quoi ?
Compétence principale
Sous-compétences
Sous-agents
Lanceur d'exécution
Python isolé `~/.claude/skills/powehi-seo/.venv/`

## Vérifier l'installation

1. Démarrer Claude Code :

```bash
claude
```

2. Vérifiez que la compétence est chargée :

```
/powehi-seo
```

Vous devriez voir un message d'aide ou une invitation pour une URL.

## Désinstallation

Si installé comme un plugin:

```
/plugin uninstall powehi-seo-geo@powehi-universal-seo-geo
/plugin marketplace remove powehi-eu/powehi-seo-geo-universal
```

Si installé manuellement, exécutez le désinstaller d'un clone frais:

```bash
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
bash powehi-seo-geo/uninstall.sh
```

`uninstall.sh` supprime toutes les sous-compétences, sous-agents installés et les entrées MCP du plugin de `~/.claude/settings.json`. Ne maintenez pas de liste `rm` codée à la main. Le désinstaller expédié est la source canonique.

**Ce qui est supprimé.** `install.sh` et `install.ps1` enregistrent chaque répertoire de skill et chaque fichier d’agent qu’ils créent dans un manifeste de propriété situé dans `~/.claude/skills/powehi-seo/.install-manifest`. Les désinstalleurs ne suppriment que ces entrées : une skill ou un agent tiers utilisant le préfixe `seo-` n’est jamais supprimé.

Si votre installation est antérieure aux manifestes, le désinstalleur retombe sur l’énumération des chemins `seo-*`. Il affiche alors la liste complète des candidats et attend un `y` explicite avant toute suppression — relisez cette liste, car elle peut inclure des skills que ce projet n’a pas installées. Passez `--force` (ou `-Force` sous Windows) pour sauter l’invite une fois la vérification faite. Dans un shell non interactif, le désinstalleur s’arrête sans rien supprimer plutôt que de présumer un accord.

## Amélioration

Pour passer à la dernière version :

Attention: Préférez télécharger, inspecter, puis exécuter des scripts à distance; le formulaire pipe-to-shell ci-dessous est l'option de commodité moins sûre.

```bash
# Uninstall current version
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/uninstall.sh | bash

# Install new version
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh | bash
```

## Dépannage

### Erreur "Traitement non trouvé"

S'assurer que les compétences sont installées au bon endroit :

```bash
ls ~/.claude/skills/powehi-seo/SKILL.md
```

Si le fichier n'existe pas, réexécutez l'installateur.

### Erreurs de dépendance de Python

Exécutez à nouveau la configuration gérée :

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo setup
```

### Erreurs de capture d'écran de Playwright

Exécutez à nouveau la configuration gérée et inspectez le résultat:

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo setup
~/.claude/skills/powehi-seo/bin/powehi-seo-geo doctor
```

### Erreurs de permission sur Unix

Assurez-vous que les scripts sont exécutables :

```bash
chmod +x ~/.claude/skills/powehi-seo/scripts/*.py
```
