---
layout: page
title: Marchés des acteurs
permalink: /acteurs/marches/
---

{%- assign jt = site.data['acteurs-jointures'] -%}

Les marchés notifiés en {{ jt.meta.annee_notification }} dont un acteur du
[registre des acteurs]({{ '/acteurs/' | relative_url }}) est titulaire ou
acheteur, joints par SIREN. C’est un **ajout de ce site, hors paquet**. Le
tableau d’ensemble, et ce qu’il ne prouve pas, sont sur la page des acteurs, à
la section
[Marchés publics et représentation d’intérêts]({{ '/acteurs/' | relative_url }}#marchés-publics-et-représentation-dintérêts).

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

- **Un marché n’est pas une dépendance.** Il établit une transaction, jamais
  une entente ni un accès privilégié.
- **La jointure se fait par entité juridique, jamais par groupe.** Les
  marchés des filiales n’y figurent pas.
- **Rien n’est additionné.** Le montant d’un accord-cadre est un plafond,
  celui d’un marché à plusieurs titulaires vaut pour le marché entier, et
  certains montants sont des valeurs de remplissage : chaque cas est signalé.
- **Une exception à la date d’arrêt**, la même que pour la
  [commande publique]({{ '/commande-publique/' | relative_url }}) : les
  fichiers sont lus tels que publiés le 22 octobre 2026, mais tous les
  marchés ont été notifiés en {{ jt.meta.annee_notification }}.

</div>

Les marchés sont classés par date de notification. L’objet et le montant
sont ceux que déclare l’acheteur ; les noms des contreparties viennent du
répertoire Sirene.

{% for j in jt.acteurs -%}
{%- if j.titulaire.size > 0 or j.acheteur.size > 0 %}
<details class="detail-marches" id="marches-{{ j.actor_id }}">
  <summary>{{ j.nom }} : {% if j.titulaire.size > 0 %}{% include nombre-fr.html n=j.titulaire.size %} comme titulaire{% endif %}{% if j.titulaire.size > 0 and j.acheteur.size > 0 %}, {% endif %}{% if j.acheteur.size > 0 %}{% include nombre-fr.html n=j.acheteur.size %} comme acheteur{% endif %}</summary>
  {%- assign roles = "titulaire,acheteur" | split: "," -%}
  {%- for role in roles %}
  {%- assign lignes = j[role] %}
  {%- if lignes.size > 0 %}
  <div class="table-defilante">
  <table>
    <caption>Comme {{ role }}</caption>
    <thead>
      <tr><th>Notification</th><th>{% if role == "titulaire" %}Acheteur{% else %}Titulaires{% endif %}</th><th>Objet</th><th>Montant déclaré</th></tr>
    </thead>
    <tbody>
      {%- for l in lignes %}
      <tr>
        <td>{{ l.date }}</td>
        <td>
          {%- for c in l.contreparties -%}
          {{ c.nom | default: "nom non trouvé" }} <span class="meta">{{ c.siren }}</span>{% unless forloop.last %} ; {% endunless %}
          {%- else -%}<span class="meta">aucun SIREN déclaré</span>
          {%- endfor -%}
        </td>
        <td>{{ l.objet }}</td>
        <td>
          {%- if l.montant_fr -%}{{ l.montant_fr }}{%- else -%}<span class="meta">non déclaré</span>{%- endif -%}
          {%- if l.accord_cadre %} <span class="meta">plafond d’accord-cadre</span>{% endif -%}
          {%- if l.titulaires > 1 %} <span class="meta">marché entier, {{ l.titulaires }} titulaires identifiés</span>{% endif -%}
          {%- if l.montant_ecarte and l.montant_fr %} <span class="meta">valeur de remplissage probable</span>{% endif -%}
        </td>
      </tr>
      {%- endfor %}
    </tbody>
  </table>
  </div>
  {%- endif %}
  {%- endfor %}
</details>
{%- endif %}
{%- endfor %}

<script>
  // Un lien vers #marches-FR-ACT-xxxx ouvre le volet de cet acteur.
  (function () {
    function ouvrir() {
      var d = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (d && d.tagName === "DETAILS") d.open = true;
    }
    ouvrir();
    window.addEventListener("hashchange", ouvrir);
  })();
</script>

## Données et sources

- Le détail, en tableur :
  [`ajout_acteurs_jointures.csv`]({{ '/assets/donnees/ajout_acteurs_jointures.csv' | relative_url }}).
- Les données d’origine : les données essentielles de la commande publique
  (<a href="{{ '/registre/' | relative_url }}#FR-SRC-0042"><code>FR-SRC-0042</code></a>).
- Le calcul : `scripts/joindre-acteurs.py`, dans le dépôt du site. Quelques
  objets portent des caractères mal encodés par l’acheteur (apostrophe,
  tiret) ; le script les rétablit, sans rien changer d’autre.
