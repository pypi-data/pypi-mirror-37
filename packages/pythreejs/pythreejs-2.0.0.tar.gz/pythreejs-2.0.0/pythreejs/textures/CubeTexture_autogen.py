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
class CubeTexture(Texture):
    """CubeTexture

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/textures/CubeTexture
    """

    def __init__(self, images=[], mapping="UVMapping", wrapS="ClampToEdgeWrapping", wrapT="ClampToEdgeWrapping", magFilter="LinearFilter", minFilter="LinearMipMapLinearFilter", format="RGBAFormat", type="UnsignedByteType", anisotropy=1, **kwargs):
        kwargs['images'] = images
        kwargs['mapping'] = mapping
        kwargs['wrapS'] = wrapS
        kwargs['wrapT'] = wrapT
        kwargs['magFilter'] = magFilter
        kwargs['minFilter'] = minFilter
        kwargs['format'] = format
        kwargs['type'] = type
        kwargs['anisotropy'] = anisotropy
        super(CubeTexture, self).__init__(**kwargs)

    _model_name = Unicode('CubeTextureModel').tag(sync=True)

    images = List().tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    CubeTexture.__signature__ = inspect.signature(CubeTexture.__init__)
