PathMe Viewer |build| |coverage| |docs| |zenodo|
================================================

This plugin initializes the pathway viewer in ComPath that allows to explore overlaps between pathways using
the canonical mappings.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
1. ``pathme_viewer`` can be installed with the following commands:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/ComPath/PathMe-Viewer.git@master

2. or in editable mode with:

.. code-block:: sh

    $ git clone https://github.com/ComPath/PathMe-Viewer.git
    $ cd PathMe-Viewer
    $ python3 -m pip install -e .


Database
--------
The web application requires to load the pathways from the databases in the BEL. Thus, it is required to the following
command to load the database (note that the first time it runs might take a couple of hours).

.. code-block:: python

    python3 -m pathme_viewer manage load

In order to check the status of the database, you can run:

.. code-block:: python

    python3 -m pathme_viewer manage summarize

The content of the database can be erased by running:

.. code-block:: python

    python3 -m pathme_viewer manage drop

Deployment
----------
Once the desired pathway databases are loaded, you can deploy the web application by running:

.. code-block:: python

    python3 -m pip install pathme_viewer web

Note that the database runs by default in the following port: http://0.0.0.0:5000/. The Flask host and port can be
modified by changing the default parameters (run: "python3 -m pathme_viewer web --help" for more info).

Deployment of ComPath with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: the docker file is meant to be run on 0.0.0.0:5000. If you want to change the host/port
please modify dockerfile (line 55) and src/bin/bootstrap.sh (line 23).

1. Build the container named 'pathme' version 0.0.1.

.. code-block:: sh

    docker build -t pathme:0.0.1 .

2. Run docker the pathme container version 0.0.1.

.. code::

    docker run --name=pathme -d -p 5000:5000 --restart=always -d pathme:0.0.1


How to Use
----------

Here is an example of the visualization of Apoptosis equivalent pathways.

.. image:: https://github.com/ComPath/PathMe-Viewer/blob/master/src/pathme_viewer/static/img/visualization_example.png
    :width: 500px



.. |build| image:: https://travis-ci.org/ComPath/PathMe-Viewer.svg?branch=master
    :target: https://travis-ci.org/ComPath/PathMe-Viewer
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/ComPath/PathMe-Viewer/coverage.svg?branch=master
    :target: https://codecov.io/gh/ComPath/PathMe-Viewer?branch=master
    :alt: Coverage Status

.. |docs| image:: http://readthedocs.org/projects/pathme_viewer/badge/?version=latest
    :target: https://pathme_viewer.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |climate| image:: https://codeclimate.com/github/compath/pathme_viewer/badges/gpa.svg
    :target: https://codeclimate.com/github/compath/pathme_viewer
    :alt: Code Climate

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/pathme_viewer.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/pathme_viewer.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/pathme_viewer.svg
    :alt: Apache-2.0

.. |zenodo| image:: https://zenodo.org/badge/144898535.svg
   :target: https://zenodo.org/badge/latestdoi/144898535

