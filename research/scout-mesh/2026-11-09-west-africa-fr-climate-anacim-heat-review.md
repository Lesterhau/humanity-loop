# Sénégal — bulletin provisoire de vérification des températures, 9–10 novembre 2026

**Cellule :** `west-africa-fr-climate` | **Statut :** `source_reviewed_provisional`, **PAS** une alerte météorologique ou sanitaire officielle. **Observation :** 2026-11-09 (UTC; time of source review not independently logged). **Permissions :** lecture de sources publiques et préparation d'un document à revoir ; aucun contact externe ni action de production.

## Action utile réalisée
Extraction structurée et vérification arithmétique de la grille de prévisions publiée dans le **texte indexé du site officiel de l'ANACIM** (Sénégal) pour les 9 et 10 novembre 2026. Fichier de données joint : [CSV de 38 observations](2026-11-09-west-africa-fr-climate-anacim-heat-grid-provisional.csv). Les 19 libellés de lieux sont conservés tels qu'affichés (par ex. `FATIC`, `ZIGUI`), sans les convertir en noms administratifs ni en stations certifiées.

**Relevé de maxima prévus ≥40 °C :**
- **9 novembre : 10/19 libellés** — BAKEL 40, DIOUR 40, FATIC 40, KAFFR 40, LINGU 40, LOUGA 41, MATAM 42, PODOR 41, SAINT 41, THIES 40.
- **10 novembre : 6/19 libellés** — BAKEL 42, LOUGA 41, MATAM 42, PODOR 40, SAINT 40, TAMBA 40.
- **Contrôle déterministe :** 38 enregistrements uniques (19 × 2 dates) ; chaque minimum est ≤ son maximum ; dénombrement du seuil reproduit 10 et 6. Le seuil ≥40 °C est **un filtre descriptif pour relecture**, pas un seuil de vigilance officielle ni un indice de risque clinique.

## Sources primaires et limites importantes
1. **ANACIM**, [site officiel et tableau de prévisions](https://anacim.sn/index.php) ; texte de recherche indexé consulté le 9 novembre 2026, montrant les trois dates 8–10 novembre. L'ouverture directe de la page a échoué par délai d'attente lors de ce contrôle. **Les données ci-dessus ne sont donc pas confirmées par une lecture directe ou une capture de navigateur.** Le texte narratif visible de prévision annonce une validité **du 6 novembre à 12h au 9 novembre à 12h**, alors que la grille indexée comprend le 10 novembre ; il peut s'agir de modules mis à jour à des cadences différentes. Il faut vérifier la date de génération et la validité de chaque module avant toute diffusion comme prévision actuelle.
2. **OMS**, [« Chaleur et santé » (31 juillet 2026)](https://www.who.int/fr/news-room/fact-sheets/detail/climate-change-heat-and-health), lu directement : limiter les efforts aux heures les plus chaudes, chercher l'ombre, maintenir l'hydratation et vérifier les avertissements locaux. L'OMS précise que l'exposition, l'humidité, l'acclimatation et les vulnérabilités individuelles influencent le risque ; la température maximale seule ne permet pas de qualifier une vague de chaleur.
3. **Anomalie à vérifier et non à corriger silencieusement :** `ZIGUI` affiche une minimale de **33 °C** les 9 et 10 novembre dans le texte indexé, contre **24 °C** le 8 novembre ; cela mérite une confirmation auprès d'un bulletin horodaté, mais ne prouve ni une erreur de prévision ni un risque supplémentaire.

## Produit utilisable pour une revue humaine (pas de diffusion automatique)
- Pour un acteur local de santé, d'école ou de protection civile : comparer la grille du jour à un **bulletin ANACIM horodaté et à la carte de vigilance officielle** ; consigner la date, la zone et l'heure, puis décider si une information préventive locale est appropriée. Ne pas appeler ce tableau « alerte ANACIM ».
- En attendant une confirmation, la **recommandation générale de l'OMS** peut être citée comme conseil non personnalisé, sans associer un diagnostic ni un statut d'alerte aux localités listées.
- **Critère de clôture de ce contrôle :** obtenir une capture de navigateur et/ou un bulletin ANACIM du 9–10 novembre avec validité explicite ; comparer `ZIGUI`, le module narratif et la grille ; noter `confirmé`, `corrigé` ou `inconnu`. S'il n'existe pas de source vérifiable, conserver le statut provisoire et ne pas contacter l'agence sans autorisation séparée.

**Contre-expertise (10th Man) :** Un moteur de recherche peut afficher un assemblage de modules d'âges différents ; un maximum de 40 °C n'est pas à lui seul une vague de chaleur ; des codes de lieux abrégés peuvent être ambigus. Ce dossier ne démontre ni défaut public confirmé, ni alerte manquée, ni décès, ni effet sur des bénéficiaires.

**Décision :** `verified_candidate_for_human_recheck`, pas `institutional_failure`. **Prochain contrôle non répété :** bulletin ANACIM direct et carte de vigilance pour les 9–10 novembre ; si indisponibles, revue d'une nouvelle source officielle à la prochaine échéance de la cellule. Aucun contact externe, appel de modèle Foundry, déploiement, coût AppDeploy, changement d'horaire ou effet réel n'est revendiqué.
