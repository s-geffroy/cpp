---
layout: page
title: Données
permalink: /donnees/
---

Les fichiers d’origine du paquet, **tels qu’ils sont dans l’archive**, sans
retraduction ni retraitement. Ce sont eux qui font foi ; les pages de ce site
n’en sont qu’un rendu.

## Le paquet complet

<ul class="telechargements">
  <li>
    <a href="{{ '/assets/donnees/France_2026_Source_Registry_System_Mapping_v0.1.zip' | relative_url }}">
      <code>France_2026_Source_Registry_System_Mapping_v0.1.zip</code></a>
    <span class="meta">l’archive entière : données, méthode, rapports</span>
  </li>
</ul>

## Le registre des sources

<ul class="telechargements">
  <li>
    <a href="{{ '/assets/donnees/france_master_source_registry.json' | relative_url }}">
      <code>france_master_source_registry.json</code></a>
    <span class="meta">{{ site.data.registre | size }} sources</span>
  </li>
  <li>
    <a href="{{ '/assets/donnees/france_master_source_registry.csv' | relative_url }}">
      <code>france_master_source_registry.csv</code></a>
    <span class="meta">les mêmes, en tableur</span>
  </li>
  <li>
    <a href="{{ '/assets/donnees/france_master_source_registry.schema.json' | relative_url }}">
      <code>france_master_source_registry.schema.json</code></a>
    <span class="meta">le schéma JSON qui valide le registre</span>
  </li>
</ul>

## La carte du système

<ul class="telechargements">
  <li>
    <a href="{{ '/assets/donnees/system_nodes.csv' | relative_url }}">
      <code>system_nodes.csv</code></a>
    <span class="meta">{{ site.data.noeuds | size }} nœuds</span>
  </li>
  <li>
    <a href="{{ '/assets/donnees/system_edges.csv' | relative_url }}">
      <code>system_edges.csv</code></a>
    <span class="meta">{{ site.data.aretes | size }} arêtes</span>
  </li>
  <li>
    <a href="{{ '/assets/donnees/power_dimensions.csv' | relative_url }}">
      <code>power_dimensions.csv</code></a>
    <span class="meta">{{ site.data.dimensions | size }} dimensions de pouvoir</span>
  </li>
  <li>
    <a href="{{ '/assets/donnees/coverage_matrix.csv' | relative_url }}">
      <code>coverage_matrix.csv</code></a>
    <span class="meta">{{ site.data.couverture | size }} domaines</span>
  </li>
</ul>

## Comment ce site est fabriqué

Trois couches, séparées à dessein.

**Les données d’origine** sont celles ci-dessus. Elles ne sont jamais modifiées.

**Les données de rendu** sont les mêmes, converties en JSON pour que Jekyll
puisse les parcourir. Une seule transformation les sépare des CSV d’origine :
le retrait du BOM UTF-8 qui ouvre chaque fichier, plus l’éclatement des champs
`a;b;c` en tableaux. Aucune valeur n’est ajoutée, corrigée ni supprimée.

**Les libellés français** vivent dans un fichier à part, écrit à la main. Le
script d’import ne l’écrit jamais : une future v0.2 régénère les données et
laisse les traductions intactes.

Cette séparation a une conséquence à connaître : ce que vous lisez en français
sur ce site est une **traduction d’affichage**. En cas de doute sur un libellé,
le fichier d’origine tranche. Les identifiants (`FR-SRC-0001`, `FR-NODE-001`,
`P-OWN`, `A0_CLOSED`) sont d’ailleurs affichés partout à côté de leur
traduction, pour que le passage de l’un à l’autre reste vérifiable.

## Ce qui n’est pas traduit

Les **adresses, les identifiants et les dates** ne bougent jamais : ce sont les
clés qui permettent de retrouver une ligne dans les fichiers d’origine.

Les **titres des documents** sont traduits à l’affichage lorsqu’ils étaient
rédigés en anglais — sept d’entre eux, émanant de la Commission européenne, du
Conseil de l’Union, de la BCE et de la Cour européenne des droits de l’homme.
C’est un compromis assumé : un titre traduit se cherche mal dans un moteur de
recherche, mais un titre anglais au milieu d’un site français se lit mal. Le
lien de chaque source mène au document lui-même, où figure le titre officiel,
et la valeur d’origine reste dans les fichiers ci-dessus.

Les **apostrophes** des titres français sont normalisées en apostrophe courbe.
C’est un changement de glyphe, jamais de mot.

## Date et portée

Snapshot du **{% include date-snapshot.html %}**. Toute information postérieure
est hors du champ de cette version : c’est une règle de la
[méthode]({{ '/methode/' | relative_url }}#admission), pas un retard de mise à
jour.

Version {{ site.data.paquet.version }}, statut :
{{ site.data.libelles.paquet_valeurs[site.data.paquet.status] | downcase }}.
