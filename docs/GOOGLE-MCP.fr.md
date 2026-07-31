> **Langue :** Français | [English](GOOGLE-MCP.md)

# Intégration Google MCP

Ce dépôt prend en charge les preuves Google Search Console, GA4 et CrUX via
configurations standard MCP stdio pour Codex, Curseur et Code VS.

## Ordre de configuration

1. Installez le binaire `gsc-mcp` approprié à la plate-forme et l'exécutable `analytics-mcp` en amont
Google Suite MCP scripts d'installation.
2. Sur Windows, exécutez `powershell -ExecutionPolicy Bypass -File scripts/configure-google-mcp.ps1`; sur macOS/Linux, exécutez `bash scripts/configure-google-mcp.sh`. Ces scripts ajoutent une commande stable `gsc-mcp` à l'utilisateur `PATH`.
3. Créez ou sélectionnez les identifiants Google décrits ci-dessous.
4. Exportez les variables d'environnement avant de lancer l'éditeur ou l'agent.
5. Vérifier les fichiers et les autorisations avec la vérification d'authentification en amont.
6. Redémarrez le client pour recharger les définitions du serveur MCP.

Installateurs :

```powershell
.\scripts\install-google-gsc.ps1
.\scripts\install-google-ga4.ps1
```

```bash
./scripts/install-google-gsc.sh
./scripts/install-google-ga4.sh
```

Les installateurs téléchargent l'actif de sortie spécifique à la plate-forme GSC et installent
le GA4 MCP dans un environnement virtuel dédié. Ils ne stockent pas de binaires
ou des références dans ce dépôt. Pour un téléchargement GSC vérifié, set
`GSC_MCP_SHA256` au total de contrôle de la libération (insensible aux cas); installation
échoue si le bilan ne correspond pas. Le téléchargement est mis en scène dans un temporaire
fichier et déplacé seulement après vérification, donc un échec de vérification quitte
tout `gsc-mcp` précédemment installé n'a pas été modifié. Lorsque `GSC_MCP_SHA256` est défini
installateur re-télécharge et re-vérifie à chaque fois.

Sur une plate-forme, l'installateur ne reconnaît pas `GSC_MCP_RELEASE_ASSET`
le nom de l'actif à utiliser.

Les modèles de configuration sont :

- `.mcp.json` pour les clients compatibles Codex;
- `.cursor/mcp.json` pour le curseur;
- `.vscode/mcp.json` pour le code VS.

Installez séparément les exécutables `gsc-mcp` et `analytics-mcp` appropriés à la plate-forme, puis exposez
Ils sont sur `PATH`. Définir ces variables d'environnement dans le processus qui lance
le client:

- `GOOGLE_SERVICE_ACCOUNT_FILE`: chemin JSON du compte de service GSC;
- `GOOGLE_APPLICATION_CREDENTIALS`: GA4 le chemin OAuth client ou compte de service JSON;
- `GOOGLE_PROJECT_ID` : projet Google Cloud utilisé par le GA4 MCP.

L'intégration GSC utilise un compte de service avec accès à la propriété Search Console.
Activer l'API Search Console et ajouter le compte de service `client_email` à la
cible Rechercher la propriété Console. OAuth n'est nécessaire que pour un OAuth
Flux GSC; ils ne sont pas requis par le chemin MCP par défaut.

L'intégration GA4 accepte soit les identifiants du client OAuth, soit un compte de service
JSON. OAuth utilise la portée en lecture seule de l'analytique; un compte de service doit avoir
accès à la propriété GA4. JSON doit être valide UTF-8 sans BOM.
Les requêtes CrUX peuvent utiliser l'API publique; définir `CRUX_API_KEY` lorsque le quota est géré
l'accès est nécessaire.

Pour GA4 OAuth, utilisez :

```text
https://www.googleapis.com/auth/analytics.readonly
```

Pour un débit GSC basé sur OAuth, utilisez l'un des systèmes suivants:

```text
https://www.googleapis.com/auth/webmasters.readonly
https://www.googleapis.com/auth/webmasters
```

Le projet en amont fournit également les guides d'agrément français et anglais,
scripts d'installation, et `check-auth.ps1`:
[Google-suite-seo-mcp](https://github.com/bgrenat/google-suite-seo-mcp).

Après avoir installé des identifiants, exécutez `scripts/check-google-auth.ps1` sous Windows ou
`scripts/check-google-auth.sh` sur macOS/Linux. Les vérifications valident uniquement les exigences
JSON champs et jamais imprimer des clés ou des jetons privés.

`check-google-auth` et `check-google-mcp` résolvent les identifiants par
`GOOGLE_SERVICE_ACCOUNT_FILE` et `GOOGLE_APPLICATION_CREDENTIALS` — les mêmes
variables que les serveurs MCP lisent — et reviennent à `CODEX_SECRETS_DIR`
(par défaut `~/.codex/secrets/google`) lorsque ceux-ci ne sont pas exportés. A GA4 OAuth
fichier client est accepté si les clés sont assis au niveau supérieur (application
identifiants par défaut) ou imbriqués sous `installed` / `web` (un fichier client secret
téléchargé depuis la console Google Cloud).

## La matrice de la plate-forme

Plateforme de configuration
- Oui.
Fenêtres x64, `gsc-mcp-go-windows-amd64.exe`, `configure-google-mcp.ps1`
`gsc-mcp-go-darwin-arm64`
MacOS Intel (en anglais seulement) `gsc-mcp-go-darwin-amd64`
Linux x64: `gsc-mcp-go-linux-amd64`: `configure-google-mcp.sh`:
ARM64 de Linux `gsc-mcp-go-linux-arm64`

La configuration du dépôt appelle toujours la commande neutre `gsc-mcp`, donc
les fichiers de l'éditeur ne contiennent pas de chemins spécifiques à OS ou de suffixes exécutables.

Ne jamais commettre des fichiers JSON, clés privées, jetons de rafraîchissement, ou machine-
chemins absolus spécifiques. L'intégration en amont et ses scripts de configuration sont
maintenu dans [google-suite-seo-mcp](https://github.com/bgrenat/google-suite-seo-mcp).
