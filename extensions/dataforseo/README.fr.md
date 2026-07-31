> **Langue :** Français | [English](README.md)

# Extension DataForSEO pour Powehi Universal SEO

Live SEO données via le [DataForSEO MCP serveur](https://github.com/dataforseo/mcp-server-typescript). Ajoute 23 commandes de données sur 9 modules API : analyse SERP, recherche par mot-clé, backlinks, analyse en page, analyse des concurrents, analyse de contenu, listes d'entreprises, vérification de la visibilité AI et suivi des mentions LLM.

## Préalables

- [Powehi Universal SEO](https://github.com/powehi-eu/powehi-seo-geo-universal) installé
- Node.js 20+
- [Compte DataForSEOZ](https://app.dataforseo.com/register) avec identifiants API

## Installation

### Unix/macOS/Linux

```bash
git clone https://github.com/powehi-eu/powehi-seo-geo-universal.git
cd powehi-seo-geo
./extensions/dataforseo/install.sh
```

### Windows

```powershell
git clone https://github.com/powehi-eu/powehi-seo-geo-universal.git
cd powehi-seo-geo
.\extensions\dataforseo\install.ps1
```

L'installateur:
1. Demander votre nom d'utilisateur et votre mot de passe DataForSEO
2. Installer les fichiers de compétence et d'agent
3. Configurer le serveur MCP dans `~/.claude/settings.json`
4. Prétéléchargez le paquet `dataforseo-mcp-server` npm

## Commandes

### Analyse du SERP

Description du commandement
Commande
Google bio SERP résultats (supporte également Bing/Yahoo via le paramètre `se`)
Google Images Résultats du SERP
Résultats de la recherche sur YouTube
Vidéo YouTube analyse profonde (info, commentaires, sous-titres)

### Recherche par mots clés

Description du commandement
Commande
Mots clés, suggestions et termes connexes
Volume de recherche pour la liste des mots-clés
Mots clés scores de difficulté
`/powehi-seo dataforseo intent <keywords>`
Données de Google Trends dans le temps

### Domaine & Analyse des concurrents

Description du commandement
Commande
Profil complet de rétrolien avec scores de spam
`/powehi-seo dataforseo competitors <domain>`=Les domaines concurrents et les estimations du trafic=
Mots clés un domaine se classe pour
Recoupement des mots-clés/backlink (2-20 domaines)
Estimation du trafic en vrac
Sous-domaines avec données de classement
`/powehi-seo dataforseo top-searches <domain>`=Les principales requêtes mentionnant le domaine

### Technique / Sur la page

Description du commandement
Commande
(Lighthouse + analyse du contenu)
Détection de la pile technologique `/powehi-seo dataforseo tech <domain>`
`/powehi-seo dataforseo whois <domain>`= Données d'enregistrement WHOIS

### Contenu et données commerciales

Description du commandement
Commande
`/powehi-seo dataforseo content <keyword/url>`= Analyse du contenu, recherche et tendances des phrases=
Recherche de listes d'entreprises

### Visibilité AI / GEO

Description du commandement
Commande
ChatGPT racleur web pour la visibilité GEO
LLM mentionne le suivi sur les plateformes AI

## Modules API ##

Les 9 modules DataForSEO sont activés :

Module d'utilisation d'exemple de commandes
-- -- -- -- -- -- -- -- -- -- -- -- --
Voir les résultats du moteur de recherche Serp, serp-youtube, youtube
Mots-clés DATA
DATAFORSEO LABS Mots clés recherche, compétiteurs Mots clés, difficulté, intention, compétiteurs, classés, sous-domaines, recherches top
Profils de liens Liens, intersection
(Lighthouse)
DOMAIN ANALYTIQUES Détection technique, WHOIS
DATA Business Listes d'entreprises
Qualité du contenu, tendances
AI OPTIMISATIONS ChatGPT, LLM mentionne Ai-scrape, ai-mentions

## Crédits API

DataForSEO charge par appel API. Les coûts de crédit varient selon le paramètre:

- **SERP** appelle: ~0.001-0.03 par demande
- **Mot-clé** recherche: ~0.0005-0.002 par mot-clé
- **Backlinks**: ~0.002-0.01 par demande
- **Analyse en page**: ~0,01-0,05 par page
- optimisation **AI**: ~0,05 par demande

Les nouveaux comptes comprennent une balance d'essai gratuite. Voir [DataForSEO price](https://dataforseo.com/pricing) pour les tarifs courants.

## Filtre de champ

L'extension comprend un `field-config.json` personnalisé qui réduit les tailles de réponse de l'API de ~75%, ne conservant que les champs pertinents de SEO. Cela économise les jetons et accélère l'analyse.

## Intégration avec Powehi Universal SEO

Une fois installé, d'autres compétences Powehi Universal SEO détectent automatiquement la disponibilité de DataForSEO et utilisent des données en direct :

- **`/powehi-seo audit`**:Utilise de vraies données SERP, backlink et on-page
- **`/powehi-seo technical`**:Utilise l'analyse en page pour des données techniques réelles
- **`/powehi-seo content`**:Utilise le volume de mots clés, les données de difficulté et d'intention
- **`/powehi-seo geo`**:Utilise le racleur ChatGPT et les mentions LLM pour les signaux GEO
- **`/powehi-seo plan`**:Utilise les données des concurrents et des mots clés pour la stratégie

## Dépannage

### Serveur MCP non connecté

1. Vérifier les identifiants : `cat ~/.claude/settings.json | grep DATAFORSEO`
2. Essai manuel: `npx -y dataforseo-mcp-server`
3. Réinitialisation: `./extensions/dataforseo/install.sh`

### Erreurs de l'API

- **401 Non autorisé**: Vérifiez le nom d'utilisateur/mot de passe dans settings.json
- **402 Paiement requis** : Ajouter des crédits à [app.dataforseo.com](https://app.dataforseo.com)
- **429 Taux limité**: attente et réessayer (DataForSEO a des limites par seconde)

### Module non disponible

Si une commande spécifique échoue, vérifiez que le module est dans `ENABLED_MODULES` dans votre settings.json. Tous les 9 modules devraient être énumérés.

## Désinstaller

### Unix/macOS/Linux

```bash
./extensions/dataforseo/uninstall.sh
```

### Windows

```powershell
.\extensions\dataforseo\uninstall.ps1
```

Cela supprime la compétence, l'agent, la configuration de champ et l'entrée du serveur MCP de settings.json.

## Liens

- [DataForSEO API Docs](https://docs.dataforseo.com/)
- [DataForSEO MCP Server](https://github.com/dataforseo/mcp-server-typescript)
- [Powehi Universal SEO](https://github.com/powehi-eu/powehi-seo-geo-universal)
