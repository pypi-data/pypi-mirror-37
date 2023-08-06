.. ContextExplorer documentation master file, created by
   sphinx-quickstart on Wed Mar 14 14:03:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Context-explorer
###############

Context-explorer is a software program that facilitates analyses of data
extracted from microscope images of cells.

Motivation
==========

The analyses methods in context-explorer focuses on how populations of cells are
affected by their microenvironment, including local variations in cell
signalling and cell density. It is currently difficult for scientist without
previous programming experience to quantify these variables, although it is
relevant for many research areas. Facilitating this type of analyses can help
scientist around the world to improve their understanding of cellular behavior
and accelerate their research.

Graphical overview
==================

.. image:: img/fig1-overview.png


Installing Context-explorer
==========================

The fastest way to get up and running, is to install context-explorer via the
``conda`` package manager from the Anaconda Python distribution:

1. Download and install Anaconda Python for your platform.

2a. Open the Anaconda navigator and search for context-explorer

2b. Open a terminal or the Anaconda Prompt and type ``conda install -c
joelostblom context-explorer``.

Using context-explorer
=====================

Launch the context-explorer by opening a terminal/the ``Anaconda Navigator``,
typing ``ctexplorer``, and hitting enter. Keep the terminal window open, there
is where context-explorer will output messages of what it is doing.

Input file
----------

The minimum required input is a CSV-file containing single cell measurements
including xy-coordinates and field number for each cell. Such measurements can
be extracted from microscope images using software such as CellProfiler or
vendor-specific alternatives. The field number represents the position of the
tile/site within each well and the xy-coordinates are the position of each cell
within these tile. Ideally, at least one additional measure of interest is
present, e.g. fluorescent intensity or nuclear area.

Workflow overview
-----------------

.. image:: img/gui.png

There is `a brief video tutorial <https://vimeo.com/295958949>`_ of how to use
the software.

After loading the desired CSV-file, assign treatment groups via the plate
layout tab. In the threshold tab, it is possible to create histograms and
scatter plots of the desired measurements. One plot will be created per well.
Basic column modifications (e.g., addition and deletion) can be performed via
the ColumnModification tab.

In the colony identification tab, cells can be grouped into clusters based on
density variations within each well. The clustering parameters can be adjusted
interactively, so that the clusters represent biologically relevant entities,
e.g. colonies of stem cells or micropatterned cells. This grouping is helpful
to assess the variation of the cellular microenvironment on cell fate through
comparisons between groups at distinct spatial locations within the clusters,
.e.g. comparing the expression of certain proteins between cells growing at
the colony edge vs the middle of the colony.

The data can then be saved via the SaveData tab either as single cells data or
aggregated at the level of choice (e.g. average measurements per well or
treatment group).

Package build instructions
--------------------------

These instructions are not needed if you just want to use ``context-explorer``.
The steps below details how to build a Python package (1-2) and upload it to
`<https://pypi.org>`_ (3), and how to build a ``conda`` package (4-6) and
upload it to `<https://www.anaconda.com/download>`_ (7).

1. Create a git tag with the `version number <https://semver.org>`_.

    .. code:: python

        git tag <major.minor.patch>

    If there are any changes in the working tree since this tag, these needs to
    be stashed or ``versioneer`` will create a version tag that is incompatible
    with PyPI.

2. Build the source distribution (for ``conda`` to use in the next step) and at
   least one binary wheel (faster for ``pip install``).

    .. code:: python

        python setup.py sdist bdist_wheel

3. Upload the package to PyPI.org.

    .. code:: python

        twine upload dist/*<major.minor.path>*

4. A ``conda`` build recipe can be created from the PyPI package.

    .. code:: python

        conda skeleton pypi context-explorer

    This will create the directory ``context-explorer`` with the file
    ``meta.yml``. The only manual modification that needs to be made is to
    replace the occurrences of `pyqt5` with `pyqt`, since this package is named
    differently on ``PyPI`` and in ``conda``:

    .. code:: bash
        sed -i 's/pyqt5/pyqt/' context-explorer/meta.yaml

5. Build a ``condo`` package from the recipe.

    .. code:: python

        conda build context-explorer

6. The conda package is usually created in
   ``~anaconda3/conda-bld/linux-64/<package_name>`` and can be converted to
   support all platform architectures.

    .. code:: python

        conda convert --platform all <absolute/path/to/package> -o <outputdir>

7. Each platform's package needs to be uploaded separately to anaconda.org.

    .. code:: python

        anaconda upload <path/to/package>

    The initial package created with ``conda build`` can be uploaded
    automatically by setting the following.

    .. code:: python

        conda config --set anaconda_upload yes


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

**Heading 1**

* :ref:`genindex`
* :ref:`modindex`

**Heading 2**

* :ref:`search`
