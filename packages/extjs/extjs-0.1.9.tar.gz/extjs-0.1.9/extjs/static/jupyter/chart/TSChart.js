Ext.define('jupyter.chart.TSChart', {
  extend: 'Ext.chart.CartesianChart',
  alias: 'widget.tsChart',
  requires : ['jupyter.store.JupyterProxy','jupyter.chart.sprite.Line'],
  config : {
    /**
     * Python command which needs to be run to get a data
     */
    command : undefined
  },
  highlight:true,
  store: {
    type: 'store',
    autoLoad:true,
    proxy: {
      type : 'jupyter'
    }
  },
  legend: {
    type: 'sprite',
    docked: 'right'
  },
  interactions: {
    type: 'crosszoom',
    itemId:'crosszoom',
    zoomOnPanGesture: false
  },
  tbar: ['->',{
    text: 'Undo Zoom',
    handler: function(btn){
      btn.up('chart').down('interaction').getUndoButton().handler();
    }
  }],
  axes: [{
    type: 'numeric',
    position: 'left',
    grid: true,
    renderer: function(axis,label,layoutContext,lastLabel){
      return Ext.util.Format.number(label,'0,000');
    }
  }, {
    type: 'time',
    position: 'bottom',
    fields: ['id'],
    renderer: function(axis,label,layoutContext,lastLabel){
      return Ext.Date.format(label,'d.m.Y');
    },
    title: {
      text: 'P&L'
    }
  }],
  initComponent : function(){
    this.callParent(arguments);
    if( !this.store.storeId )
      this.store.storeId = this.getItemId();
    this.store = Ext.data.StoreManager.lookup(this.store);
    var proxy = this.store.getProxy();
    proxy.setCommand( this.getCommand() );
    var me = this;
    this.store.on({
      load: function( store, records, successful, operation, eOpts ){
        var series = [];
//        me.setLegend( new Ext.chart.legend.SpriteLegend({docked: 'right'}) );
        if(records.length>0){
          var keys = Object.keys(records[0].data);
          for(var i in keys){
            var key = keys[ i ];
            if( key != 'id' ){
              //series.push( new Ext.chart.series.Line({chart:me,xField: 'id',yField: key}) );
              series.push(me.getSeriesConfig(key));
            }
          }
        }
        me.setSeries( series );
      }
    });
  },
  getSeriesConfig : function(field){
    return {
      type:'line',
      xField: 'id',
      yField: field,
      tooltip: {
        trackMouse: true,
        showDelay: 0,
        dismissDelay: 0,
        hideDelay: 0,
        renderer: function (tooltip, record, item) {
          tooltip.setHtml('<b>'+item.field+'</b><br/>'+ Ext.Date.format(record.data.id,'d-m-Y') + ' : ' + record.data[item.field]);
        }
      }
    };
  },
  series: []
});