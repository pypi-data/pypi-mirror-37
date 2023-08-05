==========
smallerize
==========


.. image:: https://img.shields.io/pypi/v/smallerize.svg
        :target: https://pypi.python.org/pypi/smallerize
        :alt: pip version
        
.. image:: https://gitlab.com/warsquid/smallerize/badges/master/coverage.svg
        :alt: Coverage

.. image:: https://readthedocs.org/projects/smallerize/badge/?version=latest
        :target: https://smallerize.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A Python implementation of minimisation for clinical trials


* Free software: GNU General Public License v3
* Documentation: https://smallerize.readthedocs.io.


Features
--------

* Implements minimization as described in Pocock + Simon (1975): *Sequential Treatment Assignment with Balancing
  for Prognostic Factors in the Controlled Clinical Trial*
* Includes all functions described in the article: range, standard deviation,
  variance, etc.
* Also implements pure random assignment for comparison
* Simulation module to allow simulating the effects of different assignment
  schemes.

Example
-------

Comparing minimization to purely random assignment by simulation:

.. image:: https://gitlab.com/warsquid/smallerize/raw/master/examples/ps1975_factor_imbalance.png
        :scale: 50%
        :alt: Simulation results

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
