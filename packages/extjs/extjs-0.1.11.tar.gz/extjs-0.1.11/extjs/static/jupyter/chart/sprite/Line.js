Ext.define('jupyter.chart.sprite.Line',{
  extend:'Ext.chart.series.sprite.Line',
  alias:'sprite.jline',
  drawMarker: function(x, y, index){
    if(this.getSeries().isMarked(this,x,y,index))
      this.callParent(arguments);
  }
});