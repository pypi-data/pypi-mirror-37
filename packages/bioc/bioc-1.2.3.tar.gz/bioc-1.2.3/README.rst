`bioc` - BioC data structures and encoder/decoder for Python
=============================================================

.. image:: https://img.shields.io/travis/yfpeng/bioc.svg
   :alt: Build status
   :target: https://travis-ci.org/yfpeng/bioc

.. image:: https://img.shields.io/pypi/v/bioc.svg
   :target: https://pypi.python.org/pypi/bioc
   :alt: Latest version on PyPI

.. image:: https://img.shields.io/pypi/l/bioc.svg
   :alt: License
   :target: https://opensource.org/licenses/BSD-3-Clause


`BioC XML format <http://bioc.sourceforge.net/>`_ can be used to share
text documents and annotations.

``bioc`` exposes an API familiar to users of the standard library
``marshal`` and ``pickle`` modules.

Development of ``bioc`` happens on GitHub:
https://github.com/yfpeng/bioc

Getting started
---------------

Installing ``bioc``

.. code:: bash

    $ pip install bioc

Encoding the BioC collection object ``collection``:

.. code:: python

    import bioc
    # Serialize ``collection`` to a BioC formatted ``str``.
    bioc.dumps(collection)

    # Serialize ``collection`` as a BioC formatted stream to ``fp``.
    with open(filename, 'w') as fp
        bioc.dump(collection, fp)

Compact encoding:

.. code:: python

    import bioc
    bioc.dumps(collection, pretty_print=False)

Incremental BioC serialisation:

.. code:: python

    import bioc
    with bioc.iterwrite(filename, collection) as writer:
        for document in collection.documents:
            writer.writedocument(document)

Decoding the BioC XML file:

.. code:: python

    import json
    # Deserialize ``s`` to a BioC collection object.
    collection = bioc.loads(s)

    # Deserialize ``fp`` to a BioC collection object.
    with open(filename, 'r') as fp:
        bioc.load(fp)

Incrementally decoding the BioC XML file:

.. code:: python

    import bioc
    with bioc.iterparse(filename) as parser:
        collection_info = parser.get_collection_info()
        for document in parser:
            # process document
            ...

`get_collection_info` can be called after the construction of the `iterparse` anytime.

Together with Python coroutines, this can be used to generate BioC XML in an asynchronous, non-blocking fashion.

.. code:: python

    import bioc
    with bioc.iterparse(filename) as parser:
        with bioc.iterwrite(dst, parser.get_collection_info()) as writer:
            for document in parser:
                # modify the document
                ...
                writer.writedocument(document)


Requirements
------------

-  lxml (http://lxml.de)

Developers
----------

-  Yifan Peng (yifan.peng@nih.gov)

Acknowledgment
--------------

-  Hernani Marques (https://github.com/2mh/PyBioC)

Webpage
-------

The official BioC webpage is available with all up-to-date instructions,
code, and corpora in the BioC format, and other research on, based on
and related to BioC.

-  http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/
-  http://bioc.sourceforge.net/

Reference
---------

-  Comeau,D.C., Doğan,R.I., Ciccarese,P., Cohen,K.B., Krallinger,M.,
   Leitner,F., Lu,Z., Peng,Y., Rinaldi,F., Torii,M., Valencia,V.,
   Verspoor,K., Wiegers,T.C., Wu,C.H., Wilbur,W.J. (2013) BioC: A
   minimalist approach to interoperability for biomedical text
   processing. Database: The Journal of Biological Databases and
   Curation.
-  Peng,Y., Tudor,C., Torii,M., Wu,C.H., Vijay-Shanker,K. (2014) iSimp
   in BioC standard format: Enhancing the interoperability of a sentence
   simplification system. Database: The Journal of Biological Databases
   and Curation.
-  Marques,M., Rinaldi,F. (2012) PyBioC: a python implementation of the
   BioC core. In Proceedings of BioCreative IV workshop.
