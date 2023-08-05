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
class HemisphereLight(Light):
    """HemisphereLight

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/lights/HemisphereLight
    """

    def __init__(self, color="#ffffff", groundColor="#000000", intensity=1, **kwargs):
        kwargs['color'] = color
        kwargs['groundColor'] = groundColor
        kwargs['intensity'] = intensity
        super(HemisphereLight, self).__init__(**kwargs)

    _model_name = Unicode('HemisphereLightModel').tag(sync=True)

    groundColor = Color("#000000", allow_none=False).tag(sync=True)

    type = Unicode("HemisphereLight", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    HemisphereLight.__signature__ = inspect.signature(HemisphereLight.__init__)
