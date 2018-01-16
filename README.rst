===============================
smartPeak
===============================


.. image:: https://img.shields.io/pypi/v/smartPeak.svg
        :target: https://pypi.python.org/pypi/smartPeak

.. image:: https://img.shields.io/travis/dmccloskey/smartPeak.svg
        :target: https://travis-ci.org/dmccloskey/smartPeak

.. image:: https://readthedocs.org/projects/smartPeak/badge/?version=latest
        :target: https://smartPeak.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dmccloskey/smartPeak/shield.svg
     :target: https://pyup.io/repos/github/dmccloskey/smartPeak/
     :alt: Updates

fast and intelligent processing of GC and LC MS data, and HPLC data.  Supported workflows include the following:

1. metabolomic- and proteomic-based absolute quantitation by SIM, MRM, DDA, DIA, or full scan.
2. targeted isotopomer extraction for fluxomics by SIM, MRM, DDA, DIA, or full scan.


* Free software: MIT License
* Documentation: https://smartPeak.readthedocs.io.

Features
========

* Automated peak picking and peak selection

    - Advanced peak smoothing and picking
    - User defined thresholds for peak filtering
    - Multi-stage, adaptive optimization algorithm for peak selection

* External calibration curve application

	- Back calculation of sample concentration with or without IS

* Automated calibration curve fitting

    - Outlier detection with bias and R-squared optimization
    - User defined calibration model and acceptance criteria

* Advanced peak integration and baseline detection models

	- Trapezoid, simpson, and gaussian-based peak integration
	- multiple baseline definitions

* Flexible, user-defined peak, run, or batch quality control reporting

	- Peak QCs: Tailing, shouldering, points across the peak, l/ulod, l/uloq, ion ratio, etc.,
	- Run QCs: Resolution between isomers
	- Batch QCs: %RSD between QCs, %carryover, SST, etc.,

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage