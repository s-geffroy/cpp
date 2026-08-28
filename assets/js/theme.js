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

  /*
   * Icones tracees au trait, en currentColor : elles suivent la couleur du
   * bouton, donc le theme, sans seconde version a maintenir.
   *
   * Trois icones et non deux. « Soleil » et « lune » disent le theme force ;
   * l'ecran dit « je suis le reglage du systeme », etat par defaut qu'un
   * simple inverseur soleil/lune ferait disparaitre au premier clic.
   */
  var DEBUT = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" ' +
              'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
              'stroke-linejoin="round" aria-hidden="true" focusable="false">';

  var ICONES = {
    clair: DEBUT +
      '<circle cx="12" cy="12" r="4.2"/>' +
      '<path d="M12 2v2M12 20v2M2 12h2M20 12h2' +
      'M4.9 4.9l1.5 1.5M17.6 17.6l1.5 1.5' +
      'M19.1 4.9l-1.5 1.5M6.4 17.6l-1.5 1.5"/>' +
      '</svg>',

    sombre: DEBUT +
      '<path d="M20.5 14.6A8.5 8.5 0 0 1 9.4 3.5a8.5 8.5 0 1 0 11.1 11.1z"/>' +
      '</svg>',

    systeme: DEBUT +
      '<rect x="2.5" y="4" width="19" height="13" rx="2"/>' +
      '<path d="M9 20.5h6M12 17.5v3"/>' +
      '</svg>'
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
      bouton.innerHTML = ICONES[etat];

      // L'icone est purement visuelle (aria-hidden) : sans nom accessible, le
      // bouton serait annonce « bouton » et rien d'autre. Le nom dit donc
      // l'etat ET ce que le clic fera.
      var suivant = ETATS[(ETATS.indexOf(etat) + 1) % ETATS.length];
      var nom = LIBELLES[etat] + '. Basculer vers : ' +
                LIBELLES[suivant].toLowerCase() + '.';
      bouton.setAttribute('aria-label', nom);
      bouton.setAttribute('title', LIBELLES[etat]);
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
