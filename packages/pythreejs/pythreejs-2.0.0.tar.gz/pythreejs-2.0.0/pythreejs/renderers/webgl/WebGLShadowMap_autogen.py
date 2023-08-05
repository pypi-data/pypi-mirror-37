import six
from ipywidgets import (
    Widget, DOMWidget, widget_serialization, register
)
from ipywidgets.widgets.trait_types import TypedTuple
from traitlets import (
    Unicode, Int, CInt, Instance, ForwardDeclaredInstance, This, Enum,
    Tuple, List, Dict, Float, CFloat, Bool, Union, Any,
)

from ..._base.Three import ThreeWidget
from ..._base.uniforms import uniforms_serialization
from ...enums import *
from ...traits import *

from ..._base.Three import ThreeWidget


@register
class WebGLShadowMap(ThreeWidget):
    """WebGLShadowMap

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/renderers/webgl/WebGLShadowMap
    """

    def __init__(self, **kwargs):
        super(WebGLShadowMap, self).__init__(**kwargs)

    _model_name = Unicode('WebGLShadowMapModel').tag(sync=True)

    enabled = Bool(False, allow_none=False).tag(sync=True)

    type = Enum(ShadowTypes, "PCFShadowMap", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    WebGLShadowMap.__signature__ = inspect.signature(WebGLShadowMap.__init__)
