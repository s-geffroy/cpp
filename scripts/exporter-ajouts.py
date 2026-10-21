#!/usr/bin/env python3
"""Export des ajouts editoriaux de ce site vers assets/donnees/.

Deux fichiers sont ecrits a la main dans _data/, HORS PAQUET :
  - passage-dimensions.yml  : mots-cles libres du registre -> dimensions P-* ;
  - registre-complement.yml : sources ajoutees (FR-CPL-*).

Ce script ne les modifie jamais. Il les verifie, puis les rend
telechargeables en CSV et en JSON, a cote des fichiers du paquet -- sous des
noms qui ne peuvent pas se confondre avec eux.

A relancer apres chaque modification de l'un des deux fichiers.

Usage :  python3 scripts/exporter-ajouts.py
"""

import csv
import json
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "_data"
TELECHARGEMENTS = RACINE / "assets" / "donnees"

CHAMPS_REGISTRE = [
    "source_id", "domain", "institution", "title", "date", "source_type",
    "authority", "priority", "refresh", "power_dimensions", "use", "status",
    "url", "notes", "verification",
]


def charger():
    passage = yaml.safe_load((DATA / "passage-dimensions.yml").read_text(encoding="utf-8"))
    complement = yaml.safe_load((DATA / "registre-complement.yml").read_text(encoding="utf-8"))
    registre = json.loads((DATA / "registre.json").read_text(encoding="utf-8"))
    dimensions = json.loads((DATA / "dimensions.json").read_text(encoding="utf-8"))
    return passage, complement, registre, dimensions


def verifier(passage, complement, registre, dimensions):
    """Une incoherence ici ne casse pas Jekyll : elle donne des comptages faux
    sans message. D'ou l'arret franc."""
    canoniques = {d["power_dimension_id"] for d in dimensions}
    table = passage["passage"]

    for mot, entree in table.items():
        inconnues = set(entree["dimensions"]) - canoniques
        if inconnues:
            raise SystemExit(f"{mot} : dimensions inconnues {sorted(inconnues)}")

    sources = complement["sources"]
    utilises = {m for s in registre for m in s["mots_cles"]}
    utilises |= {m for s in sources for m in s["mots_cles"]}
    absents = sorted(utilises - set(table))
    if absents:
        raise SystemExit(f"Mots-cles sans entree dans la table : {absents}")

    ids = [s["source_id"] for s in sources]
    if len(ids) != len(set(ids)):
        raise SystemExit("Identifiants FR-CPL en double")
    if any(not i.startswith("FR-CPL-") for i in ids):
        raise SystemExit("Un ajout doit porter un identifiant FR-CPL-*")
    if any(not s.get("url") for s in sources):
        raise SystemExit("Un ajout n'a pas d'adresse")


def exporter_passage(table):
    chemin = TELECHARGEMENTS / "ajout_passage_dimensions.csv"
    with chemin.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "power_dimension_ids", "note"])
        for mot, entree in sorted(table.items(), key=lambda kv: kv[0].lower()):
            w.writerow([mot, ";".join(entree["dimensions"]), entree.get("note", "")])
    print(f"  {chemin.relative_to(RACINE)} : {len(table)} mots-cles")


def exporter_complement(sources):
    lignes = []
    for s in sources:
        ligne = {k: s.get(k, "") for k in CHAMPS_REGISTRE if k != "power_dimensions"}
        # Meme format que le registre du paquet : « a;b;c ».
        ligne["power_dimensions"] = ";".join(s["mots_cles"])
        lignes.append({k: ligne[k] for k in CHAMPS_REGISTRE})

    chemin = TELECHARGEMENTS / "ajout_registre_complement.csv"
    with chemin.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CHAMPS_REGISTRE)
        w.writeheader()
        w.writerows(lignes)
    print(f"  {chemin.relative_to(RACINE)} : {len(lignes)} sources")

    chemin = TELECHARGEMENTS / "ajout_registre_complement.json"
    chemin.write_text(json.dumps(lignes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {chemin.relative_to(RACINE)}")


def main():
    passage, complement, registre, dimensions = charger()
    verifier(passage, complement, registre, dimensions)
    exporter_passage(passage["passage"])
    exporter_complement(complement["sources"])


if __name__ == "__main__":
    main()
