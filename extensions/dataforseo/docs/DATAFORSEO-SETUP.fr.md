> **Langue :** Français | [English](DATAFORSEO-SETUP.md)

# Configuration du compte DataForSEO

Guide étape par étape pour obtenir les identifiants d'API DataForSEO pour l'extension Powehi Universal SEO.

## 1. Créer un compte

1. Allez à [app.dataforseo.com/register](https://app.dataforseo.com/register)
2. Inscrivez-vous avec votre adresse électronique
3. Vérifier votre courriel

Les nouveaux comptes comprennent une balance d'essai gratuite pour les tests.

## 2. Trouver des identifiants d'API

1. Connectez-vous à [app.dataforseo.com](https://app.dataforseo.com)
2. Aller à **API Access** dans la barre latérale gauche
3. Vos références sont :
- **Nom d'utilisateur**: Votre adresse email enregistrée
- **Mot de passe**: Votre mot de passe API (réglé pendant l'enregistrement)

Ce sont les valeurs que vous entrerez lors de l'exécution de l'installateur d'extension.

## 3. Comprendre les crédits

DataForSEO utilise un système de crédit :

- Chaque appel API coûte un petit nombre de crédits
- Différents paramètres ont des coûts différents
- Les crédits sont achetés à l'avance
- Surveiller l'utilisation à [app.dataforseo.com/dashboard](https://app.dataforseo.com/dashboard)

**Coûts courants par appel, vérifiés au 2026-07-10:**

Type d'extrémité Coût approximatif
-- -- -- -- -- -- -- -- -- -- --
SERP (une seule requête)
Volume de mots clés (par mot clé)
Récapitulatif des liens arrière
Liste des liens arrière
Exploration sur la page (par page)
optimisation de l'IA (par appel) 0,05$

## 4. Manuel MCP Configuration

Si la configuration automatique de l'installateur échoue, ajoutez ceci à `~/.claude/settings.json` :

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "dataforseo-mcp-server"],
      "env": {
        "DATAFORSEO_USERNAME": "<account-username>",
        "DATAFORSEO_PASSWORD": "your-api-password",
        "ENABLED_MODULES": "SERP,KEYWORDS_DATA,ONPAGE,DATAFORSEO_LABS,BACKLINKS,DOMAIN_ANALYTICS,BUSINESS_DATA,CONTENT_ANALYSIS,AI_OPTIMIZATION",
        "FIELD_CONFIG_PATH": "/path/to/dataforseo-field-config.json"
      }
    }
  }
}
```

Remplacer le nom d'utilisateur, le mot de passe et FIELD CONFIG PATH par vos valeurs réelles.

## 5. Vérifier l'installation

Après l'installation, démarrez Claude Code et lancez :

```
/powehi-seo dataforseo serp test query
```

Si vous voyez les résultats de la recherche, l'extension fonctionne correctement.
