True = true;
False = false;
require.config({
  paths: {
    'extjs': 'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/ext-all-debug',
    'extjs-charts': 'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/packages/charts/classic/charts-debug'
  }
});
require(['extjs'],function(application,defaults,config){
  require(['extjs-charts']);
});