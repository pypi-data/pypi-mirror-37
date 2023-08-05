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

from .Material import Material

from ..textures.Texture_autogen import Texture
from ..textures.CubeTexture_autogen import CubeTexture

@register
class MeshPhongMaterial(Material):
    """MeshPhongMaterial

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/materials/MeshPhongMaterial
    """

    _model_name = Unicode('MeshPhongMaterialModel').tag(sync=True)

    alphaMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    aoMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    aoMapIntensity = CFloat(1, allow_none=False).tag(sync=True)

    bumpMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    bumpScale = CFloat(1, allow_none=False).tag(sync=True)

    color = Color("#ffffff", allow_none=False).tag(sync=True)

    combine = Enum(Operations, "MultiplyOperation", allow_none=False).tag(sync=True)

    displacementMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    displacementScale = CFloat(1, allow_none=False).tag(sync=True)

    displacementBias = CFloat(0, allow_none=False).tag(sync=True)

    emissive = Color("#000000", allow_none=False).tag(sync=True)

    emissiveMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    emissiveIntensity = CFloat(1, allow_none=False).tag(sync=True)

    envMap = Instance(CubeTexture, allow_none=True).tag(sync=True, **widget_serialization)

    lightMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    lightMapIntensity = CFloat(1, allow_none=False).tag(sync=True)

    map = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    morphNormals = Bool(False, allow_none=False).tag(sync=True)

    morphTargets = Bool(False, allow_none=False).tag(sync=True)

    normalMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    normalScale = Vector2(default_value=[1, 1]).tag(sync=True)

    reflectivity = CFloat(1, allow_none=False).tag(sync=True)

    refractionRatio = CFloat(0.98, allow_none=False).tag(sync=True)

    shininess = CFloat(30, allow_none=False).tag(sync=True)

    skinning = Bool(False, allow_none=False).tag(sync=True)

    specular = Color("#111111", allow_none=False).tag(sync=True)

    specularMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    wireframe = Bool(False, allow_none=False).tag(sync=True)

    wireframeLinewidth = CFloat(1, allow_none=False).tag(sync=True)

    wireframeLinecap = Unicode("round", allow_none=False).tag(sync=True)

    wireframeLinejoin = Unicode("round", allow_none=False).tag(sync=True)

    type = Unicode("MeshPhongMaterial", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    MeshPhongMaterial.__signature__ = inspect.signature(MeshPhongMaterial.__init__)
