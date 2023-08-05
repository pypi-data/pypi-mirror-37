//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var BaseGeometryModel = require('../core/BaseGeometry.autogen.js').BaseGeometryModel;


var TetrahedronGeometryModel = BaseGeometryModel.extend({

    defaults: function() {
        return _.extend(BaseGeometryModel.prototype.defaults.call(this), {

            radius: 1,
            detail: 0,
            type: "TetrahedronGeometry",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.TetrahedronGeometry(
            this.convertFloatModelToThree(this.get('radius'), 'radius'),
            this.get('detail')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        BaseGeometryModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;

        this.property_converters['radius'] = 'convertFloat';
        this.property_converters['detail'] = null;
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'TetrahedronGeometryModel',

    serializers: _.extend({
    },  BaseGeometryModel.serializers),
});

module.exports = {
    TetrahedronGeometryModel: TetrahedronGeometryModel,
};
