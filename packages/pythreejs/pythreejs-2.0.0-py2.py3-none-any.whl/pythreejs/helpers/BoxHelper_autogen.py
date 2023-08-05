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

from ..core.Object3D import Object3D

from ..core.Object3D import Object3D

@register
class BoxHelper(Object3D):
    """BoxHelper

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/helpers/BoxHelper
    """

    def __init__(self, object=None, color="#ffffff", **kwargs):
        kwargs['object'] = object
        kwargs['color'] = color
        super(BoxHelper, self).__init__(**kwargs)

    _model_name = Unicode('BoxHelperModel').tag(sync=True)

    object = Instance(Object3D, allow_none=True).tag(sync=True, **widget_serialization)

    color = Color("#ffffff", allow_none=True).tag(sync=True)

    type = Unicode("BoxHelper", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    BoxHelper.__signature__ = inspect.signature(BoxHelper.__init__)
