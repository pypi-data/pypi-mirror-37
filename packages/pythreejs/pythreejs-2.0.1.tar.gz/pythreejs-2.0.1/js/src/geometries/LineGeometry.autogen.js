//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var LineSegmentsGeometryModel = require('./LineSegmentsGeometry.js').LineSegmentsGeometryModel;


var LineGeometryModel = LineSegmentsGeometryModel.extend({

    defaults: function() {
        return _.extend(LineSegmentsGeometryModel.prototype.defaults.call(this), {

            positions: undefined,
            colors: null,
            type: "LineGeometry",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.LineGeometry();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        LineSegmentsGeometryModel.prototype.createPropertiesArrays.call(this);
        this.datawidget_properties.push('positions');
        this.datawidget_properties.push('colors');

        this.props_created_by_three['type'] = true;

        this.property_converters['positions'] = 'convertArrayBuffer';
        this.property_converters['colors'] = 'convertArrayBuffer';
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'LineGeometryModel',

    serializers: _.extend({
        positions: dataserializers.data_union_serialization,
        colors: dataserializers.data_union_serialization,
    },  LineSegmentsGeometryModel.serializers),
});

module.exports = {
    LineGeometryModel: LineGeometryModel,
};
