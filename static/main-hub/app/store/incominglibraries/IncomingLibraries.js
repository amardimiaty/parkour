Ext.define('MainHub.store.incominglibraries.IncomingLibraries', {
  extend: 'Ext.data.Store',
  storeId: 'IncomingLibraries',

  requires: [
    'MainHub.model.incominglibraries.IncomingLibraries'
  ],

  model: 'MainHub.model.incominglibraries.IncomingLibraries',

  groupField: 'request',
  groupDir: 'DESC',

  proxy: {
    type: 'ajax',
    timeout: 1000000,
    pageParam: false,   // to remove param "page"
    startParam: false,  // to remove param "start"
    limitParam: false,  // to remove param "limit"
    noCache: false,     // to remove param "_dc",
    api: {
      read: 'api/incoming_libraries/',
      update: 'api/incoming_libraries/edit/'
    },
    reader: {
      type: 'json',
      rootProperty: 'data',
      successProperty: 'success',
      messageProperty: 'message'
    },
    writer: {
      type: 'json',
      rootProperty: 'data',
      transform: {
        fn: function (data, request) {
          if (!(data instanceof Array)) {
            data = [data];
          }

          var store = Ext.getStore('IncomingLibraries');
          var newData = _.map(data, function (item) {
            var record = store.findRecord('id', item.id, 0, false, true, true);
            if (record) {
              return Ext.Object.merge({
                pk: record.get('pk'),
                record_type: record.get('record_type')
              }, record.getChanges());
            }
          });

          return newData;
        },
        scope: this
      }
    }
  },

  getId: function () {
    return 'IncomingLibraries';
  }
});
