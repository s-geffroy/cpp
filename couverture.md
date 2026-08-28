---
layout: page
title: Couverture
permalink: /couverture/
---

{%- assign couverture = site.data.couverture -%}
{%- assign registre = site.data.registre -%}
{%- assign lib = site.data.libelles -%}

{%- comment -%}
  Trois compteurs plutot que trois tableaux : `push` est un filtre ajoute par
  Jekyll, pas du Liquid standard, et rien ici n’a besoin d’iterer sur les
  sous-ensembles. Les nombres affiches viennent donc toujours des donnees.
{%- endcomment -%}
{%- assign nb_fermes = 0 -%}
{%- assign nb_partiels = 0 -%}
{%- assign nb_lacunes = 0 -%}
{%- for c in couverture -%}
  {%- assign couleur = lib.couleurs_couverture[c.status] -%}
  {%- if couleur == "ferme" -%}{%- assign nb_fermes = nb_fermes | plus: 1 -%}
  {%- elsif couleur == "partiel" -%}{%- assign nb_partiels = nb_partiels | plus: 1 -%}
  {%- else -%}{%- assign nb_lacunes = nb_lacunes | plus: 1 -%}
  {%- endif -%}
{%- endfor -%}

Où le paquet documente, et où il ne documente pas. **{{ couverture | size }}
domaines** sont suivis au {% include date-snapshot.html %} :
**{{ nb_fermes }}** dont la route est fermée, **{{ nb_partiels }}**
ouverts sur un point précis, **{{ nb_lacunes }}** en lacune déclarée.

<div class="garde-fou" markdown="1">

### La règle qui gouverne cette page

> Une lacune reste une lacune. Elle n’est jamais silencieusement codée en zéro
> pouvoir, zéro coordination ou zéro dépendance.

C’est pourquoi les {{ nb_lacunes }} domaines sans source n’ont pas été
retirés du tableau. Une case vide se lit comme une absence de pouvoir ; une
lacune déclarée se lit comme un travail non fait.

</div>

## D’un coup d’œil

{% comment %}
  La barre de completude. Chaque domaine occupe la meme largeur, dans l'ordre
  du paquet.

  UNE LACUNE EST DESSINEE COMME UN VIDE, hachure, pas comme un bloc colorie.
  La difference n'est pas decorative : un bloc plein se lit comme une valeur
  mesuree, alors qu'une lacune est une absence de mesure. C'est la regle citee
  plus haut, appliquee au graphique lui-meme.

  PIEGE KRAMDOWN : la balise ouvrante tient sur UNE ligne et une ligne vide la
  separe du titre. Sinon kramdown absorbe le div dans le h2 et transforme les
  attributs indentes en bloc de code, sans erreur de construction.

  Et le commentaire lui-meme s'ecrit SANS tirets de rognage, sans quoi il
  supprimerait la ligne vide dont il est justement question.

  NE JAMAIS ecrire de delimiteurs Liquid litteraux dans un commentaire :
  Liquid les tokenise malgre le commentaire. Une balise de commentaire
  imbriquee ferme le bloc par le mauvais bout et avale ce qui suit.
{% endcomment %}

<div class="completude" role="img" aria-label="État de la documentation pour les {{ couverture | size }} domaines suivis : {{ nb_fermes }} documentés, {{ nb_partiels }} partiellement ouverts, {{ nb_lacunes }} sans aucune source.">
{%- for c in couverture %}<span class="c-{{ lib.couleurs_couverture[c.status] }}" title="{{ lib.domaines[c.domain] }} — {{ lib.statuts_couverture[c.status] }}"></span>{% endfor %}
</div>

<ul class="legende-completude">
<li><i class="c-ferme"></i> <strong>{{ nb_fermes }}</strong> domaines documentés : on sait où chercher, et les sources sont enregistrées</li>
<li><i class="c-partiel"></i> <strong>{{ nb_partiels }}</strong> à moitié : le chemin vers la preuve est connu, le contenu reste à produire</li>
<li><i class="c-lacune"></i> <strong>{{ nb_lacunes }}</strong> sans aucune source : le vide est déclaré, pas comblé</li>
</ul>

## Le tableau

<div class="table-defilante">
<table class="matrice">
  <thead>
    <tr>
      <th>Domaine</th>
      <th>État</th>
      <th>Sources</th>
    </tr>
  </thead>
  <tbody>
    {%- for c in couverture %}
    {%- assign couleur = lib.couleurs_couverture[c.status] -%}
    <tr class="couverture-{{ couleur }}">
      <td>{{ lib.domaines[c.domain] }}</td>
      <td>
        {%- comment -%}
          Le code d'origine passe en infobulle : il sert a retrouver la ligne
          dans les fichiers telechargeables, pas a etre lu. Affiche sous chaque
          libelle, il doublait la hauteur du tableau pour rien.
        {%- endcomment -%}
        <span class="pastille etat-{{ couleur }}" title="Code d’origine : {{ c.status }}">{{ lib.statuts_couverture[c.status] }}</span>
      </td>
      <td>
        {%- if c.sources.size > 0 -%}
        {%- for s in c.sources %}
        <a href="{{ '/registre/' | relative_url }}#{{ s }}"><code>{{ s }}</code></a>{% unless forloop.last %} {% endunless %}
        {%- endfor -%}
        {%- else -%}
        <span class="aucune-source">aucune source enregistrée</span>
        {%- endif -%}
      </td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## Les lacunes déclarées

Le paquet distingue deux niveaux. Les lacunes **A0** portent sur des routes
prioritaires ; les lacunes **A1** sur un second rang, souvent contraint par
l’accès aux données plutôt que par l’effort.

### Lacunes A0

1. Publicité et intermédiation en ligne.
2. Infrastructures et opérateurs de transport et de logistique.
3. Concentration de la distribution et de l’alimentation, pouvoir d’achat.
4. Groupes de construction et d’infrastructures publiques.
5. Propriété des médias et droits de vote, au niveau des sociétés, en 2026.
6. Aides et garanties publiques consolidées, société par société.
7. Accès aux bénéficiaires effectifs ultimes là où les données publiques sont
   restreintes.

### Lacunes A1

1. Réseau de gouvernance reliant les personnes aux organisations.
2. Circulation des carrières entre public et privé.
3. Think tanks, fondations, et financement de la recherche et de l’expertise.
4. Associations, ONG et ordres professionnels.
5. Réseaux de dépendance majeurs entre fournisseurs et clients.
6. Dépendance au crédit et à l’assurance au niveau des groupes, dans la
   mesure où l’accès aux données le permet.

## Ce que « fermé » veut dire

Une route **fermée** signifie que le chemin d’accès à la preuve est établi :
on sait quelle institution publie quoi, sous quel format, à quel rythme. Cela
ne veut **pas** dire que le domaine est analysé, ni que les acteurs y sont
recensés.

Les {{ nb_partiels }} domaines marqués partiels le disent explicitement
dans leur statut : la méthode est fermée mais l’inventaire reste ouvert, ou la
route des sources est fermée mais le graphe des acteurs reste à construire.
C’est l’objet de la [feuille de route]({{ '/feuille-de-route/' | relative_url }}).

<p class="note-table">Le code d’origine est affiché à côté de chaque libellé :
il est plus précis que sa traduction, et c’est lui qui figure dans les fichiers
<a href="{{ '/donnees/' | relative_url }}">téléchargeables</a>.</p>
