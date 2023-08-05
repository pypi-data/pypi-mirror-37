===================
CCIAPD - Agid theme
===================

Tema Plone per la Camera di commercio di Padova conforme a `Italia design system`__.

__ https://design-italia.readthedocs.io/it/stable/index.html

Questo tema si basa sulla versione 2017.1 delle linee guida.

|

This is the first Plone theme that is compliant with the `Italia design system`__ guidelines.

__ https://design-italia.readthedocs.io/it/stable/index.html

It is built on guidelines' version 2017.1.

This README is written in italian language because it's meant for Italian Public Administration websites.


Documentazione
--------------

La documentazione per l'utente finale è disponibile in `questo documento`__.

__ https://github.com/PloneGov-IT/camcomskin.padova/blob/master/docs/manuale-camcomskin-padova.pdf


Esempi
------

Questo tema può essere visto in azione nei seguenti siti web:

- `https://www.pd.camcom.it`__

__ https://www.pd.camcom.it


Traduzioni
-----------

Questo prodotto è stato tradotto nelle seguenti lingue:

- Italiano


Installazione
-------------

Installa camcomskin.padova aggiungendolo al tuo buildout::

    [buildout]

    ...

    eggs =
        camcomskin.padova


e successivamente eseguendo ``bin/buildout``.

Al successivo avvio del sito troverete il tema disponibile tra i prodotti aggiuntivi del sito, con il nome "CCIAPD: Plone Theme".


Sviluppo
--------

Per la compilazione del codice Sass e la build del bundle JavaScript, sono presenti alcuni script nel ``package.json``:

- ``npm run develop``: esegue la compilazione con grunt e lo lascia avviato in modalità watch
- ``npm run build``: compila con grunt e esegue prettier


Compatibilità
-------------

Questo prodotto è stato testato su Plone < 5.


Riconoscimenti
--------------

Sviluppato con il supporto di `Camera di commercio di Padova`__.

__ https://www.pd.camcom.it



Autori
------

Questo prodotto è stato sviluppato dal team di RedTurtle Technology.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
