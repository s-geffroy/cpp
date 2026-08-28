---
layout: page
title: France-System-2026
permalink: /
---

<!--
  layout 'page' et non 'home' : le layout 'home' de minima affiche en pied de
  page un lien « subscribe via RSS » sans condition, ce qui n'a pas de sens sur
  un site qui ne publie aucun article. Rien d'autre ne les distingue ici.

  Pas de titre de section avant la these : c'est l'ouverture de la page, et ce
  qu'elle dit est le sujet meme du site.
-->

<p class="these">Une base documentaire arrêtée au
{% include date-snapshot.html %} : d'où viennent les informations, comment le
système français est découpé, et <em>ce que les données ne prouvent pas</em>.</p>

<dl class="releve">
  <div>
    <dt>Sources canoniques, toutes vérifiées</dt>
    <dd>{{ site.data.registre | size }}</dd>
  </div>
  <div>
    <dt>Nœuds de la carte du système</dt>
    <dd>{{ site.data.noeuds | size }}</dd>
  </div>
  <div>
    <dt>Arêtes structurelles documentées</dt>
    <dd>{{ site.data.aretes | size }}</dd>
  </div>
  <div>
    <dt>Dimensions de pouvoir</dt>
    <dd>{{ site.data.dimensions | size }}</dd>
  </div>
  <div>
    <dt>Domaines suivis en couverture</dt>
    <dd>{{ site.data.couverture | size }}</dd>
  </div>
</dl>

<div class="garde-fou" markdown="1">

### Ce que ce site ne fait pas

Le paquet porte une interdiction explicite :
`comparison_with_nsdap: {{ site.data.paquet.comparison_with_nsdap }}`. Le
rapport d'audit conclut qu'**aucun calcul de similarité n'est autorisé à ce
stade**.

Ce site s'y tient. Il établit d'où viennent les informations et comment le
système est découpé — rien de plus. L'étape suivante, non franchie, est
*{{ site.data.paquet.next_gate }}*.

</div>

## Par où entrer

<ul class="sommaire">
  <li>
    <a href="{{ '/registre/' | relative_url }}">Le registre des sources</a>
    <p>Les {{ site.data.registre | size }} sources, filtrables par domaine,
    autorité et priorité. Chacune porte son institution, son type, son rythme
    de mise à jour, son usage prévu et son adresse.</p>
  </li>
  <li>
    <a href="{{ '/carte/' | relative_url }}">La carte du système</a>
    <p>Les {{ site.data.noeuds | size }} nœuds groupés par type, puis les
    {{ site.data.aretes | size }} arêtes. Chaque arête est accompagnée de son
    garde-fou d'interprétation : ce qu'elle prouve, et ce qu'elle ne prouve
    pas.</p>
  </li>
  <li>
    <a href="{{ '/dimensions/' | relative_url }}">Les dimensions de pouvoir</a>
    <p>Les {{ site.data.dimensions | size }} dimensions que la méthode interdit
    de réduire à une seule variable, avec les nœuds et les arêtes qui portent
    chacune.</p>
  </li>
  <li>
    <a href="{{ '/couverture/' | relative_url }}">La couverture</a>
    <p>Quels domaines sont documentés, lesquels ne le sont pas. Une lacune y
    est affichée comme une lacune.</p>
  </li>
  <li>
    <a href="{{ '/methode/' | relative_url }}">La méthode</a>
    <p>Les règles d'admission des sources, les douze règles dures de la
    cartographie, les statuts de preuve, et les règles du graphe des
    entreprises.</p>
  </li>
  <li>
    <a href="{{ '/audit/' | relative_url }}">L'audit</a>
    <p>Les sept constats structurels tirés de la constitution du registre.</p>
  </li>
  <li>
    <a href="{{ '/feuille-de-route/' | relative_url }}">La feuille de route</a>
    <p>Ce qui manque pour franchir l'étape suivante.</p>
  </li>
  <li>
    <a href="{{ '/donnees/' | relative_url }}">Les données</a>
    <p>Les fichiers d'origine, au format CSV, JSON et JSON Schema,
    téléchargeables tels quels.</p>
  </li>
</ul>

## Une règle de lecture

La méthode répète un avertissement qui s'applique à toutes les pages de ce
site : **une relation n'est pas une preuve d'intention**. Une dépense publique
n'est pas un contrôle, une part de marché n'est pas une domination, un contact
de représentation d'intérêts n'est pas une capture, une proximité dans le
graphe n'est pas une coordination.

Les arêtes portent un statut de preuve, de `P0` (non prouvé) à `P4` (preuve
officielle directe). Elles ne montent pas d'un cran parce qu'elles paraissent
plausibles.
