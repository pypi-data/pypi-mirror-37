Ext.define('jupyter.store.JupyterProxy', {
  extend: 'Ext.data.proxy.Ajax',
  alias: 'proxy.jupyter',
  requires:['jupyter.Engine'],
  config : {
    /**
     * Python command which needs to be run to get a data
     */
    command : undefined
  },
  reader:{
    rootProperty : 'rows'
  },
  updateCommand: function(newValue,oldValue){
    if( newValue ) {
      var me = this;
      jupyter.Engine.execute('import inspect;list(inspect.signature(' + newValue + ').parameters.keys())',function(data){
        me.pythonParams = data;
      });
    }
  },
  doRequest: function(operation) {
    var cmd = this.getCommand();
    if( cmd.indexOf('(') == -1 ){
      var params = operation.getId();
      if( !params ){
        params = this.getExtraParams();
        if( Ext.Object.isEmpty( params ) ){
          params ={};
          for(var i in this.pythonParams){
            param = this.pythonParams[ i ];
            params[ param ] = operation[ param ]; 
          }
        }
        params = '**' + Ext.encode(params).replace(/:null/g,':None');
      } else
        params = params == 'root' ? -1 : params;
      cmd = 'extjs.to_message(' + cmd+'(' + params + ') )';
    }
    var me = this;
    jupyter.Engine.execute(cmd,function(data){
      jupyter.store.JupyterProxy.readData(data);
      var reader = me.getReader();
      if( data.metaData )
        me.fireEvent('metachange', me, data.metaData);
      var resultSet = reader.read(data, {recordCreator: operation.getRecordCreator()});
      operation.setResultSet(resultSet);
      operation.setSuccessful(true);
    },this.getCommand() == 'kbs');//todo refactor kbs
  },
  readColumns : function(grid){
    var me = this;
    jupyter.Engine.execute('import json\njson.dumps((lambda s : [[n,s[n].name] for n in s.index])(' + this.getCommand() + '().dtypes))',function(data){
      data = Ext.decode(data);
      var gridView = grid.getView();
      var columns = grid.columns;
      if( !Array.isArray(columns) ) {
        if( columns.items == undefined )
          columns.items = [];
        columns = columns.items;
      }
      var idx = columns.length;
      var floatRenderer = Ext.util.Format.numberRenderer('0,000.00');
      var defaults = grid.config.columns && grid.config.columns.defaults;
      if( defaults ){
        var renderer = defaults.renderer;
        if( renderer ){
          var originalRenderer = floatRenderer;
          floatRenderer = function(value, meta, record, ixRow, ixCol, store, view){
            value = originalRenderer( value, meta, record, ixRow, ixCol, store, view );
            return renderer( value, meta, record, ixRow, ixCol, store, view );
          }
        }
      }
      var types = [],
          isTree = gridView.xtype == 'treeview';
      for( var i in data ){
        var c = data[ i ][0]
            ,t = data[ i ][1];
        types.push(t);
        if( i == 0 && isTree ){
          columns[0].dataIndex = c;
          columns[0].setText( c );
        } else{ 
          var column = {
            xtype: 'gridcolumn',
            text: c,
            dataIndex: c,
            //width: 150,
            flex: 1
          };
          if( t == 'float64' ){
            Ext.applyIf( column, {
              align: 'right',
              renderer: floatRenderer
            });
          }
          gridView.headerCt.insert( idx++, Ext.create(column) );
        }
      } 
      me.pythonColumnTypes = types;
      //gridView.refresh();
    });
  },
  statics: {
    readData: function(data,operation) {
      var rows = Ext.util.CSV.decode(data.rows);
      var columns = rows[0];
      rows = rows.slice(1);
      for(var i=0;i<rows.length;++i){
        var row = rows[ i ];
        var obj = {};
        for(var j=0;j<columns.length;++j)
          obj[ columns[ j ] ] = row[ j ];
        rows[ i ] = obj;
      }
      data.rows = rows;
    }
  }
});