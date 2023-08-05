========================
visaplan.plone.behaviors
========================

The interfaces of this package are meant to be used for new datatypes for the
UNITRACC family of Plone sites.
They provide zope.schema definitions for fields which those new datatypes have in common.

Interfaces / behaviors
----------------------

IHeightAndWidth
        Provides the integer fields ``height`` and ``width``

ICaptionAndLegend
        Provides the text fields ``caption`` and ``legend``
        (e.g. for image types)

IExcludeFromSearch
        Provides a boolean field ``excludeFromSearch``, aimed for
        selective exclusion of objects from standard catalog searches

IHierarchicalBuzzword
        This is quite incomplete;
        the provided ASCIILine field ``code`` is aimed for the implementation
        of a hierarchical buzzword index.
        The vocabulary is still to be implemented;
        the factory of this behavior will likely be (re-) implemented
        in another package.
