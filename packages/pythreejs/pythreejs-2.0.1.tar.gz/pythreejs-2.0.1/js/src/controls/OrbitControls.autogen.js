//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var ControlsModel = require('./Controls.autogen.js').ControlsModel;


var OrbitControlsModel = ControlsModel.extend({

    defaults: function() {
        return _.extend(ControlsModel.prototype.defaults.call(this), {

            autoRotate: false,
            autoRotateSpeed: 2,
            dampingFactor: 0.25,
            enabled: true,
            enableDamping: false,
            enableKeys: true,
            enablePan: true,
            enableRotate: true,
            enableZoom: true,
            keyPanSpeed: 7,
            maxAzimuthAngle: Infinity,
            maxDistance: Infinity,
            maxPolarAngle: 3.141592653589793,
            maxZoom: Infinity,
            minAzimuthAngle: -Infinity,
            minDistance: 0,
            minPolarAngle: 0,
            minZoom: 0,
            panSpeed: 1,
            rotateSpeed: 1,
            screenSpacePanning: true,
            zoomSpeed: 1,
            target: [0,0,0],

        });
    },

    constructThreeObject: function() {

        var result = new THREE.OrbitControls(
            this.convertThreeTypeModelToThree(this.get('controlling'), 'controlling')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        ControlsModel.prototype.createPropertiesArrays.call(this);


        this.property_converters['autoRotate'] = 'convertBool';
        this.property_converters['autoRotateSpeed'] = 'convertFloat';
        this.property_converters['dampingFactor'] = 'convertFloat';
        this.property_converters['enabled'] = 'convertBool';
        this.property_converters['enableDamping'] = 'convertBool';
        this.property_converters['enableKeys'] = 'convertBool';
        this.property_converters['enablePan'] = 'convertBool';
        this.property_converters['enableRotate'] = 'convertBool';
        this.property_converters['enableZoom'] = 'convertBool';
        this.property_converters['keyPanSpeed'] = 'convertFloat';
        this.property_converters['maxAzimuthAngle'] = 'convertFloat';
        this.property_converters['maxDistance'] = 'convertFloat';
        this.property_converters['maxPolarAngle'] = 'convertFloat';
        this.property_converters['maxZoom'] = 'convertFloat';
        this.property_converters['minAzimuthAngle'] = 'convertFloat';
        this.property_converters['minDistance'] = 'convertFloat';
        this.property_converters['minPolarAngle'] = 'convertFloat';
        this.property_converters['minZoom'] = 'convertFloat';
        this.property_converters['panSpeed'] = 'convertFloat';
        this.property_converters['rotateSpeed'] = 'convertFloat';
        this.property_converters['screenSpacePanning'] = 'convertBool';
        this.property_converters['zoomSpeed'] = 'convertFloat';
        this.property_converters['target'] = 'convertVector';

        this.property_assigners['target'] = 'assignVector';

    },

}, {

    model_name: 'OrbitControlsModel',

    serializers: _.extend({
    },  ControlsModel.serializers),
});

module.exports = {
    OrbitControlsModel: OrbitControlsModel,
};
