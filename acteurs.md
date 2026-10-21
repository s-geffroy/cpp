---
layout: page
title: Acteurs
permalink: /acteurs/
---

{%- assign registre = site.data.acteurs -%}
{%- comment -%} Une ligne TO_VERIFY n'est jamais publiee. {%- endcomment -%}
{%- assign acteurs = registre.acteurs | where: "statut", "VERIFIED" -%}
{%- assign liens = registre.liens | where: "statut", "VERIFIED" -%}
{%- assign lib = site.data.libelles -%}
{%- assign toutes_sources = site.data.registre | concat: site.data['registre-complement'].sources -%}
{%- assign ordre_types = "equity_ownership,special_share,single_share,appointment" | split: "," -%}

{%- comment -%}
Deux listes tirees des liens, une fois pour toutes :
  - les societes detenues (au moins un lien entrant), triees par nom ;
  - les detenteurs de tete (aucun lien entrant), dans l'ordre du registre.
Liquid ne trie pas sur une valeur calculee : on passe par des chaines
« nom<tabulation>identifiant », triees puis redecoupees. La tabulation
precede tout caractere imprimable : « Safran » passe avant « Safran Ceramics ».
{%- endcomment -%}
{%- assign cles = "" | split: "" -%}
{%- assign tetes = "" | split: "" -%}
{%- for a in acteurs -%}
  {%- assign entrants = liens | where: "target_actor", a.actor_id -%}
  {%- if entrants.size > 0 -%}
    {%- capture cle %}{{ a.nom_usuel | default: a.nom }}	{{ a.actor_id }}{% endcapture -%}
    {%- assign cles = cles | push: cle -%}
  {%- else -%}
    {%- assign tetes = tetes | push: a -%}
  {%- endif -%}
{%- endfor -%}
{%- assign cles = cles | sort_natural -%}

Qui détient quoi, société par société : **{{ cles | size }} sociétés**,
**{{ liens | size }} liens directs**, arrêtés au
{% include date-fr.html date=registre.meta.date_arret %}. Chaque chiffre renvoie
à la page du document où il se lit.

Le périmètre est volontairement étroit : les participations de l’État dans
les sociétés cotées de son portefeuille, EDF, et les entreprises de défense
où il détient du capital ou une action ; puis, dans ces sociétés cotées, les
gestionnaires d’actifs et les fonds qui ont déclaré dépasser le seuil légal. C’est un **ajout de ce site, hors
paquet** — le début du registre que la
[feuille de route]({{ '/feuille-de-route/' | relative_url }}) annonce.

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

- **Détenir n’est pas diriger.** Le contrôle ne se déduit pas d’un
  pourcentage : la mention « contrôle » reprend ce que **la source écrit**, et
  rien d’autre.
- **Deux détenteurs publics ne s’additionnent jamais.** Bpifrance, la Caisse
  des dépôts ou le CEA ne sont pas l’État. Seuls les liens **directs** sont
  saisis : quand l’État passe par une holding, chaque maillon a sa ligne, et
  aucune part « indirecte » n’est calculée.
- **Un gestionnaire d’actifs n’est pas propriétaire.** BlackRock ou Capital
  Group déclarent le plus souvent des titres détenus **pour le compte de
  clients et de fonds** ; chaque ligne dit pour le compte de qui, quand la
  source le précise.
- **Propriété publique ≠ régulation ≠ commande publique ≠ subvention.** Ces
  autres liens ne sont pas saisis ici.

</div>

<div class="filtres" data-filtre-groupe="societes">
  <label>
    Rechercher
    <input type="search" data-filtre-recherche placeholder="société, détenteur, décret…">
  </label>

  <label>
    Détenteur
    <select data-filtre-champ="detenteur">
      <option value="">tous</option>
      {%- assign detenteurs = liens | map: "source_actor" | uniq -%}
      {%- for id in detenteurs -%}
      {%- assign d = acteurs | where: "actor_id", id | first -%}
      <option value="{{ id }}">{{ d.nom_usuel | default: d.nom }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Nature du détenteur
    <select data-filtre-champ="nature">
      <option value="">toutes</option>
      {%- assign natures = "" | split: "" -%}
      {%- for id in detenteurs -%}
      {%- assign d = acteurs | where: "actor_id", id | first -%}
      {%- assign natures = natures | push: d.type_acteur -%}
      {%- endfor -%}
      {%- assign natures = natures | uniq -%}
      {%- for n in natures -%}
      <option value="{{ n }}">{{ lib.types_acteur[n] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Avec un lien de type
    <select data-filtre-champ="type">
      <option value="">tous les types</option>
      {%- for t in ordre_types -%}
      <option value="{{ t }}">{{ lib.types_lien_acteur[t] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Avec une preuve
    <select data-filtre-champ="preuve">
      <option value="">tous les statuts</option>
      {%- assign preuves = liens | map: "preuve" | uniq | sort | reverse -%}
      {%- for p in preuves -%}
      <option value="{{ p }}">{{ p }} : {{ lib.preuves[p] | downcase }}</option>
      {%- endfor -%}
    </select>
  </label>

  <p class="compteur" data-filtre-compteur
     data-total="{{ cles | size }}"
     data-nom="sociétés">{{ cles | size }} sociétés</p>
</div>

<nav class="index-societes" aria-label="Aller à une société">
  {%- for cle in cles -%}
  {%- assign morceaux = cle | split: "	" %}
  <a href="#{{ morceaux[1] }}">{{ morceaux[0] }}</a>
  {%- endfor %}
</nav>

<p class="legende-jauge">
  <span class="jauge" aria-hidden="true"><span style="width: 40%"></span></span>
  Part détenue, sur 100%. Les deux repères marquent le tiers et la moitié :
  ce sont des seuils de vote en assemblée, pas des seuils de contrôle.
</p>

<div class="fiches" data-filtre-cible="societes">
{%- for cle in cles %}
  {%- assign id = cle | split: "	" | last -%}
  {%- assign a = acteurs | where: "actor_id", id | first -%}
  {%- assign entrants = liens | where: "target_actor", id -%}
  {%- assign sortants = liens | where: "source_actor", id -%}
  {%- assign natures = "" | split: "" -%}
  {%- for l in entrants -%}
    {%- assign d = acteurs | where: "actor_id", l.source_actor | first -%}
    {%- assign natures = natures | push: d.type_acteur -%}
  {%- endfor -%}
  {%- capture cherchable -%}
    {{ a.nom }} {{ a.nom_usuel }} {{ a.identifiants.siren }}
    {%- for l in entrants -%}
      {%- assign d = acteurs | where: "actor_id", l.source_actor | first %}
      {{ d.nom }} {{ d.nom_usuel }} {{ l.link_id }} {{ lib.types_lien_acteur[l.type] }} {{ l.base_juridique }}
    {%- endfor -%}
  {%- endcapture %}
  <section class="fiche" id="{{ id }}"
           data-detenteur="{{ entrants | map: 'source_actor' | uniq | join: ' ' }}"
           data-nature="{{ natures | uniq | join: ' ' }}"
           data-type="{{ entrants | map: 'type' | uniq | join: ' ' }}"
           data-preuve="{{ entrants | map: 'preuve' | uniq | join: ' ' }}"
           data-recherche="{{ cherchable | normalize_whitespace | downcase | escape }}">
    <h3>{{ a.nom_usuel | default: a.nom }}</h3>
    <p class="meta">
      {%- assign nom_bas = a.nom | downcase -%}
      {%- assign usuel_bas = a.nom_usuel | downcase -%}
      {%- if a.nom_usuel and nom_bas != usuel_bas %}{{ a.nom }}, {% endif -%}
      {{ a.forme_juridique | default: lib.types_acteur[a.type_acteur] }}
      {%- if a.cote %}, cotée{% endif -%}
      {%- if a.identifiants.siren %} · SIREN {{ a.identifiants.siren }}{% endif -%}
      {%- if a.identifiants.autre %} · {{ a.identifiants.autre.registre }} {{ a.identifiants.autre.cle }}{% endif %}
      <br>
      {%- for c in a.categories -%}
      <a href="{{ '/carte/' | relative_url }}#{{ c }}">{{ lib.noeuds[c] }}</a>{% unless forloop.last %}, {% endunless %}
      {%- endfor -%}
    </p>

    <ul class="lignes-liens">
    {%- for t in ordre_types -%}
    {%- assign du_type = entrants | where: "type", t -%}
    {%- for l in du_type -%}
      {%- assign d = acteurs | where: "actor_id", l.source_actor | first -%}
      {%- assign source = toutes_sources | where: "source_id", l.citation.source_id | first %}
      <li class="ligne-lien" id="{{ l.link_id }}">
        <div class="qui">
          <a href="#{{ d.actor_id }}">{{ d.nom_usuel | default: d.nom }}</a>
          <span class="meta">{{ lib.types_lien_acteur[l.type] }}, au {% include date-fr.html date=l.date_observation %}</span>
          {%- if l.pour_compte %}
          <span class="meta pour-compte">{{ lib.pour_compte[l.pour_compte] }}</span>
          {%- endif %}
        </div>
        {%- if l.type == "equity_ownership" %}
        <div class="part">
          {%- if l.detention_capital_pct == nil %}
          <span class="valeur absente">non publié</span> capital
          <span class="jauge vide" aria-hidden="true"></span>
          {%- else %}
          <span class="valeur">{{ l.detention_capital_pct | replace: ".", "," }}%</span> du capital
          <span class="jauge" aria-hidden="true"><span style="width: {{ l.detention_capital_pct }}%"></span></span>
          {%- endif %}
        </div>
        <div class="part">
          {%- if l.droits_vote_pct == nil %}
          <span class="valeur absente">non publiés</span> droits de vote
          <span class="jauge vide" aria-hidden="true"></span>
          {%- else %}
          <span class="valeur">{{ l.droits_vote_pct | replace: ".", "," }}%</span> des droits de vote
          <span class="jauge" aria-hidden="true"><span style="width: {{ l.droits_vote_pct }}%"></span></span>
          {%- endif %}
        </div>
        {%- else %}
        <div class="droit">
          {%- if l.type == "appointment" -%}
          <span class="valeur">{{ l.nombre_sieges }} siège{% if l.nombre_sieges > 1%}s{% endif %}{% if l.sieges_total %} sur {{ l.sieges_total }}{% endif %}</span>
          {% endif -%}
          <span class="meta">{{ l.base_juridique }}</span>
        </div>
        {%- endif %}
        <div class="statut">
          {%- if l.controle %}<span class="controle">{{ lib.controles[l.controle] }}</span>{% endif %}
          <span class="pastille preuve-{{ l.preuve | downcase }}" title="{{ lib.preuves[l.preuve] }}">{{ l.preuve }} : {{ lib.preuves[l.preuve] | downcase }}</span>
        </div>
        <p class="ne-prouve-pas">{{ l.garde_fou }}</p>
        <details class="detail-lien">
          <summary>Source{% if l.incertitude %} et réserve{% endif %}</summary>
          {%- if l.incertitude %}
          <p>{{ l.incertitude }}</p>
          {%- endif %}
          <p>
            <a href="{{ l.citation.url }}" rel="noopener">{{ source.title | replace: "'", "’" }}</a>
            {%- if l.citation.localisation %}, {{ l.citation.localisation }}{% endif %}.
            Fiche de la source :
            <a href="{{ '/registre/' | relative_url }}#{{ l.citation.source_id }}"><code>{{ l.citation.source_id }}</code></a>.
            Lien <code>{{ l.link_id }}</code>.
          </p>
        </details>
      </li>
    {%- endfor -%}
    {%- endfor %}
    </ul>

    {%- assign aval = sortants | where: "type", "equity_ownership" -%}
    {%- if aval.size > 0%}
    <p class="aval">Détient à son tour :
      {% for l in aval -%}
      {%- assign v = acteurs | where: "actor_id", l.target_actor | first -%}
      <a href="#{{ v.actor_id }}">{{ v.nom_usuel | default: v.nom }}</a> ({% if l.detention_capital_pct == nil %}capital non publié{% else %}{{ l.detention_capital_pct | replace: ".", "," }}% du capital{% endif %}){% unless forloop.last %}, {% endunless %}
      {%- endfor %}.
    </p>
    {%- endif %}
    {%- if a.notes %}
    <p class="note">{{ a.notes }}</p>
    {%- endif %}
  </section>
{%- endfor %}
</div>

<p class="sans-js">Les filtres demandent JavaScript. Sans lui, les
{{ cles | size }} fiches restent toutes affichées.</p>

## Les détenteurs de tête

Ces {{ tetes | size }} acteurs détiennent des parts sans être eux-mêmes
détenus dans ce registre. Chacun est distinct des autres : leurs parts ne se
cumulent pas.

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Détenteur</th>
      <th>Détient directement</th>
    </tr>
  </thead>
  <tbody>
    {%- for a in tetes %}
    {%- assign sortants = liens | where: "source_actor", a.actor_id | map: "target_actor" | uniq %}
    <tr id="{{ a.actor_id }}">
      <td>
        <strong>{{ a.nom_usuel | default: a.nom }}</strong>
        <span class="meta">{{ lib.types_acteur[a.type_acteur] }}
          {%- if a.identifiants.siren %} · SIREN {{ a.identifiants.siren }}{% endif %}</span>
        {%- for c in a.categories -%}
        <span class="meta"><a href="{{ '/carte/' | relative_url }}#{{ c }}">{{ lib.noeuds[c] }}</a></span>
        {%- endfor -%}
        {%- if a.notes %}<span class="note">{{ a.notes }}</span>{% endif %}
      </td>
      <td>
        {%- for id in sortants -%}
        {%- assign v = acteurs | where: "actor_id", id | first -%}
        <a href="#{{ id }}">{{ v.nom_usuel | default: v.nom }}</a>{% unless forloop.last %}, {% endunless %}
        {%- endfor -%}
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
société étrangère n’a que sa catégorie sectorielle. Aucune personne physique
n’est enregistrée.</p>

## Ce qui manque

Ces entités relèvent du périmètre, mais ne sont pas enregistrées :

<ul class="liste-aretes">
  {%- for m in registre.meta.lacunes %}
  <li><strong>{{ m.nom }}</strong> — {{ m.raison }}</li>
  {%- endfor %}
</ul>

Le registre ne contient pas non plus, à ce stade, les liens de commande
publique, d’aide ou de crédit.

Les parts des gestionnaires d’actifs ne sont publiques qu’au-delà du seuil
légal de déclaration : **5%** du capital ou des droits de vote en France,
**3%** aux Pays-Bas pour Airbus SE. En dessous, un gestionnaire peut détenir
une part importante sans qu’elle apparaisse ici. Les parts plus petites que
certaines sociétés publient d’après leurs propres seuils statutaires ne sont
pas reprises : elles ne suivent pas une règle commune. Les banques et les
teneurs de marché, qui franchissent souvent ces seuils pour quelques jours,
ne sont pas enregistrés.

À la date d’arrêt, aucun gestionnaire d’actifs ne déclarait dépasser le seuil
légal chez Thales, Eutelsat, Air France-KLM, Dassault Aviation ni FDJ United.

## D’où viennent ces chiffres

Des documents annuels déposés par les sociétés à l’Autorité des marchés
financiers, des avis de franchissement de seuil publiés par l’AMF, du registre
des participations substantielles de l’autorité néerlandaise des marchés, de l’annexe budgétaire « État
actionnaire » et des textes du Journal officiel. Chaque document est inscrit
au [registre des sources]({{ '/registre/' | relative_url }}).

{{ registre.meta.recoupement }}

Les données complètes, avec les identifiants LEI et ISIN, se téléchargent sur la
[page des données]({{ '/donnees/' | relative_url }}#les-ajouts-de-ce-site-hors-paquet).
