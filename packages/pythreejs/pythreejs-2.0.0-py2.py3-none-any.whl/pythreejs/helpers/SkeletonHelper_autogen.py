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
class SkeletonHelper(Object3D):
    """SkeletonHelper

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/helpers/SkeletonHelper
    """

    def __init__(self, root=None, **kwargs):
        kwargs['root'] = root
        super(SkeletonHelper, self).__init__(**kwargs)

    _model_name = Unicode('SkeletonHelperModel').tag(sync=True)

    root = Instance(Object3D, allow_none=True).tag(sync=True, **widget_serialization)

    type = Unicode("SkeletonHelper", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    SkeletonHelper.__signature__ = inspect.signature(SkeletonHelper.__init__)
