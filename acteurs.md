---
layout: page
title: Acteurs
permalink: /acteurs/
---

{%- assign registre = site.data.acteurs -%}
{%- assign acteurs = registre.acteurs -%}
{%- assign liens = registre.liens -%}
{%- assign lib = site.data.libelles -%}
{%- assign toutes_sources = site.data.registre | concat: site.data['registre-complement'].sources -%}

La [carte]({{ '/carte/' | relative_url }}) décrit des **catégories** d’acteurs.
Cette page descend d’un cran : elle nomme des **organisations**, avec leurs
identifiants officiels, et les **liens** documentés entre elles —
{{ acteurs | size }} acteurs et {{ liens | size }} liens, arrêtés au
{% include date-fr.html date=registre.meta.date_arret %}.

C’est le début de l’étape que la [feuille de route]({{ '/feuille-de-route/' | relative_url }})
appelle « registre des acteurs ». Ce site l’a commencée lui-même : ces données
sont un **ajout éditorial, hors paquet**. Elles couvrent pour l’instant un
périmètre précis — les participations de l’État dans les sociétés cotées de son
portefeuille, EDF, et les entreprises de défense où il détient du capital ou
une action.

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

Un lien de détention dit **qui possède quoi, à une date**. Il ne dit pas ce que
le détenteur fait de ses droits. Trois règles de la
[méthode]({{ '/methode/' | relative_url }}#cartographie) s’appliquent à chaque
ligne :

- **Propriété publique ≠ régulation ≠ commande publique ≠ subvention.** Une
  entreprise détenue par l’État peut être régulée, payée ou aidée par lui :
  ce sont d’autres liens, non saisis ici.
- **Proximité dans le réseau ≠ coordination.** Deux détenteurs publics ne
  s’additionnent jamais : Bpifrance, la Caisse des dépôts ou le CEA ne sont pas
  l’État.
- **Le contrôle ne se déduit pas du pourcentage.** La colonne « contrôle »
  reprend ce que **la source écrit**, et rien d’autre.

Seuls les liens **directs** sont saisis. Quand l’État détient une société par
l’intermédiaire d’une holding, les deux maillons apparaissent séparément, et
aucune part « indirecte » n’est calculée.

</div>

## Les {{ liens | size }} liens

<div class="filtres" data-filtre-groupe="liens">
  <label>
    Rechercher
    <input type="search" data-filtre-recherche placeholder="société, détenteur, décret…">
  </label>

  <label>
    Type de lien
    <select data-filtre-champ="type">
      <option value="">tous les types</option>
      {%- assign types = liens | map: "type" | uniq -%}
      {%- for t in types -%}
      <option value="{{ t }}">{{ lib.types_lien_acteur[t] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Preuve
    <select data-filtre-champ="preuve">
      <option value="">tous les statuts</option>
      {%- assign preuves = liens | map: "preuve" | uniq | sort | reverse -%}
      {%- for p in preuves -%}
      <option value="{{ p }}">{{ p }} · {{ lib.preuves[p] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <p class="compteur" data-filtre-compteur
     data-total="{{ liens | size }}"
     data-nom="liens">{{ liens | size }} liens</p>
</div>

<div class="aretes" data-filtre-cible="liens">
  {%- for l in liens %}
  {%- assign de = acteurs | where: "actor_id", l.source_actor | first -%}
  {%- assign vers = acteurs | where: "actor_id", l.target_actor | first -%}
  {%- assign nom_de = de.nom_usuel | default: de.nom -%}
  {%- assign nom_vers = vers.nom_usuel | default: vers.nom -%}
  {%- assign source = toutes_sources | where: "source_id", l.citation.source_id | first -%}
  {%- capture cherchable -%}
    {{ l.link_id }} {{ de.nom }} {{ de.nom_usuel }} {{ vers.nom }} {{ vers.nom_usuel }}
    {{ lib.types_lien_acteur[l.type] }} {{ lib.controles[l.controle] }}
    {{ l.base_juridique }} {{ l.garde_fou }}
  {%- endcapture -%}
  <article class="arete"
           id="{{ l.link_id }}"
           data-type="{{ l.type }}"
           data-preuve="{{ l.preuve }}"
           data-recherche="{{ cherchable | normalize_whitespace | downcase | escape }}">
    <h3>
      <a href="#{{ de.actor_id }}">{{ nom_de }}</a>
      <span class="fleche" aria-hidden="true">→</span>
      <span class="sr-seul">vers</span>
      <a href="#{{ vers.actor_id }}">{{ nom_vers }}</a>
    </h3>
    <p class="meta">
      <code>{{ l.link_id }}</code>
      <span class="pastille">{{ lib.types_lien_acteur[l.type] }}</span>
      <span class="pastille preuve-{{ l.preuve | downcase }}" title="{{ lib.preuves[l.preuve] }}">{{ l.preuve }} · {{ lib.preuves[l.preuve] }}</span>
      {%- if l.controle %} <span class="pastille classe">{{ lib.controles[l.controle] }}</span>{% endif %}
    </p>
    <p class="chiffres-lien">
      {%- if l.type == "equity_ownership" -%}
        <strong>{{ l.detention_capital_pct | replace: ".", "," }}&nbsp;%</strong> du capital ·
        {% if l.droits_vote_pct == nil -%}
          droits de vote non publiés
        {%- else -%}
          <strong>{{ l.droits_vote_pct | replace: ".", "," }}&nbsp;%</strong> des droits de vote
        {%- endif %}
      {%- elsif l.type == "appointment" -%}
        <strong>{{ l.nombre_sieges }}</strong> siège{% if l.nombre_sieges > 1 %}s{% endif %}
        {%- if l.sieges_total %} sur {{ l.sieges_total }}{% endif %} · {{ l.base_juridique }}
      {%- else -%}
        {{ l.base_juridique }}
      {%- endif %}
      · au {% include date-fr.html date=l.date_observation %}
    </p>
    <p class="garde-fou-arete"><strong>Ce que ce lien ne prouve pas :</strong> {{ l.garde_fou }}</p>
    {%- if l.incertitude %}
    <p class="note">{{ l.incertitude }}</p>
    {%- endif %}
    <p class="preuves">
      Source :
      <a href="{{ '/registre/' | relative_url }}#{{ l.citation.source_id }}"><code>{{ l.citation.source_id }}</code></a>
      — <a href="{{ l.citation.url }}" rel="noopener">{{ source.title | replace: "'", "’" }}</a>
      {%- if l.citation.localisation %}, {{ l.citation.localisation }}{% endif %}
    </p>
  </article>
  {%- endfor %}
</div>

<p class="sans-js">Les filtres demandent JavaScript. Sans lui, les
{{ liens | size }} liens restent tous affichés.</p>

## Les {{ acteurs | size }} acteurs

Chaque organisation est identifiée par au moins une clé de registre officiel :
SIREN pour les sociétés françaises, identifiant d’entité juridique (LEI),
code ISIN pour un titre coté, ou numéro d’un registre étranger. Seul l’État en
est dispensé. Aucune personne physique n’est enregistrée.

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Acteur</th>
      <th>Catégories de la carte</th>
      <th>Identifiants</th>
    </tr>
  </thead>
  <tbody>
    {%- for a in acteurs %}
    <tr id="{{ a.actor_id }}">
      <td>
        <code>{{ a.actor_id }}</code>
        <strong>{{ a.nom_usuel | default: a.nom }}</strong>
        {%- if a.nom_usuel %}<span class="meta">{{ a.nom }}</span>{% endif %}
        <span class="meta">{{ lib.types_acteur[a.type_acteur] }}
          {%- if a.forme_juridique %} · {{ a.forme_juridique }}{% endif %}
          {%- if a.cote %} · cotée{% endif %}</span>
        {%- if a.notes %}<span class="note">{{ a.notes }}</span>{% endif %}
      </td>
      <td>
        {%- for c in a.categories -%}
        <a href="{{ '/carte/' | relative_url }}#{{ c }}">{{ lib.noeuds[c] }}</a>{% unless forloop.last %}<br>{% endunless %}
        {%- endfor -%}
      </td>
      <td class="mots-cles">
        {%- if a.identifiants.siren %}SIREN {{ a.identifiants.siren }}<br>{% endif -%}
        {%- if a.identifiants.lei %}LEI {{ a.identifiants.lei }}<br>{% endif -%}
        {%- if a.identifiants.isin %}ISIN {{ a.identifiants.isin }}<br>{% endif -%}
        {%- if a.identifiants.autre %}{{ a.identifiants.autre.registre }} {{ a.identifiants.autre.cle }}{% endif -%}
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

<p class="note-table">La catégorie de contrôle suit une règle écrite : « entreprise
publique ou contrôlée par l’État » si l’État détient la majorité du capital,
directement ou par une holding qu’il détient entièrement, ou si le document de
la société qualifie ce contrôle ; « grand groupe privé français » sinon. Une
société étrangère n’a que sa catégorie sectorielle.</p>

## Ce qui manque

Ces entités relèvent du périmètre étudié, mais ne sont pas enregistrées.
Le dire fait partie du registre.

<ul class="liste-aretes">
  {%- for m in registre.meta.lacunes %}
  <li><strong>{{ m.nom }}</strong> — {{ m.raison }}</li>
  {%- endfor %}
</ul>

Le registre ne contient pas non plus, à ce stade, les liens de commande
publique, d’aide ou de crédit, ni les participations des gestionnaires d’actifs.

## Comment ces données ont été établies

Les pourcentages viennent des documents annuels déposés par les sociétés à
l’Autorité des marchés financiers, des déclarations publiées par l’AMF, de
l’annexe budgétaire « État actionnaire » et des textes du Journal officiel.
Chaque document est inscrit au [registre des sources]({{ '/registre/' | relative_url }}),
et chaque lien renvoie à la page où se lit son chiffre.

{{ registre.meta.recoupement }}

Les fichiers sont téléchargeables sur la
[page des données]({{ '/donnees/' | relative_url }}#les-ajouts-de-ce-site-hors-paquet).
