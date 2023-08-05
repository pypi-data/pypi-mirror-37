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

from ..core.BaseBufferGeometry_autogen import BaseBufferGeometry


@register
class LineSegmentsGeometry(BaseBufferGeometry):
    """LineSegmentsGeometry

    Autogenerated by generate-wrappers.js
    This class is a custom class for pythreejs, with no
    direct corresponding class in three.js.
    """

    def __init__(self, **kwargs):
        super(LineSegmentsGeometry, self).__init__(**kwargs)

    _model_name = Unicode('LineSegmentsGeometryModel').tag(sync=True)

    positions = WebGLDataUnion(dtype="float32", shape_constraint=shape_constraints(None, 2, 3)).tag(sync=True)

    colors = WebGLDataUnion(None, dtype="float32", shape_constraint=shape_constraints(None, 2, 3), allow_none=True).tag(sync=True)

    type = Unicode("LineSegmentsGeometry", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    LineSegmentsGeometry.__signature__ = inspect.signature(LineSegmentsGeometry.__init__)
