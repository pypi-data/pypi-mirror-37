//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var MaterialModel = require('./Material.js').MaterialModel;

var TextureModel = require('../textures/Texture.autogen.js').TextureModel;

var MeshMatcapMaterialModel = MaterialModel.extend({

    defaults: function() {
        return _.extend(MaterialModel.prototype.defaults.call(this), {

            alphaMap: null,
            bumpMap: null,
            bumpScale: 1,
            color: "#ffffff",
            displacementMap: null,
            displacementScale: 1,
            displacementBias: 0,
            lights: false,
            map: null,
            matcap: null,
            morphNormals: false,
            morphTargets: false,
            normalMap: null,
            normalScale: [1,1],
            skinning: false,
            type: "MeshMatcapMaterial",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.MeshMatcapMaterial(
            {
                alphaMap: this.convertThreeTypeModelToThree(this.get('alphaMap'), 'alphaMap'),
                bumpMap: this.convertThreeTypeModelToThree(this.get('bumpMap'), 'bumpMap'),
                bumpScale: this.convertFloatModelToThree(this.get('bumpScale'), 'bumpScale'),
                color: this.convertColorModelToThree(this.get('color'), 'color'),
                displacementMap: this.convertThreeTypeModelToThree(this.get('displacementMap'), 'displacementMap'),
                displacementScale: this.convertFloatModelToThree(this.get('displacementScale'), 'displacementScale'),
                displacementBias: this.convertFloatModelToThree(this.get('displacementBias'), 'displacementBias'),
                lights: this.convertBoolModelToThree(this.get('lights'), 'lights'),
                map: this.convertThreeTypeModelToThree(this.get('map'), 'map'),
                matcap: this.convertThreeTypeModelToThree(this.get('matcap'), 'matcap'),
                morphNormals: this.convertBoolModelToThree(this.get('morphNormals'), 'morphNormals'),
                morphTargets: this.convertBoolModelToThree(this.get('morphTargets'), 'morphTargets'),
                normalMap: this.convertThreeTypeModelToThree(this.get('normalMap'), 'normalMap'),
                normalScale: this.convertVectorModelToThree(this.get('normalScale'), 'normalScale'),
                skinning: this.convertBoolModelToThree(this.get('skinning'), 'skinning'),
                type: this.get('type'),
            }
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        MaterialModel.prototype.createPropertiesArrays.call(this);
        this.three_properties.push('alphaMap');
        this.three_properties.push('bumpMap');
        this.three_properties.push('displacementMap');
        this.three_properties.push('map');
        this.three_properties.push('matcap');
        this.three_properties.push('normalMap');

        this.props_created_by_three['type'] = true;

        this.property_converters['alphaMap'] = 'convertThreeType';
        this.property_converters['bumpMap'] = 'convertThreeType';
        this.property_converters['bumpScale'] = 'convertFloat';
        this.property_converters['color'] = 'convertColor';
        this.property_converters['displacementMap'] = 'convertThreeType';
        this.property_converters['displacementScale'] = 'convertFloat';
        this.property_converters['displacementBias'] = 'convertFloat';
        this.property_converters['lights'] = 'convertBool';
        this.property_converters['map'] = 'convertThreeType';
        this.property_converters['matcap'] = 'convertThreeType';
        this.property_converters['morphNormals'] = 'convertBool';
        this.property_converters['morphTargets'] = 'convertBool';
        this.property_converters['normalMap'] = 'convertThreeType';
        this.property_converters['normalScale'] = 'convertVector';
        this.property_converters['skinning'] = 'convertBool';
        this.property_converters['type'] = null;

        this.property_assigners['normalScale'] = 'assignVector';

    },

}, {

    model_name: 'MeshMatcapMaterialModel',

    serializers: _.extend({
        alphaMap: { deserialize: serializers.unpackThreeModel },
        bumpMap: { deserialize: serializers.unpackThreeModel },
        displacementMap: { deserialize: serializers.unpackThreeModel },
        map: { deserialize: serializers.unpackThreeModel },
        matcap: { deserialize: serializers.unpackThreeModel },
        normalMap: { deserialize: serializers.unpackThreeModel },
    },  MaterialModel.serializers),
});

module.exports = {
    MeshMatcapMaterialModel: MeshMatcapMaterialModel,
};
