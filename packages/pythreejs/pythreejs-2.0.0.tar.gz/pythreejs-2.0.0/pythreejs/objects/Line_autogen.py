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

from ..materials.Material import Material
from ..core.BaseGeometry_autogen import BaseGeometry
from ..core.BaseBufferGeometry_autogen import BaseBufferGeometry

@register
class Line(Object3D):
    """Line

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/objects/Line
    """

    def __init__(self, geometry=None, material=None, **kwargs):
        kwargs['geometry'] = geometry
        kwargs['material'] = material
        super(Line, self).__init__(**kwargs)

    _model_name = Unicode('LineModel').tag(sync=True)

    material = Instance(Material, allow_none=True).tag(sync=True, **widget_serialization)

    geometry = Union([
        Instance(BaseGeometry, allow_none=True),
        Instance(BaseBufferGeometry, allow_none=True)
    ]).tag(sync=True, **widget_serialization)

    type = Unicode("Line", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    Line.__signature__ = inspect.signature(Line.__init__)
