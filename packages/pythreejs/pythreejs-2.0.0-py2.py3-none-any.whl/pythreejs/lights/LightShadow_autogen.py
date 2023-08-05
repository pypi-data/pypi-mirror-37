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

from .._base.Three import ThreeWidget

from ..cameras.Camera_autogen import Camera

@register
class LightShadow(ThreeWidget):
    """LightShadow

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/lights/LightShadow
    """

    def __init__(self, camera=UninitializedSentinel, **kwargs):
        kwargs['camera'] = camera
        super(LightShadow, self).__init__(**kwargs)

    _model_name = Unicode('LightShadowModel').tag(sync=True)

    camera = Union([
        Instance(Uninitialized),
        Instance(Camera),
        ], default_value=UninitializedSentinel, allow_none=False).tag(sync=True, **unitialized_serialization)

    bias = CFloat(0, allow_none=False).tag(sync=True)

    mapSize = Vector2(default_value=[512, 512]).tag(sync=True)

    radius = CFloat(1, allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    LightShadow.__signature__ = inspect.signature(LightShadow.__init__)
