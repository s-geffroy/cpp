# Les versions du site, choisies ici plutot que subies.
#
# C'est la difference avec le template 'github-pages' : le constructeur natif de
# GitHub Pages impose Jekyll 3.10, le safe mode et sa liste blanche de greffons.
# Ici, ce fichier decide -- et Gemfile.lock, versionne a cote, fige le resultat
# exact de la resolution.
#
# TOUTE MODIFICATION DE CE FICHIER DEMANDE DE REGENERER LE LOCK :
#
#   sudo appctl run bundle bundle lock
#
# Sans quoi le workflow echoue au `bundle install`, avec un message qui parle de
# Gemfile.lock desynchronise et non de la ligne qu'on vient d'ajouter.
source "https://rubygems.org"

# Jekyll 4, pas 3.10. Les recettes du web qui supposent Jekyll 4 -- convertisseur
# Sass moderne, options de collections -- marchent ici.
gem "jekyll", "~> 4.4"

# Le theme. Il est copie depuis rubygems, pas 'remote_theme' : ici il n'y a plus
# de liste blanche a contourner.
gem "minima", "~> 2.5"

# Les greffons. Ceux-ci se trouvaient deja dans la liste blanche du constructeur
# natif ; la difference est qu'on peut desormais en ajouter d'autres, y compris
# des greffons qui n'y figurent pas, et deposer du code dans `_plugins/`.
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
end

# Ruby 3 ne fournit plus webrick dans sa bibliotheque standard, et
# `jekyll serve` s'en sert. Sans cette ligne, la construction passe et seule la
# previsualisation locale echoue -- avec un message qui ne dit pas pourquoi.
gem "webrick", "~> 1.9"
