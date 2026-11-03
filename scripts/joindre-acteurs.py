#!/usr/bin/env python3
"""Jointure du registre des acteurs avec la commande publique et le repertoire
des representants d'interets : AJOUT EDITORIAL DE CE SITE, HORS PAQUET.

Pour chaque acteur VERIFIED qui a un SIREN (_data/acteurs.yml), cherche ce
SIREN :
  - dans les donnees essentielles de la commande publique (FR-SRC-0042),
    comme titulaire et comme acheteur des marches NOTIFIES en 2025 ; memes
    fichiers, meme dedoublonnage et meme regle de montant suspect que
    scripts/agreger-commande-publique.py ;
  - dans le repertoire des representants d'interets (FR-CPL-0113), copie
    archivee le 2026-08-12, pour l'exercice 2025.

Regles, toutes affichees sur la page /acteurs/ :
  - la jointure se fait par entite juridique (SIREN), jamais par groupe : une
    filiale n'est pas rattachee a sa mere ;
  - AUCUNE somme : chaque marche est donne un par un, avec son montant tel
    que publie. Le montant d'un accord-cadre est un plafond, celui d'un marche
    a plusieurs titulaires vaut pour le marche entier ; les deux sont
    signales, comme les montants de remplissage ;
  - pour la HATVP, trois cas distincts : exercice 2025 publie avec des
    fiches, publie sans fiche, pas encore publie dans la copie.

Les noms des contreparties viennent de l'API Recherche d'entreprises.

Usage :  python3 scripts/joindre-acteurs.py <dossier des decp-AAAA-MM.json> <agora_repertoire_opendata.json> [cache-noms.json]
"""

import csv
import glob
import importlib.util
import json
import sys
from pathlib import Path

import yaml

sys.dont_write_bytecode = True  # l'import du script voisin ne laisse pas de __pycache__

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "_data"
TELECHARGEMENTS = RACINE / "assets" / "donnees"
ANNEE = "2025"
COPIE_HATVP = "20260812133400"


def module(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, RACINE / "scripts" / fichier)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cp = module("commande_publique", "agreger-commande-publique.py")


def texte(s):
    """Espaces normalises. Quelques objets portent des caracteres Windows-1252
    mal decodes (0x80-0x9F : 0x92 pour l'apostrophe, 0x96 pour le tiret) que
    Jekyll refuse : ils sont rendus a leur caractere d'origine."""
    s = "".join(c.encode("latin-1").decode("cp1252", "replace") if 0x80 <= ord(c) <= 0x9F else c for c in s or "")
    return " ".join(s.split())


def collecter(dossier):
    """Meme cle et meme derniere version gardee que cp.collecter ; garde en
    plus la date, l'objet et la procedure."""
    marches = {}
    for f in sorted(glob.glob(str(Path(dossier) / "decp-[0-9][0-9][0-9][0-9]-[0-9][0-9].json"))):
        for m in json.loads(Path(f).read_text(encoding="utf-8"))["marches"]["marche"]:
            date = m.get("dateNotification") or ""
            if not date.startswith(ANNEE):
                continue
            acheteur = (m.get("acheteur") or {}).get("id", "")
            titulaires = [(t.get("titulaire") or {}) for t in m.get("titulaires") or []]
            marches[(acheteur, m.get("id", ""), date)] = {
                "date": date[:10],
                "acheteur": acheteur[:9],
                "titulaires": sorted({t["id"][:9] for t in titulaires
                                      if t.get("typeIdentifiant") == "SIRET" and len(t.get("id") or "") >= 9}),
                "objet": texte(m.get("objet")),
                "montant": m.get("montant"),
                "accord_cadre": any("ccord" in t for t in ((m.get("techniques") or {}).get("technique") or [])),
            }
    return marches


def montant_fr(x):
    """49900.0 -> « 49 900 € » ; 1234.5 -> « 1 234,50 € ». Espace fine insecable."""
    if x is None:
        return None
    entier, centimes = f"{x:,.2f}".split(".")
    return entier.replace(",", " ") + ("" if centimes == "00" else "," + centimes) + " €"


def hatvp(publications, siren):
    p = next((p for p in publications
              if p.get("typeIdentifiantNational") == "SIREN" and p.get("identifiantNational") == siren), None)
    if not p:
        return None
    exercices = [e["publicationCourante"] for e in p.get("exercices", [])
                 if e["publicationCourante"]["dateFin"][-4:] == ANNEE]
    r = {"denomination": p["denomination"].strip(), "exercice": None}
    if exercices:
        c = max(exercices, key=lambda c: c["dateFin"][6:] + c["dateFin"][3:5] + c["dateFin"][:2])
        r["exercice"] = {
            "date_fin": c["dateFin"],
            "publie": bool(c.get("publicationDate")),
            "defaut_declaration": bool(c.get("defautDeclaration")),
            "fiches": len(c.get("activites", [])),
            "depenses": c.get("montantDepense"),
        }
    return r


def main():
    dossier, agora = sys.argv[1], Path(sys.argv[2])
    chemin_cache = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    cache = json.loads(chemin_cache.read_text(encoding="utf-8")) if chemin_cache and chemin_cache.exists() else {}

    registre = yaml.safe_load((DATA / "acteurs.yml").read_text(encoding="utf-8"))
    acteurs = [a for a in registre["acteurs"]
               if a["statut"] == "VERIFIED" and (a.get("identifiants") or {}).get("siren")]
    sirens = {a["identifiants"]["siren"] for a in acteurs}

    marches = collecter(dossier)
    publications = json.loads(agora.read_text(encoding="utf-8"))["publications"]

    def ligne(m, contreparties):
        return {
            "date": m["date"],
            "contreparties": contreparties,
            "objet": m["objet"],
            "montant": m["montant"],
            "montant_fr": montant_fr(m["montant"]),
            "accord_cadre": m["accord_cadre"],
            "titulaires": len(m["titulaires"]),
            "montant_ecarte": cp.suspect(m["montant"]),
        }

    par_siren = {s: {"titulaire": [], "acheteur": []} for s in sirens}
    for m in marches.values():
        for t in m["titulaires"]:
            if t in sirens:
                par_siren[t]["titulaire"].append(ligne(m, [m["acheteur"]] if m["acheteur"] else []))
        if m["acheteur"] in sirens:
            par_siren[m["acheteur"]]["acheteur"].append(ligne(m, m["titulaires"]))

    a_nommer = sorted({c for r in par_siren.values() for role in r.values() for l in role for c in l["contreparties"]})
    noms = cp.nommer(a_nommer, cache)
    if chemin_cache:
        chemin_cache.write_text(json.dumps(noms, ensure_ascii=False, indent=1), encoding="utf-8")

    sortie, aucun = [], 0
    for a in acteurs:
        s = a["identifiants"]["siren"]
        r, h = par_siren[s], hatvp(publications, s)
        if not (r["titulaire"] or r["acheteur"] or h):
            aucun += 1
            continue
        for role in r.values():
            role.sort(key=lambda l: (l["date"], l["objet"]))
            for l in role:
                l["contreparties"] = [{"siren": c, "nom": (noms.get(c) or {}).get("nom")} for c in l["contreparties"]]
        sortie.append({"actor_id": a["actor_id"], "nom": a.get("nom_usuel") or a["nom"], "siren": s,
                       "titulaire": r["titulaire"], "acheteur": r["acheteur"], "hatvp": h})

    resultat = {
        "meta": {"annee_notification": ANNEE, "copie_hatvp": COPIE_HATVP,
                 "acteurs_siren": len(acteurs), "trouves": len(sortie), "aucun": aucun},
        "acteurs": sortie,
    }
    (DATA / "acteurs-jointures.json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    chemin = TELECHARGEMENTS / "ajout_acteurs_jointures.csv"
    champs = ["actor_id", "acteur", "siren", "role", "date_notification", "contreparties_siren", "objet",
              "montant_publie", "accord_cadre", "nombre_titulaires", "montant_ecarte"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        for x in sortie:
            for role in ("titulaire", "acheteur"):
                for l in x[role]:
                    w.writerow({"actor_id": x["actor_id"], "acteur": x["nom"], "siren": x["siren"], "role": role,
                                "date_notification": l["date"],
                                "contreparties_siren": ";".join(c["siren"] for c in l["contreparties"]),
                                "objet": l["objet"], "montant_publie": l["montant"], "accord_cadre": l["accord_cadre"],
                                "nombre_titulaires": l["titulaires"], "montant_ecarte": l["montant_ecarte"]})
    print(f"  {len(acteurs)} acteurs avec SIREN : {len(sortie)} trouves, {aucun} dans aucun des deux fichiers")
    print(f"  {chemin.relative_to(RACINE)} ; _data/acteurs-jointures.json")


if __name__ == "__main__":
    main()
