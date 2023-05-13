==========
Contribute
==========



Linting
=======

.. code-block:: bash

    flake8

Testing
=======

.. code-block:: bash

    python -m pytest

Documentation
=============

.. code-block:: bash

    sphinx-build doc _build


Distribute
==========

.. tab:: Ubuntu

   .. code-block:: bash

    pip install "build[virtualenv]"
    python -m build
    python -m twine upload dist/*

.. tab:: Windows

   TBD






