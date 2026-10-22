#!/usr/bin/env python3
"""Agregat du repertoire des representants d'interets : AJOUT EDITORIAL DE CE
SITE, HORS PAQUET.

Lit le fichier ouvert du repertoire tenu par la HATVP (source FR-CPL-0113),
dans sa copie archivee le 2026-08-12 -- le jour de la date d'arret -- et en
tire : les inscrits par famille, puis, pour l'exercice 2025, les
organisations qui declarent le plus de fiches d'activite et les responsables
publics les plus vises.

Regles, toutes affichees sur la page /representants-interets/ :
  - les familles regroupent les deux vocabulaires de categories que le fichier
    melange (ancien et nouveau) : la table FAMILLES ci-dessous est un choix de
    ce site ;
  - l'exercice 2025 est celui qui se termine en 2025 (la plupart vont du
    1er janvier au 31 decembre, certains sont decales) ;
  - une fiche d'activite qui vise plusieurs fois la meme categorie de
    responsables publics ne la compte qu'une fois ;
  - aucune donnee nominative (dirigeants, collaborateurs) n'est reprise.

Usage :  python3 scripts/agreger-representants-interets.py <agora_repertoire_opendata.json>
"""

import collections
import csv
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "_data"
TELECHARGEMENTS = RACINE / "assets" / "donnees"
EXERCICE = "2025"
RANG = 50
COPIE = "20260812133400"

# (code de categorie, libelle eventuel) -> famille. Le libelle ne sert que
# quand un meme code melange deux familles.
FAMILLES = {
    "ENTREPRISE": "Entreprises",
    "SOCIETE": "Entreprises",
    "GROUP_PRO": "Organisations professionnelles, syndicats et chambres consulaires",
    "ORGA_REP": "Organisations professionnelles, syndicats et chambres consulaires",
    "ORG_NO_GOUV": "Associations, fondations et ONG",
    "ORGA_NON_GOUV": "Associations, fondations et ONG",
    "JURISTE": "Cabinets de conseil, d’avocats et consultants",
    "AVO_CONS": "Cabinets de conseil, d’avocats et consultants",
    "RECHERCHE": "Recherche et groupes de réflexion",
    ("ORGA_NON_GOUV", "Organisme de recherche ou de réflexion"): "Recherche et groupes de réflexion",
    "DIVRES": "Établissements publics et autres",
    "AUTRE": "Établissements publics et autres",
    "ORGA_PUB": "Établissements publics et autres",
}
GOUVERNEMENT = "Membre du Gouvernement ou membre de cabinet ministériel"


def ministeres_de(texte):
    """« Premier ministre, Environnement, énergie et mer » : deux ministeres.
    Un intitule contient lui-meme des virgules ; un fragment qui commence par
    une minuscule continue donc le precedent."""
    morceaux = []
    for m in texte.split(", "):
        if morceaux and m[:1].islower():
            morceaux[-1] += ", " + m
        else:
            morceaux.append(m.strip())
    return morceaux


def famille(p):
    c = p.get("categorieOrganisation") or {}
    return FAMILLES.get((c.get("categorie"), c.get("label"))) or FAMILLES[c.get("categorie")]


def main():
    publications = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["publications"]

    inscrits = collections.Counter(famille(p) for p in publications)
    exercices, types, ministeres, tranches = [], collections.Counter(), collections.Counter(), collections.Counter()
    for p in publications:
        for e in p.get("exercices", []):
            c = e["publicationCourante"]
            if c["dateFin"][-4:] != EXERCICE:
                continue
            fiches = c.get("activites", [])
            exercices.append((p, c, len(fiches)))
            tranches[c.get("montantDepense") or "non déclarée"] += 1
            for f in fiches:
                vises_types, vises_min = set(), set()
                for action in f["publicationCourante"].get("actionsRepresentationInteret", []):
                    for r in action.get("reponsablesPublics", []):
                        t, _, reste = r.partition(" - ")
                        vises_types.add(t.strip())
                        if t.strip() == GOUVERNEMENT and reste:
                            vises_min.update(ministeres_de(reste))
                types.update(vises_types)
                ministeres.update(vises_min)

    classement = sorted(exercices, key=lambda x: (-x[2], x[0]["denomination"]))[:RANG]
    sortie = {
        "meta": {
            "copie": COPIE,
            "exercice": EXERCICE,
            "inscrits": len(publications),
            "exercices": len(exercices),
            "exercices_publies": sum(1 for _, c, _ in exercices if c.get("publicationDate")),
            "defauts_declaration": sum(1 for _, c, _ in exercices if c.get("defautDeclaration")),
            "fiches": sum(n for _, _, n in exercices),
        },
        "inscrits_par_famille": [{"famille": k, "nombre": n} for k, n in inscrits.most_common()],
        "organisations": [{
            "rang": i,
            "denomination": p["denomination"].strip(),
            "identifiant": p["identifiantNational"],
            "type_identifiant": p["typeIdentifiantNational"],
            "famille": famille(p),
            "categorie": (p.get("categorieOrganisation") or {}).get("label"),
            "fiches": n,
            "depenses": c.get("montantDepense"),
            "personnes_etp": c.get("nombreSalaries"),
        } for i, (p, c, n) in enumerate(classement, 1)],
        "responsables_vises": [{"categorie": k, "fiches": n} for k, n in types.most_common()],
        "ministeres_vises": [{"ministere": k, "fiches": n} for k, n in ministeres.most_common(15)],
    }
    (DATA / "representants-interets.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    chemin = TELECHARGEMENTS / "ajout_representants_interets.csv"
    champs = ["rang", "denomination", "identifiant", "type_identifiant", "famille", "categorie", "fiches", "depenses", "personnes_etp"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        w.writerows(sortie["organisations"])
    m = sortie["meta"]
    print(f"  {m['inscrits']} inscrits ; exercice {EXERCICE} : {m['exercices']} exercices, {m['fiches']} fiches")
    print(f"  {chemin.relative_to(RACINE)} ; _data/representants-interets.json")


if __name__ == "__main__":
    main()
