odoo.define('sdi_crm_kanban', function (require){
"use strict";
// require original module JS
var KanbanModel = require('web.KanbanModel');
var sdi_kanban = KanbanModel.include({
    /**
     @override
     */
    moveRecord: function (recordID, groupID, parentID) {
        console.log('************************************');

        var self = this;
        var parent = this.localData[parentID];
        var new_group = this.localData[groupID];
        var changes = {};
        var groupedFieldName = parent.groupedBy[0];
        var groupedField = parent.fields[groupedFieldName];
        if (groupedField.type === 'many2one') {
            changes[groupedFieldName] = {
                id: new_group.res_id,
                display_name: new_group.value,
            };

        } else if (groupedField.type === 'selection') {
            var value = _.findWhere(groupedField.selection, {1: new_group.value});
            changes[groupedFieldName] = value && value[0] || false;
        } else {
            changes[groupedFieldName] = new_group.value;
        }

        // Manually updates groups data. Note: this is done before the actual
        // save as it might need to perform a read group in some cases so those
        // updated data might be overriden again.
        var record = self.localData[recordID];
        var resID = record.res_id;
        // Remove record from its current group
        var old_group;
        for (var i = 0; i < parent.data.length; i++) {
            old_group = self.localData[parent.data[i]];
            var index = _.indexOf(old_group.data, recordID);
            if (index >= 0) {
                old_group.data.splice(index, 1);
                old_group.count--;
                old_group.res_ids = _.without(old_group.res_ids, resID);
                self._updateParentResIDs(old_group);
                break;
            }
        }
        if(groupedFieldName==='stage_id'){
            changes['previous_stage_id'] = {
                id: old_group.res_id,
                display_name: old_group.value,
            };
        }
        // Add record to its new group
        new_group.data.push(recordID);
        new_group.res_ids.push(resID);
        new_group.count++;

        return this.notifyChanges(recordID, changes).then(function () {
            return self.save(recordID);
        }).then(function () {
            record.parentID = new_group.id;
            return [old_group.id, new_group.id];
        });
    },
    /**
     * @override
     */
    reload: function (id, options) {
        // if the groupBy is given in the options and if it is an empty array,
        // fallback on the default groupBy
        if (options && options.groupBy && !options.groupBy.length) {
            options.groupBy = this.defaultGroupedBy;
        }
        var def = this._super(id, options);
        return this._reloadProgressBarGroupFromRecord(id, def);
    },
    prueba: $('.modal-dialog .modal-footer button').on('click', function(event) {
          var $button = $(event.target); // The clicked button
           alert('jujuuuuuuuuuuuuuuuuuuuuuuuu');
          $(this).closest('.modal').one('hidden.bs.modal', function() {
            // Fire if the button element
            console.log('The button that closed the modal is: ', $button);
          });
    }),
});

return sdi_kanban;
});

