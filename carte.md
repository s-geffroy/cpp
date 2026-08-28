---
layout: page
title: Carte
permalink: /carte/
---

{%- assign noeuds = site.data.noeuds -%}
{%- assign aretes = site.data.aretes -%}
{%- assign lib = site.data.libelles -%}

La carte compte **{{ noeuds | size }} catégories d’acteurs** et **{{ aretes | size }} relations
structurelles initiales**, arrêtés au {% include date-snapshot.html %}.

<div class="mise en garde" markdown="1">

### Ce qu’une relation dit, et ne dit pas

La méthode fixe cinq statuts de preuve, de `P0` (non prouvé) à `P4` (preuve
officielle ou primaire directe). Une relation établie par simple proximité ou
appartenance commune **ne peut pas être requalifiée en coordination** sans
preuve indépendante.

Chaque relation ci-dessous porte la mise en garde écrit dans le
paquet. Il n’est pas relégué en note : c’est la lecture qui accompagne la
relation.

</div>

## Les {{ noeuds | size }} catégories d’acteurs

Une catégorie d’acteurs n’est pas un acteur nommé : c’est une **catégorie** du système. La
distinction compte — l’étape suivante du projet, non franchie, est justement le
registre des acteurs.

<div class="filtres" data-filtre-groupe="noeuds">
  <label>
    Rechercher
    <input type="search" data-filtre-recherche placeholder="nom, type, dimension…">
  </label>

  {%- assign cles_types = noeuds | map: "node_type" | uniq -%}
  {%- capture brut -%}{%- for c in cles_types -%}{{ lib.types_noeud[c] }}|{{ c }};;{%- endfor -%}{%- endcapture -%}
  <label>
    Type
    <select data-filtre-champ="type">
      <option value="">tous les types</option>
      {%- assign paires = brut | split: ";;" | sort -%}
      {%- for p in paires -%}{%- assign kv = p | split: "|" -%}
      <option value="{{ kv[1] }}">{{ kv[0] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Dimension de pouvoir
    <select data-filtre-champ="dimension">
      <option value="">toutes les dimensions</option>
      {%- for d in site.data.dimensions -%}
      <option value="{{ d.power_dimension_id }}">{{ lib.dimensions[d.power_dimension_id].label }}</option>
      {%- endfor -%}
    </select>
  </label>

  <p class="compteur" data-filtre-compteur
     data-total="{{ noeuds | size }}"
     data-nom="catégories">{{ noeuds | size }} catégories d’acteurs</p>
</div>

<div class="table-defilante">
<table data-filtre-cible="noeuds">
  <thead>
    <tr>
      <th>Identifiant</th>
      <th>Catégorie d’acteurs</th>
      <th>Type</th>
      <th>Portée</th>
      <th>Dimensions</th>
    </tr>
  </thead>
  <tbody>
    {%- for n in noeuds %}
    {%- assign dims = n.dimensions -%}
    {%- capture cherchable -%}
      {{ n.node_id }} {{ lib.noeuds[n.node_id] }} {{ n.label }}
      {{ lib.types_noeud[n.node_type] }} {{ lib.portees[n.geographic_scope] }}
      {%- for d in dims %} {{ lib.dimensions[d].label }}{% endfor -%}
    {%- endcapture -%}
    <tr id="{{ n.node_id }}"
        data-type="{{ n.node_type }}"
        data-dimension="{{ dims | join: ' ' }}"
        data-recherche="{{ cherchable | normalize_whitespace | downcase | escape }}">
      <td class="nowrap"><code>{{ n.node_id }}</code></td>
      <td>{{ lib.noeuds[n.node_id] }}</td>
      <td>{{ lib.types_noeud[n.node_type] }}</td>
      <td>{{ lib.portees[n.geographic_scope] }}</td>
      <td>
        {%- for d in dims %}
        <span class="pastille dimension" title="{{ lib.dimensions[d].definition }}">{{ lib.dimensions[d].label }}</span>
        {%- endfor %}
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## Les {{ aretes | size }} relations

<div class="filtres" data-filtre-groupe="aretes">
  <label>
    Rechercher
    <input type="search" data-filtre-recherche placeholder="catégorie, type de relation…">
  </label>

  <label>
    Dimension de pouvoir
    <select data-filtre-champ="dimension">
      <option value="">toutes les dimensions</option>
      {%- assign dims_utilisees = aretes | map: "power_dimension" | uniq -%}
      {%- for d in site.data.dimensions -%}
      {%- if dims_utilisees contains d.power_dimension_id -%}
      <option value="{{ d.power_dimension_id }}">{{ lib.dimensions[d.power_dimension_id].label }}</option>
      {%- endif -%}
      {%- endfor -%}
    </select>
  </label>

  {%- assign cles_classes = aretes | map: "relation_class" | uniq -%}
  {%- capture brut -%}{%- for c in cles_classes -%}{{ lib.classes_relation[c] }}|{{ c }};;{%- endfor -%}{%- endcapture -%}
  <label>
    Classe de relation
    <select data-filtre-champ="classe">
      <option value="">toutes les classes</option>
      {%- assign paires = brut | split: ";;" | sort -%}
      {%- for p in paires -%}{%- assign kv = p | split: "|" -%}
      <option value="{{ kv[1] }}">{{ kv[0] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <p class="compteur" data-filtre-compteur
     data-total="{{ aretes | size }}"
     data-nom="relations">{{ aretes | size }} relations</p>
</div>

<div class="aretes" data-filtre-cible="aretes">
  {%- for a in aretes %}
  {%- assign origine = lib.noeuds[a.source_node] -%}
  {%- assign cible = lib.noeuds[a.target_node] -%}
  {%- assign sources = a.sources -%}
  {%- capture cherchable -%}
    {{ a.edge_id }} {{ origine }} {{ cible }} {{ lib.types_arete[a.edge_type] }}
    {{ lib.classes_relation[a.relation_class] }}
    {{ lib.dimensions[a.power_dimension].label }}
    {{ lib.lectures[a.edge_id] | default: a.interpretation_guardrail }}
  {%- endcapture -%}
  <article class="arete"
           id="{{ a.edge_id }}"
           data-dimension="{{ a.power_dimension }}"
           data-classe="{{ a.relation_class }}"
           data-recherche="{{ cherchable | normalize_whitespace | downcase | escape }}">
    <h3>
      <span class="origine">{{ origine }}</span>
      <span class="fleche" aria-hidden="true">→</span>
      <span class="sr-seul">vers</span>
      <span class="cible">{{ cible }}</span>
    </h3>
    <p class="meta">
      <code>{{ a.edge_id }}</code>
      <span class="pastille">{{ lib.types_arete[a.edge_type] }}</span>
      <span class="pastille dimension">{{ lib.dimensions[a.power_dimension].label }}</span>
      <span class="pastille classe">{{ lib.classes_relation[a.relation_class] }}</span>
    </p>
    <p class="mise en garde-arete"><strong>Lecture :</strong> {{ lib.lectures[a.edge_id] | default: a.interpretation_guardrail }}</p>
    <p class="preuves">
      Sources :
      {%- for s in sources %}
      <a href="{{ '/registre/' | relative_url }}#{{ s }}"><code>{{ s }}</code></a>{% unless forloop.last %},{% endunless %}
      {%- endfor %}
    </p>
  </article>
  {%- endfor %}
</div>

<p class="sans-js">Les filtres demandent JavaScript. Sans lui, les
{{ noeuds | size }} catégories d’acteurs et les {{ aretes | size }} relations restent toutes
affichés.</p>

## Ce que la carte ne contient pas

Trente relations pour cinquante-cinq catégories : la carte est **structurelle**, pas
exhaustive. Elle pose l’architecture du graphe, pas son remplissage.

L’absence d’une relation entre deux catégories ne signifie donc **pas** qu’aucune
relation n’existe entre eux. Elle signifie qu’aucune relation n’a encore été
documentée à ce niveau de preuve. La différence est exactement celle que la
[feuille de route]({{ '/feuille-de-route/' | relative_url }}) a pour objet.
