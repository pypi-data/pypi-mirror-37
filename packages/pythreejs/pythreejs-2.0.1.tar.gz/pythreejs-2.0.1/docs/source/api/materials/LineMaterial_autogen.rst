
.. py:currentmodule:: pythreejs

LineMaterial
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: LineMaterial()
    :members:
    :undoc-members:


    Inherits :py:class:`~pythreejs.Material`.

    Three.js docs: https://threejs.org/docs/#api/materials/LineMaterial


    .. py:attribute:: color


        .. sourcecode:: python

            Color("#ffffff", allow_none=False).tag(sync=True)

    .. py:attribute:: fog


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: lights


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: linewidth


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: dashScale


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: dashSize


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: gapSize


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: type


        .. sourcecode:: python

            Unicode("LineMaterial", allow_none=False).tag(sync=True)

