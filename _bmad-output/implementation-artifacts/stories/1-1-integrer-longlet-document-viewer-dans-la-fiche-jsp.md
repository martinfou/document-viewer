# Story 1.1: Intégrer l’onglet Document viewer dans la fiche JSP

Status: ready-for-dev

<!-- Validation optionnelle : bmad-create-story:validate avant dev-story -->

## Story

As a **utilisateur métier**,
I want **un onglet Document viewer sur la fiche client**,
so that **j’accède à la consultation des pièces sans quitter le contexte client**.

## Acceptance Criteria

1. **Given** je suis authentifié avec le droit d’accès aux documents du dossier  
   **When** j’ouvre la fiche client  
   **Then** l’onglet **Document viewer** est visible et activable (FR-1)

2. **Given** la fiche client est affichée  
   **When** j’active l’onglet Document viewer  
   **Then** le contenu de l’onglet s’affiche **sans rechargement full-page** de la fiche (FR-1)

3. **Given** l’onglet est actif  
   **When** le fragment est rendu  
   **Then** un conteneur racine `#document-viewer-root` (ou convention équivalente du framework) est présent dans le DOM

4. **Given** le conteneur racine existe  
   **When** le module JS s’initialise (story 1.2+)  
   **Then** l’attribut ou data-bind **`clientId`** (identifiant fiche client stable) est disponible sur le conteneur ou via config globale fiche

5. **Given** les autres onglets de la fiche (Général, etc.)  
   **When** je bascule entre onglets  
   **Then** le comportement d’onglets existant de la fiche **n’est pas régressé**

## Tasks / Subtasks

- [ ] **T1 — Cartographier le shell onglets existant** (AC: 1, 5)
  - [ ] Identifier le JSP/layout parent des onglets fiche client (chemin réel dans le dépôt hôte)
  - [ ] Documenter le pattern d’ajout d’onglet (include, taglib, config XML, etc.)
  - [ ] Vérifier alignement droits : même règle que « accès documents dossier » (PRD FR-1 assumption)

- [ ] **T2 — Créer le fragment JSP onglet** (AC: 2, 3, 4)
  - [ ] Fichier fragment dédié (ex. `document-viewer-tab.jsp` ou include dans fiche)
  - [ ] Markup minimal : `region` / panel framework + `#document-viewer-root`
  - [ ] Exposer `clientId` : `${clientId}` ou équivalent modèle serveur existant
  - [ ] **Ne pas** importer Tailwind ; utiliser classes framework (UX-DR11)

- [ ] **T3 — Enregistrer l’onglet dans la navigation fiche** (AC: 1)
  - [ ] Libellé FR : « Document viewer » (ou libellé métier validé BA)
  - [ ] Ordre d’onglet documenté (après Général ou selon charte produit)

- [ ] **T4 — Point d’entrée JS (stub)** (AC: 4)
  - [ ] Charger un bundle vide ou `document-viewer/init.js` qui ne fait qu’`console.debug` + vérifie `clientId`
  - [ ] Pas de PDF.js ni liste documents dans cette story (stories 1.2+)

- [ ] **T5 — Tests manuels / smoke** (AC: 1–5)
  - [ ] Onglet visible pour utilisateur avec droit ; masqué sinon (si applicable)
  - [ ] Activation sans full reload ; `clientId` présent dans le DOM
  - [ ] Régression : autres onglets OK

## Dev Notes

### Contexte dépôt

| Dépôt | Rôle |
|-------|------|
| **`document-viewer` (ce repo)** | Planning BMad, démos UX (`_bmad-output/demos/`), **pas de code JSP prod** |
| **Application hôte JSP** | **Cible d’implémentation** — intégrer fragment + assets |

Si le code prod vit plus tard dans ce repo, créer `src/main/webapp/...` en miroir de la structure hôte documentée en T1.

### Référence UX (interaction seulement)

- Démo onglets : `_bmad-output/demos/demo-layout-1.html` L.33–36 (onglet « Document viewer » simulé)
- **Ne pas** copier Tailwind/Alpine en prod — spec UX § Design System Foundation

### Architecture (partielle)

- Brownfield : pas de starter greenfield [Source: `architecture.md` — Project Context]
- Story 1.1 = **socle shell** ; Epic 1 stories suivantes ajoutent liste + pills
- Inventorier libs JS existantes sur la fiche avant d’ajouter le bundle (éviter double jQuery) [Source: `architecture.md` — Cross-Cutting]

### Structure fichiers proposée (hôte — à adapter)

```
webapp/
  WEB-INF/jsp/fiche-client/
    document-viewer-tab.jsp      # NEW — fragment onglet
  static/js/document-viewer/
    init.js                      # NEW — stub init (story 1.1)
    document-viewer.css          # NEW — vide ou placeholder framework
```

### Comportement attendu à la fin de 1.1

```
[Fiche client tabs] ... | Document viewer |
┌─────────────────────────────────────────┐
│ #document-viewer-root                   │
│   data-client-id="123456"               │
│   (zone vide ou message "Chargement…")   │
└─────────────────────────────────────────┘
```

### Testing

- Smoke manuel navigateur cible (Chrome/Edge — NFR-1)
- Pas de tests automatisés obligatoires MVP pour 1.1 ; option : test d’intégration JSP si framework QA l’exige
- Traçabilité QA : lier à cas CU-1 préconditions (onglet accessible) — `livrables-qa.md`

### Ce qui est hors scope (1.1)

- Liste documents, pills, PDF.js (stories 1.2–2.x)
- API préférences / position (Epic 4)
- Navigation clavier complète (Epic 5)

### References

- [Source: `_bmad-output/planning-artifacts/epics.md` — Story 1.1]
- [Source: `_bmad-output/planning-artifacts/prds/prd-document-viewer-2026-05-20/prd.md` — FR-1, §4.1]
- [Source: `_bmad-output/planning-artifacts/ux-design-specification.md` — Epic 1, UX-DR11]
- [Source: `_bmad-output/planning-artifacts/architecture.md` — Intégration JSP]
- [Source: `_bmad-output/planning-artifacts/prds/prd-document-viewer-2026-05-20/livrables-ba.md` — CU-1]

## Dev Agent Record

### Agent Model Used

_(à remplir par l’agent dev)_

### Debug Log References

### Completion Notes List

### File List
