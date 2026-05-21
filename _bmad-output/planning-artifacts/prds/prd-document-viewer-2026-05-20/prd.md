---
title: Document viewer (onglet fiche client)
status: draft
created: 2026-05-20
updated: 2026-05-20
stakes: outil-interne
working_mode: fast-path
---

# PRD: Document viewer (onglet fiche client)

## 0. Document Purpose

Ce PRD sert de **source unique** pour le cadrage d’un outil interne : un onglet **Document viewer** embarqué dans la fiche client JSP, permettant de parcourir les documents du dossier et de les consulter (**PDF, JPEG, TIFF**) sans quitter la fiche.

**Public :** chef de produit / porteur interne, **analyste fonctionnel**, **QA**, architecte, développeurs JSP/JS.

**Structure :** glossaire ancré, fonctionnalités groupées avec exigences fonctionnelles (FR) numérotées globalement, NFR transverses, index des hypothèses.

**Artefacts liés (même dossier) :**
- `livrables-ba.md` — paquet analyste fonctionnel (cas d’usage, traçabilité, critères d’acceptation)
- `livrables-qa.md` — paquet QA (stratégie, cas de test, recette UAT)
- `addendum.md` — choix techniques et alternatives écartées (PDF.js, stockage préférences, etc.)
- Démos jouables : `_bmad-output/demos/` · [GitHub Pages](https://martinfou.github.io/document-viewer/)

---

## 1. Vision

Les conseillers et utilisateurs métier consultent aujourd’hui les pièces d’un dossier client via des **boutons dispersés** (un fichier = un contrôle), ce qui fragmente l’expérience et complique la comparaison rapide entre documents.

Le **Document viewer** regroupe, dans un **onglet dédié** de la fiche client, une **liste de documents** et une **zone de visualisation** intégrée. L’utilisateur sélectionne un document dans la liste ; le viewer affiche le **PDF, JPEG ou TIFF** correspondant, avec navigation (pages pour PDF et TIFF multi-pages), zoom et réglages mémorisés selon ses préférences.

Pour un **outil interne** en contexte assurance / services financiers, la priorité est la **fiabilité d’affichage** (PDF.js plutôt que le viewer natif du navigateur), des **états métier explicites** (vide, erreur, document courant) et des **livrables BA/QA** traçables depuis ce PRD jusqu’à la recette.

---

## 2. Target User

### 2.1 Primary Persona

**Conseiller / utilisateur métier** — authentifié sur l’application fiche client. Il ouvre l’onglet Document viewer pour vérifier contrats, pièces KYC, correspondances ou photos liées au dossier, souvent en séquence (plusieurs documents, quelques minutes).

### 2.2 Jobs To Be Done

- Voir rapidement **quels documents** sont disponibles pour ce client sans ouvrir chaque fichier dans un nouvel onglet système.
- **Lire** un PDF multi-pages, une image JPEG ou un **TIFF** (y compris multi-pages) dans la page, avec zoom et navigation par page le cas échéant.
- **Enchaîner** la consultation de plusieurs pièces sans perdre le contexte fiche client.
- Retrouver **ses habitudes de lecture** (zoom, mode d’ajustement) à chaque visite grâce aux **préférences enregistrées**.
- **Reprendre** sur la fiche client où elle s’était arrêtée : **même document** et **même page** PDF que lors de la dernière consultation de cette fiche.

### 2.3 Non-Users (v1)

- Administrateurs de contenu (hors périmètre : pas de gestion documentaire ici).
- Clients finaux en libre-service (pas d’accès direct prévu dans ce PRD).
### 2.4 Key User Journeys

**UJ-1. Marie rouvre la fiche et reprend sa lecture**
- **Persona + contexte :** conseillère, fiche client **Dupont** rouverte après une session précédente (contrat page 3).
- **Entry state :** authentifiée ; position enregistrée pour cette fiche (document + page).
- **Path :** elle active l’onglet → la liste se charge → le système rouvre le **document mémorisé** à la **page mémorisée** avec zoom/fit préférences → elle continue la lecture.
- **Climax :** pas besoin de retrouver manuellement le contrat ni la page 3.
- **Resolution :** elle enchaîne sur un autre document (UJ-2) ; la nouvelle position est mémorisée pour Dupont.
- **Edge case :** première visite sur cette fiche → **premier document** de la liste (FR-5 repli) ; document mémorisé absent du dossier → repli FR-5 + page 1 ; liste vide → FR-14.

**UJ-2. Marie compare deux pièces du dossier**
- **Entry state :** UJ-1 en cours, document A affiché.
- **Path :** clic sur document B dans la liste (pills ou ligne table) → le viewer charge B → indicateur visuel du document courant dans la liste.
- **Climax :** bascule en moins de 2 s perçues pour un PDF de taille courante `[ASSUMPTION: < 5 Mo]`.
- **Resolution :** elle peut revenir à A ou quitter l’onglet ; la fiche client reste ouverte.

**UJ-3. Marie retrouve préférences et position par fiche**
- **Entry state :** nouvelle session ; fiche **Dupont** vs fiche **Martin** ont des positions distinctes `[ASSUMPTION: stockage par identifiant fiche client]`.
- **Path :** ouverture onglet sur Dupont → chargement zoom/fit + **document + page** pour Dupont → rendu ; plus tard ouverture onglet sur Martin → **autre** document/page mémorisés.
- **Climax :** chaque fiche reprend son propre point de lecture ; zoom/fit globaux `[ASSUMPTION]` s’appliquent en plus.
- **Resolution :** toute navigation document/page met à jour la position enregistrée pour la fiche courante.
- **Edge case :** échec de sauvegarde → consultation possible, repli FR-5 au prochain chargement `[ASSUMPTION: non bloquant]`.

---

## 3. Glossary

| Terme | Définition |
|-------|------------|
| **Fiche client** | Page JSP parente regroupant les informations et onglets d’un client. |
| **Onglet Document viewer** | Tab UI donnant accès à la zone liste + viewer. |
| **Dossier documents** | Ensemble des pièces rattachées au client affichées dans la liste (ordre de quelques unités à ~10). |
| **Document** | Fichier consultable : **PDF, JPEG ou TIFF** en v1. |
| **Liste de documents** | Composant de sélection (pills MVP ; table ou vignettes en variantes). |
| **Viewer** | Zone d’affichage du document sélectionné (PDF.js pour PDF ; image ou moteur TIFF pour JPEG/TIFF — voir addendum). |
| **TIFF** | Format image raster souvent multi-pages (scans, GED) ; consultation dans le viewer comme les autres types MVP. |
| **Document courant** | Document dont le contenu est affiché dans le viewer. |
| **Préférences viewer** | Réglages utilisateur persistés (zoom, mode d’ajustement, etc.). |
| **Impression** | Sortie papier du document affiché (navigateur, PDF.js ou action dédiée). |
| **Téléchargement** | Enregistrement local d’une copie du fichier source du document. |
| **Source document** | Mécanisme par lequel le viewer obtient les octets du fichier (URL, flux, identifiant GED résolu côté serveur). |
| **Liste documents (métadonnées)** | Données affichées dans le sélecteur sans nécessairement charger le fichier (id, nom, type, date, URL ou clé de résolution). |
| **Position de lecture** | Dernier **document** et **page** (PDF) consultés par un utilisateur sur une **fiche client** donnée. |
| **Contexte fiche** | Identifiant stable du client / dossier parent permettant de isoler la position de lecture (ex. `clientId`). |
| **M2 / bandeau** | Layout liste **au-dessus** du viewer (cible MVP). |
| **M1 / master-detail** | Layout liste **à gauche**, viewer à droite (variante comparaison). |
| **M3 / vignettes** | Layout liste à gauche avec miniatures (hors MVP). |

---

## 4. Features

### 4.1 Intégration onglet fiche client

**Description :** L’onglet s’intègre au shell JSP existant (tabs en tête de fiche). À l’activation, la zone Document viewer remplace le contenu de l’onglet sans navigation full-page. Réalise UJ-1.

**Functional Requirements:**

#### FR-1: Accès par onglet

L’utilisateur authentifié peut ouvrir l’onglet **Document viewer** depuis la fiche client. Réalise UJ-1.

**Consequences (testable):**
- L’onglet est visible et activable lorsque l’utilisateur a le droit d’accéder aux documents du dossier `[ASSUMPTION: droits alignés sur l’existant fiche client]`.
- L’activation n’entraîne pas de rechargement complet de la fiche client.

#### FR-2: Contexte dossier client

Le système charge la liste des documents **du client courant** de la fiche. Réalise UJ-1.

**Consequences (testable):**
- Changer de client sur la fiche (si applicable) recharge la liste et réinitialise le document courant selon les règles de FR-4.
- La liste expose au minimum les champs nécessaires à FR-3 et à la **résolution de la source** du fichier (voir OQ-7 — question équipe dev).

#### FR-2a: Acquisition des fichiers `[PENDING DEV]`

Le viewer obtient le contenu **PDF, JPEG et TIFF** via un mécanisme **défini par l’architecture** (réponse OQ-7). Réalise UJ-1, UJ-2.

**Consequences (testable):**
- Chaque document de la liste est **consultable** sans rechargement complet de la fiche client.
- Les requêtes respectent l’**authentification** de la session en cours (NFR-3).
- En cas d’échec (timeout, 403, 404), FR-15 s’applique.
- Le contrat (URL, identifiant, en-têtes) est **documenté** pour QA (jeux de données DT-xxx).

**Notes:** Détails techniques et options dans `addendum.md` §7 — ne pas figer JSP vs API avant réponse dev.

---

### 4.2 Liste de documents

**Description :** Présentation des métadonnées minimales (nom, type MIME ou libellé type, date optionnelle, catégorie optionnelle). Volume cible : quelques documents à ~10 ; tri simple (ex. date décroissante) optionnel MVP. Layout MVP : **bandeau horizontal pills** (démo layout 1). Réalise UJ-1, UJ-2.

**Functional Requirements:**

#### FR-3: Affichage liste

L’utilisateur voit tous les documents du dossier dans la liste avec au minimum **nom** et **type**. Réalise UJ-1.

**Consequences (testable):**
- Chaque entrée est sélectionnable (clic ou clavier).
- Un indicateur identifie le **document courant**.

#### FR-4: Sélection document

L’utilisateur peut sélectionner un document dans la liste ; le viewer charge ce document. Réalise UJ-2.

**Consequences (testable):**
- La sélection met à jour le document courant et déclenche le chargement viewer.
- La sélection est possible au clavier (focus + activation).

#### FR-5: Chargement initial et repli

À l’ouverture de l’onglet pour une fiche client, le système affiche le document selon **FR-19** (position mémorisée) si elle existe et reste valide ; sinon le **premier document** de la liste (après tri). Réalise UJ-1.

**Consequences (testable):**
- Si la liste contient au moins un document, le viewer n’est pas vide au premier affichage.
- Si la liste est vide, FR-14 s’applique (pas de chargement forcé).
- Document mémorisé **absent** de la liste (supprimé, droits) → repli premier document disponible, page 1.
- Page mémorisée **> nombre de pages** → repli dernière page du document.

#### FR-6: Tri simple (optionnel MVP)

`[ASSUMPTION: inclus MVP]` L’utilisateur ou le système applique un tri par défaut (date décroissante) sur la liste.

**Consequences (testable):**
- L’ordre affiché est déterministe et documenté dans `livrables-ba.md`.

**Out of Scope:**
- Recherche full-text, filtres avancés, pagination « milliers de fichiers ».

---

### 4.3 Viewer PDF

**Description :** Rendu PDF via moteur applicatif **PDF.js** (canvas), toolbar intégrée : zoom, pages précédente/suivante, ajuster largeur / hauteur, navigation document précédent/suivant si plusieurs pièces. Réalise UJ-1, UJ-2, UJ-3.

**Functional Requirements:**

#### FR-7: Affichage PDF

L’utilisateur peut consulter un document PDF multi-pages dans le viewer embarqué. Réalise UJ-1.

**Consequences (testable):**
- Le PDF s’affiche sans téléchargement obligatoire ni ouverture d’onglet navigateur externe.
- Les pages sont navigables (au moins boutons ou raccourcis précédent/suivant).

#### FR-8: Contrôles zoom et ajustement

L’utilisateur peut zoomer et basculer entre **ajuster largeur** et **ajuster hauteur** pour le PDF. Réalise UJ-1, UJ-3.

**Consequences (testable):**
- Le ratio du document n’est pas déformé (pas d’étirement incorrect du canvas).
- L’état de zoom est un nombre ou niveau reproductible pour la persistance (FR-11).

#### FR-9: Navigation inter-documents dans le viewer

L’utilisateur peut passer au document précédent/suivant de la liste depuis la barre du viewer (en plus de la liste). Réalise UJ-2.

**Consequences (testable):**
- Les boutons sont désactivés aux bornes de la liste.
- La liste reflète le document courant après navigation.

**Out of Scope:**
- Annotation PDF, formulaires interactifs avancés, signature électronique dans le viewer.

---

### 4.4 Viewer JPEG

**Description :** Images JPEG affichées via composant image adapté au conteneur viewer (zoom / fit cohérents avec l’UX PDF quand applicable). Réalise UJ-2.

**Functional Requirements:**

#### FR-10: Affichage JPEG

L’utilisateur peut consulter un document JPEG dans la zone viewer. Réalise UJ-2.

**Consequences (testable):**
- L’image est visible en entier ou via zoom sans quitter l’onglet.
- Les contrôles inapplicables au raster simple (ex. page suivante sur JPEG une page) sont masqués ou désactivés.

---

### 4.4b Viewer TIFF

**Description :** Documents TIFF affichés dans le viewer embarqué, avec expérience alignée sur PDF lorsque le fichier est **multi-pages** (navigation pages, zoom, fit). Réalise UJ-1, UJ-2. Mécanisme de rendu : `addendum.md` §8 (OQ-8).

**Functional Requirements:**

#### FR-10b: Affichage TIFF

L’utilisateur peut consulter un document TIFF dans la zone viewer. Réalise UJ-1, UJ-2.

**Consequences (testable):**
- Le TIFF s’affiche sans téléchargement obligatoire ni application externe.
- **TIFF multi-pages :** navigation page précédente/suivante comme pour PDF ; numéro de page affiché.
- **TIFF une page :** comportement proche JPEG (pas de navigation page inutile).
- Formats TIFF courants du GED métier couverts `[ASSUMPTION: TIFF baseline / multipage — préciser jeux de test avec QA]`.
- La **position de lecture** (FR-19/20) enregistre `pageNumber` pour TIFF multi-pages comme pour PDF.

**Out of Scope:**
- Édition, conversion, ou OCR dans le viewer.

---

### 4.5 Préférences et position de lecture

**Description :** Persistance des habitudes de consultation (zoom, fit) et de la **position de lecture** (document + page PDF) par utilisateur et par **fiche client**. Réalise UJ-1, UJ-3.

**Functional Requirements:**

#### FR-11: Lecture préférences et position à l’ouverture

À l’ouverture de l’onglet pour une **fiche client** donnée, le système **charge** et applique :
1. **Position de lecture** pour ce couple utilisateur + fiche (FR-19) ;
2. **Préférences viewer** globales : zoom et mode d’ajustement par défaut. Réalise UJ-1, UJ-3.

**Consequences (testable):**
- Position : `documentId` (ou clé équivalente) + `pageNumber` (entier ≥ 1 pour **PDF et TIFF multi-pages** ; **1** ou absent pour JPEG une page).
- Zoom/fit : valeurs par défaut produit si jamais enregistrées.
- Fiche A et fiche B : positions **indépendantes** pour le même utilisateur.

#### FR-12: Enregistrement préférences (zoom / fit)

Lorsque l’utilisateur modifie zoom ou mode d’ajustement, le système **enregistre** les valeurs (périmètre global utilisateur — FR-13). Réalise UJ-3.

**Consequences (testable):**
- Session ultérieure sur **n’importe quelle** fiche : mêmes zoom/fit `[ASSUMPTION: globaux]`.
- Enregistrement après modification explicite `[ASSUMPTION: debounce ou fin d’action]`.

#### FR-13: Périmètre de persistance v1

| Donnée | Portée | Clé |
|--------|--------|-----|
| **Position** (document + page) | Par **utilisateur** + par **fiche client** | `userId` + `clientId` (contexte fiche) |
| **Zoom / fit** | Par **utilisateur** (global viewer) | `userId` |

**Out of Scope v1:**
- Thème UI, choix de layout M1/M2 mémorisé.
- Position mémorisée **entre utilisateurs** (pas de « bookmark » partagé).

**Notes:** Schéma API : `addendum.md` §2.

#### FR-19: Reprise de la position de lecture

À l’ouverture de l’onglet, si une position enregistrée existe pour l’utilisateur et la **fiche client courante**, le système sélectionne le **document mémorisé** et affiche la **page mémorisée** (PDF). Réalise UJ-1, UJ-3.

**Consequences (testable):**
- Le document mémorisé est **sélectionné dans la liste** (indicateur document courant).
- Pour PDF : page affichée = page mémorisée si ≤ nombre de pages du document.
- Pour JPEG une page : document mémorisé ; page = 1.
- Pour TIFF : page mémorisée comme PDF (multi-pages) ou page 1 (monopage).
- Si aucune position enregistrée : **FR-5** (premier document, page 1).

#### FR-20: Enregistrement de la position de lecture

Le système **enregistre** la position courante pour l’utilisateur et la fiche client lorsque :
- l’utilisateur **change de document** dans la liste ou via la toolbar ;
- l’utilisateur **change de page** dans un PDF ;
- l’utilisateur **quitte** l’onglet Document viewer ou **quitte** la fiche client `[ASSUMPTION: événement « leave » côté shell JSP]`. Réalise UJ-2, UJ-3.

**Consequences (testable):**
- Position enregistrée = `documentId` + `pageNumber` au moment de l’événement.
- Changement de page : enregistrement **debounced** (ex. 500 ms) pour limiter les appels API `[ASSUMPTION]`.
- Même fiche rouverte plus tard : FR-19 retrouve la dernière position **enregistrée**.

---

### 4.6 Navigation clavier et accessibilité

**Description :** Permettre une utilisation **sans souris** pour la liste, la toolbar et la navigation de pages, selon le palier retenu avec le client (OQ-9, §8.1). Réalise UJ-1, UJ-2.

**Functional Requirements:**

#### FR-21: Navigation clavier — palier Standard (MVP recommandé)

L’utilisateur peut, au clavier seul : parcourir la **liste de documents** et activer une entrée ; parcourir les **contrôles principaux** du viewer (pages, zoom, documents préc./suiv., fit) ; changer de **page** via les boutons dédiés. Réalise UJ-1, UJ-2.

**Consequences (testable):**
- Ordre de tabulation cohérent (liste → toolbar → pas de cycle infini).
- **Focus visible** sur chaque élément interactif.
- `Enter` / `Espace` sur un pill charge le document (équivalent clic).
- Boutons « page précédente / suivante » activables au clavier ; changement annoncé `[ASSUMPTION: aria-live polite]`.
- Cible accessibilité documentée après OQ-9 (ex. WCAG 2.1 AA sur le composant).

#### FR-22: Navigation clavier — palier Avancé `[PENDING CUSTOMER — OQ-9]`

Si le client le demande : flèches dans la liste (roving tabindex), **Page Up/Down** pour les pages, raccourcis **documents préc./suiv.** et **zoom** ; matrice publiée dans l’aide UI.

**Consequences (testable):**
- Pas de conflit bloquant avec raccourcis globaux de la fiche JSP.
- Raccourcis actifs seulement lorsque le focus est dans le viewer `[ASSUMPTION]`.

**Notes:** Démos HTML : FR-21/22 **non implémentés** — story avant recette accessibilité.

---

### 4.8 États métier et robustesse

**Description :** Comportements attendus en entreprise : liste vide, erreur chargement, format non supporté. Réalise UJ-1 (edge).

**Functional Requirements:**

#### FR-14: Liste vide

Si le dossier ne contient aucun document, l’utilisateur voit un **message métier** explicite ; le viewer reste vide ou affiche un état placeholder neutre. Réalise UJ-1.

**Consequences (testable):**
- Aucune erreur technique brute exposée à l’utilisateur.

#### FR-15: Erreur chargement document

Si le fichier est inaccessible ou corrompu, l’utilisateur voit un message d’échec dans la zone viewer ; la liste reste utilisable pour tenter un autre document. Réalise UJ-2.

**Consequences (testable):**
- L’utilisateur peut sélectionner un autre document sans recharger la fiche.

#### FR-16: Format non supporté

Les formats autres que **PDF, JPEG et TIFF** ne sont pas proposés en v1 ou affichent un message « non supporté » si présents côté serveur `[ASSUMPTION: filtrage amont préférable]`.

---

### 4.7 Impression et téléchargement `[EN ATTENTE CLIENT]`

**Description :** Politique métier et conformité à valider **auprès du client** avant gel MVP. Selon la réponse, le viewer expose ou **masque** les actions d’impression et de téléchargement, et l’application applique les **mêmes règles de droits** que le reste de la fiche client.

`[NOTE FOR PM]` Poser explicitement au client : *Les utilisateurs de l’onglet Document viewer sont-ils autorisés à **imprimer** et/ou **télécharger** les documents ? Par rôle ? Par type de document ?*

**Functional Requirements:**

#### FR-17: Impression `[PENDING CUSTOMER]`

Si le client autorise l’impression, l’utilisateur disposant des droits peut imprimer le **document courant** depuis le viewer (action dédiée et/ou impression navigateur contrôlée). Si non autorisé, l’action est **absente ou désactivée** et les raccourcis d’impression ne doivent pas contourner la politique `[ASSUMPTION: durcissement CSS/JS + pas de toolbar PDF.js print si interdit]`.

**Consequences (testable):**
- Avec droit : impression produit le document affiché (PDF, JPEG ou TIFF).
- Sans droit : aucun bouton Imprimer ; tentative Ctrl+P sans fuite du contenu `[ASSUMPTION: politique à préciser avec sécurité]`.
- Droit révocable par rôle aligné sur la matrice existante.

#### FR-18: Téléchargement `[PENDING CUSTOMER]`

Si le client autorise le téléchargement, l’utilisateur disposant des droits peut **télécharger** le fichier source du document courant. Si non autorisé, l’action est **absente** et les URLs document ne doivent pas permettre un téléchargement direct non authentifié.

**Consequences (testable):**
- Avec droit : téléchargement du bon fichier (nom cohérent, type MIME correct).
- Sans droit : pas de lien/bouton Télécharger ; accès direct URL refusé (NFR-3).
- Comportement aligné sur l’existant « télécharger document » de la fiche si déjà défini.

**Out of Scope jusqu’à décision client:**
- Implémentation finale des boutons et des contrôles anti-contournement — **bloqué** sur réponse client (voir §10 OQ-6).

---

## 5. Non-Goals (Explicit)

- **Édition** ou **téléversement** de documents depuis cet onglet.
- **Recherche plein texte** dans le contenu PDF.
- **Remplacement** du GED / stockage documentaire — le viewer **consomme** des URLs ou flux existants.
- **Layout M3 vignettes** et génération de miniatures PDF côté serveur en MVP (variante démo uniquement).
- **Viewer PDF natif navigateur** comme solution principale production (voir addendum).
- **Impression / téléchargement** tant que le client n’a pas tranché — ne pas livrer de boutons actifs par défaut `[ASSUMPTION: deny-by-default jusqu’à validation]`.

---

## 6. MVP Scope

### 6.1 In Scope

- Onglet Document viewer sur fiche client JSP.
- Liste documents **bandeau pills (M2)** avec nom + type ; ~10 documents max.
- PDF via **PDF.js** ; JPEG via image ; **TIFF** via moteur à définir (addendum §8).
- Toolbar viewer : pages, zoom, fit largeur/hauteur, doc précédent/suivant.
- Premier document auto-chargé à l’ouverture.
- **Préférences utilisateur** : zoom + mode ajustement (global), persistées.
- **Position de lecture** : dernier document + page PDF **par fiche client**, persistés (FR-19, FR-20).
- États vide / erreur / non supporté.
- Livrables **BA** et **QA** dérivés de ce PRD (`livrables-ba.md`, `livrables-qa.md`).
- Maquettes jouables comme référence UX (démos layout 1 + démo B PDF.js).
- **Navigation clavier palier Standard** (FR-21) — sauf si client refuse explicitement (OQ-9).

### 6.2 Out of Scope for MVP

| Élément | Raison |
|---------|--------|
| M1 liste gauche table, M3 vignettes | Variantes feedback client ; MVP = M2 pills |
| Formats hors PDF/JPEG/TIFF (ex. Word, PNG seul si non listé) | Hors MVP — message non supporté (FR-16) |
| Recherche dans PDF | Option ~1–2 j ; lot post-MVP |
| Thumbs PDF serveur | Requis pour M3, pas pour MVP pills |
| Position de lecture **entre fiches** (un seul bookmark global) | Une position **par fiche** suffit (FR-13) |
| Groupement par catégorie documentaire | Optionnel ; peut entrer MVP si tri faible coût `[ASSUMPTION: reporté v2 sauf validation BA]` |
| Boutons Imprimer / Télécharger actifs | **En attente décision client** (OQ-6) ; MVP = consultation seule si non autorisé |
| Raccourcis clavier **Avancés** (FR-22) | Optionnel — seulement si OQ-9 = palier Avancé |

---

## 7. Success Metrics

**Primary**

- **SM-1 :** 100 % des cas de test UAT **critiques** (liste, sélection, PDF, **TIFF** mono/multi-pages, JPEG, préférences, **reprise position**) passent en recette. Valide FR-3 à FR-12, FR-10b, FR-14, FR-15, FR-19, FR-20.
- **SM-2 :** Les conseillers pilotes consultent ≥ 3 documents d’affilée **sans quitter** l’onglet lors d’un test guidé (5 utilisateurs). Valide UJ-2.

**Secondary**

- **SM-3 :** Temps perçu de bascule document < 2 s pour PDF ≤ 5 Mo sur poste standard interne. Valide FR-4, FR-9.

**Counter-metrics (do not optimize)**

- **SM-C1 :** Nombre de bibliothèques JS ajoutées — ne pas gonfler la stack au-delà du nécessaire (PDF.js + intégration existante).

---

## 8. Cross-Cutting NFRs

| ID | Exigence |
|----|----------|
| NFR-1 | Compatibilité navigateurs **cibles internes** (liste à confirmer avec QA — min. Chrome/Edge récents `[ASSUMPTION]`). |
| NFR-2 | Accessibilité : navigation clavier liste + contrôles principaux viewer ; focus visible. |
| NFR-3 | Sécurité : documents servis avec les **mêmes contrôles d’accès** que la fiche client ; pas d’URL document exposée sans auth. |
| NFR-4 | Performance : chargement initial onglet acceptable sur réseau interne `[ASSUMPTION: < 3 s jusqu’au premier rendu pour PDF standard]`. |
| NFR-5 | Préférences : persistance **durable** (survie reconnexion) si mode serveur ; pas de fuite de préférences entre utilisateurs. |
| NFR-6 | Si impression/téléchargement interdits : pas de contournement trivial (menu navigateur, lien direct, toolbar PDF.js) — détail en architecture après OQ-6. |
| NFR-7 | Accessibilité clavier : niveau confirmé par le client (OQ-9) ; **minimum recommandé** = palier « Standard » (§8.1). |

---

## 8.1 Navigation clavier — bonnes pratiques industrie et paliers

Références courantes pour visionneuses embarquées (PDF.js, viewers GED/banque-assurance, **WCAG 2.1** / **WAI-ARIA APG**) :

| Pratique | Description | Palier |
|----------|-------------|--------|
| **Ordre de tabulation logique** | Liste documents → barre d’outils viewer → zone document ; pas de piège au clavier | Standard (MVP recommandé) |
| **Focus visible** | Contour contrasté sur pill, bouton, lien — pas `outline: none` sans remplacement | Standard |
| **Liste : activation** | `Tab` / `Shift+Tab` entre pills ; `Enter` ou `Espace` pour sélectionner le document | Standard |
| **Liste : navigation rapide** | Flèches `←` `→` (bandeau horizontal) ou `↑` `↓` (liste verticale) entre documents, **roving tabindex** | Avancé (si client le demande) |
| **Pages document** | `Page préc.` / `Page suiv.` accessibles au clavier ; raccourcis **`Page Up` / `Page Down`** ou **`←` `→`** quand le focus est dans le viewer | Standard pages ; Avancé raccourcis globaux |
| **Documents préc./suiv.** | Boutons toolbar + raccourcis optionnels (ex. `Ctrl+Alt+,` / `.` — à documenter, pas de conflit navigateur) | Avancé |
| **Zoom** | Boutons +/- accessibles ; option **`+` / `-`** avec focus viewer (comme Adobe Reader web) | Avancé |
| **Annonces lecteur d’écran** | `aria-live` pour changement de document/page ; labels sur boutons icône-seuls | Standard (secteur réglementé) |
| **Rôles ARIA** | `role="tablist"` / `tab` pour pills ; `aria-selected` ; toolbar `role="toolbar"` | Standard |
| **Pas de focus dans le canvas seul** | Le focus reste sur les contrôles ; le canvas PDF/TIFF est décoratif ou `aria-label` document | Standard PDF.js |
| **Échap** | Ne ferme pas la fiche client ; éventuellement retire le focus d’un sous-mode | Contextuel |

**Recommandation produit (à valider avec le client — OQ-9) :** viser au minimum le palier **Standard** en MVP (aligné NFR-2, FR-21). Palier **Avancé** si utilisateurs power (centres d’appels, traitement sinistres intensif) ou exigence **accessibilité formelle** (WCAG AA).

Détail technique et matrice raccourcis : `addendum.md` §9.

---

## 9. Stakeholders and Downstream Artifacts

| Rôle | Livrable | Fichier |
|------|----------|---------|
| Analyste fonctionnel | Paquet cadrage + cas d’usage + traçabilité FR | `livrables-ba.md` |
| QA | Stratégie, cas de test, UAT, couverture | `livrables-qa.md` |
| UX (recommandé) | Spécification écrans détaillée | `bmad-create-ux-design` après validation PRD |
| Architecture | Décisions JSP, API préférences, PDF.js | `bmad-create-architecture` + `addendum.md` |

---

## 10. Open Questions

1. **API préférences et position** : endpoint existant ou nouveau ? Structure JSON (voir addendum §2) ; clé **clientId** pour la position ; propriétaire backend ?
2. **Format liste MVP** : pills seules ou table compacte dans le bandeau ? (démo 1 = pills)
3. **Inventaire libs JS** déjà présentes sur la fiche JSP — impact bundling PDF.js.
4. **Tri par défaut** : date décroissante confirmée métier ?
5. **Droits documents** : même matrice que l’accès consultation actuel sur la fiche ?
6. **OQ-6 — Impression et téléchargement (question client obligatoire)**  
   - Les utilisateurs sont-ils autorisés à **imprimer** les documents depuis le viewer ?  
   - Les utilisateurs sont-ils autorisés à **télécharger** les documents ?  
   - La réponse est-elle **globale**, par **rôle**, par **type/catégorie** de document, ou par **document** ?  
   - Existe-t-il déjà une politique sur la fiche client à laquelle s’aligner ?  
   *Tant que non tranché : FR-17 et FR-18 restent en suspens ; MVP sans actions actives (deny-by-default).*

7. **OQ-7 — Récupération des documents PDF et images (questions équipe dev / architecture)**  
   - **Liste :** comment l’onglet obtient-il les métadonnées (nom, type, date, id) — rendu JSP serveur, appel AJAX REST, tag existant ?  
   - **PDF :** quelle URL ou quel flux alimente PDF.js (`fetch` + `ArrayBuffer`) — servlet dédié, lien GED signé, chemin relatif applicatif ?  
   - **JPEG :** `src` direct sur URL authentifiée, blob après `fetch`, ou bytes inline dans la page ?
   - **TIFF :** flux binaire vers lib JS (UTIF/tiff.js), conversion serveur en images, ou tuiles — voir **OQ-8**.  
   - **Identifiants :** un id document stable côté GED / base ? comment le viewer le passe-t-il au chargement ?  
   - **Auth :** cookie de session seulement, token, en-têtes CSRF — même modèle que le reste de la fiche client ?  
   - **Sécurité :** URLs réutilisables hors session ? durée de vie des liens signés ?  
   - **Perf / cache :** mise en cache navigateur ou CDN autorisée pour les pièces ? taille max typique ?  
   - **Existant :** y a-t-il déjà un endpoint ou un pattern « ouvrir document » sur la fiche à réutiliser ?  
   *Bloquant pour `bmad-create-architecture` et pour les tests d’intégration (FR-2a).*

8. **OQ-8 — Rendu TIFF en MVP (question dev)**  
   - Librairie cliente (ex. UTIF.js, geotiff) vs **conversion serveur** (PNG/JPEG par page) ?  
   - TIFF **multi-pages** : même toolbar pages que PDF ?  
   - Limites taille / compression (CCITT, LZW) supportées en prod ?  
   - Jeux de fichiers TIFF réels du GED pour QA (DT-7).  

9. **OQ-9 — Navigation clavier et accessibilité (question client / consommateur)**  
   - Les utilisateurs doivent-ils pouvoir utiliser le viewer **sans souris** (clavier seul) ?  
   - Niveau attendu : **Standard** (Tab, activation liste, toolbar, pages) ou **Avancé** (flèches dans la liste, Page Up/Down, raccourcis zoom/docs) — voir §8.1 ?  
   - Exigence **WCAG** / accessibilité formelle (AA) sur ce composant ou héritée du portail ?  
   - Utilisateurs de **lecteurs d’écran** : oui/non — volume estimé ?  
   - Conflits avec raccourcis **globaux** de l’application fiche client à éviter ?  
   - Documentation **aide raccourcis** dans l’UI souhaitée (panneau, tooltip, page aide) ?  
   *Recommandation équipe : palier **Standard** en MVP (FR-21) ; Avancé (FR-22) si réponse client.*

### Question client — impression / téléchargement (copier-coller)

> Pour l’onglet Document viewer sur la fiche client :  
> 1. Les utilisateurs doivent-ils pouvoir **imprimer** les documents affichés ?  
> 2. Les utilisateurs doivent-ils pouvoir **télécharger** les fichiers ?  
> 3. Si oui, pour **tous les rôles** et **tous les types** de documents, ou avec des restrictions (rôles, catégories KYC/contrat/sinistre, etc.) ?  
> 4. Y a-t-il des exigences de **traçabilité** (journalisation des impressions/téléchargements) ?

### Question client — navigation clavier et accessibilité (copier-coller)

> Pour l’onglet Document viewer :  
> 1. Vos utilisateurs doivent-ils pouvoir **tout faire au clavier** (sans souris) ?  
> 2. Quel niveau souhaitez-vous ?  
>    - **Standard** (recommandé) : Tab entre documents et boutons, Entrée pour ouvrir, boutons page préc./suiv. au clavier, focus visible.  
>    - **Avancé** : en plus, flèches pour changer de document, Page Haut/Bas pour les pages, raccourcis zoom.  
> 3. Avez-vous une obligation **WCAG / accessibilité** (ex. niveau AA) pour cet écran ?  
> 4. Des **lecteurs d’écran** (non-voyants) sont-ils dans le public cible ?  
> 5. L’application a-t-elle déjà des **raccourcis clavier globaux** à ne pas bloquer ?  
> 6. Souhaitez-vous une **aide « Raccourcis clavier »** visible dans l’onglet ?

### Questions dev suggérées (copier-coller — atelier architecture)

> **Document viewer — comment on récupère les fichiers**  
> 1. Aujourd’hui, comment la fiche client expose-t-elle la **liste** des documents (JSP, API, GED) ?  
> 2. Pour afficher un **PDF** dans PDF.js : quelle est l’URL ou le service à appeler ? Qui génère l’URL (serveur au render vs à la sélection) ?  
> 3. Pour afficher un **JPEG** : même question — lien direct, flux binaire, ou autre ?  
> 4. Quel **identifiant** unique par document doit passer du sélecteur au viewer ?  
> 5. **Authentification** : cookie session, CSRF, headers obligatoires ?  
> 6. Les URLs document sont-elles **réutilisables** hors session ou à durée limitée ?  
> 7. Existe-t-il un **composant ou servlet** « télécharger / ouvrir document » à réutiliser tel quel ?  
> 8. Contraintes **perf** (taille max, timeout) et **cache** côté navigateur ?

---

## 11. Assumptions Index

- **A-1** — Préférences et position persistées **côté serveur** ; fallback session/local si API indisponible au sprint 1.
- **A-10** — `clientId` (contexte fiche) disponible dans la page JSP pour clé de stockage position.
- **A-11** — Zoom/fit **globaux** par utilisateur ; position **par fiche** (confirmé produit 2026-05-20).
- **A-12** — **TIFF in scope MVP** (décision produit) ; rendu technique à trancher (OQ-8).
- **A-13** — Palier clavier **Standard (FR-21)** livré en MVP sauf refus explicite client (OQ-9).
- **A-2** — PDF.js choisi pour production ; viewer natif non retenu (démo A = référence seulement).
- **A-3** — Volume liste ≤ ~10 documents ; pas de virtualisation.
- **A-4** — Droits documents = droits fiche client existants.
- **A-5** — Tri date décroissant en MVP si tri activé.
- **A-6** — Enregistrement préférences avec debounce / fin d’action, pas en continu.
- **A-7** — PDF typique ≤ 5 Mo pour cible perf SM-3.
- **A-8** — Sans réponse client sur impression/téléchargement : **aucun** bouton actif ; politique deny-by-default.
- **A-9** — Un pattern de récupération document **existe déjà** sur la fiche client et sera réutilisé `[ASSUMPTION: à confirmer en OQ-7]`.

---

## 12. Traceability to Demos

| FR / UJ | Référence démo |
|---------|----------------|
| M2 pills, PDF.js | `demo-layout-1.html`, `demo-viewer-libraries.html` |
| M1 table gauche | `demo-layout-2.html` |
| M3 vignettes | `demo-layout-3.html` (hors MVP) |
| PDF natif (non MVP) | `demo-viewer-native.html` |
| TIFF | **Pas encore en démo** — échantillons QA + spike OQ-8 avant recette |
