---
layout: page
title: Pouvoirs
permalink: /dimensions/
---

{%- assign dimensions = site.data.dimensions -%}
{%- assign noeuds = site.data.noeuds -%}
{%- assign aretes = site.data.aretes -%}
{%- assign lib = site.data.libelles -%}

Le pouvoir est traité comme **multidimensionnel**. La méthode interdit
explicitement de réduire ces {{ dimensions | size }} dimensions à une variable
unique : un acteur puissant sur l’une peut être sans prise sur les autres.

<div class="mise en garde" markdown="1">

### Deux vocabulaires qui ne se rejoignent pas

Les catégories d’acteurs et les relations utilisent les {{ dimensions | size }} identifiants
canoniques listés ci-dessous. Le
[registre des sources]({{ '/registre/' | relative_url }}), lui, étiquette ses
entrées avec un champ en **texte libre** :
{{ site.data.registre | map: "power_dimensions" | join: ";" | split: ";" | uniq | size }}
mots-clés distincts, sans rapport formel avec ces identifiants.

Le paquet v0.1 ne fournit **aucune table de correspondance** entre les deux.
Ce site n’en fabrique pas. Les croisements ci-dessous portent donc sur les
catégories d’acteurs et les relations, jamais sur les sources — construire ce pont au jugé
reviendrait à inventer une donnée, ce que la méthode proscrit.

</div>

## Vue d’ensemble

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Identifiant</th>
      <th>Dimension</th>
      <th>Catégories</th>
      <th>Relations</th>
    </tr>
  </thead>
  <tbody>
    {%- for d in dimensions %}
    {%- assign dim_id = d.power_dimension_id -%}
    {%- assign porteurs = noeuds | where_exp: "n", "n.dimensions contains dim_id" -%}
    {%- assign relations = aretes | where: "power_dimension", dim_id -%}
    <tr>
      <td class="nowrap"><code>{{ dim_id }}</code></td>
      <td><a href="#{{ dim_id | downcase }}">{{ lib.dimensions[dim_id].label }}</a></td>
      <td class="nombre">{{ porteurs | size }}</td>
      <td class="nombre">{{ relations | size }}</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

<p class="note-table">La colonne « relations » compte les relations dont la
dimension principale est celle-ci. Une relation n’en porte qu’une : les
{{ aretes | size }} relations se répartissent donc entre les lignes sans
recouvrement. Un zéro signale une dimension pour laquelle la carte v0.1 n’a
encore documenté aucune relation — pas une dimension sans pouvoir.</p>

{% for d in dimensions %}
{%- assign dim_id = d.power_dimension_id -%}
{%- assign porteurs = noeuds | where_exp: "n", "n.dimensions contains dim_id" -%}
{%- assign relations = aretes | where: "power_dimension", dim_id -%}

## {{ lib.dimensions[dim_id].label }} {#{{ dim_id | downcase }}}

<p class="meta"><code>{{ dim_id }}</code></p>

{{ lib.dimensions[dim_id].definition }}

**{{ porteurs | size }} catégories d’acteurs relèvent de cette forme de pouvoir.**

<ul class="liste-noeuds">
  {%- for n in porteurs %}
  <li><a href="{{ '/carte/' | relative_url }}#{{ n.node_id }}">{{ lib.noeuds[n.node_id] }}</a>
      <span class="meta">{{ lib.types_noeud[n.node_type] }}</span></li>
  {%- endfor %}
</ul>

{% if relations.size > 0 -%}
**{{ relations | size }} relations relèvent de cette dimension.**

<ul class="liste-aretes">
  {%- for a in relations %}
  <li>
    <a href="{{ '/carte/' | relative_url }}#{{ a.edge_id }}">{{ lib.noeuds[a.source_node] }} → {{ lib.noeuds[a.target_node] }}</a>
    <span class="meta">{{ lib.types_arete[a.edge_type] }}</span>
  </li>
  {%- endfor %}
</ul>
{%- else -%}
<p class="lacune-inline">Aucune relation de la carte v0.1 ne relève de cette
dimension. C’est un état de la documentation, pas une absence de pouvoir.</p>
{%- endif %}

{% endfor %}
