//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var MaterialModel = require('./Material.js').MaterialModel;


var LineMaterialModel = MaterialModel.extend({

    defaults: function() {
        return _.extend(MaterialModel.prototype.defaults.call(this), {

            color: "#ffffff",
            fog: false,
            lights: false,
            linewidth: 1,
            dashScale: 1,
            dashSize: 1,
            gapSize: 1,
            type: "LineMaterial",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.LineMaterial(
            {
                color: this.convertColorModelToThree(this.get('color'), 'color'),
                fog: this.convertBoolModelToThree(this.get('fog'), 'fog'),
                lights: this.convertBoolModelToThree(this.get('lights'), 'lights'),
                linewidth: this.convertFloatModelToThree(this.get('linewidth'), 'linewidth'),
                dashScale: this.convertFloatModelToThree(this.get('dashScale'), 'dashScale'),
                dashSize: this.convertFloatModelToThree(this.get('dashSize'), 'dashSize'),
                gapSize: this.convertFloatModelToThree(this.get('gapSize'), 'gapSize'),
                type: this.get('type'),
            }
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        MaterialModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;

        this.property_converters['color'] = 'convertColor';
        this.property_converters['fog'] = 'convertBool';
        this.property_converters['lights'] = 'convertBool';
        this.property_converters['linewidth'] = 'convertFloat';
        this.property_converters['dashScale'] = 'convertFloat';
        this.property_converters['dashSize'] = 'convertFloat';
        this.property_converters['gapSize'] = 'convertFloat';
        this.property_converters['type'] = null;


    },

}, {

    model_name: 'LineMaterialModel',

    serializers: _.extend({
    },  MaterialModel.serializers),
});

module.exports = {
    LineMaterialModel: LineMaterialModel,
};
