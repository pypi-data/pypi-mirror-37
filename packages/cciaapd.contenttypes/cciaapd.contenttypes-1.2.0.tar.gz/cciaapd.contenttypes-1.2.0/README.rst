.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
CCIAAPD content-types
==============================================================================

Adds two new content-types:

- Scheda
- Ufficio

These two types has additional fields that helps editors to expose specific informations
in a structured way.

Scheda type could also add some special folders into it, to better organize informations:

- Archivio (archive)
- Moduli (modules)
- Riferimenti (references)
 
There are also new portlets that can show these informations inside a Scheda.

Examples
--------

This add-on can be seen in action on `Camera di commercio di Padova` websiste:

- `A list of Uffici`__
- `A list of Schede`__

__ https://www.pd.camcom.it/camera-commercio/contatti-PEC
__ https://www.pd.camcom.it/tutela-impresa-e-consumatore


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install cciaapd.contenttypes by adding it to your buildout::

   [buildout]

    ...

    eggs =
        cciaapd.contenttypes


and then running "bin/buildout"


Contribute
----------

- Issue Tracker: https://github.com/PloneGov-IT/cciaapd.contenttypes/issues
- Source Code: https://github.com/PloneGov-IT/cciaapd.contenttypes/

Credits
-------

Developed with the support of `Camera di Commercio di Padova`__;
Camera di Commercio di Ferrara supports the `PloneGov initiative`__.

.. image:: https://www.pd.camcom.it/logo.png
   :alt: CCIAA Padova - logo

__ https://www.pd.camcom.it
__ http://www.plonegov.it/

Authors
-------

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
