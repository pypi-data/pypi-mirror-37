import six
from ipywidgets import (
    Widget, DOMWidget, widget_serialization, register
)
from ipywidgets.widgets.trait_types import TypedTuple
from traitlets import (
    Unicode, Int, CInt, Instance, ForwardDeclaredInstance, This, Enum,
    Tuple, List, Dict, Float, CFloat, Bool, Union, Any,
)

from .._base.Three import ThreeWidget
from .._base.uniforms import uniforms_serialization
from ..enums import *
from ..traits import *

from .BaseBufferGeometry_autogen import BaseBufferGeometry

from .BufferAttribute import BufferAttribute
from .InterleavedBufferAttribute_autogen import InterleavedBufferAttribute
from .BaseGeometry_autogen import BaseGeometry
from .BaseBufferGeometry_autogen import BaseBufferGeometry

class BufferGeometry(BaseBufferGeometry):
    """BufferGeometry

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/core/BufferGeometry
    """

    def __init__(self, **kwargs):
        super(BufferGeometry, self).__init__(**kwargs)

    _model_name = Unicode('BufferGeometryModel').tag(sync=True)

    index = Union([
        Instance(BufferAttribute, allow_none=True),
        Instance(InterleavedBufferAttribute, allow_none=True)
    ]).tag(sync=True, **widget_serialization)

    attributes = Dict(Union([
        Instance(BufferAttribute),
        Instance(InterleavedBufferAttribute)
    ])).tag(sync=True, **widget_serialization)

    morphAttributes = Dict(TypedTuple(Union([
        Instance(BufferAttribute),
        Instance(InterleavedBufferAttribute)
    ]))).tag(sync=True, **widget_serialization)

    userData = Dict(default_value={}, allow_none=False).tag(sync=True)

    MaxIndex = CInt(65535, allow_none=False).tag(sync=True)

    _ref_geometry = Union([
        Instance(BaseGeometry, allow_none=True),
        Instance(BaseBufferGeometry, allow_none=True)
    ]).tag(sync=True, **widget_serialization)

    _store_ref = Bool(False, allow_none=False).tag(sync=True)

    type = Unicode("BufferGeometry", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    BufferGeometry.__signature__ = inspect.signature(BufferGeometry.__init__)
