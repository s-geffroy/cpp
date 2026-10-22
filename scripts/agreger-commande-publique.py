#!/usr/bin/env python3
"""Agregat de la commande publique 2025 : AJOUT EDITORIAL DE CE SITE, HORS PAQUET.

Lit les fichiers mensuels consolides des donnees essentielles de la commande
publique (DECP, source du paquet FR-SRC-0042), garde les marches NOTIFIES en
2025, et classe titulaires et acheteurs par NOMBRE de marches.

Regles, toutes affichees sur la page /commande-publique/ :
  - un fichier mensuel regroupe des donnees PUBLIEES ce mois-la, pas des
    marches notifies ce mois-la : il faut tous les lire, de janvier 2025 au
    dernier publie ;
  - un meme marche revient d'un fichier a l'autre : il est compte une fois
    (cle acheteur + identifiant + date de notification, derniere version gardee) ;
  - le montant d'un accord-cadre est un plafond, souvent repete a l'identique
    pour chaque attributaire : il n'est JAMAIS additionne ;
  - un montant de remplissage (1 Md EUR ou plus, suite de 9, puissance de 10)
    est ecarte des sommes, le marche reste compte ;
  - le montant d'un marche a plusieurs titulaires n'est attribue a aucun ;
  - le classement est par SIREN, entite juridique : aucun regroupement par
    groupe, comme partout ailleurs sur ce site.

Les noms viennent de l'API Recherche d'entreprises (repertoire Sirene).

Usage :  python3 scripts/agreger-commande-publique.py <dossier des decp-AAAA-MM.json> [cache-noms.json]
"""

import collections
import csv
import glob
import json
import sys
import time
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "_data"
TELECHARGEMENTS = RACINE / "assets" / "donnees"
ANNEE = "2025"
RANG = 50
API = "https://recherche-entreprises.api.gouv.fr/search?q={}&per_page=1"


def suspect(x):
    if x is None or x <= 0 or x >= 1e9:
        return True
    s = str(int(x))
    return (x >= 1e6 and set(s) <= {"9"}) or (x >= 1e7 and s.strip("0") == "1")


def collecter(dossier):
    marches, lus = {}, 0
    fichiers = sorted(glob.glob(str(Path(dossier) / "decp-[0-9][0-9][0-9][0-9]-[0-9][0-9].json")))
    for f in fichiers:
        for m in json.loads(Path(f).read_text(encoding="utf-8"))["marches"]["marche"]:
            lus += 1
            date = m.get("dateNotification") or ""
            if not date.startswith(ANNEE):
                continue
            acheteur = (m.get("acheteur") or {}).get("id", "")
            titulaires = [(t.get("titulaire") or {}) for t in m.get("titulaires") or []]
            marches[(acheteur, m.get("id", ""), date)] = {
                "acheteur": acheteur[:9],
                "titulaires": sorted({t["id"][:9] for t in titulaires
                                      if t.get("typeIdentifiant") == "SIRET" and len(t.get("id") or "") >= 9}),
                "montant": m.get("montant"),
                "accord_cadre": any("ccord" in t for t in ((m.get("techniques") or {}).get("technique") or [])),
            }
    return marches, lus, [Path(f).name for f in fichiers]


def agreger(marches):
    vide = lambda: {"marches": 0, "accords_cadres": 0, "montant_hors_ac": 0.0, "montants_ecartes": 0}
    titulaires, acheteurs = collections.defaultdict(vide), collections.defaultdict(vide)
    total = {"marches": 0, "accords_cadres": 0, "montants_ecartes": 0, "marches_hors_ac": 0, "montant_hors_ac": 0.0}
    for m in marches.values():
        ecarte, ac = suspect(m["montant"]), m["accord_cadre"]
        total["marches"] += 1
        total["accords_cadres"] += ac
        total["montants_ecartes"] += ecarte
        if not ecarte and not ac:
            total["marches_hors_ac"] += 1
            total["montant_hors_ac"] += m["montant"]
        cibles = [(acheteurs, m["acheteur"], True)] if m["acheteur"] else []
        cibles += [(titulaires, t, len(m["titulaires"]) == 1) for t in m["titulaires"]]
        for table, siren, seul in cibles:
            r = table[siren]
            r["marches"] += 1
            r["accords_cadres"] += ac
            r["montants_ecartes"] += ecarte
            if not ecarte and not ac and seul:
                r["montant_hors_ac"] += m["montant"]
    return titulaires, acheteurs, total


def nommer(sirens, cache):
    for s in sirens:
        if s in cache:
            continue
        cache[s] = None
        for _ in range(3):
            try:
                with urllib.request.urlopen(API.format(s), timeout=30) as r:
                    res = [x for x in json.load(r).get("results", []) if x.get("siren") == s]
                if res:
                    cache[s] = {"nom": res[0].get("nom_raison_sociale") or res[0].get("nom_complet"),
                                "sigle": res[0].get("sigle")}
                break
            except OSError:
                time.sleep(3)
        time.sleep(0.25)
    return cache


def classer(table, noms):
    lignes = sorted(table.items(), key=lambda kv: (-kv[1]["marches"], kv[0]))[:RANG]
    return [{"rang": i, "siren": s, "nom": (noms.get(s) or {}).get("nom"), "sigle": (noms.get(s) or {}).get("sigle"),
             **{k: round(v, 2) if isinstance(v, float) else v for k, v in r.items()}}
            for i, (s, r) in enumerate(lignes, 1)]


def main():
    dossier = sys.argv[1]
    chemin_cache = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    cache = json.loads(chemin_cache.read_text(encoding="utf-8")) if chemin_cache and chemin_cache.exists() else {}

    marches, lus, fichiers = collecter(dossier)
    titulaires, acheteurs, total = agreger(marches)
    sirens = [s for t in (titulaires, acheteurs)
              for s, _ in sorted(t.items(), key=lambda kv: (-kv[1]["marches"], kv[0]))[:RANG]]
    noms = nommer(sirens, cache)
    if chemin_cache:
        chemin_cache.write_text(json.dumps(noms, ensure_ascii=False, indent=1), encoding="utf-8")

    sortie = {
        "meta": {"annee_notification": ANNEE, "fichiers": fichiers, "fiches_lues": lus,
                 "montant_hors_ac": round(total.pop("montant_hors_ac"), 2), **total},
        "titulaires": classer(titulaires, noms),
        "acheteurs": classer(acheteurs, noms),
    }
    (DATA / "commande-publique.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    chemin = TELECHARGEMENTS / f"ajout_commande_publique_{ANNEE}.csv"
    champs = ["role", "rang", "siren", "nom", "sigle", "marches", "accords_cadres", "montant_hors_ac", "montants_ecartes"]
    with chemin.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        for role in ("titulaires", "acheteurs"):
            for l in sortie[role]:
                w.writerow({"role": role[:-1], **{k: l[k] for k in champs[1:]}})
    print(f"  {len(marches)} marches notifies en {ANNEE}, lus dans {len(fichiers)} fichiers ({lus} fiches)")
    print(f"  {chemin.relative_to(RACINE)} ; _data/commande-publique.json")


if __name__ == "__main__":
    main()
