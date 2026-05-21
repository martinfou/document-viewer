# Addendum technique — Document viewer

Décisions et mécanismes qui **ne sont pas** des exigences produit dans le PRD, mais guident architecture et implémentation.

---

## 1. Moteur PDF : PDF.js (retenu) vs viewer natif (écarté)

| Option | Verdict | Raison |
|--------|---------|--------|
| **PDF.js** (démo B, layouts 1–3) | **Production MVP** | Rendu canvas contrôlé ; toolbar unifiée ; comportement stable en embed JSP / Electron |
| **Viewer natif** (`iframe`, démo A) | **Référence seulement** | Téléchargement / zone noire selon navigateur ; peu fiable en embedded |

**Implication :** bundling PDF.js, worker, CSP, chargement document via `fetch` + `ArrayBuffer` (pas `file://`).

---

## 2. Préférences utilisateur — options considérées

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **API serveur profil utilisateur** | Multi-poste, conforme outil interne, audit possible | Dépendance backend, contrat API |
| **localStorage / sessionStorage** | Rapide à prototyper | Pas de sync poste ; effacement navigateur |
| **Cookie** | — | Taille limitée ; pas adapté zoom structuré |

**Recommandation architecture (alignée PRD A-1) :**
- **MVP cible :** persistance **serveur** (JSON : `{ zoom, defaultFit: "width"|"height" }`).
- **Fallback sprint 1 :** localStorage même clé si API non prête — documenter dette dans story E5.

**Champs v1 proposés :**

*Préférences globales (utilisateur) :*
```json
{
  "documentViewer": {
    "pdfZoom": 1.25,
    "pdfDefaultFit": "width"
  }
}
```

*Position de lecture (utilisateur + fiche client) — **in scope MVP** :*
```json
{
  "documentViewerReadingPosition": {
    "clientId": "12345",
    "documentId": "doc-uuid-or-ged-key",
    "pageNumber": 3,
    "updatedAt": "2026-05-20T14:32:00Z"
  }
}
```

- **GET** à l’ouverture onglet : `?clientId=` → position ou 404 → repli FR-5.
- **PUT/PATCH** sur changement document, page (debounced), ou fermeture onglet/fiche.
- **JPEG :** enregistrer `documentId`, `pageNumber: 1` ou omettre page.
- **Invalidation :** si `documentId` ∉ liste courante → ignorer position, repli premier doc.

**Hors v1 :** `layoutMode`, `theme`, bookmark partagé entre utilisateurs.

---

## 3. Layouts M1 / M2 / M3

| Mock | Rôle |
|------|------|
| **M2 bandeau pills** | **MVP production** (`demo-layout-1.html`) |
| **M1 table gauche** | Variante secteur assurance — feedback (`demo-layout-2.html`) |
| **M3 vignettes** | Option ; requiert thumbs PDF serveur (`demo-layout-3.html`) |

---

## 4. Intégration JSP

- Shell : onglet existant fiche client ; contenu = fragment JSP + assets JS.
- Liste alimentée par **API / modèle serveur existant** `[à préciser en architecture — OQ-7]`.
- Inventaire libs JS du projet : **tâche architecture** (éviter double jQuery / conflits PDF.js).

---

## 7. Récupération des documents PDF et images (OQ-7 — à trancher avec les devs)

Les démos utilisent des fichiers statiques (`samples/*.pdf`, `*.jpg`) servis en HTTP avec `fetch` + `ArrayBuffer` (PDF.js). **La production JSP ne reproduira pas ce mécanisme tel quel** sans décision d’architecture.

### 7.1 Liste (métadonnées)

| Option | Description | À clarifier avec dev |
|--------|-------------|----------------------|
| **A — JSP inline** | Le serveur rend la liste en HTML (pills) au chargement de l’onglet | Champs disponibles dans le modèle ? id document ? |
| **B — API JSON** | AJAX au focus onglet : `GET .../clients/{id}/documents` | Contrat OpenAPI ? pagination ? |
| **C — Hybride** | Première liste en JSP ; refresh AJAX | Cas changement dossier en session |

### 7.2 Contenu PDF (octets pour PDF.js)

| Option | Description | Impact |
|--------|-------------|--------|
| **P1 — URL même origine** | `fetch(url, { credentials: 'include' })` → `ArrayBuffer` | Aligné démos ; CSP `connect-src` |
| **P2 — Servlet stream** | `/document/stream?id=` sans exposer chemin GED | Bon pour auth centralisée |
| **P3 — URL GED signée** | Lien temporaire renvoyé par le serveur à la sélection | Gérer expiration + erreur FR-15 |
| **P4 — Base64 dans page** | Rare ; éviter gros PDF | Perf |

**Recommandation de travail :** privilégier **P1 ou P2** avec session cookie ; documenter le contrat dans l’architecture.

### 7.3 Contenu JPEG

| Option | Description |
|--------|-------------|
| **I1 — `img src=url`** | URL authentifiée (cookie) — simple si pas de CORS |
| **I2 — `fetch` → blob URL** | Même pipeline que PDF si en-têtes custom / CSRF |
| **I3 — Inline base64** | Petites images seulement |

### 7.4 Checklist atelier dev (résultat attendu)

- [ ] Diagramme séquence : sélection pill → requête(s) → affichage viewer  
- [ ] Exemple de payload liste (1 entrée PDF, 1 JPEG, 1 TIFF)  
- [ ] Exemple d’URL ou d’appel pour ouvrir le PDF #1  
- [ ] Matrice erreurs (403, 404, 500) → message FR-15  
- [ ] Alignement avec téléchargement existant (si OQ-6 autorise FR-18)

---

## 8. Rendu TIFF (OQ-8 — MVP)

**Décision produit :** TIFF **in scope MVP** (PDF, JPEG, TIFF). Les démos actuelles ne couvrent pas encore le TIFF.

| Option | Description | Notes |
|--------|-------------|--------|
| **T1 — Lib JS cliente** | `fetch` bytes → UTIF.js / tiff.js → canvas par page | Aligné modèle PDF.js ; attention perf gros fichiers |
| **T2 — Conversion serveur** | Servlet renvoie PNG/JPEG par page (ou tuile) | Plus prévisible en entreprise ; charge serveur |
| **T3 — Hybride** | TIFF simple en client ; gros/multi-page en serveur | Complexité |

**UX cible :** toolbar pages **identique PDF** pour TIFF multi-pages ; zoom/fit partagés (FR-8). Position lecture (FR-19/20) avec `pageNumber`.

**QA :** obtenir 2–3 TIFF réels GED (mono + multi-pages, compressions courantes) pour DT-7.

---

## 9. Navigation clavier — référence implémentation (OQ-9)

Aligné **§8.1 PRD** et viewers documentaires courants (Adobe Acrobat web, PDF.js UI examples, viewers GED enterprise, **WAI-ARIA Authoring Practices** — tabs & toolbar).

### 9.1 Structure focus (palier Standard)

```
[Onglet Document viewer actif]
  → tablist (pills documents)     Tab / Shift+Tab, Enter/Space activer
  → toolbar viewer                Tab entre boutons
  → (canvas document — pas dans l’ordre Tab ; aria-label « Document … page N »)
```

### 9.2 Raccourcis suggérés (palier Avancé — valider avec client)

| Action | Raccourci proposé | Alternative industrie |
|--------|-------------------|------------------------|
| Document suivant | `Alt+↓` ou `]` | Flèche → dans tablist |
| Document précédent | `Alt+↑` ou `[` | Flèche ← |
| Page suivante | `Page Down` ou `↓` (focus viewer) | PDF.js default patterns |
| Page précédente | `Page Up` ou `↑` | idem |
| Zoom + | `+` ou `Ctrl++` | Éviter conflit navigateur |
| Zoom − | `-` | idem |
| Ajuster largeur | `W` (si pas conflit) | Bouton toolbar prioritaire en Standard |

**Livraison :** panneau « ? Raccourcis » ou lien aide — exigence OQ-9.

### 9.3 Lecteur d’écran

- Annoncer : nom document, type, page X sur Y au changement.
- Pills : `role="tab"`, `aria-selected="true|false"`.
- Boutons icône : `aria-label` explicite (pas « bouton » seul).
- États vide/erreur : `role="status"` ou `alert`.

### 9.4 Tests QA

- Parcours clavier seul : CU-1 + changement document + 3 pages (TC-12 étendu).
- VoiceOver / NVDA smoke si OQ-9 = oui lecteur d’écran.

---

## 5. Impression et téléchargement (en attente client)

**Décision requise avant implémentation** (PRD OQ-6, FR-17, FR-18).

| Scénario | Implication technique |
|----------|----------------------|
| **Interdit** | Pas de boutons ; désactiver/masquer print PDF.js ; URLs en streaming authentifié sans `Content-Disposition: attachment` sauf besoin inverse ; considérer durcissement Ctrl+P |
| **Autorisé (global)** | Boutons toolbar ; print PDF.js ou `window.print` sur zone viewer ; téléchargement via endpoint existant avec audit |
| **Autorisé par rôle/type** | Même UI mais actions gated côté serveur + masquage client selon métadonnées document |

**Alignement :** vérifier si la fiche client a déjà des actions Télécharger / Imprimer par document — réutiliser la matrice de droits.

**Traçabilité :** si le client exige un journal des exports, prévoir événement serveur (hors scope PRD jusqu’à confirmation).

---

## 6. Options post-MVP (estimations indicatives du brainstorm)

| Option | Ordre de grandeur |
|--------|-------------------|
| Recherche texte dans PDF | ~1–2 j |
| Thumbs PDF serveur (M3) | dépend infra GED |
| Dernier document mémorisé | ~0,5–1 j + API |
| Groupement catégories documentaires | variable métier |

*Estimations à revalider en sprint planning — non engagées dans ce PRD.*
