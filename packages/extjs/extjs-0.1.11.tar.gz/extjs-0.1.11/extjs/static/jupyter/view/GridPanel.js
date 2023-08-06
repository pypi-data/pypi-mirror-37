Ext.define('jupyter.view.GridPanel', {
  extend: 'Ext.grid.Panel',
  alias: 'widget.jgrid',
  requires : ['jupyter.store.JupyterProxy','Ext.grid.plugin.Exporter','Ext.exporter.text.CSV'],
  plugins: ['gridfilters','gridexporter'],
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
    command : undefined,
    /**
     * Show the id column
     */
    showIdColumn : false
  },
  _params : {},
  getParams:function() { 
    return this._params;
  },
  setParams:function(value) { 
    this._params = value;
    this.getSelectionModel().deselectAll();
    this.getStore().load( value );
  },
  store: {
    type: 'store',
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
    this.store.on('metachange',function(store, meta) {
      var cols = me.showIdColumn ? meta.colModel : meta.colModel.slice(1);
      me.reconfigure(store,cols);
    });
    this.callParent(arguments);
  }
});
