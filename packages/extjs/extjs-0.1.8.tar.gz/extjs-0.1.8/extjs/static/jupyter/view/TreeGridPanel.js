Ext.define('jupyter.view.TreeGridPanel', {
  extend: 'Ext.tree.Panel',
  alias: 'widget.jtree',
  requires : ['jupyter.store.JupyterProxy','Ext.grid.plugin.Exporter','Ext.exporter.text.CSV'],
  //plugins: ['gridfilters','gridexporter'],
  rootVisible: false,
  applyStore: function(store) {
    var store = this.callParent(arguments);
    store.getProxy().readColumns(this); 
    return store;
  },
  columns: [{
    xtype: 'treecolumn',
    dataIndex: 'Name',
    flex: 2
  }],
  tools: [{
    iconCls: 'frtb-excel',
    handler: function() {
      this.up('grid').saveDocumentAs({ type : 'csv' });
    }
  }],
  config : {
    /**
     * Python command which needs to be run to get a data
     */
    command : undefined
  },
  store: {
    type: 'tree',
    proxy: {
      type : 'jupyter'
    }
  },
  initComponent : function(){
    if( this.reference == undefined && this.itemId )
      this.reference = this.itemId;
    if( !this.store.storeId )
      this.store.storeId = this.getItemId();
    if( this.autoLoad )
      this.store.autoLoad = true;
    this.store = Ext.data.StoreManager.lookup(this.store);
    var proxy = this.store.getProxy();
    proxy.setCommand( this.getCommand() );
    var me = this;
    /*this.store.on('metachange',function(store, meta) {
      me.reconfigure(store,meta.colModel);
    });*/
    this.callParent(arguments);
  }
});
