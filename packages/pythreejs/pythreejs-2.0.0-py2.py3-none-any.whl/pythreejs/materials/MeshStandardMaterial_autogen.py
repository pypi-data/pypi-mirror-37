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
class MeshStandardMaterial(Material):
    """MeshStandardMaterial

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/materials/MeshStandardMaterial
    """

    _model_name = Unicode('MeshStandardMaterialModel').tag(sync=True)

    alphaMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    aoMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    aoMapIntensity = CFloat(1, allow_none=False).tag(sync=True)

    bumpMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    bumpScale = CFloat(1, allow_none=False).tag(sync=True)

    color = Color("#ffffff", allow_none=False).tag(sync=True)

    defines = Dict(default_value={"STANDARD":""}, allow_none=True).tag(sync=True)

    displacementMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    displacementScale = CFloat(1, allow_none=False).tag(sync=True)

    displacementBias = CFloat(0, allow_none=False).tag(sync=True)

    emissive = Color("#000000", allow_none=False).tag(sync=True)

    emissiveMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    emissiveIntensity = CFloat(1, allow_none=False).tag(sync=True)

    envMap = Instance(CubeTexture, allow_none=True).tag(sync=True, **widget_serialization)

    envMapIntensity = CFloat(1, allow_none=False).tag(sync=True)

    lightMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    lightMapIntensity = CFloat(1, allow_none=False).tag(sync=True)

    map = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    metalness = CFloat(0.5, allow_none=False).tag(sync=True)

    metalnessMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    morphTargets = Bool(False, allow_none=False).tag(sync=True)

    morphNormals = Bool(False, allow_none=False).tag(sync=True)

    normalMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    normalScale = Vector2(default_value=[1, 1]).tag(sync=True)

    refractionRatio = CFloat(0.98, allow_none=False).tag(sync=True)

    roughness = CFloat(0.5, allow_none=False).tag(sync=True)

    roughnessMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    skinning = Bool(False, allow_none=False).tag(sync=True)

    wireframe = Bool(False, allow_none=False).tag(sync=True)

    wireframeLinecap = Unicode("round", allow_none=False).tag(sync=True)

    wireframeLinejoin = Unicode("round", allow_none=False).tag(sync=True)

    wireframeLinewidth = CFloat(1, allow_none=False).tag(sync=True)

    type = Unicode("MeshStandardMaterial", allow_none=False).tag(sync=True)


if six.PY3:
    import inspect
    # Include explicit signature since the metaclass screws it up
    MeshStandardMaterial.__signature__ = inspect.signature(MeshStandardMaterial.__init__)
