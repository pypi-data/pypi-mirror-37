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
class CircleBufferGeometry(BaseBufferGeometry):
    """CircleBufferGeometry

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/geometries/CircleGeometry
    """

    def __init__(self, radius=1, segments=8, thetaStart=0, thetaLength=6.283185307179586, **kwargs):
        kwargs['radius'] = radius
        kwargs['segments'] = segments
        kwargs['thetaStart'] = thetaStart
        kwargs['thetaLength'] = thetaLength
        super(CircleBufferGeometry, self).__init__(**kwargs)

    _model_name = Unicode('CircleBufferGeometryModel').tag(sync=True)

    radius = CFloat(1, allow_none=False).tag(sync=True)

    segments = CInt(8, allow_none=False, min=3).tag(sync=True)

    thetaStart = CFloat(0, allow_none=False).tag(sync=True)

    thetaLength = CFloat(6.283185307179586, allow_none=False).tag(sync=True)

    type = Unicode("CircleBufferGeometry", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    CircleBufferGeometry.__signature__ = inspect.signature(CircleBufferGeometry.__init__)
