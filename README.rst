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
2. targetted isotopomer extraction for fluxomics by SIM, MRM, DDA, DIA, or full scan.


* Free software: MIT License
* Documentation: https://smartPeak.readthedocs.io.

Features
========

* Automated peak picking and peak selection

- Advanced peak smoothing and picking
- User defined peak filtering and quality control checking
- Multi-stage, adaptive optimization algorithm for peak selection

* Automated calibration curve fitting

- Outlier detection with bias and R-squared optimization
- User defined calibration model and acceptance criteria

* Advanced peak integration and baseline detection models

Getting Started
===============
Set up your fork:
-----------------
1. Fork the main repository_.

.. _repository: https://github.com/dmccloskey/smartPeak

2. Clone your fork.

:code:`git clone https://github.com/[your GitHub username]/smartPeak.git`

3. set the upstrem repository

:code:`git remote add upstream https://github.com/dmccloskey/smartPeak.git`

4. keep your develop branch in sync

:code:`git fetch --all --prune`

:code:`git checkout develop`

:code:`git merge --ff-only upstream/develop`

:code:`git push origin develop`

5. create a branch for your new changes from the develop branch

:code:`git checkout develop`

:code:`git checkout -b [your new branch]`

6. keep your new change branch in sync with develop

:code:`git checkout develop`

:code:`git merge develop`

6. make some changes, add your changes, commit your changes, and push your changes to your fork

:code:`git add .`

:code:`git commit -m "[your commit message]"`

:code:`git push origin [your new branch]`

7. open a pull request when your change is ready to be added to the main repository

8. delete your local and remote branch AFTER the pull request has been accepted

:code:`git push -d origin [your commit branch]`

:code:`git checkout develop`

:code:`git branch -d [your commit branch]`

Contributing:
-------------
Please follow the GitFlow_ project guidelines for contributing.

.. _GitFlow: http://nvie.com/posts/a-successful-git-branching-model/

In addition, please follow the following rules:

- never commit directly to the develop or master branches as it will complicate the merge

- starte every new branch from develop and not from another derived branch (unless it is not avoidable)

Documentation:
--------------
Please follow the Google Python Docstrings_ style guide.

.. _Docstrings: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Docker integration
------------------
To build the smartPeak docker image, navigate to the smartPeak/py directory

:code:`docker build -t dmccloskey/smartPeak:latest .`

To run the smartPeak docker image after building, navigate to the smartPeak/py directory

:code:`docker-compose up`

To restart the smartPeak docker image

:code:`docker-compose restart`

To remove the smartPeak docker image

:code:`docker-compose down`

Remote debugging with vscode
----------------------------
- change the luanch.json file in the .vscode directory to match your system settings
by changing the "localRoot" directory of "Attach (Remote Debug)" to match your system.

- you can then dynamically debug your application using the debug_remote.py file and
debugging using the "Attach (Remote Debug)" launch setting

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage