> **Langue :** Français | [English](README.md)

# Extension de génération d'images de banane pour Powehi Universal SEO

Générer des images SEO prêtes à la production en utilisant l'IA: prévisualisations OG/social, héros de blog,
photographie produit, infographie, et plus encore. Propulsé par Google Gemini via le
Banana Creative Director pipeline.

## Préalables

> Cette extension enveloppe [Claude Banana](https://github.com/AgriciDaniel/banana-claude)
> pour les cas d'utilisation spécifiques à SEO. Installez les compétences autonomes pour la génération d'images à usage général.

- **Powehi Universal SEO** installed (`~/.claude/skills/powehi-seo/`)
- **Node.js 20+** with npx
- **Google AI API key** (free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey))
- **ImageMagick** (optional, for post-processing)

## Installation

```bash
./extensions/banana/install.sh
```

L'installateur:
1. Vérifier que Powehi Universal SEO est installé
2. Demander pour votre clé API Google AI (si nanobanana-mcp n'est pas déjà configuré)
3. Installez les compétences et l'agent `seo-image-gen`
4. Configurer le serveur MCP dans `~/.claude/settings.json`

## Commandes

Commandement Ce qu'il fait
Commande
`/powehi-seo image-gen og <description>` OG/social preview image (1200x630 feel)
Blog image de héros (grand écran, dramatique)
Photographie de produit (propre, blanc BG)
`/powehi-seo image-gen infographic <description>`Q (vertical, data-heavy)
Personnalisé avec le pipeline Creative Director complet
Générer des variations N (par défaut: 3)

CSV batch planning helper:
```bash
powehi-seo-geo run --extension banana batch.py --csv requests.csv --model "$NANOBANANA_MODEL"
```

## Utiliser les cas par défaut

Taux d'utilisation de l'aspect Résolution de l'aspect Mode de domaine Prix
- C'est quoi ?
OG/Social Preview
Le blog Hero (en anglais seulement)
Photo du produit : 4 : 3 : 2K : Produit Vérifier le prix actuel
Infographie : 2 : 3 : 4K : Infographie : Vérifier les prix actuels
Place sociale de l'Union Européenne
Logo de vérification des prix courants

## Comment ça marche

Claude agit comme directeur exécutif**. Il ne transmet jamais de texte brut à l'API.
Au lieu de cela, il analyse votre intention, sélectionne le mode de domaine optimal, et construit
une prompte optimisée à l'aide d'un système de mémoire de raisonnement éprouvé à 6 composantes :

1. **Sujet** (30%): Spécificité physique et micro-détails
2. **Style** (25 %) : Caractéristiques de Camera, stock de films, références de marque
3. **Contexte** (15%):Lieu, temps, météo, éléments d'appui
4. **Action** (10 %) : Pose, geste, mouvement, état
5. **Composition** (10 %) : Type de tir, cadrage, focale
6. **Éclairage** (10%): Direction, qualité, température de couleur

## Post-génération SEO Liste de contrôle

Après chaque génération, Claude fournit :
- Proposition de texte Alt (riche en mots clés, descriptive)
- SEO-friendly fichier nommage convention
- Commande de conversion WebP
- Extrait de schéma ImageObject
- OG meta tag markup (pour les prévisualisations sociales)

## Intégration de la vérification

Pendant `/powehi-seo audit`, l'extension produit en option un agent d'analyse d'image qui :
- Audit des images OG/sociales existantes dans tout le site
- Indique les images manquantes ou de faible qualité
- Crée un plan de génération prioritaire avec des suggestions rapides
- Estimation du coût total du plan de production

L'agent ne produit jamais d'images. Il produit un plan pour votre examen.

## Désinstallation

```bash
./extensions/banana/uninstall.sh
```

Cela enlève l'habileté et l'agent. Si vous utilisez également [Claude Banana](https://github.com/AgriciDaniel/banana-claude),
la configuration du serveur MCP est conservée.

## Dépannage

Voir [docs/BANANA-SETUP.md](docs/BANANA-SETUP.md) pour les instructions de configuration détaillées
et des questions communes.
