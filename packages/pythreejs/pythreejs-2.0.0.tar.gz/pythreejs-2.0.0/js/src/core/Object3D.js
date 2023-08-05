var _ = require('underscore');
var Object3DAutogen = require('./Object3D.autogen').Object3DModel;

var Object3DModel = Object3DAutogen.extend({

    createPropertiesArrays: function() {
        Object3DAutogen.prototype.createPropertiesArrays.call(this);

        this.property_assigners['children'] = 'assignChildren';
    },

    assignChildren: function(obj, key, value) {
        var old = obj[key];
        var removed = _.difference(old, value);
        var added = _.difference(value, old);
        if (removed.length > 0) {
            obj.remove.apply(obj, removed);
        }
        if (added.length > 0) {
            obj.add.apply(obj, added);
        }
    }

});

module.exports = {
    Object3DModel: Object3DModel,
};
