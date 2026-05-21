# Paquet analyste fonctionnel — Document viewer

**Source :** `prd.md` (statut draft) · **Projet :** document-viewer · **Date :** 2026-05-20

Ce document est le **livrabble BA** demandé pour cadrage métier, validation et passage en développement. Il complète le PRD sans le dupliquer intégralement.

---

## 1. Résumé / contexte métier

| Élément | Contenu |
|---------|---------|
| **Problème** | Consultation fragmentée des pièces client (un bouton par fichier). |
| **Solution** | Onglet **Document viewer** : liste + viewer embarqué (PDF, JPEG). |
| **Parties prenantes** | Conseillers / utilisateurs métier, équipe JSP, BA, QA, ops internes. |
| **Périmètre v1** | MVP M2 pills + **PDF, JPEG, TIFF** + préférences + **reprise document/page par fiche**. |
| **Hors périmètre** | Édition, GED (remplacement), M3 vignettes, recherche dans PDF. |

**Références UX :** démos `_bmad-output/demos/` · [Pages publiques](https://martinfou.github.io/document-viewer/)

---

## 2. Cas d'usage

| ID | Nom | Acteur | Résumé |
|----|-----|--------|--------|
| CU-1 | Consulter le dossier | Utilisateur métier | Ouvrir l’onglet, voir la liste, premier doc affiché |
| CU-2 | Changer de document | Utilisateur métier | Sélectionner une autre pièce, viewer mis à jour |
| CU-3 | Naviguer dans un PDF | Utilisateur métier | Pages, zoom, ajuster largeur/hauteur |
| CU-4 | Consulter une image | Utilisateur métier | Afficher un JPEG |
| CU-4b | Consulter un TIFF | Utilisateur métier | Afficher TIFF mono ou multi-pages |
| CU-5 | Retrouver ses réglages | Utilisateur métier | Zoom/fit chargés et sauvegardés |
| CU-5b | Reprendre sa lecture sur la fiche | Utilisateur métier | Dernier document + page PDF mémorisés par fiche |
| CU-6 | Gérer l’absence de pièces | Utilisateur métier | Message si liste vide |
| CU-7 | Gérer une erreur | Utilisateur métier | Message si fichier inaccessible |

### CU-1 — Consulter le dossier (principal)

**Préconditions :** Utilisateur authentifié ; accès fiche client ; dossier avec ≥ 1 document.

**Flux nominal :**
1. L’utilisateur active l’onglet Document viewer.
2. Le système charge la liste des documents du client.
3. Le système applique la **position mémorisée** (FR-19) ou, à défaut, le premier document (FR-5).
4. Le système affiche le document (et la page PDF mémorisée) avec zoom/fit préférences.

**Flux alternatifs :**
- 2a. Liste vide → CU-6.
- 4a. Erreur chargement → CU-7.

**Postconditions :** Document courant identifié ; utilisateur peut enchaîner CU-2.

### CU-5 — Préférences utilisateur (zoom / fit)

**Préconditions :** Utilisateur authentifié ; préférences éventuellement déjà enregistrées.

**Flux nominal :**
1. À l’ouverture, le système charge zoom + mode ajustement par défaut.
2. L’utilisateur modifie zoom ou fit.
3. Le système enregistre les nouvelles valeurs.

**Postconditions :** Prochaine session retrouve les valeurs (CU-5 reprise).

### CU-5b — Reprise document et page (par fiche)

**Préconditions :** Utilisateur authentifié ; fiche client identifiée (`clientId`) ; position éventuellement enregistrée pour cette fiche.

**Flux nominal :**
1. L’utilisateur ouvre l’onglet Document viewer sur la fiche X.
2. Le système charge la position (document D, page P) pour (utilisateur, fiche X).
3. Le viewer affiche D à la page P ; la liste met D en surbrillance.

**Flux alternatifs :**
- Première visite fiche X → premier document, page 1 (FR-5).
- Document D supprimé du dossier → premier document disponible, page 1.
- P > nombre de pages → dernière page du document.

**Postconditions :** Navigation ultérieure met à jour la position (FR-20).

---

## 3. Exigences fonctionnelles (extrait traçable)

Liste alignée sur le PRD — numérotation **FR globale** inchangée.

| FR | Intitulé court | CU |
|----|----------------|-----|
| FR-1 | Onglet accessible | CU-1 |
| FR-2 | Liste liée au client | CU-1 |
| FR-2a | Acquisition fichiers (PDF/JPEG) | CU-1, CU-2 |
| FR-3 | Affichage liste | CU-1, CU-2 |
| FR-4 | Sélection document | CU-2 |
| FR-5 | Premier doc auto | CU-1 |
| FR-6 | Tri simple | CU-1 |
| FR-7 | Affichage PDF | CU-3 |
| FR-8 | Zoom / fit PDF | CU-3, CU-5 |
| FR-9 | Navigation docs dans viewer | CU-2 |
| FR-10 | Affichage JPEG | CU-4 |
| FR-10b | Affichage TIFF | CU-4b |
| FR-11 | Lecture préférences + position | CU-5, CU-5b |
| FR-12 | Enregistrement zoom/fit | CU-5 |
| FR-13 | Périmètre persistance | CU-5, CU-5b |
| FR-19 | Reprise position | CU-5b |
| FR-20 | Enregistrement position | CU-5b |
| FR-21 | Clavier Standard | CU-1, CU-2 |
| FR-22 | Clavier Avancé | CU-1, CU-2 |
| FR-14 | Liste vide | CU-6 |
| FR-15 | Erreur chargement | CU-7 |
| FR-16 | Format non supporté | CU-7 |
| FR-17 | Impression `[PENDING CUSTOMER]` | CU-8 |
| FR-18 | Téléchargement `[PENDING CUSTOMER]` | CU-8 |

---

## 2b. Cas d'usage — impression / téléchargement (en attente client)

| ID | Nom | Statut |
|----|-----|--------|
| CU-8 | Exporter le document (imprimer ou télécharger) | **Bloqué** — validation client requise (PRD OQ-6) |

**Flux nominal (si autorisé) :** document courant affiché → action Imprimer ou Télécharger → sortie conforme aux droits.

**Flux nominal (si interdit) :** actions absentes ou désactivées ; pas de contournement documenté en recette.

### Question client (à envoyer)

Reprendre le bloc **« Question client — impression »** du PRD §10 (OQ-6).

### Question client — navigation clavier (copier-coller)

Reprendre le bloc **« Question client — navigation clavier »** du PRD §10 (OQ-9). **Recommandation BA :** palier Standard (FR-21) en MVP.

---

## 4. Critères d'acceptation (échantillon MVP)

Format : **Étant donné / Quand / Alors** — à compléter en recette avec QA.

| ID | FR | Critère d'acceptation |
|----|-----|------------------------|
| CA-1 | FR-5 | Étant donné un dossier avec ≥ 1 PDF, quand l’onglet s’ouvre, alors le premier document du tri est visible sans clic supplémentaire. |
| CA-2 | FR-4 | Étant donné deux documents, quand l’utilisateur sélectionne le second, alors le viewer affiche le second et la liste marque le courant. |
| CA-3 | FR-7 | Étant donné un PDF de 3 pages, quand l’utilisateur utilise page suivante, alors la page 2 s’affiche. |
| CA-4 | FR-11, FR-12 | Étant donné un zoom 125 % enregistré, quand l’utilisateur rouvre l’onglet (nouvelle session), alors le PDF s’ouvre à 125 %. |
| CA-7 | FR-19, FR-20 | Étant donné doc B page 3 enregistrés sur fiche X, quand l’utilisateur rouvre l’onglet sur fiche X, alors B page 3 s’affiche sans action manuelle. |
| CA-8 | FR-19, FR-13 | Étant donné position sur fiche X, quand l’utilisateur ouvre fiche Y, alors la position de Y s’applique (pas celle de X). |
| CA-9 | FR-5, FR-19 | Étant donné doc mémorisé absent de la liste, quand l’onglet s’ouvre, alors le premier document disponible page 1 s’affiche. |
| CA-5 | FR-14 | Étant donné un dossier sans document, quand l’onglet s’ouvre, alors un message métier s’affiche et aucune erreur technique brute. |
| CA-6 | FR-10b | Étant donné un TIFF multi-pages dans le dossier, quand l’utilisateur le sélectionne, alors toutes les pages sont consultables avec navigation. |
| CA-10 | FR-16 | Étant donné un format hors MVP (ex. `.docx`), quand présent dans le dossier, alors il n’est pas consultable dans le viewer (filtré ou message non supporté). |

*Liste complète : étendre CA-1…CA-N pour chaque FR avant gel recette.*

---

## 5. Matrice de traçabilité

| FR | CU | Mock / démo | Composant JSP (à nommer en architecture) |
|----|-----|-------------|------------------------------------------|
| FR-1, FR-2 | CU-1 | index + layout 1 | Tab + conteneur onglet |
| FR-3–FR-6 | CU-1, CU-2 | demo-layout-1.html | Composant liste (pills) |
| FR-7–FR-9 | CU-2, CU-3 | demo-viewer-libraries.html | Viewer PDF.js + toolbar |
| FR-10 | CU-4 | demo-viewer-libraries.html | Viewer image |
| FR-11–FR-13 | CU-5 | démo B (zoom/fit) | Module préférences + API |
| FR-14–FR-16 | CU-6, CU-7 | — | États vides / erreur |

---

## 6. Backlog structuré (ébauche)

| Epic | Stories indicatives |
|------|---------------------|
| E1 — Shell onglet | Intégrer tab JSP ; charger contexte client |
| E2 — Liste documents | API liste ; pills ; tri ; indicateur courant |
| E3 — Viewer PDF | Intégrer PDF.js ; toolbar ; fit width/height |
| E4 — Viewer JPEG | Affichage image ; masquer contrôles pages |
| E4b — Viewer TIFF | Spike OQ-8 ; rendu + pages ; parité toolbar PDF |
| E5 — Préférences & position | API zoom/fit + position par `clientId` ; reprise FR-19 ; sauvegarde FR-20 |
| E6 — Robustesse | Vide, erreur, formats exclus |
| E7 — Accessibilité clavier | FR-21 (ARIA tabs, focus, tab order) ; FR-22 si OQ-9 Avancé |

---

## 7. Glossaire

Reprendre **§3 Glossary** du `prd.md` comme référence normative. Ne pas introduire de synonymes (ex. utiliser **Document courant**, pas « fichier actif »).

---

## 8. Questions ouvertes BA

| Priorité | Question | Action |
|----------|----------|--------|
| **P0** | Impression / téléchargement autorisés ? (OQ-6) | Envoyer question client PRD §10 ; mettre à jour FR-17/18 et CA associés |
| **P1** | Niveau navigation clavier ? (OQ-9) | Question client §10 ; Standard vs Avancé (FR-21/22) |
| **P0** | Comment récupérer liste + PDF + JPEG + TIFF ? (OQ-7) | Atelier dev — PRD §10 + `addendum.md` §7 |
| **P0** | Comment afficher TIFF ? (OQ-8) | Spike dev — `addendum.md` §8 ; FR-10b |
| P1 | API préférences | Architecture |
| P1 | Droits consultation vs export | Aligner avec réponse OQ-6 |

Voir **§10 Open Questions** du PRD pour le libellé complet.
