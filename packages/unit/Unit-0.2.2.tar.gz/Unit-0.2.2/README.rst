Unit -- An asynchronous web framework written in Python
=======================================================


Installation
------------

Unit requires Python 3.5 and is available on PyPI.
Use pip to install it::

    $ pip install unit


"Hello, World!" Example
-----------------------

.. code-block:: python

    import unit

    app = unit.Application(__name__)


    @app.route('/')
    def hello(request):
        return 'Hello, World!'


    if __name__ == '__main__':
        app.run()


License
-------

Unit is developed and distributed under the Apache 2.0 license.
