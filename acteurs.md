---
layout: page
title: Acteurs
permalink: /acteurs/
---

{%- assign registre = site.data.acteurs -%}
{%- comment -%} Une ligne TO_VERIFY n'est jamais publiee. {%- endcomment -%}
{%- assign acteurs = registre.acteurs | where: "statut", "VERIFIED" -%}
{%- assign liens_tous = registre.liens | where: "statut", "VERIFIED" -%}
{%- comment -%}
  La dependance a l'Etat client n'est pas une detention : elle reste hors des
  decomptes, des filtres et du tableau des detenteurs de tete.
{%- endcomment -%}
{%- assign liens = liens_tous | where_exp: "l", "l.type != 'defense_procurement'" -%}
{%- assign clients = liens_tous | where: "type", "defense_procurement" -%}
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
gestionnaires d’actifs et les fonds qui ont déclaré dépasser le seuil légal ;
les [entreprises de défense privées](#entreprises-de-défense-privées)
cotées à Paris et leurs actionnaires ; enfin, les sept banques d’importance
systémique désignées par l’ACPR
(<a href="{{ '/registre/' | relative_url }}#FR-CPL-0126"><code>FR-CPL-0126</code></a>)
et leurs actionnaires directs à 5% ou plus. Pour les groupes mutualistes, le
registre s’arrête à l’organe central : les caisses et les sociétaires qui le
détiennent n’y entrent pas. S’y ajoutent les groupes de médias en 2026 :
télévision, radio et presse cotées, les groupes non cotés dont l’actionnaire
est publié dans un document primaire, et l’audiovisuel public. La propriété
d’un média ne prouve jamais une intervention dans sa ligne éditoriale. Enfin,
les quarante sociétés du CAC 40 à la date d’arrêt, avec leurs actionnaires
directs au-delà du seuil légal (5%, ou 3% pour les sociétés de droit
néerlandais), d’après leur dernier document annuel et les avis de l’AMF
publiés avant le {% include date-fr.html date=registre.meta.date_arret %}. C’est un **ajout de ce site, hors
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
- **Propriété publique ≠ régulation ≠ commande publique ≠ subvention.** Seule
  la [dépendance des entreprises de défense à l’État client](#dépendance-à-létat-client)
  est saisie, à part, d’après la part de chiffre d’affaires qu’elles publient.
  **Un client n’est pas un contrôle.**

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

    {%- assign client = clients | where: "target_actor", id | first -%}
    {%- if client %}
    <p class="dependance">
      <strong>{{ lib.types_lien_acteur[client.type] }}</strong>, exercice {{ client.exercice }} :
      défense {% if client.part_ca_defense_pct == nil %}<span class="absente">non publiée</span>{% else %}{{ client.part_ca_defense_pct | replace: ".", "," }}% du chiffre d’affaires{% if client.libelle_defense %} ({{ client.libelle_defense }}){% endif %}{% endif %} ;
      France {% if client.part_ca_france_pct == nil %}<span class="absente">non publiée</span>{% else %}{{ client.part_ca_france_pct | replace: ".", "," }}%, {{ lib.perimetre_france[client.perimetre_france] }}{% endif %}.
      <a href="#{{ client.link_id }}">Source et réserve</a>.
    </p>
    {%- endif %}
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
directement ou par une holding qu’il détient entièrement, si une entité
publique (Caisse des dépôts, Bpifrance) en détient la majorité, ou si le
document de la société qualifie ce contrôle ; « grand groupe privé français » sinon. Une
société étrangère n’a que sa catégorie sectorielle. Aucune personne physique
n’est enregistrée : voir <a href="{{ '/beneficiaires-effectifs/' | relative_url }}">Bénéficiaires effectifs</a>.</p>

## Ce qui manque

Ces entités relèvent du périmètre, mais ne sont pas enregistrées :

<ul class="liste-aretes">
  {%- for m in registre.meta.lacunes %}
  <li><strong>{{ m.nom }}</strong> — {{ m.raison }}</li>
  {%- endfor %}
</ul>

Le registre ne contient pas non plus, à ce stade, les liens de commande
publique, d’aide ou de crédit, hors la dépendance des entreprises de défense
à l’État client.

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

## Entreprises de défense privées

Une entreprise de défense « privée », ici, est une société **sans capital ni
action de l’État**. Elle peut compter d’autres détenteurs publics, comme
Bpifrance : ils sont enregistrés comme tels. Trois conditions, toutes écrites
dans les documents de la société, la font entrer dans le registre :

- elle est cotée sur Euronext Paris ou Euronext Growth Paris, et son siège est
  en France ;
- son dernier document annuel avant la date d’arrêt publie une part de la
  défense **d’au moins 10%** du chiffre d’affaires, seule ou dans un secteur
  mixte qui la nomme (« Défense/Spatial », « Défense, Sécurité & Espace »), ou
  écrit que la défense est majoritaire ;
- aucun pourcentage n’est calculé par ce site pour l’atteindre.

Sont enregistrés ses actionnaires au-delà du seuil légal de 5%, dont les
holdings familiales ou de contrôle. Les personnes physiques ne le sont jamais :
quand une famille détient une société par une holding, seule la holding
apparaît.

Ont été examinées puis écartées, faute de part de défense publiée ou parce
qu’elle restait sous 10% : Alten, Archos, Assystem, Atos, Bureau Veritas,
Capgemini, Dassault Systèmes, Derichebourg, Drone Volt, Europlasma, Figeac Aéro,
Groupe Crit, Lacroix, Latécoère, Lisi, Logic Instrument, Manitou, Mersen,
Nexans, Parrot, Prodways, Soditech, Spie, Vallourec et Wallix. Archos annonce
« 75% de l’activité tirée par la défense » dans un communiqué de résultats,
mais pas dans son rapport financier annuel. SII, radiée d’Euronext Paris le
12 mars 2024, sort du périmètre.

## Dépendance à l’État client

Le paquet relie l’État, acheteur stratégique, à l’industrie de défense
(relation `defense_procurement`). Ce tableau la descend au niveau des
sociétés, pour l’exercice 2025 : la part de leur chiffre d’affaires réalisée
dans la défense, et celle réalisée en France ou avec l’État français, **telles
que chaque société les publie**. Une part non publiée reste vide : ce site
n’en calcule aucune, même à partir de montants publiés.

<div class="garde-fou" markdown="1">

**Un client n’est pas un contrôle.** Une part de chiffre d’affaires mesure une
dépendance commerciale, pas une influence. Les libellés ne se comparent pas
d’une société à l’autre : « Défense/Spatial » ou « Airbus Defence and Space »
débordent la défense seule, et « France » désigne tantôt tous les clients
situés en France, tantôt l’État lui-même.

</div>

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Société</th>
      <th>Part défense</th>
      <th>Part France</th>
      <th>Source et réserve</th>
    </tr>
  </thead>
  <tbody>
    {%- for l in clients %}
    {%- assign v = acteurs | where: "actor_id", l.target_actor | first -%}
    {%- assign source = toutes_sources | where: "source_id", l.citation.source_id | first %}
    <tr id="{{ l.link_id }}">
      <td><a href="#{{ v.actor_id }}">{{ v.nom_usuel | default: v.nom }}</a></td>
      <td>
        {%- if l.part_ca_defense_pct == nil -%}<span class="meta">non publiée</span>
        {%- else -%}{{ l.part_ca_defense_pct | replace: ".", "," }}%{% if l.libelle_defense %} <span class="meta">{{ l.libelle_defense }}</span>{% endif %}{%- endif -%}
      </td>
      <td>
        {%- if l.part_ca_france_pct == nil -%}<span class="meta">non publiée</span>
        {%- else -%}{{ l.part_ca_france_pct | replace: ".", "," }}% <span class="meta">{{ lib.perimetre_france[l.perimetre_france] }}</span>{%- endif -%}
      </td>
      <td>
        <a href="{{ l.citation.url }}" rel="noopener">{{ source.title | replace: "'", "’" }}</a>, {{ l.citation.localisation }}
        (<a href="{{ '/registre/' | relative_url }}#{{ l.citation.source_id }}"><code>{{ l.citation.source_id }}</code></a>, lien <code>{{ l.link_id }}</code>).
        <span class="note">{{ l.incertitude }}</span>
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

Ce que mesure la demande étrangère se lit dans le
[rapport au Parlement sur les exportations d’armement]({{ '/registre/' | relative_url }}#FR-CPL-0130).

## Marchés publics et représentation d’intérêts

{%- assign jt = site.data['acteurs-jointures'] %}
{%- capture ancre_cp %}les-{{ site.data['commande-publique'].acheteurs | size }}-acheteurs-les-plus-fréquents{% endcapture %}

Chaque acteur qui a un SIREN est cherché, par ce numéro, dans deux fichiers
publics : les marchés notifiés en {{ jt.meta.annee_notification }}, tels que
les déclarent les données essentielles de la commande publique (la même
extraction que la page [Commande publique]({{ '/commande-publique/' | relative_url }}),
avec la même exception de date), et le répertoire des représentants
d’intérêts, dans sa copie archivée le {% include date-snapshot.html %} (la
même que la page [Représentants d’intérêts]({{ '/representants-interets/' | relative_url }})).
Sur {{ jt.meta.acteurs_siren }} acteurs qui ont un SIREN,
**{{ jt.meta.trouves }}** apparaissent dans au moins un des deux fichiers ;
{{ jt.meta.aucun }} n’apparaissent dans aucun.

<div class="garde-fou" markdown="1">

**Ce que ce tableau ne prouve pas.**

- **Un marché n’est pas une dépendance, une fiche n’est pas une influence.**
  L’un établit une transaction, l’autre un contact déclaré.
- **La jointure se fait par entité juridique, jamais par groupe.** Une société
  de tête qui ne signe aucun marché peut avoir des filiales qui en signent des
  milliers ; une organisation peut s’inscrire à la Haute Autorité sous le
  SIREN d’une autre entité. Un zéro ne veut donc pas dire « absent ».
- **Rien n’est additionné.** Les marchés sont listés un par un, avec le
  montant que déclare l’acheteur : celui d’un accord-cadre est un plafond,
  celui d’un marché à plusieurs titulaires vaut pour le marché entier, et
  certains montants sont des valeurs de remplissage. Chacun de ces cas est
  signalé.

</div>

Les acheteurs publics du registre passent chacun des centaines, parfois des
milliers de marchés par an. Leurs achats ne sont donc pas détaillés ici : le
tableau donne leur rang et leurs comptes, repris tels quels du classement des
[acheteurs les plus fréquents]({{ '/commande-publique/' | relative_url }}#{{ ancre_cp }}).
La Caisse des dépôts et France Télévisions, dont le détail était publié avant
qu’ils soient classés parmi les acheteurs, le gardent.

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Acteur</th>
      <th>Marchés {{ jt.meta.annee_notification }} comme titulaire</th>
      <th>Marchés {{ jt.meta.annee_notification }} comme acheteur</th>
      <th>Répertoire des représentants d’intérêts, exercice {{ jt.meta.annee_notification }}</th>
    </tr>
  </thead>
  <tbody>
    {%- for j in jt.acteurs %}
    {%- assign ac_t = j.titulaire | where: "accord_cadre", true | size -%}
    {%- assign ac_a = j.acheteur | where: "accord_cadre", true | size %}
    <tr>
      <td><a href="#{{ j.actor_id }}">{{ j.nom }}</a> <span class="meta">SIREN {{ j.siren }}</span></td>
      <td>
        {%- if j.titulaire.size > 0 -%}
        <a href="{{ '/acteurs/marches/' | relative_url }}#marches-{{ j.actor_id }}">{% include nombre-fr.html n=j.titulaire.size %}</a>{% if ac_t > 0 %} <span class="meta">dont {{ ac_t }} accord{% if ac_t > 1 %}s{% endif %}-cadre{% if ac_t > 1 %}s{% endif %}</span>{% endif %}
        {%- else -%}<span class="meta">aucun</span>{%- endif -%}
      </td>
      <td>
        {%- if j.acheteur_classement -%}
        {%- assign rg = site.data['commande-publique'].acheteurs | where: "siren", j.siren | first -%}
        {%- if rg -%}
        <a href="{{ '/commande-publique/' | relative_url }}#{{ ancre_cp }}">{% include nombre-fr.html n=rg.marches %}</a> <span class="meta">dont {% include nombre-fr.html n=rg.accords_cadres %} accords-cadres ; rang {{ rg.rang }} des acheteurs, non détaillé ici</span>
        {%- else -%}<span class="meta">hors du classement des acheteurs</span>{%- endif -%}
        {%- elsif j.acheteur.size > 0 -%}
        <a href="{{ '/acteurs/marches/' | relative_url }}#marches-{{ j.actor_id }}">{% include nombre-fr.html n=j.acheteur.size %}</a>{% if ac_a > 0 %} <span class="meta">dont {{ ac_a }} accord{% if ac_a > 1 %}s{% endif %}-cadre{% if ac_a > 1 %}s{% endif %}</span>{% endif %}
        {%- else -%}<span class="meta">aucun</span>{%- endif -%}
      </td>
      <td>
        {%- if j.hatvp == nil -%}<span class="meta">non inscrit sous ce SIREN</span>
        {%- elsif j.hatvp.exercice == nil -%}inscrit <span class="meta">aucun exercice {{ jt.meta.annee_notification }}</span>
        {%- elsif j.hatvp.exercice.publie == false -%}inscrit <span class="meta">exercice {{ jt.meta.annee_notification }} non publié dans la copie{% if j.hatvp.exercice.defaut_declaration %}, signalé en défaut de déclaration{% endif %}</span>
        {%- else -%}
        {{ j.hatvp.exercice.fiches }} fiche{% if j.hatvp.exercice.fiches > 1 %}s{% endif %}
        <span class="meta">
          {%- if j.hatvp.exercice.depenses -%}
          dépenses {{ j.hatvp.exercice.depenses | replace: "> = ", "de " | replace: " et < ", " à moins de " | replace: "< ", "moins de " | replace: " euros", " €" }}
          {%- else -%}dépenses non déclarées{%- endif -%}
        </span>
        {%- endif -%}
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

Chaque marché, un par un, avec son objet et le montant déclaré par
l’acheteur, est sur la page
[Marchés des acteurs]({{ '/acteurs/marches/' | relative_url }}).

Le détail se télécharge en tableur :
[`ajout_acteurs_jointures.csv`]({{ '/assets/donnees/ajout_acteurs_jointures.csv' | relative_url }}).
Le calcul : `scripts/joindre-acteurs.py`, dans le dépôt du site.

## D’où viennent ces chiffres

Des documents annuels déposés par les sociétés à l’Autorité des marchés
financiers, des avis de franchissement de seuil publiés par l’AMF, du registre
des participations substantielles de l’autorité néerlandaise des marchés, de l’annexe budgétaire « État
actionnaire » et des textes du Journal officiel. Chaque document est inscrit
au [registre des sources]({{ '/registre/' | relative_url }}).

{{ registre.meta.recoupement }}

Les données complètes, avec les identifiants LEI et ISIN, se téléchargent sur la
[page des données]({{ '/donnees/' | relative_url }}#les-ajouts-de-ce-site-hors-paquet).
