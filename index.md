---
layout: page
title: France-System-2026
permalink: /
---

<!--
  layout 'page' et non 'home' : le layout 'home' de minima affiche en pied de
  page un lien « subscribe via RSS » sans condition, ce qui n'a pas de sens sur
  un site qui ne publie aucun article.
-->

<p class="chapeau">Qui décide, en France, et sur quoi&nbsp;? Ce site ne répond
pas à la question. Il fait le travail qui doit venir avant&nbsp;: établir
<strong>d’où viennent les informations</strong> dont on dispose, et
<strong>où elles manquent</strong>.</p>

## De quoi il s’agit

Quand on parle du pouvoir en France, on cite souvent des chiffres sans dire
d’où ils sortent. Ce site fait l’inverse. Il publie l’état, arrêté au
{% include date-snapshot.html %}, d’un travail de recensement&nbsp;:

- **{{ site.data.registre | size }} sources officielles** — textes de loi,
  registres publics, données de régulateurs, rapports parlementaires — dont on
  sait qui les publie, à quel rythme et à quoi elles servent&nbsp;;
- **{{ site.data.noeuds | size }} catégories d’acteurs** — l’État, les
  régulateurs, les entreprises, les banques, les médias, les syndicats,
  l’Union européenne — et **{{ site.data.aretes | size }} relations** établies
  entre elles, chacune accompagnée de ce qu’elle prouve et de ce qu’elle ne
  prouve pas&nbsp;;
- **{{ site.data.couverture | size }} domaines** dont on dit franchement
  lesquels sont documentés et lesquels ne le sont pas.

## Ce qui rend ce travail utilisable

**Rien n’est affirmé sans source.** Chaque relation entre deux catégories
d’acteurs renvoie aux documents officiels qui l’établissent. On peut remonter
la chaîne, à chaque fois.

**Les trous sont déclarés.** {{ site.data.couverture | size }} domaines sont
suivis&nbsp;; {{ site.data.couverture | where_exp: "c", "c.status contains 'GAP'" | size }}
n’ont aucune source enregistrée, et le disent. C’est ce qui distingue un travail
de recensement d’une opinion&nbsp;: savoir où l’on ne sait pas, et l’écrire.

**Une relation n’est pas une intention.** Qu’une entreprise ait un contrat
public ne dit rien de son influence. Qu’un régulateur rencontre un lobbyiste ne
prouve pas qu’il lui cède. Ces distinctions sont écrites noir sur blanc à côté
de chaque relation, plutôt que laissées à l’interprétation du lecteur.

## Par où commencer

<ul class="sommaire">
  <li>
    <a href="{{ '/carte/' | relative_url }}">Comment le système est découpé</a>
    <p>Les {{ site.data.noeuds | size }} catégories d’acteurs et les
    {{ site.data.aretes | size }} relations documentées entre elles. C’est la
    vue d’ensemble&nbsp;: qui régule qui, qui finance qui, qui dépend de qui.</p>
  </li>
  <li>
    <a href="{{ '/couverture/' | relative_url }}">Ce qu’on sait et ce qu’on ignore</a>
    <p>Domaine par domaine, l’état du recensement. La page la plus honnête du
    site, et sans doute la plus instructive.</p>
  </li>
  <li>
    <a href="{{ '/registre/' | relative_url }}">Les {{ site.data.registre | size }} sources</a>
    <p>La liste complète, avec pour chacune son institution, son usage prévu et
    son adresse. Filtrable par domaine et par autorité.</p>
  </li>
  <li>
    <a href="{{ '/dimensions/' | relative_url }}">Les {{ site.data.dimensions | size }} formes de pouvoir</a>
    <p>Faire la loi, dépenser, posséder, prêter, distribuer l’information,
    contraindre&nbsp;: autant de pouvoirs distincts, qu’il serait faux de
    confondre en un seul.</p>
  </li>
</ul>

<p class="sommaire-plus">Pour aller plus loin&nbsp;:
<a href="{{ '/methode/' | relative_url }}">la méthode</a> qui fixe ce qui entre
dans le recensement,
<a href="{{ '/audit/' | relative_url }}">les constats</a> qu’il permet déjà de
tirer, <a href="{{ '/feuille-de-route/' | relative_url }}">ce qui manque</a>
pour aller plus loin, et
<a href="{{ '/donnees/' | relative_url }}">les fichiers</a>, téléchargeables et
réutilisables.</p>

## Ce que ce site ne fait pas

Il ne classe pas, ne compare pas, ne conclut pas. En particulier, **aucune
comparaison avec un régime historique n’y est calculée** — le travail de
recensement n’est pas assez avancé pour qu’une telle comparaison veuille dire
quoi que ce soit, et le paquet l’interdit explicitement à ce stade.

Ce qui viendra ensuite est décrit dans la
[feuille de route]({{ '/feuille-de-route/' | relative_url }}).
