//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var MeshModel = require('./Mesh.js').MeshModel;

var LineMaterialModel = require('../materials/LineMaterial.js').LineMaterialModel;
var LineSegmentsGeometryModel = require('../geometries/LineSegmentsGeometry.js').LineSegmentsGeometryModel;

var LineSegments2Model = MeshModel.extend({

    defaults: function() {
        return _.extend(MeshModel.prototype.defaults.call(this), {

            material: 'uninitialized',
            geometry: 'uninitialized',
            type: "LineSegments2",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.LineSegments2(
            this.convertThreeTypeModelToThree(this.get('geometry'), 'geometry'),
            this.convertThreeTypeModelToThree(this.get('material'), 'material')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        MeshModel.prototype.createPropertiesArrays.call(this);
        this.three_properties.push('material');
        this.three_properties.push('geometry');

        this.props_created_by_three['geometry'] = true;
        this.props_created_by_three['material'] = true;
        this.props_created_by_three['morphTargetInfluences'] = true;
        this.props_created_by_three['type'] = true;
        this.props_created_by_three['rotation'] = true;
        this.props_created_by_three['quaternion'] = true;
        this.props_created_by_three['matrixWorldNeedsUpdate'] = true;

        this.property_converters['material'] = 'convertThreeType';
        this.property_converters['geometry'] = 'convertThreeType';
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'LineSegments2Model',

    serializers: _.extend({
        material: { deserialize: serializers.unpackThreeModel },
        geometry: { deserialize: serializers.unpackThreeModel },
    },  MeshModel.serializers),
});

module.exports = {
    LineSegments2Model: LineSegments2Model,
};
