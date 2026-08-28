/*
 * Bouton clair / sombre.
 *
 * Trois etats, et non deux : Systeme -> Clair -> Sombre -> Systeme. Un simple
 * inverseur ferait perdre « suivre le systeme » des le premier clic, alors
 * que c'est le reglage par defaut et le meilleur pour la plupart des gens.
 *
 * Le bouton est CREE PAR CE SCRIPT et n'existe pas dans le balisage. Sans
 * JavaScript il ne servirait a rien : plutot que de laisser un bouton mort
 * dans la page, on ne l'affiche pas, et la feuille de style continue de
 * suivre le reglage du systeme.
 *
 * L'application du choix au chargement n'est PAS ici : elle est dans un
 * script inline du <head>, sans quoi la page apparaitrait brievement dans le
 * mauvais theme avant de basculer.
 */
(function () {
  'use strict';

  var CLE = 'theme';
  var ETATS = ['systeme', 'clair', 'sombre'];

  var LIBELLES = {
    systeme: 'Thème : système',
    clair: 'Thème : clair',
    sombre: 'Thème : sombre'
  };

  // Couleur de la barre d'adresse sur mobile, alignee sur --fond.
  var FONDS = { clair: '#ffffff', sombre: '#0d1117' };

  function lire() {
    try {
      var v = localStorage.getItem(CLE);
      return ETATS.indexOf(v) > 0 ? v : 'systeme';
    } catch (e) {
      return 'systeme';
    }
  }

  function ecrire(etat) {
    try {
      if (etat === 'systeme') localStorage.removeItem(CLE);
      else localStorage.setItem(CLE, etat);
    } catch (e) {
      /* Stockage refuse : le choix vaut pour la page en cours, sans plus. */
    }
  }

  function systemeEstSombre() {
    return window.matchMedia &&
           window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function appliquer(etat, bouton) {
    var racine = document.documentElement;

    if (etat === 'systeme') racine.removeAttribute('data-theme');
    else racine.setAttribute('data-theme', etat);

    var effectif = etat === 'systeme'
      ? (systemeEstSombre() ? 'sombre' : 'clair')
      : etat;

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', FONDS[effectif]);

    if (bouton) {
      bouton.textContent = LIBELLES[etat];
      // Le nom accessible annonce l'etat ET ce que le clic fera : un bouton
      // dont le libelle change doit dire les deux.
      var suivant = ETATS[(ETATS.indexOf(etat) + 1) % ETATS.length];
      bouton.setAttribute(
        'aria-label',
        LIBELLES[etat] + '. Basculer vers : ' + LIBELLES[suivant].toLowerCase() + '.'
      );
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var ancre = document.querySelector('.site-header .wrapper');
    if (!ancre) return;

    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.className = 'bascule-theme';

    var etat = lire();
    appliquer(etat, bouton);

    bouton.addEventListener('click', function () {
      etat = ETATS[(ETATS.indexOf(etat) + 1) % ETATS.length];
      ecrire(etat);
      appliquer(etat, bouton);
    });

    ancre.appendChild(bouton);

    // Tant que le lecteur est sur « systeme », suivre les changements de
    // reglage a chaud -- bascule automatique jour/nuit, par exemple.
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var surChangement = function () {
        if (etat === 'systeme') appliquer(etat, bouton);
      };
      if (mq.addEventListener) mq.addEventListener('change', surChangement);
      else if (mq.addListener) mq.addListener(surChangement);
    }
  });
})();
