---
layout: page
title: Méthode
permalink: /methode/
---

Les trois documents de méthode du paquet, traduits. Ils fixent ce qui entre
dans le registre, comment le système est découpé, et ce qu’on a le droit de
conclure d’une relation entre deux entreprises.

Les versions d’origine, en anglais, sont dans l’archive
[téléchargeable]({{ '/donnees/' | relative_url }}).

- [Admission des sources](#admission)
- [Cartographie du système](#cartographie)
- [Règles du graphe des entreprises](#graphe)

## Admission des sources {#admission}

### Ordre de priorité

1. Textes juridiques et registres officiels.
2. Statistiques officielles et jeux de données des régulateurs.
3. Documents d’entreprise audités et informations réglementées AMF.
4. Enquêtes parlementaires et pièces judiciaires.
5. Recherche indépendante de qualité, pour combler les lacunes.
6. Presse **uniquement** pour repérer un événement, ou lorsqu’aucune preuve
   primaire n’est disponible.

### Règle de date

Le snapshot est le **{% include date-snapshot.html %}**. Toute information
postérieure est exclue de la v0.1. Aucun document, changement de propriété,
nomination, décision publique, observation de part de marché ou évolution
institutionnelle survenu après cette date n’entre dans le snapshot sans une
nouvelle version.

### Provenance des entreprises

Pour chaque groupe, la chaîne à établir est :

> entité juridique → filiales → détention → droits de vote → gouvernance →
> financement → marchés publics → subventions → régulation → infrastructures →
> médias et actifs

**Le bénéficiaire effectif ultime ne se devine pas** lorsque le registre des
bénéficiaires effectifs de l’INPI est inaccessible.

### Provenance des médias

Cinq couches à ne jamais confondre :

> capital → droits de vote et de contrôle → gouvernance éditoriale → audience →
> distribution → publicité → plateformes et algorithmes → sources primaires et
> agences

**La propriété ne prouve jamais l’intervention éditoriale.**

### Provenance des personnes et des réseaux

Un administrateur commun, un emploi passé, une relation d’école ou une
appartenance ne créent qu’une **arête de réseau**. Elle ne devient
`coordination`, `conflit`, `capture` ou `influence` qu’avec une preuve
indépendante.

## Cartographie du système {#cartographie}

### L’objet

L’objet n’est pas « l'État français ». C’est **France-System-2026** :

> acteurs → ressources → dépendances → relations → décisions → coercition →
> influence → bénéficiaires et perdants → contre-pouvoirs

### Le pouvoir est multidimensionnel

Les {{ site.data.dimensions | size }} dimensions ne doivent jamais être
réduites à une variable unique. Elles sont détaillées, avec les nœuds et les
arêtes qui les portent, sur la
[page des dimensions]({{ '/dimensions/' | relative_url }}).

### Les douze règles dures

1. **Dépense publique ≠ contrôle étatique.**
2. **Propriété publique ≠ régulation ≠ commande publique ≠ subvention.**
3. **Concentration du marché ≠ domination**, sauf à établir indépendamment la
   contestabilité du marché et le contrôle effectif.
4. **Proximité dans le réseau ≠ coordination ou entente.**
5. **Contact de représentation d’intérêts ≠ capture.**
6. **Financement public d’un média ≠ contrôle éditorial gouvernemental.**
7. **Pouvoir de distribution d’une plateforme ≠ propriété d’un média.**
8. **Capacité réglementaire ≠ intention politique.**
9. **Financement élevé de la santé et du social ≠ propriété des offreurs de
   soins.**
10. **Les contraintes de l’Union, de la BCE et de la CEDH s’imputent au niveau
    supranational**, pas à l’exécutif français.
11. **Aucune observation locale ou sectorielle n’est extrapolée au niveau
    national** sans preuve de représentativité.
12. Toute affirmation causale forte exige un mécanisme documenté et l’examen
    des explications alternatives.

### Statuts de preuve

| Statut | Ce qu’il signifie |
|---|---|
| `P4` | Preuve officielle ou primaire directe |
| `P3` | Preuve forte et corroborée |
| `P2` | Probable |
| `P1` | Plausible ou contesté |
| `P0` | Non prouvé |

Une arête établie par la seule proximité ou une appartenance commune **ne peut
pas être requalifiée en coordination** sans preuve indépendante.

### Architecture du graphe

**Nœuds** : institutions formelles, régulateurs, entreprises publiques,
entreprises privées, banques, assureurs, médias, plateformes, opérateurs
d’infrastructures, partenaires sociaux, institutions d’expertise, société
civile, institutions extérieures.

**Arêtes** : propriété, nomination, financement budgétaire, commande publique,
subvention, crédit, assurance, régulation, autorisation, contrôle
juridictionnel, représentation d’intérêts, négociation collective, distribution
de l’information, classement algorithmique, mobilité des personnes, apport
d’expertise, contrainte supranationale.

## Règles du graphe des entreprises {#graphe}

### Identifiants exigés

SIREN ou SIRET, LEI, EUID, identifiant émetteur AMF, ou toute clé de registre
officiel.

### Propriété

À conserver pour chaque lien : pourcentage de détention directe, pourcentage
de droits de vote, statut de contrôle, date, source, incertitude.

**Le contrôle ultime ne se déduit pas de la marque.**

### Dépendance financière

Six canaux à garder distincts, jamais agrégés : crédit bancaire, obligations,
capital, garanties publiques, subventions, chiffre d’affaires issu de la
commande publique, assurance et réassurance, clients et fournisseurs majeurs,
accès aux réseaux régulés.

### Pouvoir de marché

Parts de marché, indice HHI, barrières à l’entrée et substituabilité,
**lorsque des données officielles existent**. Un chiffre d’affaires élevé n’est
pas, à lui seul, un pouvoir de marché.

### Coordination entre l'État et les entreprises

Cinq relations à coder séparément :

- État → entreprise : direction ;
- entreprise → État : influence ;
- dépendance mutuelle ;
- coordination collective formalisée ;
- capture réglementaire — **uniquement si elle est établie de façon
  indépendante**.

### Le test du corporatisme

Qualifier un système de corporatiste exige les **quatre** conditions
réunies :

1. représentation des intérêts institutionnalisée ;
2. relation structurée à la décision publique ;
3. rôle effectif dans la décision ou dans sa mise en œuvre ;
4. autonomie mesurée des organisations représentées.

L’existence de syndicats, de fédérations patronales, d’une régulation ou de
grandes entreprises **ne suffit pas**.
