#!/usr/bin/env python3
"""Export des ajouts editoriaux de ce site vers assets/donnees/.

Trois fichiers sont ecrits a la main dans _data/, HORS PAQUET :
  - passage-dimensions.yml  : mots-cles libres du registre -> dimensions P-* ;
  - registre-complement.yml : sources ajoutees (FR-CPL-*) ;
  - acteurs.yml             : registre des acteurs v0.2 (FR-ACT-*, FR-LNK-*),
                              valide contre assets/donnees/ajout_acteurs.schema.json.

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


def verifier_acteurs(acteurs, sources, noeuds, dates_sources):
    """Le schema JSON controle la forme ; les references croisees, il ne les
    voit pas. Un identifiant de source ou de categorie mal tape donnerait un
    lien mort sur le site, sans erreur de construction."""
    import jsonschema

    schema = json.loads((TELECHARGEMENTS / "ajout_acteurs.schema.json").read_text(encoding="utf-8"))
    erreurs = sorted(jsonschema.Draft202012Validator(schema).iter_errors(acteurs), key=str)
    if erreurs:
        raise SystemExit("acteurs.yml : " + "\n".join(
            f"{'/'.join(map(str, e.path))} : {e.message}" for e in erreurs))

    ids_acteurs = [a["actor_id"] for a in acteurs["acteurs"]]
    ids_liens = [l["link_id"] for l in acteurs["liens"]]
    for nom, ids in (("acteurs", ids_acteurs), ("liens", ids_liens)):
        if len(ids) != len(set(ids)):
            raise SystemExit(f"Identifiants en double dans les {nom}")

    citations = [c for a in acteurs["acteurs"] for c in a["citations"]]
    citations += [l["citation"] for l in acteurs["liens"]]
    inconnues = sorted({c["source_id"] for c in citations} - set(sources))
    if inconnues:
        raise SystemExit(f"Sources citees absentes du registre : {inconnues}")
    for c in citations:
        if c["source_id"].startswith("FR-CPL-") and "bdif.amf-france.org" in c["url"]:
            # Un document AMF cite sous le mauvais numero : l'identifiant de
            # l'avis ou du depot doit figurer dans l'adresse de la source.
            attendu = sources[c["source_id"]].split("/documents/")[1].split("/")[1]
            if attendu not in c["url"]:
                raise SystemExit(f"{c['source_id']} cite avec une adresse d'un autre document : {c['url']}")

    categories = {c for a in acteurs["acteurs"] for c in a["categories"]}
    if categories - set(noeuds):
        raise SystemExit(f"Categories inconnues : {sorted(categories - set(noeuds))}")

    for l in acteurs["liens"]:
        for bout in (l["source_actor"], l["target_actor"]):
            if bout not in ids_acteurs:
                raise SystemExit(f"{l['link_id']} : acteur inconnu {bout}")
        # Un gestionnaire detient souvent pour ses clients : sans le dire, la
        # ligne se lirait comme une propriete pleine.
        detenteur = next(a for a in acteurs["acteurs"] if a["actor_id"] == l["source_actor"])
        if (detenteur["type_acteur"] == "gestionnaire_actifs"
                and l["type"] == "equity_ownership" and "pour_compte" not in l):
            raise SystemExit(f"{l['link_id']} : gestionnaire d'actifs sans champ pour_compte")
        if l["date_observation"] > acteurs["meta"]["date_arret"]:
            raise SystemExit(f"{l['link_id']} : observation posterieure a la date d'arret")
        # Une source ne prouve pas un etat posterieur a sa propre date.
        date_source = dates_sources.get(l["citation"]["source_id"], "")
        if date_source and l["date_observation"] > date_source:
            raise SystemExit(f"{l['link_id']} : observation au {l['date_observation']}, "
                             f"posterieure a la source citee ({date_source})")


def verifier_correspondances(acteurs):
    """Liens vers french-lambda : un acteur inconnu ou en double donnerait un
    lien mort ou ambigu, sans erreur de construction."""
    table = yaml.safe_load((DATA / "correspondances-french-lambda.yml").read_text(encoding="utf-8"))
    connus = {a["actor_id"] for a in acteurs["acteurs"]}
    vus = set()
    for c in table["correspondances"]:
        if c["actor_id"] not in connus:
            raise SystemExit(f"correspondances : acteur inconnu {c['actor_id']}")
        if c["actor_id"] in vus:
            raise SystemExit(f"correspondances : {c['actor_id']} en double")
        vus.add(c["actor_id"])
        if c["rapport"] not in ("meme_entite", "entite_voisine"):
            raise SystemExit(f"correspondances : rapport inconnu pour {c['actor_id']}")
        if c["rapport"] == "entite_voisine" and not c.get("note"):
            raise SystemExit(f"correspondances : {c['actor_id']} voisine sans note")

    # Publie pour que french-lambda puisse relier ses fiches a ce registre.
    chemin = TELECHARGEMENTS / "ajout_correspondances_french_lambda.json"
    chemin.write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {chemin.relative_to(RACINE)} : {len(table['correspondances'])} correspondances")


def exporter_acteurs(acteurs):
    for nom in ("acteurs", "liens"):
        chemin = TELECHARGEMENTS / f"ajout_{nom}.json"
        chemin.write_text(json.dumps(acteurs[nom], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  {chemin.relative_to(RACINE)} : {len(acteurs[nom])} {nom}")


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

    acteurs = yaml.safe_load((DATA / "acteurs.yml").read_text(encoding="utf-8"))
    # Les pourcentages sont ecrits entre guillemets dans le YAML, tels
    # qu'imprimes par la source : en nombre, « 9.90 » s'afficherait « 9,9 »
    # sur le site. Le schema et l'export, eux, attendent des nombres.
    for l in acteurs["liens"]:
        for champ in ("detention_capital_pct", "droits_vote_pct"):
            if isinstance(l.get(champ), str):
                l[champ] = float(l[champ])
    sources = {s["source_id"]: s["url"] for s in registre + complement["sources"]}
    noeuds = [n["node_id"] for n in json.loads((DATA / "noeuds.json").read_text(encoding="utf-8"))]
    dates_sources = {s["source_id"]: s.get("date", "") for s in registre + complement["sources"]}
    verifier_acteurs(acteurs, sources, noeuds, dates_sources)
    verifier_correspondances(acteurs)
    exporter_acteurs(acteurs)


if __name__ == "__main__":
    main()
