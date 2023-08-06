Arcana
======

.. image:: https://travis-ci.org/MonashBI/arcana.svg?branch=master
  :target: https://travis-ci.org/MonashBI/arcana
.. image:: https://codecov.io/gh/MonashBI/arcana/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MonashBI/arcana
.. image:: https://img.shields.io/pypi/pyversions/arcana.svg
  :target: https://pypi.python.org/pypi/arcana/
  :alt: Supported Python versions
.. image:: https://img.shields.io/pypi/v/arcana.svg
  :target: https://pypi.python.org/pypi/arcana/
  :alt: Latest Version    
.. image:: https://readthedocs.org/projects/arcana/badge/?version=latest
  :target: http://arcana.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Abstraction of Repository-Centric ANAlysis (Arcana) is Python framework
for "repository-centric" analyses of study groups (e.g. NeuroImaging
studies)

Arcana interacts closely with a repository, storing intermediate
outputs, along with the parameters used to derive them, for reuse by
subsequent analyses. Repositories can either be XNAT repositories or
(http://xnat.org) local directories organised by subject and visit,
and a BIDS module (http://bids.neuroimaging.io/) is planned as future
work. 

Analysis workflows are constructed and executed using the Nipype
package, and can either be run locally or submitted to HPC
schedulers using Nipype’s execution plugins. For a requested analysis
output, Arcana determines the required processing steps by querying
the repository to check for missing intermediate outputs before
constructing the workflow graph. When running in an environment
with `the modules package <http://modules.sourceforge.net>`_ installed,
Arcana manages the loading and unloading of software modules per
pipeline node.

Design
------

Arcana is designed with an object-oriented philosophy, with
the acquired and derived data sets along with the analysis pipelines
used to derive the derived data sets encapsulated within "Study" classes.

The Arcana package itself only provides the abstract *Study* and
*MultiStudy* base classes, which are designed to be sub-classed to
provide specialised classes representing the analysis that can be performed
on specific types of data (e.g. FmriStudy, PetStudy). These specific classes
can then be sub-classed further into classes that are specific to a particular
study, and integrate complete analysis workflows from preprocessing
to statistics.

Installation
------------

Arcana can be installed using *pip*::

    $ pip install arcana

