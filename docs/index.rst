.. Flask-Factory documentation master file, created by
   sphinx-quickstart on Sat Jul 26 16:37:53 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-Factory
=============

The **Flask-Factory** extension provides the generalized way to make
:ref:`app-factories`.

.. code-block:: python

    from flask_factory import Factory

    create_app = Factory(__name__)

    @create_app.step
    def register_routes(app):
        @app.route('/')
        def hello():
            return 'Hello, world!'

    if __name__ == '__main__':
        app = create_app()
        app.run()


Installing Flask-Factory
------------------------

Install with :program:`pip` or :program:`easy_install`:

.. code-block:: bash

    $ pip install Flask-Factory


API
---


.. toctree::
    :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

