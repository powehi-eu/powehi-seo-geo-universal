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

## Risques résiduels connus

- **Playwright + Chrome DNS reliure.** Le chrome fait sa propre résolution DNS dans le processus de rendu. La pin DNS (`url_safety._pin_dns`) de powehi-seo-geo ne peut pas l'atteindre. Le gestionnaire Playwright `route()` valide à nouveau chaque hôte de sous-ressources (`make_safe_playwright_route_handler`), qui ferme le cas commun, mais un véritable attaquant reliant peut encore courir le résolveur de Chrome après notre retour avant vol. Atténuation: ne pointez pas les compétences `/powehi-seo` sur des sites non fiables avec des redirections à haute fréquence.
- **Objectifs d'audit IPv6 uniquement.** Le validateur strict interroge `family=AF_INET` pour la résolution initiale. Les hôtes avec des enregistrements AAAA seulement feront surface comme « résolution DNS échouée ». C'est **fail-fermé** par conception — nous préférons refuser de nous connecter à un paramètre IPv6 non validé. Suivi d'un patch futur (pénage complet à double prise, similaire au gestionnaire Playwright qui utilise déjà `AF_UNSPEC`).
- **Les permissions de fichiers Windows.** `os.fchmod(fd, 0o600)` est un non-op sur Windows pour les systèmes de fichiers non-ACL. Les utilisateurs de Windows devraient compter sur les ACL de répertoire par utilisateur au lieu des bits de mode POSIX.

## Chemins de code relatifs à la sécurité

Si vous auditez, ce sont les fichiers à haut niveau de levier:

Dossier Objet
- Oui.
Module canonique reliure DNS / SSRF.
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Récupérateur Raw-HTTP construit sur `url_safety.safe_requests_session`.
La capture d'écran de Playwright avec un gestionnaire de route sûr.
Le cycle de vie du jeton OAuth `scripts/google_auth.py`, écrit `chmod 0o600`. - Oui.
`scripts/backlinks_auth.py`= Chargement des justificatifs de rétrolien-API; garde SSRF via `url_safety`.=
La batterie de régression `tests/test_url_safety.py` de 91 cas couvre chaque classe de contournement.

## Ce que cette politique fait **ne couvre pas**

- Bugs qui nécessitent le contrôle de l'attaquant de la machine de l'utilisateur (tout attaquant local est déjà fini).
- Vulnérabilités dans les dépendances en amont — veuillez les signaler à leurs responsables respectifs. Nous suivons les CVE dans `requirements.txt` et les broches de bosse sous le flux `deps:` Dependabot.
- Problèmes de qualité de sortie (recommandations SEO, erreurs de schéma, etc.) - ce sont des bogues, pas des problèmes de sécurité.

## Pratiques liées à la sécurité

- Pas d'identifiants ou de clés d'API liés à ce dépôt. `.gitignore` bloque chaque modèle de nom de fichier reconnu.
- Installer les scripts en écriture uniquement dans les répertoires de niveau utilisateur sous `~/.claude/` et `~/.config/powehi-seo-geo/`.
- Les dépendances de Python s'installent dans un environnement virtuel isolé. Les installateurs de greffons utilisent le `CLAUDE_PLUGIN_DATA` persistant; les installateurs manuels utilisent le `~/.claude/skills/powehi-seo/.venv/`. L'exécution ne revient jamais à l'installation globale ou du paquet utilisateur.
- Chaque nouveau récupérateur doit passer par `scripts/url_safety.py` — il n'y a pas d'exception pour les URL "confiées".
