# document-viewer

Visionneuse de documents embarquée (PDF, JPEG) — projet greenfield BMad, démos comparatives **natif vs PDF.js**.

## Démo en ligne (GitHub Pages)

**https://martinfou.github.io/document-viewer/**

- [Index — comparer A vs B](https://martinfou.github.io/document-viewer/)
- [Démo A — viewer natif (iframe)](https://martinfou.github.io/document-viewer/demo-viewer-native.html)
- [Démo B — PDF.js](https://martinfou.github.io/document-viewer/demo-viewer-libraries.html)

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
