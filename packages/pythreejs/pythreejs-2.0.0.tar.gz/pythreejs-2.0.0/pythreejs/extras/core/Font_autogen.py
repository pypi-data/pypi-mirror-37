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
class Font(ThreeWidget):
    """Font

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/extras/core/Font
    """

    def __init__(self, **kwargs):
        super(Font, self).__init__(**kwargs)

    _model_name = Unicode('FontModel').tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    Font.__signature__ = inspect.signature(Font.__init__)
