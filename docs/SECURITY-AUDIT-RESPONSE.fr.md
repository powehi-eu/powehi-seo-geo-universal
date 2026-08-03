> **Langue :** Français | [English](SECURITY-AUDIT-RESPONSE.md)

# Réponse à l'audit de sécurité

Réponse à l'audit de sécurité ClawHub de Powehi Universal SEO v2.2.9
(date de l'audit : 2026-08-01).

Les constats sont regroupés par issue : **corrigé** (code ou documentation
modifiés) ou **pas une vulnérabilité** (correspondance de motif du scanner,
avec justification documentée).

---

## Corrigé

### Désinstalleur trop large (High)

`uninstall.sh` et `uninstall.ps1` supprimaient chaque répertoire
`~/.claude/skills/seo-*` et chaque fichier `~/.claude/agents/seo-*.md`. Toute
skill tierce utilisant le même préfixe de nommage était supprimée sans aucun
avertissement.

**Correctif.** `install.sh` et `install.ps1` écrivent désormais un manifeste de
propriété dans `~/.claude/skills/powehi-seo/.install-manifest`, listant chaque
répertoire de skill et chaque fichier d'agent créés par l'installeur. Les
désinstalleurs ne suppriment que les entrées du manifeste, et rejettent toute
entrée contenant un séparateur de chemin ou `..`.

Les installations antérieures au manifeste retombent sur l'ancienne
énumération, mais affichent maintenant la liste complète des candidats et
exigent une confirmation interactive `y` (ou `--force` / `-Force`). Sans
confirmation, rien n'est supprimé, et dans un shell non interactif le
désinstalleur s'arrête plutôt que de deviner.

### Instructions de contournement des filtres de sécurité (High)

`skills/seo-image-gen/references/prompt-engineering.md` (et son miroir dans
`extensions/banana/`) documentait des stratégies de reformulation permettant de
faire passer des prompts bloqués à travers les filtres de sécurité de Gemini,
avec des exemples couvrant la violence, le gore, des mineurs en contexte à
risque, du contenu NSFW et des ressemblances de célébrités.

**Correctif.** Cette section a été remplacée par « When a Safety Filter Blocks a
Prompt ». Les conseils conservés ne couvrent que les faux positifs sur des
visuels marketing réellement inoffensifs, et limitent les nouvelles tentatives à
une seule. Les catégories ci-dessus constituent désormais une liste explicite de
sujets à ne pas tenter, avec pour consigne de signaler le blocage et de
s'arrêter plutôt que d'itérer sur la formulation. Les tableaux d'erreurs de
`gemini-models.md` et de `SKILL.md` ont été mis à jour en conséquence.

### Stockage d'identifiants sans information de l'utilisateur (High / Medium)

Les installeurs d'extensions écrivent des identifiants d'API dans
`~/.claude/settings.json`. L'installeur DataForSEO écrivait déjà de manière
atomique en mode `0600` et passait les identifiants par `argv`, mais aucun
installeur n'indiquait à l'utilisateur que la valeur est stockée en clair.

**Correctif.** Chaque invite de saisie d'identifiant, dans tous les installeurs
d'extensions (DataForSEO, Firecrawl, Ahrefs, SE Ranking, Profound, Bing
Webmaster, Banana ; `.sh` et `.ps1`), affiche désormais un avertissement de
stockage avant la lecture de la valeur : où elle est stockée, qu'elle l'est en
clair, qui peut la lire, et qu'il faut utiliser des identifiants révocables
chez le fournisseur.

Il s'agit d'une exposition réelle, et pas seulement d'un défaut d'information :
`settings.json` est lisible par tout processus tournant sous le compte de
l'utilisateur, ainsi que par tout outil de sauvegarde ou de synchronisation
couvrant le répertoire personnel. La révocation chez le fournisseur est le seul
remède complet en cas de fuite de clé.

### Exécution de commande dans le lanceur de hook (Critical, partiellement valide)

`hooks/run-python-hook.js` utilise `spawnSync` pour localiser un interpréteur
Python et exécuter le hook de validation de schéma. Aucun shell n'a jamais été
utilisé : il n'y avait donc pas d'injection de commande. Deux faiblesses de
durcissement étaient réelles :

1. `POWEHI_SEO_GEO_PYTHON` était accepté tel quel comme exécutable : un
   environnement corrompu pouvait diriger l'exécution du hook vers un programme
   arbitraire.
2. Le chemin du script de hook provenait d'`argv` sans aucune contrainte.

**Correctif.** La variable d'environnement n'est acceptée que s'il s'agit d'un
chemin absolu vers un fichier existant dont le nom de base correspond à
`python[0-9.]*(.exe)?` et ne contient aucun métacaractère de shell ; sinon elle
est ignorée avec un message sur stderr et l'ordre de détection normal
s'applique. Le script de hook doit se résoudre en un fichier `.py` existant
situé dans le répertoire `hooks/` du lanceur lui-même. Les deux appels
`spawnSync` passent maintenant explicitement `shell: false`.

Tests de non-régression : `tests/test_cross_platform_hooks.py` couvre le
confinement des chemins et le rejet de la variable d'environnement.

### Comportements de traitement des données non documentés (Medium, plusieurs constats)

L'audit signalait la fuite d'URL privées ou authentifiées vers des services
externes, la capture d'écran de pages authentifiées, les soumissions
d'indexation sans garde-fou, et des écritures de fichiers silencieuses.

**Correctif.** `skills/powehi-seo/SKILL.md` comporte désormais une section
**Data Handling Rules** opposable à chaque sous-skill et sous-agent : aucune
soumission d'URL non publique (localhost, IP privées, noms d'hôtes internes,
sous-domaines de préproduction, ou URL portant un jeton ou un identifiant de
session) à une API tierce ; confirmation explicite à chaque usage pour IndexNow,
l'API Google Indexing et toute étape de publication ; capture d'écran limitée
aux URL nommées par l'utilisateur, avec avertissement avant toute capture
derrière une authentification ; et aucune écriture hors d'un chemin indiqué par
l'utilisateur.

L'application au niveau réseau existait déjà : `scripts/url_safety.py`
(`validate_url_strict()` et les fonctions de requête à DNS épinglé) bloque les
IP privées, la boucle locale, les points de terminaison de métadonnées cloud,
ainsi que le rebinding par redirection et par DNS ; tout script qui récupère une
URL fournie par l'utilisateur passe par ce module.

### Modèles de tickets sans avertissement de caviardage (Medium)

**Correctif.** Les trois modèles de tickets GitHub (`bug_report.yml`,
`feature_request.yml`, `task.yml`) portent désormais un avertissement de
caviardage, répété dans la description du champ « Full error output ».
L'avertissement précise que les tickets sont publics et indexés, et qu'un
identifiant déjà publié doit être révoqué et remplacé : supprimer le ticket ne
le dépublie pas.

---

## Pas une vulnérabilité

### Exécution de code dynamique dans les tests (Critical, 3 occurrences)

- `tests/test_banana_api_key_safety.py:24`
- `tests/test_runtime.py:19`
- `tests/test_sync_flow.py:121`

Ces lignes appellent `importlib.util.spec_from_file_location()` puis
`spec.loader.exec_module()` pour importer des scripts du dépôt qui ne sont pas
empaquetés comme modules importables (`scripts/runtime.py`,
`scripts/sync_flow.py`).

Non exploitable, pour trois raisons indépendantes :

1. Le chemin est une constante dérivée de
   `Path(__file__).resolve().parents[1]`. Aucune entrée utilisateur, réseau ou
   variable d'environnement ne l'atteint.
2. Le fichier chargé est du code source du dépôt que le processus de test
   pourrait exécuter de toute façon. Le charger n'accorde aucune capacité
   supplémentaire à un attaquant capable de modifier le dépôt.
3. `tests/` n'est pas distribué. Ce répertoire n'est copié ni par `install.sh`,
   ni par `install.ps1`, ni par le manifeste du plugin : il n'atteint jamais la
   machine d'un utilisateur final.

C'est l'idiome standard pour tester un script dépourvu d'`__init__` de paquet,
et la détection porte sur le nom de l'API plutôt que sur un flux de données réel.
Aucune modification.

### Présence de `spawnSync` en elle-même (Critical)

Le lanceur doit démarrer un interpréteur Python : c'est toute sa raison d'être.
L'appel n'utilisait déjà aucun shell et passait un vecteur d'arguments. Voir
ci-dessus le durcissement appliqué aux parties réellement actionnables de ce
constat.

---

## Corrigé au passage

Ce ne sont pas des constats d'audit, mais de vrais défauts trouvés en traitant
le rapport :

- `install.ps1` cherchait la skill orchestratrice dans `skills\seo` ; le
  répertoire du dépôt est `skills\powehi-seo`. L'installation manuelle sous
  Windows échouait avec « Could not find skill source folder in repo clone. »
- `uninstall.ps1` et cinq installeurs d'extensions (`ahrefs`,
  `bing-webmaster`, `profound`, `seranking`, `unlighthouse`) vérifiaient le même
  chemin erroné `skills\seo` : l'installation de ces extensions sous Windows
  refusait de s'exécuter face à une installation de base pourtant correcte.
