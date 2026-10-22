---
layout: page
title: Représentants d’intérêts
permalink: /representants-interets/
---

{%- assign ri = site.data['representants-interets'] -%}
{%- assign meta = ri.meta -%}

Qui déclare agir auprès des décideurs publics, et auprès de qui : les
**{% include nombre-fr.html n=meta.inscrits %} inscrits** au répertoire des
représentants d’intérêts que tient la Haute Autorité pour la transparence de la
vie publique, et les **{% include nombre-fr.html n=meta.fiches %} fiches
d’activité** de l’exercice {{ meta.exercice }}. C’est un **ajout de ce site,
hors paquet** : le paquet donne la route vers ces déclarations et laisse leur
extraction ouverte ; cette page la fait.

Les chiffres viennent du fichier ouvert du répertoire
(<a href="{{ '/registre/' | relative_url }}#FR-CPL-0113"><code>FR-CPL-0113</code></a>)
dans sa **copie archivée le {% include date-snapshot.html %}**, jour de la date
d’arrêt : le site de la Haute Autorité était indisponible au moment de
l’extraction.

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

- **Une fiche déclarée n’est ni une capture ni une coordination.** Elle établit
  qu’un contact a eu lieu, sur un objet, auprès d’une catégorie de
  responsables ; jamais qu’il a pesé sur la décision.
- **Un cabinet de conseil agit pour ses clients.** Ses dépenses déclarées sont
  les siennes, souvent moins de 10 000 €, mais ses fiches couvrent l’activité
  de ses clients : son rang mesure un volume d’intermédiation, pas un poids
  propre.
- **Le décompte suit les déclarations.** Une organisation qui déclare peu, en
  retard ou pas du tout paraît moins active qu’elle ne l’est.
- **Aucun nom de personne n’est repris**, ni dirigeant, ni collaborateur, ni
  responsable public.

</div>

## Les inscrits

{% include nombre-fr.html n=meta.inscrits %} organisations ou personnes inscrites à la date d’arrêt,
regroupées en familles. Le fichier mélange deux vocabulaires de catégories,
l’ancien et le nouveau : le regroupement est un **choix de ce site**, écrit
dans le script de calcul.

<div class="table-defilante">
<table>
  <thead>
    <tr><th>Famille</th><th>Inscrits</th></tr>
  </thead>
  <tbody>
    {%- for f in ri.inscrits_par_famille %}
    <tr><td>{{ f.famille }}</td><td>{% include nombre-fr.html n=f.nombre %}</td></tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## L’exercice {{ meta.exercice }}

<ul class="chiffres-cles">
  <li><strong>{% include nombre-fr.html n=meta.exercices %}</strong> exercices se terminant en {{ meta.exercice }}, la plupart du 1<sup>er</sup> janvier au 31 décembre</li>
  <li><strong>{% include nombre-fr.html n=meta.exercices_publies %}</strong> déjà déclarés à la date d’arrêt, <strong>{{ meta.defauts_declaration }}</strong> signalés en défaut de déclaration</li>
  <li><strong>{% include nombre-fr.html n=meta.fiches %}</strong> fiches d’activité publiées</li>
</ul>

### Les {{ ri.organisations | size }} organisations qui déclarent le plus de fiches

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Rang</th>
      <th>Organisation</th>
      <th>Famille</th>
      <th>Fiches</th>
      <th>Dépenses déclarées</th>
      <th>Personnes (équivalent temps plein)</th>
    </tr>
  </thead>
  <tbody>
    {%- for o in ri.organisations %}
    <tr>
      <td>{{ o.rang }}</td>
      <td>{{ o.denomination }} <span class="meta">{{ o.type_identifiant }} {{ o.identifiant }}</span></td>
      <td>{{ o.famille }}</td>
      <td>{{ o.fiches }}</td>
      <td>
        {%- if o.depenses -%}
        {{ o.depenses | replace: "> = ", "de " | replace: " et < ", " à moins de " | replace: "< ", "moins de " | replace: " euros", " €" }}
        {%- else -%}<span class="meta">non déclarées</span>{%- endif -%}
      </td>
      <td>{% if o.personnes_etp != nil %}{{ o.personnes_etp | round: 1 | replace: ".", "," }}{% endif %}</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

### Les responsables publics visés

Nombre de fiches qui visent chaque catégorie de responsables. Une fiche peut
en viser plusieurs : les nombres ne s’additionnent pas.

<div class="table-defilante">
<table>
  <thead>
    <tr><th>Catégorie de responsables publics</th><th>Fiches</th></tr>
  </thead>
  <tbody>
    {%- for r in ri.responsables_vises %}
    <tr><td>{{ r.categorie }}</td><td>{% include nombre-fr.html n=r.fiches %}</td></tr>
    {%- endfor %}
  </tbody>
</table>
</div>

Pour les membres du Gouvernement et de leurs cabinets, la déclaration précise
le ministère, dans la nomenclature du répertoire. Les
{{ ri.ministeres_vises | size }} plus visés :

<div class="table-defilante">
<table>
  <thead>
    <tr><th>Ministère</th><th>Fiches</th></tr>
  </thead>
  <tbody>
    {%- for m in ri.ministeres_vises %}
    <tr><td>{{ m.ministere }}</td><td>{% include nombre-fr.html n=m.fiches %}</td></tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## Données et sources

- Le classement des organisations, en tableur :
  [`ajout_representants_interets.csv`]({{ '/assets/donnees/ajout_representants_interets.csv' | relative_url }}).
- Les données d’origine : le
  [répertoire des représentants d’intérêts](https://www.data.gouv.fr/datasets/repertoire-des-representants-dinterets)
  (<a href="{{ '/registre/' | relative_url }}#FR-CPL-0113"><code>FR-CPL-0113</code></a>),
  lu dans la [copie archivée du {% include date-snapshot.html %}](https://web.archive.org/web/{{ meta.copie }}/https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json).
  Le rapport d’activité de la Haute Autorité en donne la lecture officielle
  (<a href="{{ '/registre/' | relative_url }}#FR-SRC-0080"><code>FR-SRC-0080</code></a>).
- Le calcul : `scripts/agreger-representants-interets.py`, dans le dépôt du
  site. Il se relance sur le même fichier et redonne les mêmes chiffres.
