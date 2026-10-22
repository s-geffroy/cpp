---
layout: page
title: Commande publique
permalink: /commande-publique/
---

{%- assign cp = site.data['commande-publique'] -%}
{%- assign meta = cp.meta -%}

Qui vend le plus souvent aux acheteurs publics, et qui achète le plus souvent :
les **{% include nombre-fr.html n=meta.marches %} marchés notifiés en
{{ meta.annee_notification }}** que déclarent les données essentielles de la
commande publique, classés par entité juridique. C’est un **ajout de ce site,
hors paquet** : le paquet donne la route vers ces données
(<a href="{{ '/registre/' | relative_url }}#FR-SRC-0042"><code>FR-SRC-0042</code></a>)
et laisse leur extraction ouverte ; cette page la fait.

<div class="garde-fou" markdown="1">

### Une exception à la date d’arrêt

Le reste du site s’arrête au {% include date-snapshot.html %}. Ces chiffres,
eux, viennent des fichiers **tels que publiés le 22 octobre 2026** : la
plateforme ne garde que leur dernière version, et un acheteur peut déclarer
un marché des mois après l’avoir notifié. Tous les marchés comptés ont été
notifiés en {{ meta.annee_notification }} ; seule l’exhaustivité de leur
déclaration dépasse la date d’arrêt. Aucun fait postérieur n’y entre.

</div>

<div class="garde-fou" markdown="1">

### Ce que cette page ne prouve pas

- **Un marché attribué n’est pas une influence.** Il établit une transaction,
  au mieux une dépendance commerciale ; jamais une entente, ni un accès
  privilégié.
- **Un rang n’est pas une part de marché.** Les marchés sont comptés, pas
  pondérés : un contrat d’entretien d’espaces verts pèse autant qu’un contrat
  d’infrastructure.
- **Une entité n’est pas un groupe.** Colas France et Eiffage Route Grand Sud
  sont classées chacune pour elle-même ; aucun total par groupe n’est calculé.
- **Une absence ne prouve rien.** Une partie des acheteurs ne déclare pas, ou
  mal ; les marchés de défense et de sécurité sont presque absents des données.

</div>

## En chiffres

<ul class="chiffres-cles">
  <li><strong>{% include nombre-fr.html n=meta.marches %}</strong> marchés notifiés en {{ meta.annee_notification }}, après dédoublonnage de {% include nombre-fr.html n=meta.fiches_lues %} fiches lues dans {{ meta.fichiers | size }} fichiers mensuels</li>
  <li><strong>{% include nombre-fr.html n=meta.accords_cadres %}</strong> accords-cadres, dont le montant déclaré est un plafond : il n’est jamais additionné</li>
  {%- assign md = meta.montant_hors_ac | divided_by: 100000000.0 | round | divided_by: 10.0 %}
  <li><strong>{{ md | replace: ".", "," }} Md€</strong> déclarés pour les {% include nombre-fr.html n=meta.marches_hors_ac %} autres marchés</li>
  <li><strong>{{ meta.montants_ecartes }}</strong> montants de remplissage écartés des sommes (le marché reste compté)</li>
</ul>

## Comment les chiffres sont établis

1. **Tous les fichiers mensuels sont lus**, de janvier 2025 à octobre 2026 :
   un fichier regroupe les données publiées ce mois-là, pas les marchés
   notifiés ce mois-là. Seuls restent les marchés dont la date de
   notification tombe en {{ meta.annee_notification }}.
2. **Un marché déclaré plusieurs fois est compté une fois** : même acheteur,
   même identifiant, même date de notification.
3. **Le classement se fait au nombre de marchés.** Les montants sont trop
   fragiles pour classer : valeurs de remplissage (10<sup>16</sup> €,
   999 999 999 €), plafonds d’accords-cadres recopiés à l’identique pour
   chacun de leurs attributaires.
4. **La colonne « montant déclaré » ne retient que les marchés hors
   accord-cadre**, à titulaire unique, et sans valeur de remplissage (un
   milliard d’euros ou plus, suite de 9, puissance de 10). C’est le montant
   tel que l’acheteur l’a déclaré, non vérifié.
5. **Chaque ligne est une entité juridique** (SIREN, tiré du SIRET déclaré),
   nommée d’après le répertoire Sirene. Un titulaire étranger, identifié
   autrement que par un SIRET, n’est pas classé.

## Les {{ cp.titulaires | size }} titulaires les plus fréquents

{% assign tableau = cp.titulaires %}
<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Rang</th>
      <th>Titulaire</th>
      <th>Marchés</th>
      <th>dont accords-cadres</th>
      <th>Montant déclaré hors accords-cadres</th>
    </tr>
  </thead>
  <tbody>
    {%- for l in tableau %}
    <tr>
      <td>{{ l.rang }}</td>
      <td>{{ l.nom | default: "nom non trouvé dans Sirene" }}{% if l.sigle and l.sigle != l.nom %} ({{ l.sigle }}){% endif %} <span class="meta">SIREN {{ l.siren }}</span></td>
      <td>{% include nombre-fr.html n=l.marches %}</td>
      <td>{% include nombre-fr.html n=l.accords_cadres %}</td>
      {%- assign mm = l.montant_hors_ac | divided_by: 1000000.0 | round %}
      <td>{% include nombre-fr.html n=mm %} M€</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

## Les {{ cp.acheteurs | size }} acheteurs les plus fréquents

{% assign tableau = cp.acheteurs %}
<div class="table-defilante">
<table>
  <thead>
    <tr>
      <th>Rang</th>
      <th>Acheteur</th>
      <th>Marchés</th>
      <th>dont accords-cadres</th>
      <th>Montant déclaré hors accords-cadres</th>
    </tr>
  </thead>
  <tbody>
    {%- for l in tableau %}
    <tr>
      <td>{{ l.rang }}</td>
      <td>{{ l.nom | default: "nom non trouvé dans Sirene" }}{% if l.sigle and l.sigle != l.nom %} ({{ l.sigle }}){% endif %} <span class="meta">SIREN {{ l.siren }}</span></td>
      <td>{% include nombre-fr.html n=l.marches %}</td>
      <td>{% include nombre-fr.html n=l.accords_cadres %}</td>
      {%- assign mm = l.montant_hors_ac | divided_by: 1000000.0 | round %}
      <td>{% include nombre-fr.html n=mm %} M€</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

Un acheteur centralisé, comme le Réseau des acheteurs hospitaliers, passe des
marchés pour le compte d’autres établissements : son rang mesure son rôle
d’intermédiaire, pas sa propre consommation.

## Données et sources

- Les deux classements, en tableur :
  [`ajout_commande_publique_{{ meta.annee_notification }}.csv`]({{ '/assets/donnees/ajout_commande_publique_2025.csv' | relative_url }}).
- Les données d’origine :
  [données essentielles de la commande publique, fichiers consolidés](https://www.data.gouv.fr/datasets/donnees-essentielles-de-la-commande-publique-fichiers-consolides)
  (<a href="{{ '/registre/' | relative_url }}#FR-SRC-0042"><code>FR-SRC-0042</code></a>),
  publiées par les ministères économiques et financiers. Le recensement
  économique de la commande publique en donne la vue d’ensemble
  (<a href="{{ '/registre/' | relative_url }}#FR-SRC-0041"><code>FR-SRC-0041</code></a>).
- Le calcul : `scripts/agreger-commande-publique.py`, dans le dépôt du site.
  Il se relance sur les mêmes fichiers et redonne les mêmes chiffres.
