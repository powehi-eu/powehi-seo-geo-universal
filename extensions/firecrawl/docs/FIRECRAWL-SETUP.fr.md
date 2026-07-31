> **Langue :** Français | [English](FIRECRAWL-SETUP.md)

# Guide de configuration Firecrawl

## 1. Obtenez votre clé API

1. Aller à [firecrawl.dev/app/sign-up](https://www.firecrawl.dev/signup)
2. Créer un compte gratuit (500 crédits/mois inclus)
3. Naviguez vers les touches **API** dans le tableau de bord
4. Copier votre clé API (démarre avec `fc-`)

## 2. Exécutez l'installateur

L'installateur gère tout automatiquement :

```bash
./extensions/firecrawl/install.sh
```

Il vous invite à utiliser votre clé API et à configurer le serveur MCP.

## 3. Manuel MCP Configuration

Si l'installateur échoue, ajoutez ceci à `~/.claude/settings.json` manuellement :

```json
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "fc-your-api-key-here"
      }
    }
  }
}
```

## 4. Vérifier l'installation

Démarrez Claude Code et essayez :

```
/powehi-seo firecrawl map https://example.com
```

Vous devriez voir une liste des URL découvertes. Si vous obtenez une erreur "outil non disponible", redémarrez Claude Code pour recharger les serveurs MCP.

## 5. Comprendre les crédits

Opérations Crédits utilisés
C'est quoi ?
1 par page rampée
1 par page
0.5 par URL découverte
1 par résultat retourné

**Étage gratuit**: 500 crédits/mois réinitialisent à votre date de facturation.

**Astuce**: Utilisez d'abord `map` (faible) pour voir combien de pages un site a, puis décider combien de `crawl` (plus cher).
