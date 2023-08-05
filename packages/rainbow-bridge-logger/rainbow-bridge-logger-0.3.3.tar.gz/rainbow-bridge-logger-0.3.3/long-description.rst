

Rainbow Bridge Logger
=================================
A wrapper for the native logging module of Python.

.. code-block:: python

    from rainbow import RainbowLogger

    # __name__ will get the current context
    # but you can pass any text you want, for identification
    logger = RainbowLogger(__name__)

    logger.info('my info')
    logger.warning('my warn')
    logger.error('my error')
    logger.debug('my debug')
