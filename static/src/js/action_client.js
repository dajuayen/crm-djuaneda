odoo.define('sdi_crm_kanban', function (require){
"use strict";
// require original module JS
var KanbanModel = require('web.KanbanModel');
var sdi_kanban = KanbanModel.include({


openerp.guard_payments = function(instance, local) {
var _t = instance.web._t,
    _lt = instance.web._lt;
var QWeb = instance.web.qweb;

local.HomePage = instance.Widget.extend({
    template: 'MyQWebTemplate',
    init: function(parent, options){
      this._super.apply(this, arguments);
      this.name=parent.name;
    },
    start: function() {
      this._super.apply(this, arguments);
      console.log('Widget Start')
    },
});

//Following code will attach the above widget to the defined client action

instance.web.client_actions.add('report.report_page', 'instance.guard_payments.HomePage');
}
