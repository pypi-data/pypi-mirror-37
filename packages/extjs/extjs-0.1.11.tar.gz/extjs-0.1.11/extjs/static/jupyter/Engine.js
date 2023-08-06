Ext.define('jupyter.Engine',{
  statics: {
    execute : function(cmd,callback,withTimeout){
      var kernel = IPython.notebook.kernel;
      var me = this;
      var callbacks  = {
        iopub : {
          output : function(msg){
            var content = msg.content,
                data = content.data;
            if( data ){
              console.log('Has got a response: ' + data);
              callback(Ext.decode(data['text/plain']));
            } else if (msg.content.evalue){
              var stacktrace = content.traceback.join('\n');
              stacktrace = stacktrace.replace(new RegExp('\\[(0|1);3.m','g'),'').replace(new RegExp('\\[0m','g'),'')
              console.warn('"' + cmd + '" failed. \n' + content.evalue + '\n' + stacktrace);
            }
          }
        }
      };
      console.log('Running: ' + cmd);
      if(withTimeout)
        setTimeout(function(){
          kernel.execute(cmd,callbacks,{silent:false})
        },200);
      else
        kernel.execute(cmd,callbacks,{silent:false})
    }
  }
});