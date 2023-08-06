
.. py:currentmodule:: pythreejs

LineSegments2
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: LineSegments2(geometry=UninitializedSentinel, material=UninitializedSentinel, )
    :members:
    :undoc-members:


    Inherits :py:class:`~pythreejs.Mesh`.

    Three.js docs: https://threejs.org/docs/#api/objects/LineSegments2


    .. py:attribute:: material


        .. sourcecode:: python

            Union([
                Instance(Uninitialized),
                Instance(LineMaterial),
                ], default_value=UninitializedSentinel, allow_none=True).tag(sync=True, **unitialized_serialization)

    .. py:attribute:: geometry


        .. sourcecode:: python

            Union([
                Instance(Uninitialized),
                Instance(LineSegmentsGeometry),
                ], default_value=UninitializedSentinel, allow_none=True).tag(sync=True, **unitialized_serialization)

    .. py:attribute:: type


        .. sourcecode:: python

            Unicode("LineSegments2", allow_none=False).tag(sync=True)

