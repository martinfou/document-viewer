# Paquet QA — Document viewer

**Source :** `prd.md` + `livrables-ba.md` · **Projet :** document-viewer · **Date :** 2026-05-20

---

## 1. Stratégie de test

| Niveau | Périmètre | Responsable |
|--------|-----------|-------------|
| **Unitaire** | Helpers préférences, mapping liste, parsers métadonnées | Dev |
| **Intégration** | Appels API documents + API préférences ; rendu PDF.js avec fixture | Dev / QA |
| **UI / composant** | Liste pills, toolbar, états vide/erreur | QA |
| **Recette UAT** | Parcours conseiller sur environnement représentatif | Métier + QA |
| **Exploratoire** | Parité démos vs build JSP | QA |

**Risques prioritaires :**
- **Contrat récupération documents non défini (OQ-7)** — bloque jeux de données réalistes et tests intégration.
- PDF.js sous JSP / CSP / chemins ressources.
- Régression droits d’accès documents.
- Persistance préférences (perte, mélange utilisateurs).
- Performance PDF multi-pages volumineux.

**Hors périmètre test v1 :** recherche texte PDF, M3 vignettes production.

**Conditionnel (OQ-6 client) :** cas de test impression/téléchargement exécutés **seulement après** décision client — deux branches (autorisé / interdit).

---

## 2. Plan de test (phases)

| Phase | Contenu | Entrée | Sortie |
|-------|---------|--------|--------|
| T0 | Jeux de données | Scripts `generate-samples.py` + échantillons métier | Dossier test référencé |
| T1 | Smoke intégration | Build avec onglet | Liste + 1 PDF + 1 JPEG |
| T2 | Fonctionnel MVP | Cas TC-xxx ci-dessous | Rapport exécution |
| T3 | UAT | CA du BA | PV recette signé |
| T4 | NFR | Navigateurs, clavier, perf | Checklist NFR |

---

## 3. Jeux de données de test

| ID | Fichier / type | Usage |
|----|----------------|-------|
| DT-1 | PDF 1 page | FR-7 smoke |
| DT-2 | PDF multi-pages (≥ 3) | FR-7 navigation pages |
| DT-3 | PDF ~5 Mo | SM-3 perf |
| DT-4 | JPEG valide | FR-10 |
| DT-5 | Liste vide | FR-14 |
| DT-6 | URL document 404 | FR-15 |
| DT-7 | TIFF 1 page | FR-10b smoke |
| DT-7b | TIFF multi-pages (scan GED) | FR-10b navigation pages |
| DT-7c | Format hors MVP (ex. docx) | FR-16 |
| DT-8 | 8–10 documents mixtes | FR-4, FR-9 charge liste |

*Réutiliser les échantillons `_bmad-output/demos/samples/` comme baseline **UI seulement**.*

**Après OQ-7 :** dupliquer DT-1…DT-8 sur l’**environnement JSP** (mêmes fichiers via servlet/API réelle) — les chemins `samples/` ne valident pas l’auth ni les URLs prod.

---

## 4. Cas de test (échantillon)

| ID | FR / CU | Étapes (résumé) | Résultat attendu |
|----|---------|-----------------|------------------|
| TC-01 | FR-1 / CU-1 | Ouvrir fiche → onglet Document viewer | Onglet actif, zone viewer visible |
| TC-02 | FR-5 / CU-1 | Dossier avec 3 PDF triés | Premier affiché sans clic |
| TC-03 | FR-4 / CU-2 | Clic pill document 2 | Viewer = doc 2, indicateur liste |
| TC-04 | FR-7 / CU-3 | PDF 3 pages, page + | Page 2 affichée |
| TC-05 | FR-8 / CU-3 | Ajuster largeur | Document lisible, pas écrasé |
| TC-06 | FR-10 / CU-4 | Sélectionner JPEG | Image visible, pas de contrôle « page » |
| TC-07 | FR-11, FR-12 / CU-5 | Zoom 150 % → fermer session → rouvrir | 150 % appliqué |
| TC-08 | FR-12 / CU-5 | Changer fit hauteur → recharger onglet | Mode hauteur conservé |
| TC-18 | FR-19, FR-20 / CU-5b | Fiche X : doc B page 3 → quitter fiche → revenir | B page 3 affiché |
| TC-19 | FR-13 / CU-5b | Position fiche X vs Y différentes | Pas de mélange |
| TC-20 | FR-5, FR-19 | Doc mémorisé retiré du dossier | Premier doc page 1 |
| TC-21 | FR-20 | PDF : changer page 1→4, attendre debounce, rouvrir | Page 4 |
| TC-22 | FR-19 | JPEG mémorisé | Image correcte, pas contrôle page |
| TC-23 | FR-10b | Sélectionner TIFF 1 page | Image visible |
| TC-24 | FR-10b | TIFF 3 pages, page + | Page 2 affichée |
| TC-25 | FR-19, FR-20 | TIFF multi-pages : mémoriser page 2, rouvrir fiche | Page 2 |
| TC-26 | FR-16 | Fichier .docx dans dossier | Non consultable / message |
| TC-09 | FR-14 / CU-6 | Dossier vide | Message métier, pas d’exception UI |
| TC-10 | FR-15 / CU-7 | Document URL invalide | Message erreur, liste utilisable |
| TC-11 | FR-9 / CU-2 | Bouton doc. suivant dans toolbar | Doc suivant + synchro liste |
| TC-12 | FR-21, NFR-2 | Tab liste → Entrée → Tab toolbar → activer page suiv. | Parcours sans souris |
| TC-12b | FR-21 | Focus visible sur chaque contrôle | Contour perceptible |
| TC-27 | FR-22 | `[Si Avancé]` Flèche → change document sans souris | Document suivant |
| TC-28 | FR-22 | `[Si Avancé]` Page Down dans viewer | Page suivante |
| TC-29 | OQ-9 | `[Si lecteur écran]` NVDA/VoiceOver : changement doc annoncé | Nom + page |
| TC-13 | NFR-3 | Utilisateur sans droit document | Accès refusé cohérent fiche |
| TC-14 | FR-17 | `[Si interdit]` Aucun bouton Imprimer ; Ctrl+P ne contourne pas `[à valider sécurité]` | Politique deny |
| TC-15 | FR-17 | `[Si autorisé]` Imprimer PDF 2 pages | Sortie papier complète |
| TC-16 | FR-18 | `[Si interdit]` Pas de téléchargement ; URL directe 403 | Fichier non récupérable |
| TC-17 | FR-18 | `[Si autorisé]` Télécharger document courant | Fichier correct |

*Compléter jusqu’à couverture 1:1 des CA BA avant gel. TC-14…17 : activer la branche selon réponse client.*

---

---

## 5. Critères de recette UAT (checklist métier)

- [ ] Je consulte tous les documents d’un dossier type sans quitter la fiche.
- [ ] Les PDF multi-pages sont lisibles (zoom, pages).
- [ ] Les photos (JPEG) s’affichent correctement.
- [ ] Les documents **TIFF** (y compris multi-pages) sont consultables avec navigation par page.
- [ ] Mes réglages de zoom / ajustement sont retrouvés à la prochaine connexion.
- [ ] En rouvrant une fiche client, je retrouve le **même document** et la **même page** que lors de ma dernière visite sur **cette** fiche.
- [ ] Je peux **sélectionner un document et changer de page** sans utiliser la souris (si OQ-9 = oui).
- [ ] Un dossier sans pièce est clair pour l’utilisateur.
- [ ] En cas de fichier manquant, je peux choisir un autre document.

---

## 6. Matrice de couverture

| FR | Cas de test | CA BA |
|----|-------------|-------|
| FR-1 | TC-01 | — |
| FR-2 | TC-01 | — |
| FR-3 | TC-01, TC-03 | CA-2 |
| FR-4 | TC-03 | CA-2 |
| FR-5 | TC-02 | CA-1 |
| FR-6 | TC-02 | — |
| FR-7 | TC-04 | — |
| FR-8 | TC-05, TC-07, TC-08 | CA-4 |
| FR-9 | TC-11 | — |
| FR-10 | TC-06 | — |
| FR-11 | TC-07 | CA-4 |
| FR-12 | TC-07, TC-08 | CA-4 |
| FR-13 | TC-19 | CA-8 |
| FR-19 | TC-18, TC-20, TC-22 | CA-7, CA-9 |
| FR-20 | TC-18, TC-21 | CA-7 |
| FR-14 | TC-09 | CA-5 |
| FR-15 | TC-10 | — |
| FR-10b | TC-23, TC-24, TC-25 | CA-6 |
| FR-16 | TC-26 | CA-10 |
| FR-17 | TC-14 ou TC-15 | — (après client) |
| FR-18 | TC-16 ou TC-17 | — (après client) |

---

## 7. Checklist non fonctionnelle

| ID | Contrôle | Méthode |
|----|----------|---------|
| NFR-1 | Navigateurs cibles internes | Exécuter TC-01 sur chaque navigateur validé |
| NFR-2, FR-21 | Clavier liste + toolbar | TC-12, TC-12b |
| FR-22 | TC-27, TC-28 | — (si OQ-9 Avancé) |
| NFR-3 | AuthZ documents | TC-13 |
| NFR-4 | Perf premier rendu | DT-3 + chronomètre / trace réseau |
| NFR-5 | Isolation préférences | Deux comptes : TC-07 sur A et B, pas de fuite |

---

## 8. Modèle rapport de test

```
Exécution : [date]
Build / version :
Environnement :
Exécutant :

| TC ID | Statut (Pass/Fail/Blocked) | Défaut | Commentaire |
|-------|------------------------------|--------|-------------|
| TC-01 |                              |        |             |

Synthèse : X Pass / Y Fail / Z Blocked
Décision : [ ] Go recette  [ ] No-go
```

---

## 9. Lien démos ↔ tests exploratoires

| Démo | Tests exploratoires suggérés |
|------|------------------------------|
| demo-layout-1.html | Parité MVP layout + pills |
| demo-viewer-libraries.html | Toolbar PDF, préférences manuelles (sans API) |
| demo-layout-2/3.html | Non régression si variantes livrées plus tard |

*Note : les démos ne testent pas la persistance serveur des préférences — TC-07/08 obligatoires sur build JSP.*
