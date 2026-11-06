---
layout: page
title: Décisions
permalink: /decisions/
---

{%- assign registre = site.data.acteurs -%}
{%- comment -%} Une ligne TO_VERIFY n'est jamais publiee. {%- endcomment -%}
{%- assign decisions = registre.decisions | where: "statut", "VERIFIED" -%}
{%- assign competences = registre.competences | where: "statut", "VERIFIED" -%}
{%- assign acteurs = registre.acteurs | where: "statut", "VERIFIED" -%}
{%- assign lib = site.data.libelles -%}
{%- assign toutes_sources = site.data.registre | concat: site.data['registre-complement'].sources -%}
{%- assign ordre_roles = "decide,homologue_ou_approuve,avis_conforme,demande_reexamen,propose,avis_simple,encadre,execute,peut_annuler" | split: "," -%}
{%- assign domaines = decisions | map: "domaine" | uniq -%}

Les autres pages de ce site disent surtout **qui possède quoi**. Celle-ci
commence à dire **qui décide de quoi** : pour un objet de décision précis,
quel acteur tranche, lequel propose, lequel peut bloquer, lequel est
seulement consulté, et quel juge peut annuler.

Chaque ligne renvoie à l’article de loi ou de règlement qui fonde la
compétence, dans sa version en vigueur au {% include date-snapshot.html %}.

<div class="garde-fou" markdown="1">

### Un pouvoir juridique, pas un pouvoir de fait

Cette page dit qui a **le droit** de décider. Elle ne dit pas qui pèse
effectivement sur la décision, ni dans quel sens la compétence a été
exercée : **capacité réglementaire ≠ intention politique** (règle 8 de la
[méthode]({{ '/methode/' | relative_url }}#cartographie)). Les contraintes de
l’Union s’imputent à l’Union (règle 10). Aucune affirmation sur l’influence
réelle n’est tirée de ce tableau (règle 12).

Les fonctions — Président de la République, ministre, président d’une
assemblée — sont enregistrées comme des **sièges**, jamais comme les
personnes qui les occupent.

</div>

C’est un **pilote**, limité pour l’instant au domaine
{% for d in domaines %}« {{ lib.domaines[d] | default: d }} »{% unless forloop.last %}, {% endunless %}{% endfor %} :
{{ decisions | size }} objets de décision, {{ competences | size }} compétences.
C’est un ajout éditorial, hors paquet.

## Qui intervient sur quoi

Chaque acteur, et les décisions où il tient un rôle. Les numéros renvoient
au détail plus bas.

<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Acteur</th>
      {%- for r in ordre_roles %}
      {%- assign avec_role = competences | where: "role", r %}
      {%- if avec_role.size > 0 %}
      <th>{{ lib.roles_competence[r] }}</th>
      {%- endif %}
      {%- endfor %}
    </tr>
  </thead>
  <tbody>
    {%- assign ids_acteurs = competences | map: "acteur" | uniq -%}
    {%- for id in ids_acteurs %}
    {%- assign a = acteurs | where: "actor_id", id | first %}
    {%- assign siennes = competences | where: "acteur", id %}
    <tr>
      <td><strong><a href="{{ '/acteurs/' | relative_url }}#{{ a.actor_id }}">{{ a.nom_usuel | default: a.nom }}</a></strong>
        <span class="meta">{{ lib.types_acteur[a.type_acteur] }}</span></td>
      {%- for r in ordre_roles %}
      {%- assign avec_role = competences | where: "role", r %}
      {%- if avec_role.size > 0 %}
      {%- assign ici = siennes | where: "role", r | map: "decision" | uniq %}
      <td>
        {%- for d in ici -%}
        <a href="#{{ d }}">{{ d | remove: "FR-DEC-" | plus: 0 }}</a>{% unless forloop.last %}, {% endunless %}
        {%- endfor -%}
      </td>
      {%- endif %}
      {%- endfor %}
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## Le détail, décision par décision

{% for d in decisions %}
{%- assign siennes = competences | where: "decision", d.decision_id %}
<section class="fiche" id="{{ d.decision_id }}">
  <h3>{{ d.decision_id | remove: "FR-DEC-" | plus: 0 }}. {{ d.libelle }}</h3>
  <p class="meta"><code>{{ d.decision_id }}</code> ·
    <span class="pastille dimension">{{ d.dimension }} — {{ lib.dimensions[d.dimension].label }}</span></p>
  {%- if d.notes %}
  <p class="note">{{ d.notes }}</p>
  {%- endif %}
  <div class="table-defilante">
  <table>
    <thead>
      <tr><th>Rôle</th><th>Acteur</th><th>Fondement</th><th>Preuve</th></tr>
    </thead>
    <tbody>
      {%- for r in ordre_roles %}
      {%- assign lignes = siennes | where: "role", r %}
      {%- for k in lignes %}
      {%- assign a = acteurs | where: "actor_id", k.acteur | first %}
      <tr id="{{ k.competence_id }}">
        <td>{{ lib.roles_competence[k.role] }}</td>
        <td><a href="{{ '/acteurs/' | relative_url }}#{{ a.actor_id }}">{{ a.nom_usuel | default: a.nom }}</a>
          {%- if k.nombre_sieges %} <span class="meta">{{ k.nombre_sieges }} siège{% if k.nombre_sieges > 1 %}s{% endif %} sur {{ k.sieges_total }}</span>{% endif %}</td>
        <td>
          {%- for c in k.citations %}
          {%- assign source = toutes_sources | where: "source_id", c.source_id | first %}
          <a href="{{ c.url }}" rel="noopener">{{ c.localisation | default: source.title }}</a>
          <span class="meta">{{ source.title | replace: "'", "’" }}
            (<a href="{{ '/registre/' | relative_url }}#{{ c.source_id }}"><code>{{ c.source_id }}</code></a>)</span>
          {%- endfor %}
          <span class="meta">En vigueur depuis le {% include date-fr.html date=k.en_vigueur_depuis %}.</span>
          {%- if k.incertitude %}<span class="note">{{ k.incertitude }}</span>{% endif %}
          <p class="ne-prouve-pas">{{ k.garde_fou }}</p>
        </td>
        <td><span class="pastille preuve-{{ k.preuve | downcase }}">{{ k.preuve }}</span>
          <code>{{ k.competence_id }}</code></td>
      </tr>
      {%- endfor %}
      {%- endfor %}
    </tbody>
  </table>
  </div>
</section>
{% endfor %}

## Ce qui manque

{%- assign manques = registre.meta.lacunes | where_exp: "l", "l.nom contains 'FR-DEC-'" %}
{%- if manques.size > 0 %}
<ul>
  {%- for l in manques %}
  <li><strong>{{ l.nom }}</strong> : {{ l.raison }}</li>
  {%- endfor %}
</ul>
{%- endif %}

Et, plus largement, tout le reste : ce pilote ne couvre qu’un domaine sur {{ site.data.couverture | size }}.
Les autres domaines suivront un par un,
avec la même règle : un article en vigueur à la date d’arrêt pour chaque
compétence.

## D’où viennent ces textes

Légifrance et EUR-Lex refusent les lectures automatiques. Les textes
français ont été lus dans l’export officiel de la base Légifrance publié
par la DILA (données LEGI et JORF), version par version ; les textes
européens, au Journal officiel de l’Union. Chaque ligne a été relue à la
main avant publication. Les fichiers sont téléchargeables sur la
[page des données]({{ '/donnees/' | relative_url }}) :
`ajout_decisions.json` et `ajout_competences.json`.
