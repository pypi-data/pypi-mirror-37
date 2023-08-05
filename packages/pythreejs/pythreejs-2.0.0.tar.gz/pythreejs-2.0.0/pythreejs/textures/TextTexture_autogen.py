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

from .Texture_autogen import Texture


@register
class TextTexture(Texture):
    """TextTexture

    Autogenerated by generate-wrappers.js
    This class is a custom class for pythreejs, with no
    direct corresponding class in three.js.
    """

    def __init__(self, string="", **kwargs):
        kwargs['string'] = string
        super(TextTexture, self).__init__(**kwargs)

    _model_name = Unicode('TextTextureModel').tag(sync=True)

    color = Color("white", allow_none=False).tag(sync=True)

    fontFace = Unicode("Arial", allow_none=False).tag(sync=True)

    size = CInt(12, allow_none=False).tag(sync=True)

    string = Unicode("", allow_none=False).tag(sync=True)

    squareTexture = Bool(True, allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    TextTexture.__signature__ = inspect.signature(TextTexture.__init__)
