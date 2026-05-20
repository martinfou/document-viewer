#!/usr/bin/env python3
"""Génère les assets locaux : chat JPEG + contrats PDF fictifs (multi-pages)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

SAMPLES = Path(__file__).resolve().parent / "samples"

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

# Each entry: (filename, pages) where pages = list of pages,
# each page = list of (font_size, text) rows.
CONTRACTS: list[tuple[str, list[list[tuple[int, str]]]]] = [
    (
        "contrat_yacht_megayacht.pdf",  # 4 pages
        [
            [  # p.1 — identification & parties
                (18, "CONTRAT DE VENTE — MEGAYACHT"),
                (14, "MV AURORA PACIFICA"),
                (11, "Longueur : 92,40 m  |  Pavillon : Cayman Islands  |  Annee : 2019"),
                (11, "Constructeur : Lurssen Werft  |  Architecte : Espen Oeino"),
                (11, "Ref. : YPP-2026-8842  |  Date : 15 juin 2026"),
                (11, ""),
                (12, "1. PARTIES"),
                (10, "Vendeur : Ocean Prestige Holdings Ltd., George Town, KY1-1104"),
                (10, "Acheteur : M. Jean Tremblay — Fiche client 123456, Montreal QC"),
                (10, "Courtier : Yacht Prestige Partners S.A., Geneve — agree MYBA"),
                (10, "Notaire : Me Sophie Beaulieu, Monaco — dossier YACHT-2026-441"),
                (11, ""),
                (12, "2. DESCRIPTION DU NAVIRE"),
                (10, "Type : Motor Yacht — acier / aluminium — Feadship 2019"),
                (10, "Longueur hors tout : 92,40 m  |  Largeur : 14,20 m  |  Tirant d'eau : 3,80 m"),
                (10, "Propulsion : 2 x MTU 16V 4000 M93L — 5 440 HP total"),
                (11, ""),
                (10, "— page 1 / 4 —"),
            ],
            [  # p.2 — conditions financieres
                (14, "MV AURORA PACIFICA — Conditions financieres"),
                (11, ""),
                (12, "3. PRIX ET MODALITES DE PAIEMENT"),
                (10, "Prix de vente : 148 500 000 USD"),
                (10, "  (cent quarante-huit millions cinq cent mille dollars US)"),
                (11, ""),
                (10, "Echeancier :"),
                (10, "  - Acompte a la signature : 14 850 000 USD (10 %) — virement SWIFT"),
                (10, "  - 2e versement apres inspection : 29 700 000 USD (20 %) — J+30"),
                (10, "  - Solde a la livraison : 103 950 000 USD (70 %) — port de Monaco"),
                (11, ""),
                (10, "Compte sequestre : Banque Pictet & Cie — IBAN CH93 0076 2011 6238 5295 7"),
                (10, "Frais de courtage : 5 % — a la charge du Vendeur"),
                (10, "Droits d'immatriculation : a la charge de l'Acheteur"),
                (11, ""),
                (12, "4. INSPECTION TECHNIQUE"),
                (10, "Lloyd's Register — rapport IT-2026-LR-0441 — etat excellent"),
                (10, "Moteurs : revises 2025 — 3 210 h (tribord) / 3 180 h (babord)"),
                (10, "Systemes electroniques : FURUNO NavNet TZtouch3 — mis a jour 2026"),
                (11, ""),
                (10, "— page 2 / 4 —"),
            ],
            [  # p.3 — garanties & assurances
                (14, "MV AURORA PACIFICA — Garanties et assurances"),
                (11, ""),
                (12, "5. GARANTIES"),
                (10, "Garantie constructeur residuelle : 18 mois a compter de la livraison"),
                (10, "Garantie moteurs MTU : 12 mois pieces et main d'oeuvre"),
                (10, "Equipements inclus : 2 tenders Castoldi, 1 Jet-Ski, mobilier complet"),
                (11, ""),
                (12, "6. ASSURANCES"),
                (10, "Assurance Coque & Machines : Club MMI — police YT-2026-0091"),
                (10, "Valeur assuree : 155 000 000 USD — franchise : 500 000 USD"),
                (10, "P&I : UK P&I Club — responsabilite civile 1 Md USD"),
                (10, "Transfert des polices a l'Acheteur a la date de livraison"),
                (11, ""),
                (12, "7. EQUIPEMENTS & ELECTRONIQUE"),
                (10, "Navigation : ECDIS, AIS classe A, VSAT Starlink maritime"),
                (10, "Stabilisateurs : Quantum Zero Speed  |  Helicopter pad certifie"),
                (10, "Interieurs : 10 suites, spa, cinema, beach club, cuisine professionnelle"),
                (10, "Autonomie : 4 200 nm a 12 noeuds  |  Carburant : 280 000 L"),
                (11, ""),
                (10, "— page 3 / 4 —"),
            ],
            [  # p.4 — livraison & signatures
                (14, "MV AURORA PACIFICA — Livraison et signatures"),
                (11, ""),
                (12, "8. LIVRAISON"),
                (10, "Port de livraison : Port Hercule, Monaco"),
                (10, "Date prevue : 15 septembre 2026 — tolerance +/- 15 jours"),
                (10, "Essais en mer : 48 h minimum — acheteur ou representant present"),
                (11, ""),
                (12, "9. DROIT APPLICABLE ET ARBITRAGE"),
                (10, "Contrat regi par le droit anglais (English Law)"),
                (10, "Arbitrage LMAA — London Maritime Arbitrators Association"),
                (11, ""),
                (12, "10. SIGNATURES"),
                (10, "Vendeur : ______________________________  Date : ___________"),
                (10, "Acheteur : _____________________________  Date : ___________"),
                (10, "Courtier : _____________________________  Date : ___________"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "— page 4 / 4 —"),
            ],
        ],
    ),
    (
        "contrat_voiture_luxe.pdf",  # 3 pages
        [
            [  # p.1 — identification & parties
                (18, "CONTRAT DE VENTE — VEHICULE DE LUXE"),
                (14, "Lamborghini Huracan EVO Spyder — 2025"),
                (11, "Couleur : Verde Mantis Metallic  |  VIN : ZHWUC1ZD8SLA99102 (fictif)"),
                (11, "Ref. : PMM-2026-4471  |  Date : 10 janvier 2026"),
                (11, ""),
                (12, "1. PARTIES"),
                (10, "Vendeur : Prestige Motors Montreal Inc."),
                (10, "  1000, rue Sherbrooke Ouest, Montreal QC H3A 3G4"),
                (10, "  Concessionnaire agree Lamborghini Canada — permis SAAQ 78-3392"),
                (10, "Acheteur : M. Jean Tremblay — Fiche client 123456"),
                (10, "  245, avenue des Pins Ouest, Montreal QC H2W 1R1"),
                (11, ""),
                (12, "2. DESCRIPTION DU VEHICULE"),
                (10, "Marque : Lamborghini  |  Modele : Huracan EVO RWD Spyder  |  Annee : 2025"),
                (10, "Moteur : V10 5,2 L atmospherique — 610 CV — boite LDF 7 rapports"),
                (10, "Couleur : Verde Mantis Metallic (LB6090)  |  Interieur : Nero Ade / Verde"),
                (11, ""),
                (10, "— page 1 / 3 —"),
            ],
            [  # p.2 — conditions financieres & options
                (14, "Lamborghini Huracan EVO — Conditions financieres"),
                (11, ""),
                (12, "3. PRIX ET MODALITES DE PAIEMENT"),
                (10, "Prix de vente : 348 000 CAD (trois cent quarante-huit mille)"),
                (10, "TPS (5 %) : 17 400 CAD  |  TVQ (9,975 %) : 34 716 CAD"),
                (10, "Total taxes incluses : 400 116 CAD"),
                (11, ""),
                (10, "Modalites :"),
                (10, "  - Acompte a la commande : 50 000 CAD — cheque certifie"),
                (10, "  - Financement : 298 000 CAD sur 60 mois — taux 5,9 % / an"),
                (10, "  - Mensualite estimee : 5 748 CAD / mois taxes incluses"),
                (10, "  - Organisme financier : Banque Nationale — dossier BN-2026-88321"),
                (11, ""),
                (12, "4. OPTIONS ET ACCESSOIRES INCLUS"),
                (10, "  - Pack Visibilite : camera 360, capteurs stationnement"),
                (10, "  - Pack Carbon : capot, diffuseur, prises d'air fibre de carbone"),
                (10, "  - Audio Bang & Olufsen Premium — 12 haut-parleurs"),
                (10, "  - Plaques Quebec — livraison et mise en circulation incluses"),
                (11, ""),
                (10, "— page 2 / 3 —"),
            ],
            [  # p.3 — garanties & signatures
                (14, "Lamborghini Huracan EVO — Garanties et signatures"),
                (11, ""),
                (12, "5. GARANTIES"),
                (10, "Garantie constructeur : 3 ans / 50 000 km — pieces et main d'oeuvre"),
                (10, "Extension disponible : +2 ans / +25 000 km — 8 900 CAD"),
                (10, "Antiperforation carrosserie : 12 ans"),
                (10, "Peinture : 3 ans contre defauts de fabrication"),
                (11, ""),
                (12, "6. ASSURANCES ET SERVICES"),
                (10, "Assurance tous risques 12 mois : Intact Prestige Auto"),
                (10, "  Valeur convenue : 348 000 CAD — franchise collision : 5 000 CAD"),
                (10, "Assistance routiere 24/7 incluse pendant la garantie"),
                (10, "1re revision Lamborghini Approved offerte"),
                (11, ""),
                (12, "7. SIGNATURES"),
                (10, "Vendeur : ______________________________  Date : ___________"),
                (10, "Acheteur : _____________________________  Date : ___________"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "— page 3 / 3 —"),
            ],
        ],
    ),
    (
        "contrat_jetski.pdf",  # 2 pages
        [
            [  # p.1 — identification, parties & description
                (18, "CONTRAT DE LOCATION SAISONNIERE — MOTO MARINE"),
                (14, "Sea-Doo GTX Limited 325 — 2024"),
                (11, "Moteur : Rotax 1630 ACE  |  Puissance : 325 HP  |  3 places"),
                (11, "Ref. : NLL-2026-0391  |  Date : 1er juin 2026"),
                (11, ""),
                (12, "1. PARTIES"),
                (10, "Proprietaire : Nautique Laurentides Ltee"),
                (10, "  155, chemin des Bateliers, Magog QC J1X 3W2"),
                (10, "  Permis exploitation embarcation no. QC-NAU-2026-0088"),
                (10, "Locataire : M. Jean Tremblay — Fiche client 123456"),
                (10, "  Permis de conduire embarcation de plaisance valide exige"),
                (11, ""),
                (12, "2. DESCRIPTION DE L'EMBARCATION"),
                (10, "Marque : Sea-Doo  |  Modele : GTX Limited 325  |  Annee : 2024"),
                (10, "Immatriculation : QC-4821-HT (fictif)  |  Couleur : bleu / noir"),
                (10, "Equipements : GPS integre, systeme audio, plateforme de baignade"),
                (11, ""),
                (10, "— page 1 / 2 —"),
            ],
            [  # p.2 — conditions, securite & signatures
                (14, "Sea-Doo GTX Limited 325 — Conditions et signatures"),
                (11, ""),
                (12, "3. CONDITIONS DE LOCATION"),
                (10, "Periode : 1er juin 2026 au 15 octobre 2026 — Lac Memphremagog"),
                (10, "Tarif saison : 8 900 CAD (huit mille neuf cents) — essence non incluse"),
                (10, "Caution remboursable : 2 500 CAD — retenue en cas de dommage"),
                (11, ""),
                (12, "4. SECURITE ET OBLIGATIONS"),
                (10, "Equipements fournis : gilet homologue, casque, sifflet, extincteur"),
                (10, "Zone autorisee : eaux navigables du Quebec — mer ouverte interdite"),
                (10, "Vitesse pres des rives : 10 km/h max dans zones reglementees"),
                (10, "Interdictions : alcool, sous-location, tiers non autorises"),
                (11, ""),
                (12, "5. ASSURANCE"),
                (10, "Responsabilite civile : 2 000 000 CAD — franchise 1 000 CAD"),
                (10, "Dommages corps : franchise Locataire 2 500 CAD"),
                (11, ""),
                (12, "6. SIGNATURES"),
                (10, "Proprietaire : _________________________  Date : ___________"),
                (10, "Locataire : ____________________________  Date : ___________"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "— page 2 / 2 —"),
            ],
        ],
    ),
    (
        "contrat_skidoo.pdf",  # 3 pages
        [
            [  # p.1 — identification & parties
                (18, "CONTRAT DE LOCATION HIVERNALE — MOTO NEIGE"),
                (14, "Ski-Doo Expedition SE 900 ACE Turbo R — 2025"),
                (11, "Cylindree : 900 cc  |  Chenilles 154 x 20  |  Demarrage electrique"),
                (11, "Ref. : MEE-2026-1215  |  Date : 15 decembre 2026"),
                (11, ""),
                (12, "1. PARTIES"),
                (10, "Loueur : Motoneige Estrie Inc."),
                (10, "  2200, rue King Ouest, Sherbrooke QC J1J 2G2"),
                (10, "  Membre FCMQ — Federation des clubs de motoneigistes du Quebec"),
                (10, "Locataire : M. Jean Tremblay — Fiche client 123456"),
                (10, "  Certification CFMOTO recommandee — permis de conduire valide"),
                (11, ""),
                (12, "2. DESCRIPTION DE LA MOTONEIGE"),
                (10, "Marque : Ski-Doo (BRP)  |  Modele : Expedition SE 900 ACE Turbo R"),
                (10, "Annee : 2025  |  Couleur : Oxygen White / Yellow"),
                (10, "No. serie : 2BPSCFCA8PV001247 (fictif)"),
                (10, "Carburant : 40 L  |  Conso. estimee : ~15 L / 100 km"),
                (11, ""),
                (10, "— page 1 / 3 —"),
            ],
            [  # p.2 — conditions & obligations
                (14, "Ski-Doo Expedition SE 900 ACE — Conditions"),
                (11, ""),
                (12, "3. CONDITIONS DE LOCATION"),
                (10, "Saison : 15 decembre 2026 au 31 mars 2027"),
                (10, "Sentiers autorises : reseau balisé FCMQ — Quebec seulement"),
                (10, "Forfait 8 semaines : 6 200 CAD — kilometrage illimite sentiers balises"),
                (10, "Caution remboursable : 1 800 CAD — retenue en cas de dommage ou perte"),
                (11, ""),
                (12, "4. EQUIPEMENTS INCLUS"),
                (10, "Casque BRP Seirus taille L/XL  |  Combinaison thermique taille L"),
                (10, "Coffre de rangement 50 L  |  Chaine antivol  |  Kit premiers secours"),
                (10, "Carte des sentiers FCMQ 2026-2027"),
                (11, ""),
                (12, "5. OBLIGATIONS DU LOCATAIRE"),
                (10, "Conduire uniquement sur sentiers balises et autorises FCMQ"),
                (10, "Hors-piste non balise : strictement interdit"),
                (10, "Lac gele : autorise uniquement sur parcours municipal balisé"),
                (10, "Carburant essence 87 octanes — a la charge du Locataire"),
                (11, ""),
                (10, "— page 2 / 3 —"),
            ],
            [  # p.3 — assurances & signatures
                (14, "Ski-Doo Expedition SE 900 ACE — Assurances et signatures"),
                (11, ""),
                (12, "6. ASSURANCES"),
                (10, "Responsabilite civile : 1 000 000 CAD — incluse"),
                (10, "Vol : franchise Locataire 500 CAD"),
                (10, "Dommages collision : franchise Locataire 1 200 CAD"),
                (10, "Exclusions : hors-piste, alcool, modifications non autorisees"),
                (11, ""),
                (12, "7. ENTRETIEN ET RETOUR"),
                (10, "Retour prevu : 31 mars 2027 — depot Sherbrooke"),
                (10, "Etat requis : propre, reservoir plein, aucun dommage non declare"),
                (10, "Frais de nettoyage si retour sale : 150 CAD forfait"),
                (11, ""),
                (12, "8. SIGNATURES"),
                (10, "Loueur : _______________________________  Date : ___________"),
                (10, "Locataire : ____________________________  Date : ___________"),
                (11, ""),
                (10, "DOCUMENT FICTIF — DEMO — SANS VALEUR JURIDIQUE"),
                (10, "— page 3 / 3 —"),
            ],
        ],
    ),
]


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


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


def write_contract_pdf(path: Path, pages: list[list[tuple[int, str]]]) -> None:
    """Write a multi-page PDF.

    Object numbering:
      1  Catalog
      2  Pages (root)
      3  Font /F1
      for each page i (0-based):
        4 + 2*i        Page object
        4 + 2*i + 1    Content stream
    """
    n = len(pages)
    streams = [_content_stream(p) for p in pages]

    font_id = 3
    page_ids = [4 + 2 * i for i in range(n)]
    stream_ids = [4 + 2 * i + 1 for i in range(n)]
    total = 3 + 2 * n  # highest object id

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)

    raw: dict[int, bytes] = {
        1: b"<< /Type /Catalog /Pages 2 0 R >>",
        2: f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode(),
        3: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    }
    for i in range(n):
        sid = stream_ids[i]
        raw[page_ids[i]] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {sid} 0 R "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>".encode()
        )
        raw[stream_ids[i]] = (
            f"<< /Length {len(streams[i])} >>\nstream\n".encode()
            + streams[i]
            + b"\nendstream"
        )

    out: list[bytes] = [b"%PDF-1.4\n"]
    offsets: list[int] = []
    for obj_id in range(1, total + 1):
        offsets.append(sum(len(x) for x in out))
        out.append(f"{obj_id} 0 obj\n".encode() + raw[obj_id] + b"\nendobj\n")

    xref_pos = sum(len(x) for x in out)
    out.append(f"xref\n0 {total + 1}\n0000000000 65535 f \n".encode())
    for off in offsets:
        out.append(f"{off:010d} 00000 n \n".encode())
    out.append(
        b"trailer\n<< /Size "
        + str(total + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF\n"
    )
    path.write_bytes(b"".join(out))
    print(f"OK PDF — {path.name} ({n} p., {path.stat().st_size:,} o)")


def _fetch_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "document-viewer-demo/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = resp.read()
    if len(data) < 1500:
        raise ValueError("réponse trop petite")
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
    download_cats()
    for filename, pages in CONTRACTS:
        write_contract_pdf(SAMPLES / filename, pages)
    print("Terminé —", SAMPLES)


if __name__ == "__main__":
    main()
