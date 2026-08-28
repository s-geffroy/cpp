/*
 * Filtrage cote client des tables du site.
 *
 * CE SCRIPT NE CHARGE RIEN. Les lignes sont deja dans la page, rendues par
 * Jekyll ; il ne fait que les masquer. Sans JavaScript, la table reste
 * entiere et lisible -- c'est la raison de ce choix plutot qu'un rendu
 * dynamique.
 *
 * Convention de balisage :
 *   <div data-filtre-groupe="registre">        conteneur des controles
 *     <input data-filtre-recherche>            recherche plein texte
 *     <select data-filtre-champ="domaine">     filtre sur data-domaine
 *     <p data-filtre-compteur data-total="53" data-nom="sources">
 *   <table data-filtre-cible="registre">       meme nom de groupe
 *     <tr data-recherche="..." data-domaine="...">
 *
 * Les lignes filtrables sont reperees par leur attribut data-recherche, ce
 * qui marche aussi bien sur des <tr> que sur des <article>.
 */
(function () {
  'use strict';

  // Retire les accents : chercher « energie » doit trouver « Énergie ».
  function aplatir(texte) {
    return texte
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  function installer(controles) {
    var groupe = controles.getAttribute('data-filtre-groupe');
    var cible = document.querySelector('[data-filtre-cible="' + groupe + '"]');
    if (!cible) return;

    var lignes = Array.prototype.slice.call(cible.querySelectorAll('[data-recherche]'));
    var recherche = controles.querySelector('[data-filtre-recherche]');
    var selects = Array.prototype.slice.call(controles.querySelectorAll('[data-filtre-champ]'));
    var compteur = controles.querySelector('[data-filtre-compteur]');

    // Index prepare une fois : on ne retouche pas au DOM a chaque frappe.
    var index = lignes.map(function (ligne) {
      return { ligne: ligne, texte: aplatir(ligne.getAttribute('data-recherche') || '') };
    });

    function appliquer() {
      var terme = recherche ? aplatir(recherche.value.trim()) : '';
      var visibles = 0;

      index.forEach(function (entree) {
        var garde = terme === '' || entree.texte.indexOf(terme) !== -1;

        if (garde) {
          for (var i = 0; i < selects.length; i++) {
            var attendu = selects[i].value;
            if (attendu === '') continue;
            var champ = selects[i].getAttribute('data-filtre-champ');
            var valeur = entree.ligne.getAttribute('data-' + champ) || '';
            // Un champ multivalue (« P-EXEC P-LEGAL ») est teste par mot
            // entier : sans cela, « P-EXT » repondrait a « P-EX ».
            if (valeur.split(' ').indexOf(attendu) === -1) {
              garde = false;
              break;
            }
          }
        }

        entree.ligne.hidden = !garde;
        if (garde) visibles++;
      });

      if (compteur) {
        var total = compteur.getAttribute('data-total');
        var nom = compteur.getAttribute('data-nom') || 'lignes';
        compteur.textContent = visibles === Number(total)
          ? total + ' ' + nom
          : visibles + ' ' + nom + ' sur ' + total;
      }
    }

    if (recherche) recherche.addEventListener('input', appliquer);
    selects.forEach(function (s) { s.addEventListener('change', appliquer); });

    // Un rechargement peut restaurer les valeurs saisies : on part de l'etat
    // reel des controles, pas d'un etat suppose vierge.
    appliquer();
  }

  document.addEventListener('DOMContentLoaded', function () {
    Array.prototype.slice
      .call(document.querySelectorAll('[data-filtre-groupe]'))
      .forEach(installer);

    // L'avertissement « les filtres demandent JavaScript » ne concerne plus
    // personne a partir d'ici : c'est le script lui-meme qui le retire.
    Array.prototype.slice
      .call(document.querySelectorAll('.sans-js'))
      .forEach(function (p) { p.hidden = true; });
  });
})();
