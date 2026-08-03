> **Langue :** Français | [English](SECURITY.md)

# Politique de sécurité

## Signaler une vulnérabilité

Si vous découvrez une vulnérabilité à la sécurité, veuillez le signaler de façon responsable. N'ouvrez pas un numéro public.

1. Ouvrez un privé [GitHub Security Advisory](https://github.com/powehi-eu/powehi-seo-geo-universal/security/advisories/new) sur ce dépôt (canal préféré).
2. En guise de retour, envoyez un courriel au responsable à l'adresse indiquée dans [`CITATION.cff`](CITATION.cff).
3. Chiffrer les divulgations sensibles si vous le pouvez. Demander la clé PGP du responsable dans l'avis ou l'e-mail — l'empreinte de la clé est publiée dans les fils de consultation sur première demande et est tournée chaque année.

Lors de la déclaration, veuillez inclure :

- Une brève description du problème et de l'impact que vous croyez avoir.
- Un reproducteur minimal (URL, ligne de commande, charge utile ou script court).
- Versions et plateformes affectées.
- Si vous avez une solution.

## Communication coordonnée

powehi-seo-geo suit une politique de divulgation coordonnée ** de 90 jours**.

Journée Événement
-- -- -- -- -- --
Le responsable accuse réception.
Le triage initial : classification de gravité (CVSS v3.1) et confirmation de reproductibilité.
Atténuation ou correction proposée.
Correction publiée dans une version patch ou backport; journaliste crédité dans les notes de sortie (opt-out disponible). - Oui.
Un avis public publié sinon plus tôt.

Si un correctif ne peut pas être expédié dans les 90 jours, le responsable demandera une extension avec une raison technique claire. Le journaliste conserve le droit de divulguer à 90 jours.

## Version supportée

Version ligne de l'état Notes
- Oui.
Entièrement pris en charge : Développement actif ; sécurité et corrections de bogues.
**1.9.x** (seulement pour la sécurité)
S'il vous plaît mettre à niveau.

## Modèle de menace

powehi-seo-geo est une boîte à outils de recherche et d'audit qui fonctionne sur le poste de travail d'un utilisateur. Il accepte les URL et les identifiants fournis par l'utilisateur, et émet des requêtes HTTP contre des hôtes Internet arbitraires. Le modèle de menace comporte trois principaux types d'agresseurs :

1. **Cible d ' audit raisonnable.** Un site l'utilisateur pointe powehi-seo-geo à des tentatives de fuite de données de réseau local ou de métadonnées de cloud via les chaînes SSRF: privé IP litters, décimal/hex/octal IPv4, FQDN dot trailing, 30x redirige vers des IP privés, reliure DNS (résolution publique initiale → plus tard privé), IPv4-maped IPv6, hôtes double-stack avec un enregistrement privé.

**Mitigation:** `scripts/url_safety.py` est la couche canonique pré-vol + DNS. Chaque script de saisie d'URL dans ce dépôt valide à travers lui. Voir `tests/test_url_safety.py` pour la suite de régression (91 cas sur 31 fonctions d'essai, couvrant chaque classe de contournement).

2. **Installation tapée.** Un plugin modifié, une version GitHub ou un script d'installation manuelle pourraient fournir des fichiers modifiés. Plugin install est le chemin par défaut; `curl ... | bash` est le chemin legs/manuel, de sorte que la vérification de la signature des artefacts de libération reste une préoccupation de défense en profondeur.

**État d'atténuation:** outillage manifeste SHA-256 expédié dans v2.0.0; vérification du script d'installation est suivi pour v2.3. Jusqu'à ce que les scripts d'installation vérifient les manifestes, les utilisateurs peuvent installer en clonant explicitement la balise et en inspectant la diff contre la version précédente.

3. **Progression des privilèges locaux contre les lettres de créances stockées.** Le jeton OAuth de `~/.config/powehi-seo-geo/oauth-token.json` est l'artefact le plus sensible sur disque.

**Mitigation:** v2 force `0o600` sur chaque écriture (`os.open` + `os.fchmod`) et remédie aux anciens fichiers `0o644` en place sur la première charge. Les jetons ne contiennent jamais l'OAuth `client_secret` — seulement la paire access/refresh et les métadonnées d'expiration.

4. **Environnement hostile contre la couche de hooks.** Un hook qui résout et lance un interpréteur externe peut être détourné par une variable d'environnement corrompue ou un chemin de script fourni par un attaquant, ce qui en ferait un lanceur de programmes arbitraires.

**Mitigation:** supprimé par conception en v2.2.12. La validation de schéma est désormais `hooks/validate-schema.js`, exécuté directement par Node (garanti présent dans le harnais) et n'utilisant que `fs` et `path`. Il ne démarre aucun sous-processus, ne résout aucun interpréteur et n'importe pas `child_process`. Rien sous `hooks/` ne lance de processus. Contrat complet : `hooks/README.md`. Non-régression : `tests/test_cross_platform_hooks.py`, qui vérifie l'absence de `child_process`, `spawnSync`, `execSync` et `execFileSync` dans chaque fichier `hooks/*.js`.

## Risques résiduels connus

- **Playwright + Chrome DNS reliure.** Le chrome fait sa propre résolution DNS dans le processus de rendu. La pin DNS (`url_safety._pin_dns`) de powehi-seo-geo ne peut pas l'atteindre. Le gestionnaire Playwright `route()` valide à nouveau chaque hôte de sous-ressources (`make_safe_playwright_route_handler`), qui ferme le cas commun, mais un véritable attaquant reliant peut encore courir le résolveur de Chrome après notre retour avant vol. Atténuation: ne pointez pas les compétences `/powehi-seo` sur des sites non fiables avec des redirections à haute fréquence.
- **Objectifs d'audit IPv6 uniquement.** Le validateur strict interroge `family=AF_INET` pour la résolution initiale. Les hôtes avec des enregistrements AAAA seulement feront surface comme « résolution DNS échouée ». C'est **fail-fermé** par conception — nous préférons refuser de nous connecter à un paramètre IPv6 non validé. Suivi d'un patch futur (pénage complet à double prise, similaire au gestionnaire Playwright qui utilise déjà `AF_UNSPEC`).
- **Les permissions de fichiers Windows.** `os.fchmod(fd, 0o600)` est un non-op sur Windows pour les systèmes de fichiers non-ACL. Les utilisateurs de Windows devraient compter sur les ACL de répertoire par utilisateur au lieu des bits de mode POSIX.
- **Credentials d'extensions dans `~/.claude/settings.json`.** Les serveurs MCP reçoivent leurs credentials via le bloc `env` du harnais : les clés d'API d'extensions y sont donc nécessairement stockées en clair. Les installeurs écrivent le fichier de manière atomique en `0600` et passent les secrets par `argv` (jamais interpolés dans un corps de script), et chaque invite de saisie annonce désormais l'exposition avant de lire une valeur — mais tout processus tournant sous le compte de l'utilisateur, et tout outil de sauvegarde ou de synchronisation couvrant le répertoire personnel, peut malgré tout le lire. Considérez une clé traitée ainsi comme révocable à la demande : la révocation chez le fournisseur est le seul remède complet en cas de fuite. Suivi pour un correctif ultérieur (intégration au trousseau du système d'exploitation là où le harnais offre une indirection).

## Chemins de code relatifs à la sécurité

Si vous auditez, ce sont les fichiers à haut niveau de levier :

| Fichier | Objet |
|---|---|
| `scripts/url_safety.py` | Module canonique SSRF / DNS rebinding. |
| `scripts/render_page.py` | Rendu headless partagé (Playwright + trafilatura). |
| `scripts/fetch_page.py` | Récupérateur HTTP brut bâti sur `url_safety.safe_requests_session`. |
| `scripts/capture_screenshot.py` | Capture d'écran Playwright avec gestionnaire de route sûr. |
| `scripts/google_auth.py` | Cycle de vie du jeton OAuth, écritures en `chmod 0o600`. |
| `scripts/backlinks_auth.py` | Chargement des credentials d'API backlinks ; garde SSRF via `url_safety`. |
| `tests/test_url_safety.py` | Batterie de non-régression de 91 cas couvrant chaque classe de contournement. |
| `hooks/validate-schema.js` | Validation de schéma ; built-ins Node uniquement, aucun sous-processus. |
| `hooks/README.md` | Conception et contrat des hooks. |
| `install.sh` / `install.ps1` | Génération du manifeste de propriété de l'installation. |
| `uninstall.sh` / `uninstall.ps1` | Suppression limitée au manifeste ; confirmation exigée pour les installations anciennes. |

## Ce que cette politique fait **ne couvre pas**

- Bugs qui nécessitent le contrôle de l'attaquant de la machine de l'utilisateur (tout attaquant local est déjà fini).
- Vulnérabilités dans les dépendances en amont — veuillez les signaler à leurs responsables respectifs. Nous suivons les CVE dans `requirements.txt` et les broches de bosse sous le flux `deps:` Dependabot.
- Problèmes de qualité de sortie (recommandations SEO, erreurs de schéma, etc.) - ce sont des bogues, pas des problèmes de sécurité.

## Pratiques liées à la sécurité

- Pas d'identifiants ou de clés d'API liés à ce dépôt. `.gitignore` bloque chaque modèle de nom de fichier reconnu.
- Installer les scripts en écriture uniquement dans les répertoires de niveau utilisateur sous `~/.claude/` et `~/.config/powehi-seo-geo/`.
- Les dépendances de Python s'installent dans un environnement virtuel isolé. Les installateurs de greffons utilisent le `CLAUDE_PLUGIN_DATA` persistant; les installateurs manuels utilisent le `~/.claude/skills/powehi-seo/.venv/`. L'exécution ne revient jamais à l'installation globale ou du paquet utilisateur.
- Chaque nouveau récupérateur doit passer par `scripts/url_safety.py` — il n'y a pas d'exception pour les URL "confiées".
- Les skills et sous-agents appliquent les **Data Handling Rules** de `skills/powehi-seo/SKILL.md` : aucune soumission d'URL non publique à une API tierce, confirmation explicite à chaque usage pour les effets d'indexation et de publication, capture d'écran limitée aux URL nommées par l'utilisateur, et aucune écriture hors d'un chemin indiqué par l'utilisateur.
- Les désinstalleurs ne suppriment que les chemins enregistrés dans le manifeste d'installation (`~/.claude/skills/powehi-seo/.install-manifest`). Les installations antérieures au manifeste retombent sur l'énumération `seo-*`, mais affichent la liste complète des candidats et exigent une confirmation explicite ; un shell non interactif s'arrête plutôt que de deviner.
- Les modèles de tickets portent un avertissement de caviardage. Les tickets sont publics et indexés : un credential publié doit être révoqué et remplacé, car supprimer le ticket ne le dépublie pas.

## Historique des audits

| Date | Auditeur | Périmètre | Réponse |
|---|---|---|---|
| 2026-08-01 | Audit de sécurité automatisé ClawHub | Plugin v2.2.9, dépôt complet | [docs/SECURITY-AUDIT-RESPONSE.fr.md](docs/SECURITY-AUDIT-RESPONSE.fr.md) |
| 2026-08-03 | Audit de sécurité automatisé ClawHub (relancé) | Plugin v2.2.10, dépôt complet | [Section de suivi](docs/SECURITY-AUDIT-RESPONSE.fr.md#suivi--ré-audit-de-la-2210) |
| 2026-08-03 | Audit de sécurité automatisé ClawHub (relancé) | Plugin v2.2.11, dépôt complet | [Section de suivi](docs/SECURITY-AUDIT-RESPONSE.fr.md#suivi--ré-audit-de-la-2211) |

Le document de réponse indique, constat par constat, s'il a été corrigé ou classé comme faux positif du scanner, avec la justification.
