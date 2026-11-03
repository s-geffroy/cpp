---
layout: page
title: Provenance
permalink: /provenance/
---

{%- assign couverture = site.data.couverture -%}
{%- assign registre = site.data.registre -%}
{%- assign lib = site.data.libelles -%}
{%- assign prov = site.data.provenance.domaines -%}
{%- assign ajouts = site.data['registre-complement'].sources -%}
{%- assign ajouts_verifies = ajouts | where: "status", "VERIFIED" -%}
{%- assign ajouts_a_verifier = ajouts | where: "status", "TO_VERIFY" -%}
{%- comment -%} Une ligne TO_VERIFY du registre des acteurs n'est jamais publiee. {%- endcomment -%}
{%- assign acteurs = site.data.acteurs.acteurs | where: "statut", "VERIFIED" -%}
{%- assign liens = site.data.acteurs.liens | where: "statut", "VERIFIED" -%}
{%- assign lacunes_acteurs = site.data.acteurs.meta.lacunes -%}
{%- assign cp = site.data['commande-publique'].meta -%}
{%- assign ri = site.data['representants-interets'].meta -%}
{%- assign jt = site.data['acteurs-jointures'].meta -%}

D’où vient chaque information de ce site, et où elle manque. Une ligne par
domaine du paquet ; une colonne par origine. Le tout est arrêté au
{% include date-snapshot.html %}, et recalculé à chaque construction à partir
des fichiers de données : aucun nombre de cette page n’est écrit à la main.

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

- **Un nombre compte des documents et des fiches, pas du pouvoir.** Dix
  sources sur un domaine ne disent pas qu’il pèse dix fois plus qu’un autre.
- **Une case hachurée veut dire que ce site n’a rien enregistré**, pas que
  rien n’existe.
- **Le rattachement des catégories d’acteurs aux domaines est une
  correspondance éditoriale de ce site, hors paquet.** Une même catégorie peut
  relever de plusieurs domaines : les lignes ne s’additionnent pas.

</div>

## Quatre origines

<div class="table-defilante">
<table class="origines">
  <thead>
    <tr><th>Origine</th><th>Ce qu’elle apporte</th><th>Où la lire</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Le paquet France-System-2026</strong></td>
      <td>{{ registre | size }} sources, {{ couverture | size }} domaines de couverture,
        {{ site.data.noeuds | size }} catégories d’acteurs. Publié tel quel, sans retouche.</td>
      <td><a href="{{ '/registre/' | relative_url }}">Registre</a>,
        <a href="{{ '/couverture/' | relative_url }}">Couverture</a>,
        <a href="{{ '/carte/' | relative_url }}">Carte</a></td>
    </tr>
    <tr>
      <td><strong>Les sources ajoutées par ce site</strong></td>
      <td>{{ ajouts | size }} sources <code>FR-CPL</code>, dont {{ ajouts_verifies | size }}
        lues par ce site{% if ajouts_a_verifier.size > 0 %} et {{ ajouts_a_verifier.size }} encore à vérifier{% endif %}.
        Hors paquet.</td>
      <td><a href="{{ '/registre/' | relative_url }}">Registre</a>, pastille
        <span class="pastille ajout">ajout</span></td>
    </tr>
    <tr>
      <td><strong>Le registre des acteurs</strong></td>
      <td>{{ acteurs | size }} organisations nommées et {{ liens | size }} liens directs,
        chacun avec sa source et son statut de preuve. Aucune personne physique.
        Hors paquet.</td>
      <td><a href="{{ '/acteurs/' | relative_url }}">Acteurs</a></td>
    </tr>
    <tr>
      <td><strong>Les jeux de données publics retraités</strong></td>
      <td>{% include nombre-fr.html n=cp.marches %} marchés notifiés en {{ cp.annee_notification }}, lus dans les
        données essentielles de la commande publique ; {% include nombre-fr.html n=ri.inscrits %} représentants
        d’intérêts inscrits à la HATVP ; leur jointure par SIREN avec le registre
        des acteurs ({{ jt.trouves }} acteurs trouvés sur {{ jt.acteurs_siren }}).
        Hors paquet.</td>
      <td><a href="{{ '/commande-publique/' | relative_url }}">Commande publique</a>,
        <a href="{{ '/representants-interets/' | relative_url }}">Représentants d’intérêts</a>,
        <a href="{{ '/acteurs/marches/' | relative_url }}">Marchés des acteurs</a></td>
    </tr>
  </tbody>
</table>
</div>

<p class="note-table">Une exception de date est déclarée : les fichiers de la
commande publique sont ceux publiés en octobre 2026, parce que les marchés
notifiés en 2025 y figurent au complet. Elle est déclarée sur
<a href="{{ '/commande-publique/' | relative_url }}">leur page</a>.</p>

## Domaine par domaine

{% comment %}
  Ligne vide avant et apres ce commentaire : sans elle, kramdown absorbe le
  tableau qui suit dans le titre. Les acteurs d'un domaine sont ceux dont
  une categorie figure dans _data/provenance.yml pour ce domaine ; la liste
  des identifiants, entre barres verticales, sert a ne compter chacun qu'une
  fois et a retrouver les liens qui les touchent, par l'une ou l'autre
  extremite.
{% endcomment %}

<ul class="legende-provenance">
  <li><i class="case n0"></i> rien d’enregistré</li>
  <li><i class="case n1"></i> 1 à 4</li>
  <li><i class="case n2"></i> 5 à 19</li>
  <li><i class="case n3"></i> 20 et plus</li>
  <li><i class="case sans-objet">—</i> sans objet : aucune catégorie d’acteurs ne correspond au domaine</li>
</ul>

<div class="table-defilante">
<table class="matrice provenance">
  <thead>
    <tr>
      <th>Domaine</th>
      <th title="Sources du paquet France-System-2026">Paquet</th>
      <th title="Sources FR-CPL ajoutées par ce site">Ajoutées</th>
      <th title="Organisations nommées dans le registre des acteurs">Acteurs</th>
      <th title="Liens directs du registre des acteurs qui touchent ces organisations">Liens</th>
      <th>Pages de ce site</th>
    </tr>
  </thead>
  <tbody>
    {%- assign sans_acteur = "" -%}
    {%- for c in couverture %}
    {%- assign couleur = lib.couleurs_couverture[c.status] -%}
    {%- assign m = prov[c.domain] -%}
    {%- assign proposees = ajouts | where: "domain", c.domain -%}
    {%- assign ids = "|" -%}
    {%- assign n_acteurs = 0 -%}
    {%- for cat in m.categories -%}
      {%- for a in acteurs -%}
        {%- if a.categories contains cat -%}
          {%- assign cle = "|" | append: a.actor_id | append: "|" -%}
          {%- unless ids contains cle -%}
            {%- assign ids = ids | append: a.actor_id | append: "|" -%}
            {%- assign n_acteurs = n_acteurs | plus: 1 -%}
          {%- endunless -%}
        {%- endif -%}
      {%- endfor -%}
    {%- endfor -%}
    {%- assign n_liens = 0 -%}
    {%- if n_acteurs > 0 -%}
      {%- for l in liens -%}
        {%- assign de = "|" | append: l.source_actor | append: "|" -%}
        {%- assign vers = "|" | append: l.target_actor | append: "|" -%}
        {%- if ids contains de or ids contains vers -%}{%- assign n_liens = n_liens | plus: 1 -%}{%- endif -%}
      {%- endfor -%}
    {%- endif -%}
    {%- assign sans_categorie = false -%}
    {%- if m.categories.size == 0 -%}{%- assign sans_categorie = true -%}
    {%- elsif n_acteurs == 0 -%}{%- assign sans_acteur = sans_acteur | append: c.domain | append: ";" -%}
    {%- endif %}
    <tr class="couverture-{{ couleur }}">
      <td>{{ lib.domaines[c.domain] }}
        {%- unless couleur == "ferme" %}<span class="meta">{{ lib.statuts_couverture[c.status] }}</span>{% endunless -%}
      </td>
      {% include cellule-provenance.html n=c.sources.size libelle="Sources du paquet" %}
      {% include cellule-provenance.html n=proposees.size libelle="Sources ajoutées" %}
      {% include cellule-provenance.html n=n_acteurs sans_objet=sans_categorie libelle="Acteurs nommés" %}
      {% include cellule-provenance.html n=n_liens sans_objet=sans_categorie libelle="Liens directs" %}
      <td class="pages">
        {%- for p in m.pages -%}
        <a href="{{ p.url | relative_url }}">{{ p.titre }}</a>{% unless forloop.last %}, {% endunless %}
        {%- endfor -%}
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

<p class="note-table">La première colonne reprend l’état donné par le paquet
(trait vert : documenté ; jaune : à moitié ; rouge : lacune déclarée). Le
rattachement des catégories aux domaines est écrit dans le fichier
<code>_data/provenance.yml</code> du dépôt.</p>

## Les thèmes ajoutés hors des {{ couverture | size }} domaines

{%- capture cles_couverture -%}|{% for c in couverture %}{{ c.domain }}|{% endfor %}{%- endcapture -%}
{%- assign hors = "" -%}
{%- assign domaines_ajouts = ajouts | map: "domain" | uniq | sort -%}
{%- for d in domaines_ajouts -%}
  {%- assign cle = "|" | append: d | append: "|" -%}
  {%- unless cles_couverture contains cle -%}
    {%- comment -%} Le compte, complete a quatre chiffres, sert de cle de tri : les themes les plus fournis d'abord. {%- endcomment -%}
    {%- assign n_d = ajouts | where: "domain", d | size | prepend: "000" | slice: -4, 4 -%}
    {%- assign hors = hors | append: n_d | append: "|" | append: d | append: ";" -%}
  {%- endunless -%}
{%- endfor -%}
{%- assign hors = hors | split: ";" | sort | reverse %}

Ce site a aussi ajouté des sources sur {{ hors | size }} thèmes que le paquet
ne suit pas comme domaines : surtout les documents annuels des sociétés, qui
fondent le registre des acteurs, puis des textes et des statistiques ajoutés
pour que chaque dimension de pouvoir s’appuie sur au moins cinq sources. Ils ne
figurent pas dans la grille :

<ul class="hors-domaines">
{%- for h in hors %}
{%- assign paire = h | split: "|" %}
{%- comment -%} Variable intermediaire : Liquid ne resout pas une indexation imbriquee. {%- endcomment -%}
{%- assign cle_d = paire[1] %}
  <li>{{ lib.domaines[cle_d] }} <span class="meta-inline">{{ paire[0] | plus: 0 }}</span></li>
{%- endfor %}
</ul>

## Ce qui manque

{%- assign sans_source = couverture | where_exp: "c", "c.sources.size == 0" -%}
{%- assign sans_acteur = sans_acteur | split: ";" -%}
{%- assign cats_vides = "" -%}
{%- for n in site.data.noeuds -%}
  {%- assign dans = acteurs | where_exp: "a", "a.categories contains n.node_id" -%}
  {%- if dans.size == 0 -%}{%- assign cats_vides = cats_vides | append: n.node_id | append: ";" -%}{%- endif -%}
{%- endfor -%}
{%- assign cats_vides = cats_vides | split: ";" %}

<dl class="manques">
  <dt>{{ sans_source | size }} domaines sans aucune source du paquet</dt>
  <dd>{% for c in sans_source %}{{ lib.domaines[c.domain] }}{% unless forloop.last %} ; {% endunless %}{% endfor %}.
    Ce site y propose des sources, qui ne ferment pas la lacune
    (<a href="{{ '/couverture/' | relative_url }}#les-lacunes-déclarées">couverture</a>).</dd>

  <dt>{{ sans_acteur | size }} domaines dont aucun acteur n’est nommé</dt>
  <dd>{% for d in sans_acteur %}{{ lib.domaines[d] }}{% unless forloop.last %} ; {% endunless %}{% endfor %}.</dd>

  <dt>{{ cats_vides | size }} catégories d’acteurs sur {{ site.data.noeuds | size }} sans aucune organisation nommée</dt>
  <dd>
    <details class="detail-lien">
      <summary>Voir les catégories</summary>
      <p>{% for id in cats_vides %}{{ lib.noeuds[id] }}{% unless forloop.last %} ; {% endunless %}{% endfor %}.</p>
    </details>
  </dd>

  <dt>{{ lacunes_acteurs | size }} lacunes déclarées par le registre des acteurs</dt>
  <dd>Des organisations repérées mais non saisies, faute de source qui donne
    leur part ou leur identité :
    {% for l in lacunes_acteurs %}{{ l.nom }}{% unless forloop.last %} ; {% endunless %}{% endfor %}.
    Chaque raison est donnée sur la page
    <a href="{{ '/acteurs/' | relative_url }}#ce-qui-manque">Acteurs</a>.</dd>

  <dt>Les bénéficiaires effectifs</dt>
  <dd>Le registre n’est plus ouvert au public : ce site ne nomme aucun
    bénéficiaire effectif (<a href="{{ '/beneficiaires-effectifs/' | relative_url }}">méthode</a>).</dd>
</dl>

## Solidité des liens

{%- assign par_type = liens | group_by: "type" %}

Chaque lien du registre des acteurs porte un statut de preuve, de P4
(preuve officielle directe) à P0 (non prouvé), défini sur la page
[Méthode]({{ '/methode/' | relative_url }}).

<div class="table-defilante">
<table class="matrice solidite">
  <thead>
    <tr>
      <th>Type de lien</th>
      {%- for p in lib.preuves %}<th title="{{ p[1] }}">{{ p[0] }}</th>{% endfor %}
    </tr>
  </thead>
  <tbody>
    {%- for g in par_type %}
    <tr>
      <td>{{ lib.types_lien_acteur[g.name] }}</td>
      {%- for p in lib.preuves -%}
      {%- assign du_statut = g.items | where: "preuve", p[0] %}
      <td class="nombre">{{ du_statut.size }}</td>
      {%- endfor %}
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>
