---
status: complete
stepsCompleted: [1, 2, 3, 4]
validatedDate: 2026-05-20
inputDocuments:
  - prds/prd-document-viewer-2026-05-20/prd.md
  - prds/prd-document-viewer-2026-05-20/addendum.md
  - prds/prd-document-viewer-2026-05-20/livrables-ba.md
  - prds/prd-document-viewer-2026-05-20/livrables-qa.md
  - planning-artifacts/architecture.md
  - ux-design-specification.md
---

# document-viewer - Epic Breakdown

## Overview

Décomposition des exigences PRD, spec UX et analyse d’architecture (partielle) en epics et stories implémentables.

**Ordre de livraison recommandé :** Epic 1 → 2 → 3 → 4 → 5 · Epic 6 en backlog (OQ-6).

## Requirements Inventory

### Functional Requirements

FR-1: L’utilisateur authentifié ouvre l’onglet Document viewer depuis la fiche client sans rechargement full-page.
FR-2: Le système charge la liste des documents du client courant de la fiche.
FR-2a: Le viewer obtient les octets PDF/JPEG/TIFF via un mécanisme documenté (OQ-7), avec auth session (NFR-3).
FR-3: L’utilisateur voit la liste (nom + type) avec indicateur document courant ; sélection clavier/souris.
FR-4: Sélection d’un document déclenche le chargement dans le viewer.
FR-5: À l’ouverture, affichage position mémorisée (FR-19) ou premier document ; repli si doc/page invalide ; FR-14 si liste vide.
FR-6: Tri simple (ex. date décroissante) sur la liste — optionnel MVP assumé inclus.
FR-7: Consultation PDF multi-pages via PDF.js embarqué, sans onglet externe.
FR-8: Zoom et ajustement largeur/hauteur PDF sans déformation ; état reproductible pour persistance.
FR-9: Navigation document précédent/suivant depuis la toolbar ; bornes désactivées ; sync liste.
FR-10: Consultation JPEG ; contrôles page masqués si non pertinents.
FR-10b: Consultation TIFF mono/multi-pages ; navigation pages si multi-pages ; position page persistée.
FR-11: À l’ouverture, chargement position par fiche + prefs zoom/fit globales utilisateur.
FR-12: Enregistrement prefs zoom/fit à modification (debounce).
FR-13: Position par userId+clientId ; zoom/fit globaux par userId.
FR-19: Reprise document + page mémorisés à l’ouverture onglet (PDF/TIFF/JPEG).
FR-20: Enregistrement position sur changement doc/page, leave onglet/fiche (debounced).
FR-21: Navigation clavier Standard — tablist, toolbar, focus visible, Enter/Espace, aria-live.
FR-22: Navigation clavier Avancé — conditionnel OQ-9 (hors MVP par défaut).
FR-14: Message métier si dossier vide ; pas de toolbar pages active.
FR-15: Erreur fichier dans zone viewer ; liste reste utilisable.
FR-16: Formats hors PDF/JPEG/TIFF non supportés ou filtrés.
FR-17: Impression — PENDING OQ-6 (deny-by-default MVP).
FR-18: Téléchargement — PENDING OQ-6 (deny-by-default MVP).

### NonFunctional Requirements

NFR-1: Compatibilité Chrome/Edge récents (liste QA à confirmer).
NFR-2: Accessibilité clavier liste + contrôles ; focus visible.
NFR-3: Mêmes contrôles d’accès que fiche client ; pas d’URL document sans auth.
NFR-4: Premier rendu PDF < 3 s réseau interne (assumption).
NFR-5: Persistance durable serveur ; isolation par utilisateur.
NFR-6: Anti-contournement export si interdit (post OQ-6).
NFR-7: Palier clavier confirmé OQ-9 ; minimum Standard (FR-21).

### Additional Requirements

- Intégration **brownfield JSP** : fragment onglet + module JS (pas starter greenfield).
- **PDF.js** via `pdfjs-dist` (cible 5.7.x) ; worker + CSP ; migration depuis démos 3.11.
- **Façade renderers** : PdfRenderer, JpegRenderer, TiffRenderer derrière ViewerStage.
- API **préférences** + **position lecture** (addendum §2) : GET/PATCH, debounce, repli FR-5.
- Contrat **liste + stream** documents (addendum §7) — **bloqué OQ-7** jusqu’à ADR.
- Moteur **TIFF** (addendum §8) — **bloqué OQ-8**.
- Inventaire libs JS hôte (éviter double PDF.js / jQuery).
- Fallback **localStorage** prefs si API non prête (dette documentée).
- Destroy renderer à chaque changement document (perf/mémoire).
- Deny-by-default impression/téléchargement (OQ-6).

### UX Design Requirements

UX-DR1: Layout MVP **M2 bandeau pills** mappé sur composants framework (réf. demo-layout-1).
UX-DR2: **DocumentPillTablist** — `role="tablist"`, `aria-selected`, roving tabindex (FR-21).
UX-DR3: **ViewerChromeBar** — libellé document + mode ; `aria-live="polite"` sur changement.
UX-DR4: **ViewerToolbar** — pagination/zoom/fit/doc prec-suiv. ; masquage Page −/+ pour JPEG.
UX-DR5: **ViewerStage** — zone rendu scroll ; états loading/error/ready.
UX-DR6: États **vide / erreur / chargement** via composants framework (alert, empty, spinner).
UX-DR7: Hiérarchie boutons — primaire toolbar, pills sélection forte, disabled aux bornes.
UX-DR8: Persistance **silencieuse** — pas de toast succès (reprise à la prochaine visite).
UX-DR9: Desktop-first ; pills `flex-wrap` ; hauteur viewer min/max relative.
UX-DR10: Ordre tab liste → toolbar ; pas de piège focus canvas.
UX-DR11: **Pas de Tailwind en prod** — tokens/composants framework fiche client.

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR-1 | 1 | Onglet fiche |
| FR-2 | 1 | Liste documents client |
| FR-2a | 1,2,3 | Acquisition octets (liste + stream par format) |
| FR-3 | 1 | Affichage liste pills |
| FR-4 | 1 | Sélection document |
| FR-5 | 1,4 | Chargement initial / repli |
| FR-6 | 1 | Tri liste |
| FR-7 | 2 | PDF multipage |
| FR-8 | 2 | Zoom/fit PDF |
| FR-9 | 2 | Doc prec/suiv toolbar |
| FR-10 | 3 | JPEG |
| FR-10b | 3 | TIFF |
| FR-11 | 4 | Lecture prefs + position |
| FR-12 | 4 | Save prefs |
| FR-13 | 4 | Périmètre persistance |
| FR-14 | 1 | Liste vide |
| FR-15 | 2,3 | Erreur chargement |
| FR-16 | 3 | Format non supporté |
| FR-17 | 6 | Impression (backlog) |
| FR-18 | 6 | Téléchargement (backlog) |
| FR-19 | 4 | Reprise position |
| FR-20 | 4 | Save position |
| FR-21 | 5 | Clavier Standard |
| FR-22 | — | Hors MVP (OQ-9) |

## Epic List

### Epic 1: Ouvrir l’onglet et parcourir le dossier
L’utilisateur métier active l’onglet, voit la liste des pièces du client (pills), sélectionne un document et obtient un chargement initial cohérent (premier doc ou placeholder en attendant Epic 4).
**FRs covered:** FR-1, FR-2, FR-3, FR-4, FR-5 (sans persistance), FR-6, FR-14 · **UX-DR:** 1, 6, 7, 9, 11

### Epic 2: Consulter les documents PDF
L’utilisateur lit un PDF multi-pages dans le viewer embarqué avec toolbar (pages, zoom, fit, doc. prec/suiv.).
**FRs covered:** FR-7, FR-8, FR-9, FR-15 (PDF) · **FR-2a** (stream PDF) · **UX-DR:** 3, 4, 5

### Epic 3: Consulter les images JPEG et TIFF
L’utilisateur consulte JPEG et TIFF (mono/multi-pages) avec contrôles adaptés et gestion des formats non supportés.
**FRs covered:** FR-10, FR-10b, FR-15 (images), FR-16 · **FR-2a** (stream images) · **UX-DR:** 4, 5

### Epic 4: Reprendre sa lecture et ses réglages
L’utilisateur retrouve zoom/fit et la dernière position document+page **par fiche client** à chaque visite.
**FRs covered:** FR-11, FR-12, FR-13, FR-19, FR-20, FR-5 (repli complet) · **UX-DR:** 8

### Epic 5: Utiliser le viewer au clavier (Standard)
L’utilisateur parcourt liste et toolbar sans souris, avec focus visible et annonces accessibles.
**FRs covered:** FR-21 · **NFR:** 2, 7 · **UX-DR:** 2, 10

### Epic 6: Impression et téléchargement (backlog — OQ-6)
Politique export client ; deny-by-default jusqu’à décision.
**FRs covered:** FR-17, FR-18 · **NFR:** 6

---

## Epic 1: Ouvrir l’onglet et parcourir le dossier

L’utilisateur métier active l’onglet Document viewer, voit et parcourt la liste des documents du dossier client.

### Story 1.1: Intégrer l’onglet Document viewer dans la fiche JSP

As a **utilisateur métier**,
I want **un onglet Document viewer sur la fiche client**,
So that **je accède à la consultation des pièces sans quitter le contexte client**.

**Acceptance Criteria:**

**Given** je suis authentifié avec droit d’accès aux documents du dossier
**When** j’ouvre la fiche client
**Then** l’onglet Document viewer est visible et activable (FR-1)
**And** l’activation affiche le contenu de l’onglet sans rechargement full-page de la fiche
**And** le fragment JSP inclut le conteneur racine du module JS (`clientId` exposé au script)

### Story 1.2: Charger la liste des documents du client

As a **utilisateur métier**,
I want **voir la liste des documents rattachés au client courant**,
So that **je sache quelles pièces sont disponibles**.

**Acceptance Criteria:**

**Given** l’onglet Document viewer est actif pour un `clientId`
**When** le module s’initialise
**Then** la liste est chargée via le contrat retenu (JSP inline ou API JSON — OQ-7) (FR-2, FR-2a métadonnées)
**And** chaque entrée expose au minimum `documentId`, nom, type MIME ou libellé
**And** les requêtes incluent les credentials de session (NFR-3)
**And** un indicateur de chargement s’affiche pendant le fetch (UX-DR6)

### Story 1.3: Afficher et sélectionner des documents via le bandeau pills

As a **utilisateur métier**,
I want **sélectionner un document dans un bandeau pills (M2)**,
So that **je indique clairement quelle pièce consulter**.

**Acceptance Criteria:**

**Given** la liste contient ≥ 1 document
**When** l’onglet s’affiche
**Then** les pills montrent nom + badge type (FR-3, UX-DR1, UX-DR11)
**When** je clique une pill
**Then** elle devient le document courant (FR-4) et déclenche le chargement viewer
**And** une seule pill a le style « sélectionné » (UX-DR7)
**And** le compteur optionnel « N / total » est affiché si présent dans la maquette framework

### Story 1.4: Appliquer le chargement initial (premier document)

As a **utilisateur métier**,
I want **qu’un document pertinent s’affiche dès l’ouverture de l’onglet**,
So that **je n’ai pas un écran vide inutile**.

**Acceptance Criteria:**

**Given** la liste contient ≥ 1 document et Epic 4 n’est pas encore livré
**When** j’ouvre l’onglet
**Then** le **premier document** après tri (FR-6) est sélectionné et chargé (FR-5 repli sans FR-19)
**Given** Epic 4 est livré
**When** j’ouvre l’onglet
**Then** FR-19/FR-5 s’appliquent (story 4.3)
**And** le viewer stage affiche l’état chargement (UX-DR5)

### Story 1.5: Trier la liste des documents

As a **utilisateur métier**,
I want **une liste triée de façon prévisible**,
So that **je retrouve rapidement les pièces récentes**.

**Acceptance Criteria:**

**Given** plusieurs documents dans le dossier
**When** la liste est rendue
**Then** l’ordre par défaut est documenté (ex. date décroissante) (FR-6)
**And** l’ordre est identique entre rechargements pour le même dossier

### Story 1.6: Afficher l’état dossier vide

As a **utilisateur métier**,
I want **un message clair si aucun document n’est disponible**,
So that **je comprends que le dossier est vide et non qu’il y a une panne**.

**Acceptance Criteria:**

**Given** la liste retournée est vide
**When** j’ouvre l’onglet
**Then** un message métier explicite s’affiche (FR-14, UX-DR6)
**And** la zone viewer reste vide ou placeholder neutre
**And** la toolbar pages n’est pas affichée comme active

---

## Epic 2: Consulter les documents PDF

L’utilisateur consulte des PDF multi-pages dans le viewer embarqué avec PDF.js.

### Story 2.1: Intégrer PDF.js dans le build applicatif

As a **développeur**,
I want **PDF.js (pdfjs-dist) bundlé avec worker et CSP compatibles**,
So that **le rendu PDF est fiable en embed JSP**.

**Acceptance Criteria:**

**Given** le pipeline build du projet hôte
**When** le bundle document-viewer est produit
**Then** `pdfjs-dist` (version cible documentée, ex. 5.7.x) et le worker sont référencés correctement
**And** aucun conflit avec une autre instance PDF.js/jQuery existante
**And** la CSP autorise worker + fetch même origine (addendum §1)

### Story 2.2: Charger le flux PDF authentifié

As a **utilisateur métier**,
I want **que le PDF se charge depuis le serveur avec ma session**,
So that **je consulte des documents autorisés sans lien public**.

**Acceptance Criteria:**

**Given** un document PDF sélectionné dans la liste
**When** le viewer charge le document
**Then** les octets sont obtenus via le contrat stream retenu (OQ-7 P1/P2/P3) (FR-2a, NFR-3)
**And** `fetch` utilise `credentials: 'include'` ou équivalent session
**And** le document est passé à PDF.js en `ArrayBuffer`
**And** un spinner s’affiche jusqu’au premier rendu (UX-DR5, NFR-4)

### Story 2.3: Afficher et naviguer dans les pages PDF

As a **utilisateur métier**,
I want **parcourir les pages d’un PDF dans le viewer**,
So that **je lis un contrat multi-pages sans quitter la fiche**.

**Acceptance Criteria:**

**Given** un PDF valide chargé
**When** le rendu est prêt
**Then** la page courante s’affiche sur canvas sans ouvrir un onglet navigateur (FR-7)
**When** j’utilise Page − / Page +
**Then** la page change et le libellé « page X / Y » est mis à jour (UX-DR4)
**And** les boutons sont désactivés aux bornes 1 et Y (UX-DR7)

### Story 2.4: Zoom et ajuster largeur / hauteur (PDF)

As a **utilisateur métier**,
I want **zoomer et ajuster le PDF à la largeur ou hauteur du viewer**,
So that **je lis confortablement selon le format du document**.

**Acceptance Criteria:**

**Given** un PDF affiché
**When** j’utilise Zoom − / Zoom + ou Largeur / Hauteur
**Then** le rendu respecte le ratio sans déformation (FR-8)
**And** l’état zoom/fit est exposé au module persistance (préparation FR-12)
**And** les contrôles suivent la hiérarchie UX (UX-DR4, UX-DR7)

### Story 2.5: Naviguer entre documents depuis la toolbar

As a **utilisateur métier**,
I want **passer au document précédent ou suivant depuis la barre du viewer**,
So that **j’enchaîne les pièces sans revenir uniquement aux pills**.

**Acceptance Criteria:**

**Given** ≥ 2 documents dans la liste
**When** j’active Doc. préc. ou Doc. suiv.
**Then** le document courant change (FR-9)
**And** la pill correspondante est synchronisée
**And** les boutons sont désactivés sur le premier / dernier document
**And** le renderer précédent est détruit avant chargement du suivant (additional req)

### Story 2.6: Gérer l’échec de chargement d’un PDF

As a **utilisateur métier**,
I want **un message clair si un PDF ne charge pas**,
So that **je peux essayer un autre document**.

**Acceptance Criteria:**

**Given** un PDF inaccessible (403, 404, timeout, corrompu)
**When** le chargement échoue
**Then** un message métier s’affiche dans la zone viewer (FR-15, UX-DR6)
**And** les pills restent cliquables pour sélectionner un autre document
**And** aucune stack trace n’est visible

---

## Epic 3: Consulter les images JPEG et TIFF

L’utilisateur consulte JPEG et TIFF dans la même zone viewer.

### Story 3.1: Afficher les documents JPEG

As a **utilisateur métier**,
I want **consulter une image JPEG dans le viewer**,
So that **je vérifie des photos ou scans raster sans application externe**.

**Acceptance Criteria:**

**Given** un document JPEG sélectionné
**When** le flux image est chargé (FR-2a)
**Then** l’image est visible dans ViewerStage avec zoom/fit cohérents (FR-10, UX-DR5)
**And** les boutons Page − / Page + sont masqués ou désactivés (UX-DR4)
**And** la barre chrome indique le mode image (UX-DR3)

### Story 3.2: Afficher les documents TIFF (mono et multi-pages)

As a **utilisateur métier**,
I want **consulter des TIFF y compris multi-pages**,
So that **je traite les scans GED comme les PDF**.

**Acceptance Criteria:**

**Given** un TIFF sélectionné
**When** le moteur de rendu retenu (OQ-8) charge le fichier
**Then** le TIFF s’affiche sans téléchargement obligatoire (FR-10b)
**Given** un TIFF multi-pages
**When** j’utilise Page − / Page +
**Then** la navigation page fonctionne comme pour PDF avec compteur page X / Y
**Given** un TIFF une page
**Then** la navigation page est masquée
**And** les jeux de test QA couvrent au moins un TIFF baseline et un multipage `[ASSUMPTION]`

### Story 3.3: Gérer les erreurs de chargement image/TIFF

As a **utilisateur métier**,
I want **le même comportement d’erreur que pour les PDF**,
So that **l’expérience reste cohérente**.

**Acceptance Criteria:**

**Given** un JPEG ou TIFF en échec de chargement
**When** l’erreur survient
**Then** FR-15 s’applique (message viewer, liste utilisable)
**And** le mode erreur utilise les composants framework (UX-DR6)

### Story 3.4: Traiter les formats non supportés

As a **utilisateur métier**,
I want **ne pas voir de formats hors périmètre proposés comme consultables**,
So that **je ne lance pas de chargements voués à l’échec**.

**Acceptance Criteria:**

**Given** un document dont le type n’est pas PDF, JPEG ou TIFF
**When** il apparaît côté serveur
**Then** il est filtré en amont **ou** un message « non supporté » s’affiche à la sélection (FR-16)
**And** le comportement est documenté pour QA

---

## Epic 4: Reprendre sa lecture et ses réglages

L’utilisateur retrouve zoom, fit et position document+page par fiche.

### Story 4.1: Exposer les API préférences et position de lecture

As a **développeur**,
I want **des endpoints GET/PATCH documentés pour prefs et position**,
So that **la persistance est centralisée et auditable**.

**Acceptance Criteria:**

**Given** un utilisateur authentifié
**When** le contrat addendum §2 est implémenté côté serveur
**Then** GET/PATCH prefs globales (`pdfZoom`, `pdfDefaultFit`) fonctionnent (FR-13)
**And** GET position par `clientId` retourne `documentId` + `pageNumber` ou 404
**And** PATCH position met à jour `updatedAt` (NFR-5, isolation par userId)

### Story 4.2: Appliquer et enregistrer les préférences zoom / fit

As a **utilisateur métier**,
I want **retrouver mon zoom et mon mode d’ajustement habituels**,
So that **je n’ai pas à reconfigurer à chaque visite**.

**Acceptance Criteria:**

**Given** des prefs enregistrées pour mon userId
**When** j’ouvre l’onglet sur n’importe quelle fiche
**Then** zoom et fit sont appliqués au PDF (FR-11, FR-12)
**When** je modifie zoom ou fit
**Then** les valeurs sont persistées (debounce) sans toast de succès (UX-DR8)
**Given** l’API serveur indisponible en sprint 1
**Then** un fallback localStorage documenté est actif (dette explicite)

### Story 4.3: Reprendre et enregistrer la position par fiche client

As a **utilisateur métier**,
I want **retrouver le même document et la même page sur chaque fiche**,
So that **je reprends ma lecture où je l’avais laissée**.

**Acceptance Criteria:**

**Given** une position enregistrée pour (userId, clientId)
**When** j’ouvre l’onglet sur cette fiche
**Then** le document mémorisé est sélectionné et la page affichée (FR-19, UJ-1)
**When** je change de document ou de page
**Then** la position est enregistrée debounced (FR-20)
**When** je quitte l’onglet ou la fiche
**Then** un save final est déclenché `[ASSUMPTION: hook shell JSP]`
**And** les fiches A et B conservent des positions indépendantes (FR-13, UJ-3)

### Story 4.4: Replier gracieusement les positions invalides

As a **utilisateur métier**,
I want **un comportement cohérent si ma position mémorisée n’est plus valide**,
So that **je ne reste pas bloqué**.

**Acceptance Criteria:**

**Given** un `documentId` mémorisé absent de la liste courante
**When** j’ouvre l’onglet
**Then** le premier document disponible page 1 est affiché (FR-5)
**Given** une `pageNumber` > nombre de pages du document
**When** le document charge
**Then** la dernière page du document est affichée (FR-5)
**And** aucune erreur technique n’est montrée à l’utilisateur

---

## Epic 5: Utiliser le viewer au clavier (Standard)

L’utilisateur utilise le viewer sans souris (palier Standard).

### Story 5.1: Navigation clavier dans la liste pills (tablist)

As a **utilisateur métier**,
I want **parcourir et activer les documents au clavier**,
So that **je consulte le dossier sans souris**.

**Acceptance Criteria:**

**Given** le bandeau pills rendu
**When** j’utilise Tab / Shift+Tab
**Then** le focus se déplace entre les pills (FR-21, UX-DR2)
**When** j’appuie Entrée ou Espace sur une pill focusée
**Then** le document se charge comme un clic (FR-21)
**And** `role="tablist"`, `role="tab"`, `aria-selected` sont présents
**And** le focus visible respecte le framework (NFR-2)

### Story 5.2: Navigation clavier dans la toolbar

As a **utilisateur métier**,
I want **actionner les contrôles du viewer au clavier**,
So that **je change de page, zoom et document sans souris**.

**Acceptance Criteria:**

**Given** un PDF ou TIFF multi-pages affiché
**When** je tabule après la liste
**Then** le focus parcourt les boutons de la toolbar dans l’ordre logique (UX-DR10)
**When** j’active Page − / Page + au clavier
**Then** la page change (FR-21)
**And** les boutons désactivés ne reçoivent pas l’action

### Story 5.3: Annoncer les changements document et page

As a **utilisateur métier**,
I want **que les changements importants soient annoncés aux technologies d’assistance**,
So that **je suis l’état du viewer**.

**Acceptance Criteria:**

**Given** un changement de document ou de page
**When** le viewer met à jour l’affichage
**Then** une région `aria-live="polite"` annonce le changement (FR-21, UX-DR3)
**And** les boutons icône-seuls ont un nom accessible
**And** le focus ne est pas piégé dans le canvas PDF (UX-DR10)

---

## Epic 6: Impression et téléchargement (backlog — OQ-6)

**Statut :** en attente décision client · deny-by-default en MVP.

### Story 6.1: Implémenter la politique impression / téléchargement (placeholder)

As a **product owner**,
I want **impression et téléchargement alignés sur la décision client**,
So that **la conformité métier est respectée**.

**Acceptance Criteria:**

**Given** la réponse OQ-6 est documentée
**When** le client autorise ou interdit print/download par rôle
**Then** les boutons et garde-fous FR-17/FR-18 sont implémentés (NFR-6)
**Until** OQ-6 est tranché
**Then** aucun bouton actif d’impression/téléchargement n’est livré (deny-by-default)
**And** la toolbar PDF.js n’expose pas d’actions de téléchargement non contrôlées

---

## Validation Report (étape 4 — 2026-05-20)

### FR Coverage — ✅ PASS

| Statut | Détail |
|--------|--------|
| Couvert | FR-1 à FR-21 + FR-2a, FR-10b (24 FR MVP) |
| Backlog | FR-17, FR-18 → Epic 6 (OQ-6) |
| Hors MVP | FR-22 (palier Avancé, OQ-9) — documenté dans la matrice |

### UX Design Requirements — ✅ PASS (1 écart mineur)

| UX-DR | Couverture |
|-------|------------|
| UX-DR1–8, 10–11 | Stories explicites |
| UX-DR9 | Listé Epic 1 ; **recommandation** : ajouter AC flex-wrap / hauteur viewer en recette 1.3 si absent du framework |

**Écart mineur :** UX-DR3 (chrome bar) explicite pour images (3.1) et a11y (5.3) — **ajouter** libellé mode PDF en recette story 2.3 si non couvert par le framework.

### Architecture / Starter — ✅ PASS (brownfield)

- Pas de starter greenfield : **Story 1.1** (fragment JSP) conforme à l’analyse d’architecture.
- **Avertissement :** `architecture.md` incomplet (étapes 1–2) — trancher **OQ-7 / OQ-8** avant stories **2.2**, **3.2**, **4.1**.

### Story Quality — ✅ PASS

- 24 stories avec AC Given/When/Then.
- Taille adaptée à un agent dev par story.
- Story **1.4** : dépendance **forward** vers Epic 4 documentée explicitement (premier doc jusqu’à 4.3) — acceptable.

### Epic & Dependencies — ✅ PASS

| Epic | Indépendance |
|------|----------------|
| 1 | Valeur seule (liste + shell) |
| 2 | Requiert 1 ; livrable PDF autonome |
| 3 | Requiert 1 ; JPEG/TIFF autonome |
| 4 | Requiert 2 ou 3 pour page PDF ; API + prefs |
| 5 | Requiert UI 1–3 |
| 6 | Backlog |

**File churn :** module `document-viewer` partagé — découpé par **capability utilisateur**, pas par couche technique — validé.

### Verdict

**✅ Prêt pour sprint planning** sous réserve : finaliser ADR fetch/TIFF (CA) et PRD `final` recommandés avant **2.2** / **4.1**.
