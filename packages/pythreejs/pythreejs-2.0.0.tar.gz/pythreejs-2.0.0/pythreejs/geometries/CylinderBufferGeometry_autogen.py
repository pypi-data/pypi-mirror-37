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
class CylinderBufferGeometry(BaseBufferGeometry):
    """CylinderBufferGeometry

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/geometries/CylinderGeometry
    """

    def __init__(self, radiusTop=1, radiusBottom=1, height=1, radiusSegments=8, heightSegments=1, openEnded=False, thetaStart=0, thetaLength=6.283185307179586, **kwargs):
        kwargs['radiusTop'] = radiusTop
        kwargs['radiusBottom'] = radiusBottom
        kwargs['height'] = height
        kwargs['radiusSegments'] = radiusSegments
        kwargs['heightSegments'] = heightSegments
        kwargs['openEnded'] = openEnded
        kwargs['thetaStart'] = thetaStart
        kwargs['thetaLength'] = thetaLength
        super(CylinderBufferGeometry, self).__init__(**kwargs)

    _model_name = Unicode('CylinderBufferGeometryModel').tag(sync=True)

    radiusTop = CFloat(1, allow_none=False).tag(sync=True)

    radiusBottom = CFloat(1, allow_none=False).tag(sync=True)

    height = CFloat(1, allow_none=False).tag(sync=True)

    radiusSegments = CInt(8, allow_none=False).tag(sync=True)

    heightSegments = CInt(1, allow_none=False).tag(sync=True)

    openEnded = Bool(False, allow_none=False).tag(sync=True)

    thetaStart = CFloat(0, allow_none=False).tag(sync=True)

    thetaLength = CFloat(6.283185307179586, allow_none=False).tag(sync=True)

    type = Unicode("CylinderBufferGeometry", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    CylinderBufferGeometry.__signature__ = inspect.signature(CylinderBufferGeometry.__init__)
