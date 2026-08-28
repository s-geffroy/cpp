# cpp

Site **Jekyll** bati par **GitHub Actions**, servi par **GitHub Pages**.
**Rien n'est heberge ici.**

## Ce que ce depot est

Un espace de travail versionne, isole des autres applications du VPS, avec son
propre Claude Code authentifie. Le site, lui, est construit par un workflow
GitHub a chaque `git push` et servi depuis les serveurs de GitHub.

`sudo appctl validate` repondra « 1 service » : c'est `bundle`, un outil range
derriere le profil Compose `cli`, qui ne tourne pas. `appctl up` repond
« aucun service declare » et sort en 0 -- `app.yaml` declare explicitement
qu'il n'y a rien a demarrer.

Si quelqu'un demande de « deployer le site ici », c'est qu'il s'est trompe de
template : `static` est celui d'un site servi par ce VPS.

## Ce template ou `github-pages` ?

Les deux publient sur GitHub Pages, et dans les deux cas publier c'est pousser.
Ils different par le **constructeur**, et **ils s'excluent** : un depot est sur
l'un ou sur l'autre, jamais sur les deux.

| | `github-pages` | `github-pages-ci` (ici) |
|---|---|---|
| Constructeur | natif, chez GitHub | `.github/workflows/pages.yml`, dans ce depot |
| Settings > Pages | *Deploy from a branch* | **GitHub Actions** |
| Jekyll | 3.10, impose | celui du `Gemfile` |
| Greffons | liste blanche seule | libres ; `_plugins/` charge |
| Versions | subies | figees par `Gemfile.lock`, **a maintenir** |
| Build local | deconseille (deux verites) | legitime (meme lock que le runner) |

Prendre `github-pages` par defaut. Prendre celui-ci quand on sait pourquoi :
Jekyll 4, un greffon hors liste blanche, ou une etape a inserer autour du build.

## Prerequis, a trancher AVANT de creer le depot distant

GitHub Pages est disponible :

- sur un depot **public**, avec un compte **GitHub Free** ;
- sur un depot **prive**, seulement a partir de **GitHub Pro** (payant).

Et dans les deux cas, **le site publie est public**. Un depot prive protege les
sources, pas le site. Restreindre l'acces au site lui-meme demande une
organisation sur GitHub Enterprise Cloud.

C'est a decider avant l'etape « Rattacher un depot GitHub prive ? » de
`workon new` : apres, le depot existe.

## Activer Pages

1. Creer le depot sur GitHub, y pousser ce projet.
2. Depot > **Settings** > **Pages**.
3. **Source** : **GitHub Actions**.

Il n'y a pas de branche ni de dossier a choisir : c'est le workflow qui publie.

**Ce reglage est manuel et rien ne le fait a votre place.** Tant qu'il est reste
sur *Deploy from a branch*, le workflow tourne, produit son artefact, et echoue
a la derniere etape sur une erreur d'API -- pendant que le constructeur natif
publie un site bati autrement.

## Publier

```bash
git add -A
git commit -m "..."
git push
```

C'est tout. La construction prend une a deux minutes ; son deroulement et ses
echecs sont dans l'onglet **Actions** du depot.

## Les versions du site

`Gemfile` decide, `Gemfile.lock` fige. **Le lock est versionne** : le workflow
s'appuie dessus (`bundler-cache`), et sans lui chaque push resoudrait des
versions differentes.

Apres toute modification du `Gemfile` :

```bash
sudo appctl run bundle bundle lock
git add Gemfile Gemfile.lock && git commit -m "..."
```

Le conteneur `bundle` a la meme architecture que le runner GitHub : le lock
produit ici porte les plateformes dont le runner a besoin. Si la construction
echoue un jour en reclamant une plateforme absente du lock, l'ajouter
explicitement -- `bundle lock --add-platform x86_64-linux`.

Le `ruby-version` du workflow et le tag de l'image du service `bundle` doivent
rester **identiques** : c'est ce qui garantit qu'une construction locale et une
construction sur le runner donnent le meme site.

## Construire ou previsualiser en local

```bash
sudo appctl run bundle bundle install
sudo appctl run bundle bundle exec jekyll build
```

La sortie va dans `_site/`, gitignore. Le seul ecart avec le site publie est le
`baseurl` : le workflow le passe en ligne de commande d'apres les reglages reels
du depot, la construction locale prend celui de `_config.yml`.

La construction affiche des **avertissements de depreciation Sass** venant de
`minima` 2.5, qui n'a pas suivi le passage de Jekyll 4 a dart-sass. Ils sont
sans effet sur le site produit. Ils disparaitront en changeant de theme -- ce
qui est libre ici, contrairement au constructeur natif.

## Organisation

```
.github/workflows/pages.yml   construction et publication
Gemfile, Gemfile.lock         versions du site (le lock est versionne)
_config.yml                   reglages du site (titre, url, baseurl, exclusions)
index.md                      page d'accueil
404.html                      page servie sur une adresse inconnue
_posts/                       articles : AAAA-MM-JJ-titre.md
_drafts/                      brouillons : jamais publies (a creer au besoin)
_plugins/                     greffons Ruby, reellement charges (a creer au besoin)
assets/                       images, fichiers joints
specs/                        specifications du projet, exclues du site
```

Un article porte un front matter :

```markdown
---
layout: post
title: "Titre de l'article"
date: 2026-08-25
categories: [notes]
---
```

## Domaine personnalise

Saisir le domaine dans **Settings > Pages** : GitHub cree lui-meme le commit du
fichier `CNAME`. Cote DNS, chez le registrar :

- apex (`exemple.fr`) : quatre enregistrements **A** vers `185.199.108.153`,
  `185.199.109.153`, `185.199.110.153`, `185.199.111.153` ;
- sous-domaine (`www`) : un **CNAME** vers `<utilisateur>.github.io`.

Puis cocher **Enforce HTTPS** -- disponible jusqu'a 24 h apres la
configuration, le temps que le certificat soit emis.

**Rien de tout cela ne passe par ce VPS** : ni Traefik, ni `app.yaml`, ni
`app-exposure.py`, ni la zone publique de `/opt/infra/.env`.

Le `baseurl` de `_config.yml` ne sert qu'a la construction locale : le workflow
lit la valeur reelle dans les reglages du depot. Le mettre a jour reste utile
pour que l'apercu local ressemble au site.

## Commandes

`sudo appctl validate` repond « 1 service » : le profil `cli` est valide aussi.
`build`, `up`, `down`, `rebuild` et `restart` sortent en 0 sans rien faire. Le
service `bundle` se lance a la demande : `sudo appctl run bundle <commande>`.
