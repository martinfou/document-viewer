# document-viewer

Visionneuse de documents embarquée (PDF, JPEG) — projet greenfield BMad, démos comparatives **natif vs PDF.js**.

## Démo en ligne (GitHub Pages)

**https://martinfou.github.io/document-viewer/**

- [Index — comparer A vs B](https://martinfou.github.io/document-viewer/)
- [Démo A — viewer natif (iframe)](https://martinfou.github.io/document-viewer/demo-viewer-native.html)
- [Démo B — PDF.js](https://martinfou.github.io/document-viewer/demo-viewer-libraries.html)

**Layouts UX (M1–M3, PDF.js) :**

- [Démo 1 — pills · MVP](https://martinfou.github.io/document-viewer/demo-layout-1.html)
- [Démo 2 — table à gauche (M1)](https://martinfou.github.io/document-viewer/demo-layout-2.html)
- [Démo 3 — M3 vignettes](https://martinfou.github.io/document-viewer/demo-layout-3.html)

Les PDF et images sont servis en HTTPS ; pas besoin de `file://` ni de serveur local pour tester en ligne.

## Développement local

```bash
cd _bmad-output/demos
python3 generate-samples.py   # régénère PDF + photos chat
python3 serve-demos.py          # http://localhost:8765/
```

## Structure

| Dossier | Rôle |
|---------|------|
| `_bmad-output/demos/` | Démos HTML (Alpine.js, Tailwind CDN, PDF.js) |
| `_bmad-output/demos/samples/` | PDF et JPEG d’exemple |
| `_bmad/` | Configuration BMad |
