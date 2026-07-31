> **Langue :** Français | [English](google-seo-reference.md)

Mise à jour : 2026-07-10 -->
Référence rapide Google SEO (juillet 2026)

Guide de référence autonome obsolète. Il n'est connecté à aucun chemin de chargement subagent.
Résume les concepts clés de recherche Google, les exigences et les meilleures pratiques. Pas une reproduction de la documentation de Google;
Voir les liens de documentation officielle en bas pour plus de détails.

---

## Comment fonctionne la recherche Google

Google Search fonctionne en trois étapes : **Crawling** (Googlebot découvre les pages en suivant les liens et la lecture des plans du site), **Indexing** (Google traite et stocke le contenu, les métadonnées et les signaux des pages dans son index de recherche) et **Serving** (lorsqu'un utilisateur recherche, les algorithmes de Google classent les pages indexées par pertinence, qualité et facilité d'utilisation pour retourner les résultats les plus utiles). Les pages doivent être rampables et indexées pour apparaître dans les résultats de recherche.

---

## Recherche Google Essentiels

Autrefois connu sous le nom de "Webmaster Guidelines". Principales exigences:

### Exigences techniques
- Les pages doivent être accessibles à Googlebot (pas bloquées par robots.txt ou pas d'index)
- Les pages doivent retourner le statut HTTP 200 pour le contenu indexable
- Le contenu doit être dans un format Google peut traiter (HTML préféré, le contenu rendu JS pris en charge mais plus lent)

### Politiques de Spam
- Pas de cachette (montrant différents contenus à Googlebot vs utilisateurs)
- Pas de pages de porte (pages créées uniquement pour les requêtes spécifiques)
- Pas de texte ou de liens cachés
- Pas de mot-clé
- Aucun lien de spam (achat de liens, échanges de liens excessifs)
- Aucun contenu gratté ou généré automatiquement sans valeur ajoutée
- Pas de redirection sournoise
- Pas de pages d'affiliation minces

### Principales pratiques exemplaires
- Créer du contenu pour les utilisateurs, pas les moteurs de recherche
- Rendre votre site facile à naviguer avec une hiérarchie claire
- Utiliser des titres descriptifs uniques et des méta descriptions par page
- Utiliser les balises de cap (H1-H6) pour structurer logiquement le contenu
- Optimiser les images avec du texte alt et des tailles de fichiers appropriées
- Assurer un design adapté et adapté aux besoins des mobiles
- Servir des pages sur HTTPS pour la sécurité, la confiance et un signal de classement léger
- Améliorer la vitesse de chargement des pages (Core Web Vitals)
- Soumettre une carte de site XML à Google Search Console
- Utiliser des données structurées (JSON-LD) pour aider Google à comprendre le contenu

---

## Signaux de qualité du contenu

Google évalue la qualité du contenu à travers le cadre E-E-A-T:

- **Expérience**: Le créateur de contenu a-t-il une expérience directe avec le sujet? (Photos originales, histoires personnelles, utilisation démontrée)
- **Expertise**: Le créateur possède-t-il des connaissances ou des qualifications pertinentes? (Contexte professionnel, profondeur technique, approvisionnement précis)
- **Autorisation**: Le créateur ou le site est-il reconnu comme source d'accès? (Citations industrielles, mentions de marque, reconnaissance d'expert)
- **Fiabilité**: Le contenu et le site sont-ils fiables et transparents? (Coordonnées, site sécurisé, normes rédactionnelles, revendications précises)

> **YMYL Note** : Les sujets « Votre argent ou votre vie » (santé, finances, sécurité, juridique) sont classés selon les normes E-E-A-T les plus élevées. Un contenu YMYL inexact peut causer des dommages réels, donc Google applique des seuils de qualité plus stricts.

> **Note de portée**: E-E-A-T informe les systèmes de classement de base et de contenu utile de Google en général (pas seulement YMYL), mais Google n'a jamais publié un "scénario de décembre 2025" l'étendant à *toutes* requêtes concurrentielles, ni les chiffres de la baisse de trafic par industrie - traiter de telles allégations comme une interprétation de tiers, pas Google fait.

---

## Principaux éléments vitaux du Web

Mesuré au 75e centile des données réelles des utilisateurs (données de terrain).

Un bon besoin d'amélioration
- C'est quoi ?
**LCP** (Peinture la plus importante) ≤ 2,5s
**INP** (Interaction avec la peinture suivante)
**CLS** (Déplacement cumulatif)

** Principaux faits:**
- INP a remplacé FID (premier retard d'entrée) le 12 mars 2024. Le FID a été retiré des outils de données de champ de Chrome (CrUX API, PageSpeed Insights) sur Septembre 9, 2024 (Lighthouse est un outil de laboratoire qui n'a jamais signalé FID). NE PAS faire référence au FID.
- Core Web Vitals sont un signal de classement confirmé (depuis juin 2021)
- Les données de terrain (CrUX) sont préférées aux données de laboratoire (Lighthouse) pour l'évaluation
- Passer les trois mesures à "Bon" est la cible

**Outils de mesure:**
- Google PageSpeed Perspectives (champ + données de laboratoire)
- Rapport d'expérience utilisateur Chrome (CrUX): données de champ
- Phare (données de laboratoire seulement)
- Rapport de recherche Google Console Core Web Vitals

---

## Meilleures pratiques en matière de données structurées

- **JSON-LD est le format préféré de Google** (sur Microdonnées et RDFa)
- Placez JSON-LD dans les étiquettes `<script type="application/ld+json">` dans les `<head>` ou `<body>`
- Inclure toujours les propriétés `@context` et `@type`
- **Les biens requis** doivent être présents pour l'admissibilité aux résultats riches
- **Propriétés recommandées** améliorer la qualité des résultats riches mais ne sont pas obligatoires
- Indique uniquement le contenu visible sur la page
- Utilisez les résultats riches de Google Essai de validation avant déploiement
- Ne pas marquer un contenu trompeur ou caché aux utilisateurs
- Garder le schéma à jour : mettre à jour lorsque le contenu de la page change

### Types obsolètes ou restreints (en date de mai 2026)
- **HowTo**: Les résultats riches sont supprimés (septembre 2023)
- **FAQ** : Des résultats riches ont été retirés pour tous les sites (7 mai 2026). FAQPage reste un type valide de Schema.org, mais aucun bénéfice d'IA ou de classement n'est confirmé.
- **Annonce spéciale** : obsolète (31 juillet 2025)
- **CourseInfo, Estimation du salaire, ApprentissageVidéo**: Retraité (juin 2025)
- **Demande de révision**: retraité (juin 2025)
- **VehicleListing**: Retraité (juin 2025)

---

## Pénalités communes et comment les éviter

### Actions manuelles
Recherche Google Console notifications pour les violations. Causes fréquentes:
- ** Liens naturels** (achat/vente de liens): Désavouer les mauvais liens, demander un réexamen
- **This content**: Ajouter une valeur unique substantielle aux pages touchées
- **Redirections floues/incohérentes**: Supprimer la signification trompeuse, demander un réexamen
- **Pourriel généré par l'utilisateur**: commentaires/forums modérés, ajouter nofollow aux liens utilisateurs
- ** Problèmes de données structurées** : Correction du marquage trompeur ou spam

### Démotions algorithmiques
Aucune notification manuelle, détectée par des baisses de classement. Causes fréquentes:
- **Helpful Content System**: Fusionné dans le classement de Google en mars 2024: pas un système autonome. Les signaux d'aide sont maintenant évalués dans chaque mise à jour de base. Des contenus de faible valeur, générés par l'IA ou peu utiles à l'échelle déclenchent encore des démotions via des mises à jour de base.
- ** Mises à jour de base** : Réévaluation générale de la qualité de tous les signaux
- ** Mises à jour sur les pourriels** : détection automatisée des pourriels
- **Lien Mises à jour pourriel**: Dévaluation des profils de liaison manipulatrice

### Étapes de récupération
1. Identifier le problème (Search Console, analyse chronologique de classement)
2. Correction de la cause racine (supprimer le spam, améliorer le contenu, nettoyer les liens)
3. Pour les actions manuelles: soumettre une demande de réexamen via Search Console
4. Pour l'algorithmique: améliorer la qualité, attendre la prochaine réévaluation de la mise à jour de base
5. Surveiller la récupération dans les rapports de performance Search Console

---

## Liens de documentation officielle

- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [Comment fonctionne la recherche Google](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Aperçu des données structurées](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Rapport sur les éléments vitaux du Web de base](https://support.google.com/webmasters/answer/9205520)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Rechercher la console Help](https://support.google.com/webmasters)
- [Rapport sur les actions manuelles](https://support.google.com/webmasters/answer/9044175)
- [Statut de recherche Google Dashboard](https://status.search.google.com/)
- [Recherche Google Central Blog](https://developers.google.com/search/blog)
- [Politiques de diffusion](https://developers.google.com/search/docs/essentials/spam-policies)
- [Lignes directrices E-E-A-T et Quality Rater](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

> **L’indexation mobile-first** est la norme pour le Web indexé, et Googlebot Smartphone est le robot d’exploration principal (déploiement achevé en 2024). Une version mobile n’est pas strictement obligatoire — Google la recommande toutefois très fortement. Pour un site uniquement conçu pour ordinateur, le risque principal est une perte de contenu ou de parité, et non une exclusion automatique.
