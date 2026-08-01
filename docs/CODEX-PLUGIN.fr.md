> **Langue :** Français | [English](CODEX-PLUGIN.md)

# Manifeste du plugin Codex

## Résumé

Cette amélioration ajoute un manifeste de plugin compatible Codex à :

```text
.codex-plugin/plugin.json
```

Le but est de rendre le dépôt `powehi-seo-geo` existant directement reconnaissable comme un plugin Codex sans changer le packaging Claude Code actuel, la disposition des compétences ou le modèle d'exécution.

## Pourquoi ça a été ajouté

Le dépôt contient déjà les actifs de base nécessaires à la consommation de Codex:

- une identité stable du projet
- une grande surface `skills/`
- instructions de mise en commun en `AGENTS.md`
- fichiers portables `SKILL.md`

Ce qui manquait était le manifeste spécifique à Codex attendu à `.codex-plugin/plugin.json`.

L'ajout de ce manifeste fournit un point d'entrée vers Codex tout en préservant la structure Claude Code existante sous `.claude-plugin/`.

## Portée du changement

Cette contribution ne fait qu'une chose :

- ajoute un manifeste Codex valide

Elle ne:

- déplacer ou renommer les compétences
- modifier les flux d'installation existants de Claude Code
- ajouter ou supprimer des serveurs MCP
- ajouter des métadonnées de marché Codex
- modifier le comportement d'exécution des compétences SEO elles-mêmes

## Fichiers impliqués

### Ajouté

- `.codex-plugin/plugin.json`

### Réutilisé comme source de vérité

- `.claude-plugin/plugin.json`
- `skills/`
- `assets/product-architecture.png`
- `AGENTS.md`

## Conception du manifeste

Le manifeste Codex reflète l'identité du plugin existant plutôt que d'introduire une deuxième identité de produit.

### Valeurs choisies

- `name`: `powehi-seo-geo`
- `version`: `2.2.9`
- `skills`: `./skills/`
- `displayName`: `Powehi Universal SEO`
- `developerName`: `Powehi`

Le manifeste comprend également:

- métadonnées du dépôt et de la page d'accueil
- un jeu minimal de mots clés pour la découverte
- une courte description de l'interface utilisateur orientée Codex
- trois instructions par défaut
- un actif de capture d'écran existant

## Relation avec l'emballage existant

Le dépôt expose désormais deux surfaces manifestes parallèles :

Surface
- Oui.
`.claude-plugin/plugin.json`
Découverte et validation du plugin `.codex-plugin/plugin.json`

C'est un ajout de compatibilité, pas une migration.

Le dépôt actuel reste Claude-premier dans sa documentation et son flux d'installation. Le nouveau manifeste Codex rend simplement ce même pack de compétences lisible à l'outil Codex.

## Vérification actuelle

La surface Codex est courante sur la branche `main` du dépôt au 2026-07-29:

- `.codex-plugin/plugin.json` et `.claude-plugin/plugin.json` déclarent la version `2.2.9`.
- Le manifeste Codex pointe vers le répertoire `./skills/` existant.
- Le validateur manifeste passe.
- Le contrôle de portabilité passe pour les 33 fichiers `SKILL.md` avec zéro erreur ou avertissement.

Cela confirme que la couche de compatibilité Codex est alignée avec la version actuelle du plugin; il ne prétend pas que le dépôt est un paquet de marché Codex.

## Validation effectuée

Le manifeste a été validé avec le plugin Codex validateur:

```bash
python <path-to-codex-plugin-validator> <path-to-this-repository>
```

Résultat de validation:

```text
Plugin validation passed
```

La vérification de portabilité est effectuée à partir de la racine du dépôt avec :

```bash
python scripts/portability_check.py
```

Résultat escompté :

```text
Portability lint: 33 SKILL.md files checked
  errors:   0
  warnings: 0
```

## Limites actuelles

Cette amélioration est intentionnellement minime. Quelques choses sont encore hors de portée:

### No Codex entrée du marché

La repo contient maintenant un manifeste Codex local valide, mais elle ne définit pas encore un chemin d'installation du marché Codex ou une entrée JSON du marché.

### Aucune application spécifique à Codex ou manifeste MCP

Le nouveau manifeste renvoie uniquement au répertoire `skills/` existant. Il n'ajoute pas actuellement:

- `.app.json`
- `.mcp.json`
- câblage de crochet spécifique à Codex

### Les métadonnées de l'interface utilisateur sont prudentes

Le bloc `interface` est valide et utilisable, mais intentionnellement léger. Il convient pour la compatibilité technique et la validation locale, pas encore pour la présentation du marché poli.

## Pourquoi le manifeste a été maintenu minimal

Un manifeste minimal réduit le risque de révision :

- moins de métadonnées dupliquées à maintenir
- moindre probabilité de dérive par rapport à `.claude-plugin/plugin.json`
- aucune capacité Codex-seulement spéculative
- une extension plus facile à l'emballage sur le marché

Cela facilite l'examen de la contribution en tant qu'amélioration de la compatibilité additive.

## Prochaines étapes recommandées

Si le responsable veut prendre en charge Codex, les prochaines étapes logiques sont :

1. document Codex installation et utilisation explicitement dans `README.md`
2. ajouter une entrée de marché Codex pour une installation locale ou distributable
3. décider si cette repo doit rester Claude-premier ou devenir duo-premier
4. enrichir le bloc `interface` avec copie finale du produit, branding et screenshots
5. ajouter Codex spécifique MCP ou l'application manifeste seulement lorsqu'il y a un besoin réel d'exécution

## Déroulement de la contribution pour ce changement

Cette amélioration doit être soumise en utilisant le flux de contribution normal du dépôt:

1. fourche le dépôt
2. créer une branche de fonctionnalité
3. faire et valider le changement localement
4. essai avec une cible d ' échantillon représentative, le cas échéant
5. ouvrir un PR qui explique ce qui a changé et pourquoi

Si le responsable demande une reproduction de type bug ou des preuves de suivi, le dépôt
Demande `CONTRIBUTING.md` :

- Version OS et Python
- sortie d'erreur complète du terminal
- la commande ou l'étape qui a échoué
- l'URL analysée, le cas échéant

Cette information est particulièrement utile ici si la rétroaction d'examen touche le comportement de validation,
compatibilité des emballages, ou ingestion manifeste de Codex.

### Règles de contribution à suivre

Tout travail de suivi sur cette couche de compatibilité Codex doit rester aligné sur le dépôt
règles de contribution:

- Les scripts Python doivent afficher JSON pour que l'agent hôte puisse analyser les résultats de manière fiable
- les scripts shell doivent utiliser `set -euo pipefail`
- Les fichiers `SKILL.md` doivent rester sous 500 lignes
- les fichiers de référence doivent rester concentrés et moins de 200 lignes
- répertoires et fichiers devraient utiliser kebab-case nommage
- les dépendances doivent rester minimales
- Le code Python doit suivre la PEP 8 et être vérifié avec `ruff check` ou `flake8` avant la soumission

Pour cette amélioration spécifique, ces règles soutiennent une stratégie de mise en œuvre étroite:

- conserver l'additif du manifeste Codex plutôt que de restructurer le repo
- éviter d'introduire de nouvelles dépendances d'exécution sauf si le support Codex les nécessite réellement
- garder les documents de référence ou de configuration spécifiques à Codex petits et ciblés
- préserver la disposition des compétences existantes au lieu de renommer les dossiers sans forte nécessité de compatibilité

## Note de l'examinateur

Ce changement visait à :

- additif
- faible risque
- compatible avec l ' arrière
- facile à valider mécaniquement

Il devrait être examiné comme une amélioration de la compatibilité des emballages plutôt que comme un changement architectural.
