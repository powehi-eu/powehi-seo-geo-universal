> **Langue :** Français | [English](TROUBLESHOOTING.md)

# Dépannage

## Questions communes

### Compétence non chargée

**Symptôme:** Commande `/powehi-seo` non reconnue

**Solutions:**

For plugin installs, verify and reinstall through Claude Code:
```bash
/plugin list
/plugin marketplace add powehi-eu/powehi-seo-geo-universal
/plugin install powehi-seo-geo@powehi-universal-seo-geo
```

Pour les installations manuelles:

1. Verify installation:
```bash
ls ~/.claude/skills/powehi-seo/SKILL.md
```

2. Check SKILL.md has proper frontmatter:
```bash
head -5 ~/.claude/skills/powehi-seo/SKILL.md
```
Should start with `---` followed by YAML.

3. Restart Claude Code:
```bash
claude
```

4. Réinitialisation :

Attention: Préférez télécharger, inspecter, puis exécuter des scripts à distance; le formulaire pipe-to-shell ci-dessous est l'option de commodité moins sûre.

```bash
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh | bash
```

---

### Erreurs de dépendance de Python

**Symptôme:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**

Les dépendances appartiennent à l'exécution gérée. Pour installer un plugin, exécutez :

```bash
/powehi-seo doctor
/powehi-seo setup
```

For a manual install, run:
```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo doctor
~/.claude/skills/powehi-seo/bin/powehi-seo-geo setup
```

N'installez pas de paquets individuels, utilisez `pip --user` ou créez un shim PATH.

### requires.txt Non trouvé

**Symptôme:** `No such file: requirements.txt` après installation

**Solution:** Pour les installations de plugin, réinstallez le plugin d'abord:

```bash
/plugin install powehi-seo-geo@powehi-universal-seo-geo
```

Pour les installations manuelles, requirements.txt est copié dans le répertoire des compétences :

```bash
ls ~/.claude/skills/powehi-seo/requirements.txt
```

If missing, download it directly:
```bash
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/requirements.txt \
  -o ~/.claude/skills/powehi-seo/requirements.txt
```

### Problèmes de détection de Python Windows

**Symptôme:** `python is not recognized` ou `pip points to wrong Python`

**Solution (v1.2.0+):** L'installateur Windows essaie maintenant `python` et `py -3`. Si les deux échouent:

1. Installez Python depuis [python.org](https://python.org) et cochez "Ajouter à PATH"
2. Relancez `install.ps1` ; il résout `py -3`, `python3`, puis `python`
3. Exécuter `/powehi-seo doctor` après installation

---

### Erreurs de capture d'écran de Playwright

**Symptôme:** `playwright._impl._errors.Error: Executable doesn't exist`

**Solution:** rerun managed setup so the browser is installed through the same
interpreter and persistent browser directory:
```bash
/powehi-seo setup
/powehi-seo doctor
```

---

### Autorisation refusée Erreurs

**Symptôme:** `Permission denied` lors de l'exécution des scripts

**Solution:**
```bash
chmod +x ~/.claude/skills/powehi-seo/scripts/*.py
```

---

---

### Sous-agent non trouvé

**Symptôme:** `Agent 'seo-technical' not found`

**Solution:**

Pour installer le plugin, vérifiez `/plugin list` et réinstallez `powehi-seo-geo@powehi-universal-seo-geo`; chargez les sous-agents à partir du plugin, pas `~/.claude/agents/`.

Pour les installations manuelles:

1. Verify agent files exist:
```bash
ls ~/.claude/agents/seo-*.md
```

2. Check agent frontmatter:
```bash
head -5 ~/.claude/agents/seo-technical.md
```

3. Re-install agents:
```bash
cp /path/to/powehi-seo-geo/agents/*.md ~/.claude/agents/
```

---

### Erreurs de délai

**Symptôme:** `Request timed out after 30 seconds`

**Solutions:**

1. Le site cible peut être lent: essayez à nouveau
2. Augmenter la durée des appels de script
3. Vérifiez votre connexion réseau
4. Certains sites bloquent les demandes automatisées

---

### La validation du schéma faux positifs

**Symptôme:** Crocheter bloque le schéma valide

**Vérifier:**

1. S'assurer que les détenteurs de place sont remplacés
2. Vérifier @context est `https://schema.org`
3. Vérifier les types dépréciés/retraités: Comment et spécialAnnonce, plus les retraites de juin 2025 (ClaimReview, VehicleListing, EstimatedSalary, LearningVideo, and the CourseInfo carrousel)
4. FAQPage riche résultats ont été retirés pour tous les sites sur 2026-05-07. Le crochet ne le bloque pas parce qu'il reste un type Schema.org valide, mais aucun avantage AI ou classement n'est confirmé.
5. Valider à [Google's Rich Results Test](https://search.google.com/test/rich-results)

---

### Rendement de la vérification lente

**Symptôme:** L'audit complet prend trop de temps

**Solutions:**

1. L’audit explore jusqu’à 500 pages : les sites volumineux demandent davantage de temps
2. Les sous-agents fonctionnent en parallèle pour accélérer l'analyse
3. Pour des vérifications plus rapides, utilisez `/powehi-seo page` sur des URL spécifiques
4. Vérifier si le site a des temps de réponse lents

---

## Pour obtenir de l'aide

1. **Check the docs:** Review [COMMANDS.md](COMMANDS.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

2. **GitHub Questions :** Signaler les bogues dans le dépôt

3. **Logs :** Vérifiez la sortie de Claude Code pour les détails d'erreur

## Mode de débogage

Pour voir la sortie détaillée, vérifiez les journaux internes ou les scripts d'exécution de Claude Code directement :

```bash
# Test fetch
python3 ~/.claude/skills/powehi-seo/scripts/fetch_page.py https://example.com

# Analyse
python3 ~/.claude/skills/powehi-seo/scripts/parse html.py page.html --json

# Test screenshot
python3 ~/.claude/skills/powehi-seo/scripts/capture_screenshot.py https://example.com
```
