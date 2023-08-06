
.. py:currentmodule:: pythreejs

DataTexture3D
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: DataTexture3D(data=None, format="RGBAFormat", type="UnsignedByteType", mapping="UVMapping", wrapS="ClampToEdgeWrapping", wrapT="ClampToEdgeWrapping", magFilter="NearestFilter", minFilter="NearestFilter", anisotropy=1, )
    :members:
    :undoc-members:

    This widget has some manual overrides on the Python side.

    Inherits :py:class:`~pythreejs.Texture`.

    Three.js docs: https://threejs.org/docs/#api/textures/DataTexture3D


    .. py:attribute:: data


        .. sourcecode:: python

            WebGLDataUnion().tag(sync=True)

    .. py:attribute:: minFilter


        .. sourcecode:: python

            Enum(Filters, "NearestFilter", allow_none=False).tag(sync=True)

    .. py:attribute:: magFilter


        .. sourcecode:: python

            Enum(Filters, "NearestFilter", allow_none=False).tag(sync=True)

    .. py:attribute:: flipY


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: generateMipmaps


        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

