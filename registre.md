---
layout: page
title: Registre
permalink: /registre/
---

Les **{{ site.data.registre | size }} sources canoniques** du paquet, arrêtées
au {% include date-snapshot.html %}. Toutes portent le statut *vérifiée*.

L'ordre de priorité qui gouverne leur admission est fixé par la
[méthode]({{ '/methode/' | relative_url }}) : textes juridiques et registres
officiels d'abord, presse en dernier et seulement pour repérer un événement ou
à défaut de preuve primaire.

{% comment %}
  PIEGE KRAMDOWN, deja rencontre sur la page de couverture.

  Les deux tags assign ci-dessous s'ecrivent SANS tirets de rognage. Un tiret
  accole aux accolades supprime les sauts de ligne qui entourent le tag ; le
  div suivant se retrouve alors colle au paragraphe precedent, kramdown le lit
  comme du texte et l'echappe. L'attribut data-filtre-groupe disparait du DOM
  et les filtres cessent de fonctionner, sans erreur de construction.

  Et ne PAS ecrire de delimiteurs Liquid litteraux dans ce commentaire :
  Liquid les tokenise malgre le commentaire, et un tiret de rognage ecrit ici
  rogne pour de vrai -- c'est exactement ce qui a casse cette page.
{% endcomment %}
{% assign registre = site.data.registre %}
{% assign lib = site.data.libelles %}

<div class="filtres" data-filtre-groupe="registre">
  <label>
    Rechercher
    <input type="search" data-filtre-recherche placeholder="institution, titre, usage…">
  </label>

  {%- comment -%}
    Les listes deroulantes sont construites depuis les donnees, jamais ecrites
    a la main : une source ajoutee en v0.2 apparait sans toucher a cette page.
    Le tri se fait sur le libelle francais, d'ou le detour par « libelle|cle ».
  {%- endcomment -%}

  {%- assign cles_domaines = registre | map: "domain" | uniq -%}
  {%- capture brut -%}{%- for c in cles_domaines -%}{{ lib.domaines[c] }}|{{ c }};;{%- endfor -%}{%- endcapture -%}
  <label>
    Domaine
    <select data-filtre-champ="domaine">
      <option value="">tous les domaines</option>
      {%- assign paires = brut | split: ";;" | sort -%}
      {%- for p in paires -%}{%- assign kv = p | split: "|" -%}
      <option value="{{ kv[1] }}">{{ kv[0] }}</option>
      {%- endfor -%}
    </select>
  </label>

  {%- assign cles_autorites = registre | map: "authority" | uniq -%}
  {%- capture brut -%}{%- for c in cles_autorites -%}{{ lib.autorites[c] }}|{{ c }};;{%- endfor -%}{%- endcapture -%}
  <label>
    Autorité
    <select data-filtre-champ="autorite">
      <option value="">toutes les autorités</option>
      {%- assign paires = brut | split: ";;" | sort -%}
      {%- for p in paires -%}{%- assign kv = p | split: "|" -%}
      <option value="{{ kv[1] }}">{{ kv[0] }}</option>
      {%- endfor -%}
    </select>
  </label>

  <label>
    Priorité
    <select data-filtre-champ="priorite">
      <option value="">A0 et A1</option>
      {%- assign priorites = registre | map: "priority" | uniq | sort -%}
      {%- for p in priorites -%}
      <option value="{{ p }}">{{ p }}</option>
      {%- endfor -%}
    </select>
  </label>

  <p class="compteur" data-filtre-compteur
     data-total="{{ registre | size }}"
     data-nom="sources">{{ registre | size }} sources</p>
</div>

<div class="table-defilante">
<table data-filtre-cible="registre">
  <thead>
    <tr>
      <th>Identifiant</th>
      <th>Domaine</th>
      <th>Institution</th>
      <th>Source</th>
      <th>Autorité</th>
      <th>Mise à jour</th>
    </tr>
  </thead>
  <tbody>
    {%- for s in registre %}
    {%- comment -%}
      Tout le texte cherchable est concatene une fois ici, en minuscules : le
      JS compare des chaines deja pretes plutot que de fouiller le DOM.
    {%- endcomment -%}
    {%- capture cherchable -%}
      {{ s.source_id }} {{ s.institution }} {{ s.title }} {{ s.use }} {{ s.notes }}
      {{ lib.domaines[s.domain] }} {{ lib.autorites[s.authority] }}
      {{ lib.types_source[s.source_type] }} {{ s.power_dimensions }}
    {%- endcapture -%}
    <tr id="{{ s.source_id }}"
        data-domaine="{{ s.domain }}"
        data-autorite="{{ s.authority }}"
        data-priorite="{{ s.priority }}"
        data-recherche="{{ cherchable | normalize_whitespace | downcase | escape }}">
      <td class="nowrap">
        <code>{{ s.source_id }}</code>
        <span class="pastille priorite-{{ s.priority | downcase }}">{{ s.priority }}</span>
      </td>
      <td>{{ lib.domaines[s.domain] }}</td>
      <td>{{ s.institution }}</td>
      <td>
        <a href="{{ s.url }}" rel="noopener">{{ s.title }}</a>
        <span class="meta">{{ lib.types_source[s.source_type] }}</span>
        {%- if s.use %}<span class="usage">{{ s.use }}</span>{% endif -%}
        {%- if s.notes %}<span class="note">{{ s.notes }}</span>{% endif -%}
        {%- if s.power_dimensions %}<span class="mots-cles">{{ s.mots_cles | join: " · " }}</span>{% endif -%}
      </td>
      <td>{{ lib.autorites[s.authority] }}</td>
      <td class="nowrap">{{ lib.rafraichissements[s.refresh] }}</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
</div>

<p class="sans-js">Les filtres ci-dessus demandent JavaScript. Sans lui, la
table reste entière et lisible : c'est du filtrage, pas du chargement.</p>

## Sur les mots-clés affichés sous chaque source

Le champ `power_dimensions` du registre est en **texte libre** :
{{ registre | map: "power_dimensions" | join: ";" | split: ";" | uniq | size }}
mots-clés distincts, propres au registre. Ce ne sont **pas** les
[{{ site.data.dimensions | size }} dimensions de pouvoir]({{ '/dimensions/' | relative_url }}),
qui forment un vocabulaire fermé utilisé par la carte du système.

Le paquet v0.1 ne fournit aucune table de correspondance entre les deux. Ce
site n'en invente pas : les mots-clés sont affichés tels quels, et l'écart est
[porté à la feuille de route]({{ '/feuille-de-route/' | relative_url }}).
