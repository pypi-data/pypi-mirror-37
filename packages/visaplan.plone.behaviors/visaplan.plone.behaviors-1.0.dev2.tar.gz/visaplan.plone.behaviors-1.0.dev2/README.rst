.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

========================
visaplan.plone.behaviors
========================

Interfaces and behaviors for a family of datatypes,
based on zope.schema and Dexterity.


Features
--------

Interfaces / behaviors
~~~~~~~~~~~~~~~~~~~~~~

IHeightAndWidth
        Provides the integer fields ``height`` and ``width``

ICaptionAndLegend
        Provides the text fields ``caption`` and ``legend``
        (e.g. for image types)

IExcludeFromSearch
        Provides a boolean field ``excludeFromSearch``, aimed for
        selective exclusion of objects from standard catalog searches

IHierarchicalBuzzword
        **This is quite incomplete;**
        the provided ASCIILine field ``code`` is aimed for the implementation
        of a hierarchical buzzword index.
        The vocabulary is still to be implemented;
        the factory of this behavior will likely be (re-) implemented
        in another package.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Documentation
-------------

Sorry, we don't have real user documentation yet.


Installation
------------

This package won't normally be installed on its own.
Add it to the requirements of your package in which you intend to
use one or more of its behaviors (in ``setup.py``)::

    setup(...
        install_requires=[
            'setuptools',
            ...
            'visaplan.plone.behaviors',
            ],
        ...)

and add the behaviors you need to the list in the FTI file of your
Dexterity-based type.


Contribute
----------

- Issue Tracker: https://github.com/visaplan/plone.behaviors/issues
- Source Code: https://github.com/visaplan/plone.behaviors


Support
-------

If you are having issues, please let us know;
please use the issue tracker mentioned above.


License
-------

The project is licensed under the GPLv2.

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
