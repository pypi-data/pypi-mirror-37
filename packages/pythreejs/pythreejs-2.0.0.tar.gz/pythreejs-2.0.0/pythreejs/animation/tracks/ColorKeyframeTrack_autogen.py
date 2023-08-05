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

from ..KeyframeTrack_autogen import KeyframeTrack


@register
class ColorKeyframeTrack(KeyframeTrack):
    """ColorKeyframeTrack

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/animation/tracks/ColorKeyframeTrack
    """

    def __init__(self, name="", times=None, values=None, interpolation="InterpolateLinear", **kwargs):
        kwargs['name'] = name
        kwargs['times'] = times
        kwargs['values'] = values
        kwargs['interpolation'] = interpolation
        super(ColorKeyframeTrack, self).__init__(**kwargs)

    _model_name = Unicode('ColorKeyframeTrackModel').tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    ColorKeyframeTrack.__signature__ = inspect.signature(ColorKeyframeTrack.__init__)
