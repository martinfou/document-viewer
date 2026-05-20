#!/usr/bin/env python3
"""Génère les assets locaux : chat JPEG + contrats PDF fictifs."""
from __future__ import annotations

import urllib.request
from pathlib import Path

SAMPLES = Path(__file__).resolve().parent / "samples"

# 4 chats mignons — URLs différentes pour des images distinctes
CAT_PHOTOS: list[tuple[str, str]] = [
    ("photo_chat_1.jpg", "https://cataas.com/cat/cute?width=520&height=400"),
    ("photo_chat_2.jpg", "https://cataas.com/cat?tags=kitten,cute&width=520&height=400"),
    ("photo_chat_3.jpg", "https://cataas.com/cat?tags=fluffy&width=520&height=400"),
    ("photo_chat_4.jpg", "https://cataas.com/cat?tags=silly,cute&width=520&height=400"),
]

CAT_FALLBACK_URLS = [
    "https://cataas.com/cat?width=520&height=400",
    "https://cataas.com/cat/cute?type=square&width=520&height=400",
]

# Yacht : liste de pages ; autres contrats : une seule page (liste de lignes).
CONTRACTS: list[tuple[str, list | list[list[tuple[int, str]]]]] = [
    (
        "contrat_yacht_megayacht.pdf",
        [
            [
                (18, "CONTRAT DE VENTE — MEGAYACHT"),
                (14, "MV AURORA PACIFICA"),
                (11, "Longueur : 92,40 m  |  Pavillon : Cayman Islands  |  Annee : 2019"),
                (11, "Constructeur : Lurssen Werft  |  Architecte : Espen Oeino"),
                (11, ""),
                (12, "PARTIES"),
                (10, "Vendeur : Ocean Prestige Holdings Ltd., George Town, KY1-1104"),
                (10, "Acheteur : M. Jean Tremblay — Fiche client 123456"),
                (10, "Courtier : Yacht Prestige Partners S.A., Geneve — ref. YPP-2026-8842"),
                (10, "Notaire : Me Sophie Beaulieu, Monaco — dossier YACHT-2026-441"),
                (11, ""),
                (10, "Page 1 / 3 — suite aux pages suivantes"),
            ],
            [
                (12, "CONDITIONS FINANCIERES"),
                (11, ""),
                (10, "Prix de vente : 148 500 000 USD (cent quarante-huit millions cinq cents mille)"),
                (10, "Depot a la signature : 14 850 000 USD (10 %) — compte escrow Credit Suisse"),
                (10, "Versement intermediaire : 44 550 000 USD (30 %) — apres inspection technique"),
                (10, "Solde a la livraison : 89 100 000 USD (60 %) — livraison Monaco, 15 juin 2026"),
                (11, ""),
                (12, "ASSURANCES & GARANTIES"),
                (10, "Garantie constructeur residuelle : 18 mois moteurs et coque"),
                (10, "Assurance P&I / Coque incluse 12 mois : Club MMI — police YT-2026-0091"),
                (10, "Franchise collision : 250 000 USD  |  Responsabilite tiers : 50 M USD"),
                (11, ""),
                (10, "Page 2 / 3"),
            ],
            [
                (12, "EQUIPEMENT & LIVRAISON"),
                (11, ""),
                (10, "Tender : Williams 505 Jet  |  Helicopter pad certifie (non inclus)"),
                (10, "Stabilisateurs : Quantum Zero Speed  |  Propulsion : diesel-electric hybrid"),
                (10, "Interieurs : 6 cabines invites, 1 master, spa, cinema, beach club"),
                (10, "Electronics : navigation ECDIS, AIS, VSAT Starlink maritime"),
                (11, ""),
                (12, "SIGNATURES"),
                (10, "Vendeur : _________________________   Date : ____/____/2026"),
                (10, "Acheteur : _________________________   Date : ____/____/2026"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "Page 3 / 3"),
            ],
        ],
    ),
    (
        "contrat_winnebago.pdf",
        [
            [
                (18, "CONTRAT DE VENTE — VR / MOTORISE"),
                (14, "Winnebago Adventurer 35F — 2024"),
                (11, "Longueur : 36 pi  |  Classe A diesel  |  VIN : 1GB8G4FL8RU123456 (fictif)"),
                (11, "Kilometrage : 18 400 km  |  Couchages : 6  |  Lave-vaisselle, solarium"),
                (11, ""),
                (12, "PARTIES"),
                (10, "Vendeur : VR Prestige Quebec Inc., 2500 boul. des Laurentides, Laval QC"),
                (10, "Acheteur : M. Jean Tremblay — Fiche client 123456"),
                (10, "Concessionnaire agree Winnebago — no permis 77219-QC"),
                (11, ""),
                (10, "Page 1 / 2 — suite aux conditions financieres"),
            ],
            [
                (12, "CONDITIONS FINANCIERES"),
                (11, ""),
                (10, "Prix de vente : 289 900 CAD (deux cent quatre-vingt-neuf mille neuf cents)"),
                (10, "Acompte a la signature : 35 000 CAD"),
                (10, "Financement : 254 900 CAD sur 84 mois — taux 6,4 % / an"),
                (10, "Garantie structure : 5 ans  |  Groupe motopropulseur : 3 ans / 60 000 km"),
                (10, "Assurance VR tous risques 12 mois  |  Immatriculation et plaques incluses"),
                (11, ""),
                (12, "SIGNATURES"),
                (10, "Vendeur : _________________________   Date : ____/____/2026"),
                (10, "Acheteur : _________________________   Date : ____/____/2026"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "Page 2 / 2"),
            ],
        ],
    ),
    (
        "contrat_jetski.pdf",
        [
            (18, "CONTRAT DE LOCATION SAISONNIERE — MOTO MARINE"),
            (14, "Sea-Doo GTX Limited 325 — 2024"),
            (11, "Moteur : Rotax 1630 ACE  |  Puissance : 325 HP  |  3 places"),
            (11, ""),
            (12, "PARTIES"),
            (10, "Proprietaire : Nautique Laurentides Ltee, Magog QC"),
            (10, "Locataire : M. Jean Tremblay — Permis bateau valide requis"),
            (11, ""),
            (12, "CONDITIONS"),
            (10, "Periode : 1er juin 2026 au 15 octobre 2026 — Lac Memphremagog"),
            (10, "Tarif saison : 8 900 CAD (huit mille neuf cents) — essence non incluse"),
            (10, "Caution : 2 500 CAD  |  Gilet de sauvetage et casque fournis"),
            (10, "Zone autorisee : eaux du Quebec — interdit mer ouverte"),
            (10, "Assurance responsabilite : 2 M CAD — franchise 1 000 CAD"),
            (11, ""),
            (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
        ],
    ),
    (
        "contrat_skidoo.pdf",
        [
            [
                (18, "CONTRAT DE LOCATION HIVERNALE — MOTO NEIGE"),
                (14, "Ski-Doo Expedition SE 900 ACE — 2025"),
                (11, "Cylindree : 900  |  Chenilles 154 x 20  |  Demarrage electrique"),
                (11, "No serie : 2BPSGAM00NC123456 (fictif)  |  Heures moteur : 42 h"),
                (11, ""),
                (12, "PARTIES"),
                (10, "Loueur : Motoneige Estrie Inc., 4500 boul. Bourque, Sherbrooke QC J1N 1A1"),
                (10, "Locataire : M. Jean Tremblay — Fiche client 123456"),
                (10, "Permis conduire valide + carte motoneige FCMQ recommandee"),
                (11, ""),
                (10, "Page 1 / 5"),
            ],
            [
                (12, "PERIODE & TARIFICATION"),
                (11, ""),
                (10, "Saison : 15 decembre 2026 au 31 mars 2027 — sentiers Quebec autorises"),
                (10, "Forfait 8 semaines : 6 200 CAD — kilometrage illimite sentiers balises"),
                (10, "Prolongation : 750 CAD / semaine supplementaire (avis 48 h)"),
                (10, "Caution remboursable : 1 800 CAD — prelevement sur carte au depart"),
                (10, "Carburant : plein a plein (essence 91 octane)"),
                (11, ""),
                (12, "EQUIPEMENT INCLUS"),
                (10, "Casque modular, combinaison -20 C, sac secours, trousse outils"),
                (10, "Piste GPS BRP Link en location : 15 CAD / jour (option)"),
                (11, ""),
                (10, "Page 2 / 5"),
            ],
            [
                (12, "ASSURANCE & RESPONSABILITE"),
                (11, ""),
                (10, "Responsabilite civile : 1 000 000 CAD — franchise 500 CAD par sinistre"),
                (10, "Collision / vol : franchise 1 000 CAD — vehicule remplacement non garanti"),
                (10, "Assistance routiere sentiers : 24/7 — remorquage 100 km inclus"),
                (10, "Locataire responsable des amendes et infractions FCMQ / MELCC"),
                (11, ""),
                (12, "SECURITE"),
                (10, "Port du casque obligatoire  |  Vitesse max 70 km/h sur sentiers"),
                (10, "Zero alcool / drogue au volant — resiliation immediate si positif"),
                (10, "Declaration sinistre sous 24 h avec photos et constat"),
                (11, ""),
                (10, "Page 3 / 5"),
            ],
            [
                (12, "REGLES D UTILISATION"),
                (11, ""),
                (10, "Autorise : sentiers balises FCMQ, clubs partenaires Estrie / Chaudiere-Appalaches"),
                (10, "Interdit : hors-piste non balise, lac gele sans autorisation municipale"),
                (10, "Interdit : transport passager non declare, course, modification moteur"),
                (10, "Retour : propre, niveaux verifies, batterie chargee, photos etat general"),
                (11, ""),
                (12, "ENTRETIEN & DOMMAGES"),
                (10, "Usure normale incluse — chenilles cassees hors negligence : 350 CAD"),
                (10, "Dommages esthetiques > 500 CAD factures au locataire apres expertise"),
                (10, "Vol sans cadenas fourni : franchise majoree a 2 500 CAD"),
                (11, ""),
                (10, "Page 4 / 5"),
            ],
            [
                (12, "SIGNATURES"),
                (11, ""),
                (10, "Loueur : _________________________   Date : ____/____/2026"),
                (10, "Locataire : _________________________   Date : ____/____/2026"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "Page 5 / 5"),
            ],
        ],
    ),
]


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _normalize_pages(content: list) -> list[list[tuple[int, str]]]:
    if content and isinstance(content[0], list):
        return content
    return [content]


def _content_stream(rows: list[tuple[int, str]]) -> bytes:
    parts = [b"BT"]
    first = True
    for size, text in rows:
        if not text:
            parts.append(b"0 -10 Td")
            continue
        esc = _pdf_escape(text)
        if first:
            parts.append(f"/F1 {size} Tf 50 750 Td ({esc}) Tj".encode())
            first = False
        else:
            parts.append(f"0 -{max(14, size + 2)} Td /F1 {size} Tf ({esc}) Tj".encode())
    parts.append(b"ET")
    return b"\n".join(parts)


def write_contract_pdf(path: Path, content: list) -> None:
    pages = _normalize_pages(content)
    streams = [_content_stream(rows) for rows in pages]
    n_pages = len(pages)

    kid_refs: list[str] = []
    page_content: list[tuple[int, int, bytes]] = []
    next_id = 3
    for stream in streams:
        page_id = next_id
        content_id = next_id + 1
        next_id += 2
        kid_refs.append(f"{page_id} 0 R")
        page_content.append((page_id, content_id, stream))

    font_id = next_id
    size = font_id

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{' '.join(kid_refs)}] /Count {n_pages} >>".encode(),
    ]
    for page_id, content_id, stream in page_content:
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {content_id} 0 R /Resources << /Font << /F1 {font_id} 0 R >> >> >>".encode()
        )
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = [b"%PDF-1.4\n"]
    offsets = [0]
    for i, body in enumerate(objects, start=1):
        offsets.append(sum(len(x) for x in out))
        out.append(f"{i} 0 obj\n".encode() + body + b"\nendobj\n")
    xref_pos = sum(len(x) for x in out)
    out.append(f"xref\n0 {size + 1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]:
        out.append(f"{off:010d} 00000 n \n".encode())
    out.append(
        b"trailer\n<< /Size "
        + str(size).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF\n"
    )
    path.write_bytes(b"".join(out))
    label = f"{n_pages} p." if n_pages > 1 else "1 p."
    print(f"OK PDF — {path.name} ({label}, {path.stat().st_size:,} o)")


def _fetch_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "document-viewer-demo/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = resp.read()
    if len(data) < 1500:
        raise ValueError("réponse trop petite")
    # Rejeter GIF si on veut du JPEG dans <img> — cataas /cat sans /gif renvoie souvent JPEG
    if data[:6] == b"GIF89a" or data[:3] == b"GIF":
        raise ValueError("image GIF — réessayer autre URL")
    return data


def download_cats() -> None:
    used_urls: list[str] = []
    for filename, url in CAT_PHOTOS:
        out = SAMPLES / filename
        candidates = [url] + [u for u in CAT_FALLBACK_URLS if u not in used_urls]
        ok = False
        for try_url in candidates:
            try:
                data = _fetch_url(try_url)
                out.write_bytes(data)
                used_urls.append(try_url)
                print(f"OK chat — {filename} ({len(data):,} o)")
                ok = True
                break
            except Exception as e:
                print(f"  essai {try_url[:50]}… : {e}")
        if not ok:
            raise SystemExit(f"Impossible de télécharger {filename}")


def main() -> None:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    for old in SAMPLES.glob("contrat_yacht*.pdf"):
        old.unlink()
    for old in SAMPLES.glob("contrat_voiture*.pdf"):
        old.unlink()
    for old in SAMPLES.glob("photo_chat.jpg"):
        old.unlink()
    download_cats()
    for filename, rows in CONTRACTS:
        write_contract_pdf(SAMPLES / filename, rows)
    print("Terminé —", SAMPLES)


if __name__ == "__main__":
    main()
