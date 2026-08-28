# Regles du projet cpp

Ce fichier est lu par Claude Code au demarrage. Il fixe les regles non
negociables de ce projet sur ce VPS.

## Ce projet n'heberge rien

Le site est un **Jekyll bati par GitHub Actions** et servi par GitHub Pages.
Ici, il n'y a ni conteneur qui tourne, ni base, ni URL a verifier.
`sudo appctl validate` repondra « 1 service » : c'est `bundle`, range derriere
le profil `cli`, qui ne tourne pas. `appctl up` repond « aucun service
declare » et sort en 0.

Ce que ce repertoire apporte : un espace de travail versionne, isole des autres
applications du VPS, avec son propre Claude Code authentifie.

Si quelqu'un demande de « deployer le site ici », c'est qu'il s'est trompe de
template : `static` est celui d'un site servi par ce VPS.

## Publier, c'est pousser

Le geste ne change pas : `git push`, et le site part. Ce qui change par rapport
au template `github-pages`, c'est le constructeur -- ce n'est plus celui de
GitHub Pages, c'est `.github/workflows/pages.yml`, dans ce depot.

Il n'y a donc **pas** de `appctl up` a lancer, pas de build a declencher a la
main.

## Le reglage qui conditionne tout

Le workflow ne publie que si le depot est regle sur :

**Settings > Pages > Source : GitHub Actions.**

- Ce reglage est **manuel**. Aucun push ne le fait a votre place.
- Tant qu'il est reste sur « Deploy from a branch », le workflow s'execute,
  produit son artefact, et **echoue a la derniere etape** avec une erreur d'API
  -- pendant que le constructeur natif, lui, continue de publier un site bati
  autrement. Deux constructeurs, deux resultats.
- **Ne rebascule jamais Settings > Pages sur « Deploy from a branch ».** Le
  workflow deviendrait muet : il tournerait toujours, en vert, sans que rien de
  ce qu'il produit n'atteigne le site.

Si le workflow echoue, le message est dans l'onglet **Actions** du depot. Va le
lire avant de toucher au contenu.

## Le projet est responsable de ses versions

C'est la contrepartie de ce template, et elle n'est pas negociable.

- `Gemfile` decide des versions, `Gemfile.lock` les fige. **Le lock est
  versionne** : sans lui, chaque push resoudrait des versions differentes.
- **Toute modification du `Gemfile` demande de regenerer le lock**, sinon le
  workflow echoue au `bundle install` :

  ```
  sudo appctl run bundle bundle lock
  ```

  Le conteneur `bundle` a la meme architecture que le runner GitHub : le lock
  produit ici porte donc les plateformes dont le runner a besoin. Si un jour la
  construction echoue en reclamant une plateforme absente du lock, l'ajouter
  explicitement -- `bundle lock --add-platform x86_64-linux`.
- Le `ruby-version` du workflow et le tag de l'image du service `bundle`
  (`compose.yaml`) doivent rester **identiques**. Changer l'un sans l'autre,
  c'est reintroduire deux verites.
- Ajouter un greffon est permis -- il n'y a plus de liste blanche, et
  `_plugins/` est reellement charge. Mais chaque ajout entre dans le `Gemfile`,
  passe par le lock, et devient quelque chose a maintenir. Dis-le quand tu en
  ajoutes un.

## Construire en local est legitime ici

Contrairement au template `github-pages`, la construction locale ne cree pas
une seconde verite : elle lit le **meme `Gemfile.lock`** que le runner.

```
sudo appctl run bundle bundle install
sudo appctl run bundle bundle exec jekyll build
```

La sortie va dans `_site/`, qui est gitignore. Le seul ecart avec le site
publie est le `baseurl` : le workflow le passe en ligne de commande d'apres les
reglages reels du depot, la construction locale prend celui de `_config.yml`.

## Le site est en ligne

Chaque push est une publication immediate et publique.

- **Travaille en brouillon dans `_drafts/`** : Jekyll ne les publie pas. Un
  article n'entre dans `_posts/` que quand il est pret.
- Aucune **suppression** de page existante, aucune **refonte de structure**
  -- permaliens, categories, arborescence -- sans demande explicite. Une URL
  qui disparait laisse des liens morts partout ailleurs.
- Avant toute modification en masse -- retag, recategorisation, reecriture de
  metadonnees, passage sur les images -- annonce le nombre d'elements touches
  et attends l'accord.

## Ecrire le contenu

- Les articles vont dans `_posts/`, nommes `AAAA-MM-JJ-titre.md`. **Le nom du
  fichier n'est pas decoratif** : Jekyll en tire la date et l'URL de l'article.
- Front matter obligatoire : `layout`, `title`, `date`, et `categories` si le
  site en utilise.
- **Le contenu publie s'ecrit en francais normal, avec ses accents.** La regle
  « sans accents » de ce depot vise les fichiers d'infrastructure
  -- `CLAUDE.md`, `README.md`, les YAML -- pas ce que liront les visiteurs.
- Sur un site existant, commence par le lire : articles recents, categories
  reellement utilisees, ton employe, gabarits de titres. Aligne-toi dessus
  plutot que d'imposer une nouvelle mise en forme.

## Perimetre

- Travaille uniquement dans /srv/apps/cpp.
- Ne touche jamais a /opt/infra.
- Ne tente jamais d'acceder aux autres applications du VPS.
- N'installe aucun runtime sur l'hote : ni Ruby, ni Jekyll, ni Bundler. Ils
  tournent dans le conteneur `bundle`, lance par `sudo appctl run`.
- Ne touche a rien dans `~/.claude/` : ce qui s'y trouve est pose par le socle
  du VPS.

## Interdictions

- N'ajoute aucun service **qui tourne** dans `compose.yaml` sans demande
  explicite. Le service `bundle` est un outil derriere le profil `cli` : il ne
  tourne pas, il est lance le temps d'une commande.
- Ne commite pas `_site/`, `vendor/` ni `.bundlecache/` : c'est de la sortie et
  du cache, ils se refabriquent.
- **Ne cree pas le fichier `CNAME` avant que le DNS resolve.** GitHub sert
  alors une erreur a la place du site. Le bon geste est de saisir le domaine
  dans Settings > Pages : GitHub cree le commit lui-meme, une fois le DNS
  verifie.
- Ne retire pas les entrees de `exclude:` dans `_config.yml` : sans elles,
  `CLAUDE.md`, `app.yaml` et `compose.yaml` sont publies sur le site.
- N'ajoute pas de secret au workflow. Le `GITHUB_TOKEN` suffit a publier ; un
  workflow qui reclame un jeton personnel est un workflow a relire.
- Le domaine du site ne passe **pas** par Traefik. Ne cherche ni `app.yaml`, ni
  `app-exposure.py`, ni la zone publique du VPS : ils ne servent a rien ici.

## Secrets

- Aucun jeton, mot de passe ou URL d'administration dans le depot, dans un
  prompt ou dans les logs. Un depot Pages est souvent public : ce qui y entre
  est definitif, l'historique le garde.
- Rien a mettre dans /etc/app-secrets/cpp/ : ce repertoire sert a injecter
  des secrets dans des conteneurs qui tournent, et il n'y en a pas ici.
- Un depot prive ne rend pas le site prive. Le site publie reste public.

## Fin de tache

1. relire le front matter des fichiers touches -- une date ou un `layout`
   errone fait disparaitre une page sans message d'erreur ;
2. si le `Gemfile` a bouge : regenerer `Gemfile.lock` et le committer avec ;
3. `git add` + `git commit` ;
4. `git push` -- **c'est cela, la publication**, dis-le clairement ;
5. donner l'URL des pages touchees ;
6. rappeler que la construction prend une a deux minutes, et que son deroulement
   comme ses echecs sont dans l'onglet **Actions** du depot ;
7. signaler tout echec restant sans le masquer.
