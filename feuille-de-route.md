---
layout: page
title: Feuille de route
permalink: /feuille-de-route/
---

{%- assign couverture = site.data.couverture -%}
{%- assign lib = site.data.libelles -%}
{%- assign nb_partiels = 0 -%}
{%- assign nb_lacunes = 0 -%}
{%- for c in couverture -%}
  {%- assign couleur = lib.couleurs_couverture[c.status] -%}
  {%- if couleur == "partiel" -%}{%- assign nb_partiels = nb_partiels | plus: 1 -%}
  {%- elsif couleur == "lacune" -%}{%- assign nb_lacunes = nb_lacunes | plus: 1 -%}
  {%- endif -%}
{%- endfor -%}

La v0.1 est une **base documentaire fermée**, pas une analyse. Cette page dit
ce qui manque pour franchir l’étape suivante, telle que le paquet la nomme :

> {{ lib.paquet_valeurs[site.data.paquet.next_gate] }}

<div class="mise en garde" markdown="1">

### La porte reste fermée

Le paquet déclare toute comparaison avec le NSDAP
**{{ lib.paquet_valeurs[site.data.paquet.comparison_with_nsdap] }}**, et
l'[audit]({{ '/audit/' | relative_url }}) conclut qu’aucun calcul de similarité
n’est autorisé.

Ce n’est pas une précaution de forme. Tant que le registre des acteurs n’existe
pas, il n’y a rien à comparer : la carte actuelle décrit des **catégories**
— « grands groupes privés français », « organisations syndicales » — et non des
organisations nommées, avec leurs détentions, leurs financements et leurs
dépendances mesurées.

</div>

## Ce qui bloque, dans l’ordre

### 1. Les {{ nb_lacunes }} domaines en lacune

Aucune source n’y est enregistrée. Ils sont listés, avec leur statut, sur la
[page de couverture]({{ '/couverture/' | relative_url }}) — publicité et
intermédiation, transport et logistique, distribution et alimentation,
construction et infrastructures pour les lacunes A0 ; ordres professionnels,
associations et fondations, think tanks et réseaux d’expertise, réseau des
personnes et de la gouvernance pour les A1.

### 2. Les {{ nb_partiels }} domaines dont la route est fermée mais le contenu ouvert

Ce sont les plus trompeurs : leur statut commence par `A0_..._CLOSED`, ce qui
peut se lire comme « fait ». Il signifie seulement que **le chemin d’accès à la
preuve est connu**. Le graphe des acteurs, les mesures par acteur, l’extraction
des enregistrements et la mise à jour 2026 restent à produire.

<div class="table-defilante">
<table class="matrice">
  <thead>
    <tr><th>Domaine</th><th>Ce qui reste ouvert</th></tr>
  </thead>
  <tbody>
    {%- for c in couverture -%}
    {%- if lib.couleurs_couverture[c.status] == "partiel" %}
    <tr class="couverture-partiel">
      <td>{{ lib.domaines[c.domain] }}</td>
      <td><span class="pastille etat-partiel">{{ lib.statuts_couverture[c.status] }}</span></td>
    </tr>
    {%- endif -%}
    {%- endfor %}
  </tbody>
</table>
</div>

### 3. L’accès aux bénéficiaires effectifs

L’audit le qualifie de **lacune de preuve réelle**. La méthode interdit de
deviner le bénéficiaire effectif ultime quand le registre de l’INPI est
inaccessible. Aucune ingéniosité de traitement ne remplace une donnée dont
l’accès est restreint par le droit.

### 4. Deux vocabulaires de dimensions qui ne se joignent pas

Ce point n’est pas dans les rapports du paquet : il ressort de la lecture des
fichiers.

Les catégories d’acteurs et les relations de la carte utilisent les
{{ site.data.dimensions | size }} identifiants canoniques `P-*`. Le
[registre des sources]({{ '/registre/' | relative_url }}) étiquette ses entrées
avec un champ `power_dimensions` en texte libre, comptant
{{ site.data.registre | map: "power_dimensions" | join: ";" | split: ";" | uniq | size }}
mots-clés distincts. Aucune table de correspondance n’existe entre les deux.

Conséquence pratique : on ne peut pas répondre, depuis les données seules, à la
question « quelles sources documentent la dimension *{{ lib.dimensions['P-OWN'].label | downcase }}* ? ».
Ce site s’abstient d’y répondre plutôt que d’inventer la correspondance. La
combler suppose soit d’étiqueter les {{ site.data.registre | size }} sources
avec le vocabulaire fermé, soit de publier explicitement une table de passage.

### 5. Une carte structurelle, pas un graphe rempli

{{ site.data.aretes | size }} relations pour {{ site.data.noeuds | size }} catégories d’acteurs.
L’architecture est posée ; l’absence de relation entre deux catégories signale une
relation non documentée, jamais une relation inexistante.

## Ce que l’étape suivante suppose

Passer au registre des acteurs demande de descendre de la **catégorie** à
l'**organisation nommée**, avec pour chacune la chaîne exigée par la
[méthode]({{ '/methode/' | relative_url }}#graphe) : entité juridique,
filiales, détention, droits de vote, gouvernance, financement, marchés publics,
subventions, régulation, infrastructures, médias.

Et à chaque lien, le statut de preuve qui va avec — de `P0` à `P4`. C’est ce
niveau d’exigence, et non la seule quantité de données, qui sépare les deux
étapes.

## Ce que franchir cette étape ne rendrait toujours pas légitime

Même complet, un registre d’acteurs ne rend recevable aucune comparaison
historique par lui-même. Les douze règles dures de la méthode continueraient de
s’appliquer, en particulier la douzième : **toute affirmation causale forte
exige un mécanisme documenté et l’examen des explications alternatives**.
