
.. py:currentmodule:: pythreejs

MeshMatcapMaterial
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: MeshMatcapMaterial()
    :members:
    :undoc-members:


    Inherits :py:class:`~pythreejs.Material`.

    Three.js docs: https://threejs.org/docs/#api/materials/MeshMatcapMaterial


    .. py:attribute:: alphaMap


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: bumpMap


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: bumpScale


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: color


        .. sourcecode:: python

            Color("#ffffff", allow_none=False).tag(sync=True)

    .. py:attribute:: displacementMap


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: displacementScale


        .. sourcecode:: python

            CFloat(1, allow_none=False).tag(sync=True)

    .. py:attribute:: displacementBias


        .. sourcecode:: python

            CFloat(0, allow_none=False).tag(sync=True)

    .. py:attribute:: lights


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: map


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: matcap


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: morphNormals


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: morphTargets


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: normalMap


        .. sourcecode:: python

            Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: normalScale


        .. sourcecode:: python

            Vector2(default_value=[1, 1]).tag(sync=True)

    .. py:attribute:: skinning


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: type


        .. sourcecode:: python

            Unicode("MeshMatcapMaterial", allow_none=False).tag(sync=True)

