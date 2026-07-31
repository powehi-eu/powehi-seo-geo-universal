> **Langue :** Français | [English](MIGRATION-v1-to-v2.md)

# Migration de powehi-seo-geo v1.x à v2.0.0

v2 est **compatible vers l'arrière par conception**. Chaque invocation v1.x CLI, chaque
signature de script, et chaque commande d'habileté fonctionne toujours. La rupture
les modifications sont limitées à deux surfaces étroites:

1. L'héritage du retour de `backlinks_auth.py` (IP privés en silence)
a été enlevé. Si `scripts/url_safety.py` ne peut pas être importé,
module soulève désormais `RuntimeError` au moment de l'importation au lieu de courir
avec protection SSRF désactivée.
2. Six types de résultats riches `Schema.org` Google retraité en 2025 sont maintenant
marqués comme des constatations critiques lorsque la compétence `seo-schema` les détecte
(Liste des véhicules, examen des demandes, salaire estimatif, vidéo d'apprentissage,
Annonce spéciale, cours Info carrousel). Sites encore générateurs
ceux-ci dans les blocs `<script type="application/ld+json">` verront un nouveau
Ligne critique dans la sortie de l'audit.

Tout le reste est additif — nouvelles commandes, nouveaux scripts, nouvelle référence
fichiers, nouvelles extensions. Les rapports d'audit existants seront légèrement plus complets.
Mais utilisez exactement la même structure globale.

Ce guide couvre le v1.x → v2.0.0 saut seulement; le v2.1.0 à v2.2.4
les rejets sont documentés dans [../CHANGELOG.md](../CHANGELOG.md), et
suite est maintenant à 410 tests.

## Quoi de neuf en v2

### Fondation

- **`scripts/url_safety.py`** est la reliure canonique SSRF + DNS
module. Chaque ramasseur y passe. Cinq contournements distincts
les classes sont fermées au moment de l'analyse, y compris IPv4 obfusqué (décimal,
hexagone, octal, zéros de tête), dérivations FQDN et les
redirection-reliure chaîne.
- **`scripts/render_page.py`** est le rendu sans tête partagé. Chaque
Le sous-agent de recherche l'appelle maintenant avec `--mode auto`, donc les sites SPA (Réagir,
Next.js, Vue, Nuxt, Svelte, Astro îles) sont vérifiés correctement
sans adaptation par compétence.
- **Les permissions de jeton OAuth** sont forcées à `0o600` pour chaque charge
et sauver. Les fichiers Legacy `0o644` (par défaut pré-v2) sont corrigés dans
lieu au prochain appel à `_load_oauth_token`.

### Qualité du contenu (phase B)

Nouveau Ce qu'il fait
- Oui.
`python3 scripts/content_quality.py`=Remplisseur aligné QRG / profil AI / marqueur de densité d'information=
40+ remplacements déterministes de phrasés AI
`python3 scripts/content_verify.py`= Extraction de la réclamation + détection d'écart de citation
`python3 scripts/domain_history.py`
Mots-clés : `python3 scripts/seo_updates.py`
18 mises à jour Google confirmées 2024-03 → 2025-12

### Profondeur technique / CWV (phase C)

Nouveau Ce qu'il fait
- Oui.
Règles de spécification + bfcache + prérender + LCP audit précharge
Envoyer jusqu'à 10k URLs à IndexNow (Bing/Yandex/Seznam/Naver)
La décomposition de LCP par `python3 scripts/lcp_subparts.py` (TTFB, délai de charge, durée de charge, délai de rendu)
Le phare de plusieurs pages `python3 scripts/unlighthouse_run.py` par le MIT Unlighthouse CLI

### (phase D)

Nouveau Ce qu'il fait
- Oui.
JSON-LD générateurs pour les quatre types v2 à haut levier
Validateur de la politique de schéma de produit (hasMerchantRetourPolitique, expéditionDétails, Programme des membres, Classe énergétique de l'UE, Groupe de produits)
Référence: chaque type de résultat riche retraité avec son remplacement

### Recherche AI + 5 nouvelles extensions (phase E)

Nouveau Ce qu'il fait
- Oui.
`python3 scripts/parasite_risk.py`.Scanner de risque d'abus-réputation par nov 2024 Politique Google
Le serveur officiel `@ahrefs/mcp` est connecté à Claude Code
`extensions/seranking/`=I Part-of-Voice sur ChatGPT/Gemini/Perplexité/AI Aperçus/mode AI
`extensions/profound/`=Série chronologique LLM citation tracker=
Bing Webmaster + IndexNow unifié
`extensions/unlighthouse/`
`skills/seo-geo/references/llmstxt-evidence.md`=Reframe basé sur des preuves: llms.txt n'est pas un levier de citation=

### Local + International + Vernis de confidentialité (phase F)

Nouveau Ce qu'il fait
- Oui.
`python3 scripts/gbp_deprecation_lint.py`=Détecte le chat GBP retraité; traite `.business.site` comme non résolu et Q&A comme un examen seulement=
`skills/seo-google/references/dma-consent-mode-v2.md`= Diagnostic CTR UE + cadrage adouci sans cookies=
`skills/seo-hreflang/references/machine-translation-qa.md`=Détection non traduite-MT par janvier 2025 QRG §4.6.5=

### Portabilité multiplateforme (phase G)

Nouveau Ce qu'il fait
- Oui.
`AGENTS.md` (prolongé)
`python3 scripts/portability_check.py`=Lint avant de la plate-forme transversale SKILL.md
Tableau de compatibilité avec les noms d'outils

### Signature de sortie (phase H)

Nouveau Ce qu'il fait
- Oui.
Générer un manifeste SHA-256 de chaque fichier suivi par git
`python3 scripts/verify_release.py`.Vérifier une commande contre un manifeste signé.

### En durcissant

- **Reliure du DNS via la cible de redirection** (gravité de l'HIGH) — fermé.
- **Parallèle IPv4 obfusquée** dans `validate_url` (HIGH) - fermé.
- **Parallèle FQDN à point de fuite** de la liste de points d'entrée des métadonnées (HIGH) - fermé.
- **Point mort IPv6 dans le gestionnaire de route Playwright** (MEDIUM) — fermé.
- **Oauth fichier-permission TOTCOU** (LOW) — fermé.
- **Scénarios d'installation non signés:** partiellement clos; manifeste de libération
outillage expédié dans v2.0.0, install.sh intégration suivi pour v2.3.

## Changements de rupture (liste complète)

Il y a exactement deux ruptures visibles de surface :

### 1. `backlinks_auth.py` hard-fails without `url_safety`

```python
# v1.x
from backlinks_auth import validate_url  # silently uses unsafe fallback
                                          # if url_safety not importable

# v2.x
from backlinks_auth import validate_url  # raises RuntimeError if
                                          # url_safety can't be imported
```

Il s'agit de la clôture d'un élément de sécurité reporté de v19.0. Le v1.x
replis expédiés sans contrôle de portée IP; nous préférons refuser de courir
Permettre silencieusement le transfert privé.

### 2. `seo-schema` flags retired rich-result types as Critical

Si votre JSON-LD généré inclut `@type: ClaimReview`, `Vehicle`,
`EstimatedSalary`, `LearningVideo`, `SpecialAnnouncement`, ou
`CourseInfo` (variante carrousel), la nouvelle
`scripts/schema_ecommerce_validate.py` émettra une recherche `Critical`.

**Action:** consulter `skills/seo-schema/references/deprecated-types-2024-2026.md`
pour le remplacement recommandé par type. Si vous avez besoin de
balisage à des fins non-Google, vous pouvez supprimer la conclusion en supprimant
le type de la liste dépréciée du validateur (non recommandé —
le résultat riche est mort).

## Des choses qui allaient casser mais qui n'ont pas

Nous avons considéré, mais en fin de compte, que **pas** ne cassent ce qui suit:

- `validate_url` contrat de retour booléen. v2 retourne toujours `bool` pour
C'est du dos-compat. Utilisez `validate_url_strict` si vous voulez le nouveau strict
comportement de reliure DNS.
- Signature de la fonction `fetch_page()`. Le drapeau `--render` a été ajouté au
CLI couche seulement ; la fonction sous-jacente reste en mode brut par défaut.
- API `capture_screenshot()`. Pré-vol est amélioré mais l'appel
la signature et les résultats sont inchangés.
- Tous les noms de commande v1.x (`/powehi-seo audit`, `/powehi-seo content`, ...). Chaque
l'un d'eux fonctionne en v2.

## Comment mettre à jour

Attention: Préférez télécharger, inspecter, puis exécuter des scripts à distance; le formulaire pipe-to-shell ci-dessous est l'option de commodité moins sûre.

```bash
# Pull v2.0.0
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh | bash

# Vérifier les nouvelles exigences pin débarqué
pip installation -r requirements.txt

# Confirmer que Playwright Chrome est installé (utilisé par rendu page)
dramaturge installer chrome

# Verify manifest consistency
python3 -m pytest tests/test_manifest_consistency.py -v
```

C'est ça. La première fois que vous lancez tout ce qui touche
`~/.config/powehi-seo-geo/oauth-token.json`, v2 va le re-chmod en silence
à `0o600` — aucune action utilisateur requise.

## Couverture des essais

Suite: v1.9.9.
-- -- -- -- -- -- -- -- --
Manifeste de consistance
Détection par labyrinthe
Synchronisation FLOW
**`url_safety` (nouveau)**
**`render_page` (nouveau)**
**Qualité du contenu (nouveau)**
**Profondeur technique (nouveau)**
**Schema v2 (nouveau)**
**Risque de départ + extensions (nouveau)**
Linge et vernis (nouveau)
**Portabilité (nouveau)**
Total**

v2 ajoute 209 nouveaux cas d'essai (5.4× la base de v1) couvrant chaque nouveau
modes de défaillance de la fonction plus toutes les classes de contournement SSRF connues.
