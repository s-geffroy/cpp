---
layout: page
title: France-System-2026
permalink: /
---

<!--
  layout 'page' et non 'home' : le layout 'home' de minima affiche en pied de
  page un lien « subscribe via RSS » sans condition, ce qui n'a pas de sens sur
  un site qui ne publie aucun article. Rien d'autre ne les distingue ici.
-->

**Snapshot du {% include date-snapshot.html %}.** Version
{{ site.data.paquet.version }} du paquet `{{ site.data.paquet.project }}`.

Ce site publie une **base documentaire** : le registre des sources et la
cartographie du système français à une date donnée. Il ne publie aucune
conclusion politique, aucun classement et aucune comparaison.

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

## Ce que contient le paquet

<ul class="chiffres">
  <li><strong>{{ site.data.registre | size }}</strong> sources canoniques, toutes vérifiées</li>
  <li><strong>{{ site.data.noeuds | size }}</strong> nœuds dans la carte du système</li>
  <li><strong>{{ site.data.aretes | size }}</strong> arêtes structurelles initiales</li>
  <li><strong>{{ site.data.dimensions | size }}</strong> dimensions de pouvoir</li>
  <li><strong>{{ site.data.couverture | size }}</strong> domaines suivis en couverture</li>
</ul>

## Par où entrer

**[Le registre des sources]({{ '/registre/' | relative_url }})** — les
{{ site.data.registre | size }} sources, filtrables par domaine, autorité et
priorité. Chacune porte son institution, son type, son rythme de mise à jour,
son usage prévu et son adresse.

**[La carte du système]({{ '/carte/' | relative_url }})** — les
{{ site.data.noeuds | size }} nœuds groupés par type, puis les
{{ site.data.aretes | size }} arêtes. Chaque arête est accompagnée de son
garde-fou d'interprétation : ce qu'elle prouve, et ce qu'elle ne prouve pas.

**[Les dimensions de pouvoir]({{ '/dimensions/' | relative_url }})** — les
{{ site.data.dimensions | size }} dimensions que la méthode interdit de
réduire à une seule variable, avec les nœuds et les arêtes qui portent chacune.

**[La couverture]({{ '/couverture/' | relative_url }})** — quels domaines sont
documentés, lesquels ne le sont pas. Une lacune y est affichée comme une
lacune.

**[La méthode]({{ '/methode/' | relative_url }})** — les règles d'admission des
sources, les douze règles dures de la cartographie, les statuts de preuve, et
les règles du graphe des entreprises.

**[L'audit]({{ '/audit/' | relative_url }})** — les sept constats structurels
tirés de la constitution du registre.

**[La feuille de route]({{ '/feuille-de-route/' | relative_url }})** — ce qui
manque pour franchir l'étape suivante.

**[Les données]({{ '/donnees/' | relative_url }})** — les fichiers d'origine,
au format CSV, JSON et JSON Schema, téléchargeables tels quels.

## Une règle de lecture

La méthode répète un avertissement qui s'applique à toutes les pages de ce
site : **une relation n'est pas une preuve d'intention**. Une dépense publique
n'est pas un contrôle, une part de marché n'est pas une domination, un contact
de représentation d'intérêts n'est pas une capture, une proximité dans le
graphe n'est pas une coordination.

Les arêtes portent un statut de preuve, de `P0` (non prouvé) à `P4` (preuve
officielle directe). Elles ne montent pas d'un cran parce qu'elles paraissent
plausibles.
