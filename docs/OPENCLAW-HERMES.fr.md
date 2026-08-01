> **Langue :** Français | [English](OPENCLAW-HERMES.md)

# Distribution OpenClaw et Hermes

Le dépôt conserve un arbre source unique `skills/` et propose deux modes de
consommation complémentaires.

## OpenClaw / ClawHub

Le fichier racine `openclaw.plugin.json` déclare le plugin OpenClaw natif et
`openclaw/index.js` fournit l’adaptateur runtime. Pour vérifier une installation
locale :

```bash
openclaw plugins install --link .
openclaw plugins enable powehi-universal-seo-geo
openclaw gateway restart
openclaw plugins inspect powehi-universal-seo-geo --runtime --json
```

Après publication sur ClawHub :

```bash
openclaw plugins install clawhub:powehi-universal-seo-geo
```

## Hermes Agent

Hermes consomme directement les skills portables. Ajoutez le dépôt comme tap :

```bash
hermes skills tap add powehi-eu/powehi-seo-geo-universal
hermes skills search seo --source github
hermes skills install powehi-eu/powehi-seo-geo-universal/skills/powehi-seo
```

Pour un checkout local, ajoutez le chemin dans `~/.hermes/config.yaml` :

```yaml
skills:
  external_dirs:
    - H:/powehi-seo-geo-universal/skills
```

## Positionnement ClawHub

Powehi Universal SEO doit être présenté comme une **suite modulaire
d’intelligence SEO et GEO fondée sur des preuves**, et non comme une simple
checklist SEO ou un prompt d’analyse concurrentielle.

Pour assurer la transparence, indiquez aussi qu’il s’agit d’un **fork maintenu
par Powehi et d’une évolution de
[AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)**. Le
projet upstream et les contributions tierces restent crédités dans `LICENSE`,
`CONTRIBUTORS.md` et `docs/UPSTREAM.md`.

La suite apporte notamment :

- 33 skills portables et 18 agents spécialisés ;
- la séparation des preuves source, build et live ;
- les audits techniques, contenu, schema, local, e-commerce et backlinks ;
- les données Google Search Console, GA4, CrUX et PageSpeed ;
- la visibilité ChatGPT, Google AI Overviews, Gemini et Perplexity ;
- les rapports reproductibles, le suivi de dérive et les fetchers SSRF-safe ;
- les extensions MCP optionnelles Firecrawl, Ahrefs, DataForSEO, Bing, SE
  Ranking et recherche de citations de marque.

### Description ClawHub

Utilisez la description anglaise publiée dans
[OPENCLAW-HERMES.md](OPENCLAW-HERMES.md) pour la fiche ClawHub. Elle mentionne
la provenance upstream, les capacités distinctives et la compatibilité Claude
Code, Codex, Cursor, OpenClaw et Hermes.

## Publication et mises à jour

Depuis la racine du dépôt :

```bash
clawhub package validate .
clawhub package publish . --family code-plugin --dry-run
clawhub package publish . --family code-plugin
```

Chaque mise à jour suit le même processus après alignement de la version et du
changelog. ClawHub conserve des versions immuables ; les utilisateurs peuvent
mettre à jour avec :

```bash
openclaw plugins update clawhub:powehi-universal-seo-geo
```

Ne publiez pas avant d’avoir vérifié l’alignement entre les métadonnées du
package, le manifeste du plugin et la version de release.
