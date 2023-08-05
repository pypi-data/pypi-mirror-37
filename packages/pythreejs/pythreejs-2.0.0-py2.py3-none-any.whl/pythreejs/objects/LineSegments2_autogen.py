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

from .Mesh_autogen import Mesh

from ..materials.LineMaterial_autogen import LineMaterial
from ..geometries.LineSegmentsGeometry_autogen import LineSegmentsGeometry

@register
class LineSegments2(Mesh):
    """LineSegments2

    Autogenerated by generate-wrappers.js
    This class is a custom class for pythreejs, with no
    direct corresponding class in three.js.
    """

    def __init__(self, geometry=UninitializedSentinel, material=UninitializedSentinel, **kwargs):
        kwargs['geometry'] = geometry
        kwargs['material'] = material
        super(LineSegments2, self).__init__(**kwargs)

    _model_name = Unicode('LineSegments2Model').tag(sync=True)

    material = Union([
        Instance(Uninitialized),
        Instance(LineMaterial),
        ], default_value=UninitializedSentinel, allow_none=True).tag(sync=True, **unitialized_serialization)

    geometry = Union([
        Instance(Uninitialized),
        Instance(LineSegmentsGeometry),
        ], default_value=UninitializedSentinel, allow_none=True).tag(sync=True, **unitialized_serialization)

    type = Unicode("LineSegments2", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    LineSegments2.__signature__ = inspect.signature(LineSegments2.__init__)
