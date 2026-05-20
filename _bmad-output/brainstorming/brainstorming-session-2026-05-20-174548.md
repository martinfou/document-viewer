---
stepsCompleted: [1, 2]
inputDocuments: []
session_topic: 'Onglet Document viewer sur fiche client JSP : liste de documents client + viewer embarqué (PDF, JPEG — TIFF hors périmètre pour l''instant), sélection rapide, mocks et livrables BA/QA'
session_goals: 'Mockups statiques et jouables, liste de fonctionnalités, périmètre MVP, options additionnelles avec estimations de durée; alternatives UX au modèle « un bouton par fichier »; clarifier libs JS existantes; livrables analyste d''affaires; livrables QA (stratégie de test, cas de test, critères de recette, matrices de couverture)'
selected_approach: 'progressive-flow'
techniques_used: ['Morphological Analysis', 'Solution Matrix', 'SCAMPER Method', 'Decision Tree Mapping']
ideas_generated: ['A1-A10 disposition', 'M1-M3 mocks client', 'B1-B12 axe liste', 'secteur assurance-banque', 'axe C viewer', 'demos HTML native + CDN']
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** breaking-code
**Date:** 2026-05-20

## Session Overview

**Topic:** Visionneur de documents embarqué (PDF, JPEG) dans pages HTML/JSP, avec sélection rapide des documents d'un dossier et maquettes interactives pour recueillir du feedback. **TIFF : retiré du périmètre actuel.**

**Goals:**
- Produire des mockups (statiques et **jouables** pour tests utilisateurs)
- Liste de fonctionnalités, définition **MVP** vs **options additionnelles**
- **Estimations de durée** par lot
- Explorer des patterns UX de **sélection de documents** (remplacer les boutons « un fichier = un bouton »)
- Tenir compte : JSP + JSP tags pour le layout; inventaire des librairies JavaScript du projet **à faire**
- **Livrables analyste d'affaires** : documentation formelle pour cadrage, validation métier et passage en développement

### Business Analyst Deliverables (cible de fin de parcours)

| Livrable | Rôle |
|----------|------|
| **Résumé / contexte métier** | Problème, parties prenantes, périmètre |
| **Cas d'usage** | Acteurs, flux principaux et alternatifs (ouvrir dossier, sélectionner doc, consulter PDF/JPEG) |
| **Exigences fonctionnelles** | Liste numérotée, testable (viewer embedded, formats, navigation) |
| **Exigences non fonctionnelles** | Perf, navigateurs, accessibilité, sécurité des fichiers |
| **Critères d'acceptation** | Par exigence ou par story — base pour recette |
| **Matrice de traçabilité** | Exigence ↔ mock ↔ composant JSP (optionnel mais utile) |
| **Backlog structuré** | Epics / stories dérivées du MVP et des options |
| **Glossaire** | Termes métier (dossier, document, visionneuse, etc.) |

_Note : les mocks jouables servent de support BA (validation UX) ; la Phase 4 (Decision Tree) produira la structure MVP/options/temps que l'on transformera en ces artefacts._

### QA Deliverables (cible de fin de parcours)

| Livrable | Rôle |
|----------|------|
| **Stratégie de test** | Périmètre, niveaux (unitaire, intégration, UI, recette), risques |
| **Plan de test** | Calendrier / phases alignées MVP vs options |
| **Cas de test** | Scénarios pas-à-pas (sélection doc, affichage par format, régression embed JSP) |
| **Jeux de données de test** | PDF simple/multi-pages, JPEG, fichiers invalides (TIFF exclu pour l'instant) |
| **Critères de recette (UAT)** | Alignés sur critères d'acceptation BA — checklist recette métier |
| **Matrice de couverture** | Exigence / cas d'usage ↔ cas de test |
| **Checklist non fonctionnel** | Navigateurs, perf chargement gros PDF, accessibilité clavier |
| **Rapport de test** (modèle) | Structure pour exécution future |

_Lien BA ↔ QA : chaque exigence + critère d'acceptation BA alimente au moins un cas de test ; les mocks jouables servent de base pour tests exploratoires et recette UX._

### Context Guidance

_Projet greenfield côté BMad; stack imposée JSP; formats PDF, JPEG (TIFF hors scope); viewer embedded dans la page._

### Flux applicatif actuel (cadrage métier)

1. L'utilisateur arrive depuis une **fiche client** (contexte parent).
2. Un **onglet (tab) en haut de page** — libellé type **« Document viewer »** — donne accès à la zone dédiée.
3. **Contenu de l'onglet :** **liste de documents** (dossier lié au client) **+ zone viewer** (affichage du document sélectionné).

_Implications : layout master-detail (liste | viewer), navigation inter-documents sans quitter la fiche client, intégration JSP/tabs existants du shell fiche client._

**Décisions UX validées :**
- **Disposition liste :** à gauche **ou** au-dessus du viewer (les deux variantes à explorer en mock)
- **Chargement initial :** premier document de la liste chargé automatiquement à l'ouverture de l'onglet
- **Volume :** quelques documents à ~une dizaine — pas besoin de patterns « milliers de fichiers » ; tri simple optionnel

**Mocks client validés (3) :**
- **M1 Classique** — liste gauche table (nom + type), viewer droite
- **M2 Bandeau** — liste horizontale compacte au-dessus, viewer dessous
- **M3 Vignettes** — liste à gauche avec **miniatures réelles** (JPEG aperçu direct ; PDF si thumbs serveur) + nom, viewer droite — variante visuelle pour feedback client (hors MVP)
- Squelette HTML commun ; checklist de test identique sur les 3

**Décision client / prod :**
- **3 mocks** (M1, M2, M3) pour tests et feedback client
- **Cible production / MVP :** **liste en haut + viewer en dessous** (layout **M2**) — liste type **B1 table horizontale** ou **B3 pills** à trancher en axe C ; M1/M3 = comparaison / alternatives

**Démos HTML (couleurs, Tailwind CSS + Alpine.js) :**
- `_bmad-output/demos/demo-viewer-native.html` — UI Tailwind/Alpine · 0 lib viewer (iframe/img/embed)
- `_bmad-output/demos/demo-viewer-libraries.html` — UI Tailwind/Alpine · JPEG (chat) — pas de TIFF
- `_bmad-output/demos/index.html` — index des deux démos

**Alignement secteur assurance / banque (axe B) :**
- Pattern principal : **table métadonnées** (nom, type/catégorie, date) — tri date décroissante
- **M1 = référence secteur** (master-detail gauche) ; M2/M3 = variantes pour validation client
- **M3 mock :** **miniatures image** (B5) — vraies thumbs si backend les fournit ; sinon placeholder par type pour le mock HTML
- Groupement optionnel par **catégorie documentaire** (KYC, contrat, sinistre, correspondance)
- Comportements entreprise : états vide/erreur, indicateur doc courant, navigation clavier

### Session Setup

Approche retenue : **flux progressif** (exploration large → patterns → développement → plan d'action).

## Technique Selection

**Approach:** Progressive Technique Flow
**Journey Design:** Développement systématique de l'exploration vers l'action

**Progressive Techniques:**

- **Phase 1 - Exploration:** Morphological Analysis — cartographier les combinaisons (formats × sélecteur × viewer × embed)
- **Phase 2 - Pattern Recognition:** Solution Matrix — croiser variables problème / approches solutions, prioriser
- **Phase 3 - Development:** SCAMPER Method — affiner les concepts retenus (viewer + navigation + mocks)
- **Phase 4 - Action Planning:** Decision Tree Mapping — MVP, options, branches et estimations temps

**Journey Rationale:** Session orientée livrables concrets (features, MVP, effort, mocks testables) avec forte dimension UX (sélection docs) et contraintes techniques JSP — le flux progressif structure la divergence créative puis la convergence vers un plan implémentable.
