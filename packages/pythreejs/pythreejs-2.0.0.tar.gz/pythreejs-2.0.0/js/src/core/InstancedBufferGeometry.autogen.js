//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var BufferGeometryModel = require('./BufferGeometry.js').BufferGeometryModel;


var InstancedBufferGeometryModel = BufferGeometryModel.extend({

    defaults: function() {
        return _.extend(BufferGeometryModel.prototype.defaults.call(this), {

            maxInstancedCount: null,
            type: "InstancedBufferGeometry",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.InstancedBufferGeometry();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        BufferGeometryModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;

        this.property_converters['maxInstancedCount'] = null;
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'InstancedBufferGeometryModel',

    serializers: _.extend({
    },  BufferGeometryModel.serializers),
});

module.exports = {
    InstancedBufferGeometryModel: InstancedBufferGeometryModel,
};
