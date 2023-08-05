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

from .Light_autogen import Light


@register
class RectAreaLight(Light):
    """RectAreaLight

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/lights/RectAreaLight
    """

    def __init__(self, color="#ffffff", intensity=1, width=10, height=10, **kwargs):
        kwargs['color'] = color
        kwargs['intensity'] = intensity
        kwargs['width'] = width
        kwargs['height'] = height
        super(RectAreaLight, self).__init__(**kwargs)

    _model_name = Unicode('RectAreaLightModel').tag(sync=True)

    width = CFloat(10, allow_none=False).tag(sync=True)

    height = CFloat(10, allow_none=False).tag(sync=True)

    type = Unicode("RectAreaLight", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    RectAreaLight.__signature__ = inspect.signature(RectAreaLight.__init__)
