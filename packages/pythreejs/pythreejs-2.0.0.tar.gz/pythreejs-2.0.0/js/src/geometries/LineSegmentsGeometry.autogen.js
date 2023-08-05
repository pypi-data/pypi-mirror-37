//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var BaseBufferGeometryModel = require('../core/BaseBufferGeometry.autogen.js').BaseBufferGeometryModel;


var LineSegmentsGeometryModel = BaseBufferGeometryModel.extend({

    defaults: function() {
        return _.extend(BaseBufferGeometryModel.prototype.defaults.call(this), {

            positions: undefined,
            colors: null,
            type: "LineSegmentsGeometry",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.LineSegmentsGeometry();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        BaseBufferGeometryModel.prototype.createPropertiesArrays.call(this);
        this.datawidget_properties.push('positions');
        this.datawidget_properties.push('colors');

        this.props_created_by_three['type'] = true;

        this.property_converters['positions'] = 'convertArrayBuffer';
        this.property_converters['colors'] = 'convertArrayBuffer';
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'LineSegmentsGeometryModel',

    serializers: _.extend({
        positions: dataserializers.data_union_serialization,
        colors: dataserializers.data_union_serialization,
    },  BaseBufferGeometryModel.serializers),
});

module.exports = {
    LineSegmentsGeometryModel: LineSegmentsGeometryModel,
};
