.. borobudur documentation master file, created by
   sphinx-quickstart on Sun Sep 16 18:16:42 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Borobudur
=====================================
is a Python web frameworks that helps building `single page applications <http://en.wikipedia.org/wiki/Single-page_application>`_
and focus on sharing server's and client's code. It uses:

    * `pyramid <http://www.pylonsproject.org/>`_ Python web application framework
    * `backbone.js <http://www.backbonejs.org/>`_ Javascript client MVC framework
    * `prambanan <http://docs.microvac.co.id/prambanan/>`_ Python to javascript compiler

Starting new borobudur project
------------------------------
#. Get a `python <http://www.python.org/>`_  interpreter

#. Install `nodejs <http://www.nodejs.org/>`_, used for compiling assets

#. Install borobudur

    .. code-block:: text

        pip install borobudur

#. Create project

    .. code-block:: text

        pcreate -t borobudur_starter test_app

#. Install dependency

    .. code-block:: text

        cd test_app
        pip install -e .
        npm install -d

#. Run forest, run!

    .. code-block:: text

        pserve development.ini

Guide
------------------------------

.. toctree::
    :maxdepth: 2

    app
    model
    template
    view
    page
    resources
    javascript
    script
    misc

API Docs
------------------------------

