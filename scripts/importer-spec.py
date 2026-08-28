#!/usr/bin/env python3
"""Import du paquet France-System-2026 vers _data/ et assets/donnees/.

Ce script ne traduit rien et n'ecrit JAMAIS dans _data/libelles.fr.yml :
les libelles francais sont ecrits a la main et survivent a un reimport.

Il fait deux choses :
  1. convertir les donnees du zip en JSON propre dans _data/, pour Jekyll ;
  2. copier les fichiers d'origine tels quels dans assets/donnees/, pour le
     telechargement -- la provenance compte plus que l'economie de place.

Usage :  python3 scripts/importer-spec.py
"""

import csv
import io
import json
import shutil
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SPECS = RACINE / "specs" / "comparaison-programme-politique"
DATA = RACINE / "_data"
TELECHARGEMENTS = RACINE / "assets" / "donnees"

# Les CSV du paquet commencent par un BOM UTF-8. Lus sans 'utf-8-sig', la
# premiere colonne devient la cle '﻿source_id' et Jekyll affiche des
# cellules vides SANS la moindre erreur de construction.
ENCODAGE_CSV = "utf-8-sig"

# fichier dans le zip -> fichier dans _data/
CSV_VERS_DATA = {
    "data/system_map/system_nodes.csv": "noeuds.json",
    "data/system_map/system_edges.csv": "aretes.json",
    "data/system_map/power_dimensions.csv": "dimensions.json",
    "data/system_map/coverage_matrix.csv": "couverture.json",
}

# copies verbatim, telechargeables depuis le site
VERBATIM = [
    "data/source_registry/france_master_source_registry.csv",
    "data/source_registry/france_master_source_registry.json",
    "data/source_registry/france_master_source_registry.schema.json",
    "data/system_map/system_nodes.csv",
    "data/system_map/system_edges.csv",
    "data/system_map/power_dimensions.csv",
    "data/system_map/coverage_matrix.csv",
]


def trouver_zip():
    zips = sorted(SPECS.glob("*.zip"))
    if not zips:
        raise SystemExit(f"Aucun zip trouve dans {SPECS}")
    return zips[-1]


# Champs multivalues du paquet, ecrits « a;b;c ». On ajoute a cote un vrai
# tableau, sans toucher au champ d'origine.
#
# Ce n'est pas du confort : en Liquid, `contains` sur une CHAINE fait une
# recherche de sous-chaine. Sur un TABLEAU, il fait une egalite exacte. Tant
# que les identifiants du paquet ne se prefixent pas les uns les autres, les
# deux coincident -- le jour ou un « P-INFOSEC » apparait a cote de
# « P-INFO », seul le tableau reste juste.
MULTIVALUES = {
    "registre.json": [("power_dimensions", "mots_cles")],
    "noeuds.json": [("power_dimensions", "dimensions")],
    "aretes.json": [("evidence_source_ids", "sources")],
    "couverture.json": [("source_ids", "sources")],
}


def eclater(nom, lignes):
    for origine, cible in MULTIVALUES.get(nom, []):
        for ligne in lignes:
            brut = ligne.get(origine) or ""
            membres = [m for m in brut.split(";") if m]
            # Doublons retires. Le paquet en contient au moins un :
            # FR-NODE-036 est declare « P-INFO;P-FISCAL;P-INFO ». Sans ce
            # dedoublonnage, la carte affiche deux fois la meme dimension et
            # les comptages par dimension sont fausses.
            #
            # Le champ D'ORIGINE n'est pas touche : il reste tel quel dans ce
            # JSON et dans les CSV telechargeables, ou le doublon reste
            # visible. Seul le tableau derive, qui sert au rendu et au
            # filtrage, est nettoye.
            ligne[cible] = list(dict.fromkeys(membres))
    return lignes


def ecrire_json(nom, donnees):
    donnees = eclater(nom, donnees)
    chemin = DATA / nom
    chemin.write_text(
        json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  _data/{nom} : {len(donnees)} entrees")


def main():
    archive = trouver_zip()
    print(f"Paquet : {archive.name}")

    DATA.mkdir(exist_ok=True)
    TELECHARGEMENTS.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive) as z:
        # Le zip a un unique repertoire racine ; on s'en sert comme prefixe
        # plutot que de le coder en dur, la version changera.
        prefixe = z.namelist()[0].split("/")[0] + "/"

        def lire(chemin):
            return z.read(prefixe + chemin)

        # Le registre : deja du JSON propre dans le paquet, aucune conversion.
        registre = json.loads(lire("data/source_registry/france_master_source_registry.json"))
        ecrire_json("registre.json", registre)

        # Les CSV : c'est ici que le BOM meurt.
        for source, cible in CSV_VERS_DATA.items():
            texte = lire(source).decode(ENCODAGE_CSV)
            ecrire_json(cible, list(csv.DictReader(io.StringIO(texte))))

        # snapshot.yml : deja du YAML, copie telle quelle dans _data/.
        (DATA / "paquet.yml").write_bytes(lire("snapshot.yml"))
        print("  _data/paquet.yml")

        # Copies verbatim pour telechargement.
        for source in VERBATIM:
            (TELECHARGEMENTS / Path(source).name).write_bytes(lire(source))
        print(f"  assets/donnees/ : {len(VERBATIM)} fichiers")

    # Le zip complet, pour qui veut le paquet d'origine et rien d'autre.
    shutil.copyfile(archive, TELECHARGEMENTS / archive.name)
    print(f"  assets/donnees/{archive.name}")


if __name__ == "__main__":
    main()
