Rundeck Resources
=================

.. image:: https://gitlab.com/elazkani/rundeck-resources/badges/master/build.svg
    :target: https://gitlab.com/elazkani/rundeck-resources
    :alt: Gitlab-CI Pipeline

.. image:: https://codecov.io/gl/elazkani/rundeck-resources/branch/master/graph/badge.svg
    :target: https://codecov.io/gl/elazkani/rundeck-resources
    :alt: CodeCov.io

.. image:: https://readthedocs.org/projects/rundeck-resources/badge/?version=latest
  :target: http://rundeck-resources.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/rundeck-resources.svg
    :target: https://pypi.org/project/rundeck-resources
    :alt: Pypi Package Version

.. image:: https://img.shields.io/pypi/pyversions/rundeck-resources.svg
    :target: https://pypi.org/project/rundeck-resources
    :alt: Python Versions Supported

.. image:: https://img.shields.io/badge/license-BSD-blue.svg
   :target: https://img.shields.io/badge/license-BSD-blue.svg
   :alt: BSD License


Python tool to query resources from different sources and export them into a data structure that ``Rundeck`` can consume.

Installation
------------

::

    pip install rundeck-resources
      
Usage
-----

::

    $ rundeck-resources -h
    usage: rundeck-resources [-h] [-v] [-l LOGGER] [--no-cache] [-V] config

    Generates rundeck resources file from different API sources.

    positional arguments:
      config                Configuration file.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Verbosity level to use.
      -l LOGGER, --logger LOGGER
                            The logger YAML configuration file.
      --no-cache            Do not use cache.
      -V, --version         Prints version.


The ``rundeck-resources`` requires an INI configuration file.
You can see the example configuration in the `example.ini <https://gitlab.com/elazkani/rundeck-resources/blob/master/config/example.ini>`_.

Docker
------

There is a docker image tagged with the version of the released package.

+--------+-----------+-------------------------------------+
| ENV    | OPTIONAL  | DESCRIPTION                         |
+========+===========+=====================================+
| ARGS   | ``True``  | The command line arguments.         |
+--------+-----------+-------------------------------------+
| CONFIG | ``False`` | The path to the configuration file. |
+--------+-----------+-------------------------------------+

Usage:
  ::
  
       $ docker run -it -v ~/config/:/config \
         -v ~/export/:/export \
         -e ARGS="-vvv" -e CONFIG="/config/config.ini" \
         elazkani/rundeck-resources

Assumptions:
  * ``~/config/`` holds the ``config.ini`` configuration file.
  * The configuration is set to export to the ``/export/`` path.
  * ``/export`` will hold the resources exported file inside the container.
  * ``~/export/`` exists on the host.

Importers
---------

``rundeck-resources`` currently offer the following **importers**:
  * Chef: ``ChefImporter``


Exporters
---------

``rundeck-resources`` currently offers the following **exporters**:
  * YAML: ``YAMLExporter``

Contributors:
-------------

* `Andrew Rabert <https://gitlab.com/nvllsvm>`_
