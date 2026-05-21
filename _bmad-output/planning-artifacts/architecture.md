---
stepsCompleted: [1, 2]
inputDocuments:
  - prds/prd-document-viewer-2026-05-20/prd.md
  - prds/prd-document-viewer-2026-05-20/addendum.md
  - prds/prd-document-viewer-2026-05-20/livrables-ba.md
  - prds/prd-document-viewer-2026-05-20/livrables-qa.md
  - prds/prd-document-viewer-2026-05-20/.decision-log.md
  - ux-design-specification.md
workflowType: architecture
project_name: document-viewer
user_name: breaking-code
date: 2026-05-20
---

# Architecture Decision Document

_Ce document est construit collaborativement, étape par étape. Les sections sont ajoutées au fil des décisions architecturales._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
- **Intégration (FR-1–2, FR-2a)** : onglet fiche sans full reload ; liste + bytes documents via mécanisme **à définir** (OQ-7) avec auth session.
- **Liste (FR-3–6)** : pills MVP, sélection, repli position/first doc, tri optionnel.
- **Viewers (FR-7–10b)** : PDF.js multipage ; JPEG ; TIFF (multi-pages aligné PDF) — **3 adaptateurs rendu** derrière une façade `ViewerStage`.
- **Navigation (FR-9, FR-21–22)** : doc. préc./suiv. ; clavier Standard MVP ; Avancé conditionnel OQ-9.
- **Persistance (FR-11–13, FR-19–20)** : GET/PATCH prefs + position par `clientId` ; debounce ; invalidation si doc absent.
- **Robustesse (FR-14–16)** : empty, erreur fichier, format non supporté.
- **Export (FR-17–18)** : pending OQ-6 — architecture deny-by-default jusqu’à décision.

**Non-Functional Requirements:**
- **NFR-1** : Chrome/Edge récents.
- **NFR-2/7** : clavier + focus ; WCAG AA si OQ-9 confirmé.
- **NFR-3** : contrôle d’accès aligné fiche ; pas d’URL document non authentifiée.
- **NFR-4** : premier rendu PDF < 3 s (réseau interne).
- **NFR-5** : persistance durable serveur ; isolation par utilisateur.
- **NFR-6** : anti-contournement export si interdit.

**Scale & Complexity:**
- Primary domain: web embarqué (JSP + module JS) dans application métier existante
- Complexity level: **medium**
- Estimated architectural components: ~8–10 (shell tab, document list API adapter, document stream adapter, viewer orchestrator, 3 renderers, preferences API client, persistence debouncer, error/empty state handler)

### Technical Constraints & Dependencies

- Héritage shell onglets et droits fiche client existants.
- PDF.js (worker, CSP, bundling) — pas viewer natif iframe.
- Inventaire libs JS projet (éviter conflits jQuery / double PDF.js).
- Spec UX : framework UI prod ; démos = référence interaction uniquement.
- Pas de mobile MVP ; pas de offline.
- Questions ouvertes bloquantes pour détail implémentation : **OQ-7** (liste + stream), **OQ-8** (TIFF), **OQ-6** (export), **OQ-9** (a11y).

### Cross-Cutting Concerns Identified

1. **Authentification et autorisation** — toutes requêtes liste/stream/prefs.
2. **Acquisition document** — contrat API ou JSP model (OQ-7).
3. **Rendu multi-format** — PDF.js vs image vs TIFF (OQ-8).
4. **État client viewer** — sélection, page, zoom, loading, error.
5. **Persistance utilisateur** — serveur cible, fallback localStorage (dette sprint 1).
6. **Accessibilité** — tablist, toolbar, aria-live.
7. **Performance perçue** — lazy load bytes, debounce save, destroy renderer on switch.
8. **Sécurité export** — CSP, désactivation toolbar PDF.js si deny (post OQ-6).
