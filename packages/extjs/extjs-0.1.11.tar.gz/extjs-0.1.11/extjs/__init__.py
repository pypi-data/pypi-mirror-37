from ._version import version_info, __version__

from IPython.display import display,Javascript
import numpy as np
import pandas as pd

def app(app,viewClass=None, controllers=None, config={'height': 800}):
  capitalizedApp = app.capitalize()
  if viewClass is None:
    viewClass = '{}.view.{}Panel'.format(app,capitalizedApp)

  code = '''
    var out = this.element[0];
    function initUI() {{
      Ext.application({{
        name: '{}',
        paths: {{
          'jupyter' : '/nbextensions/jupyter-extjs/jupyter',
          'Ext' : '/nbextensions/jupyter-extjs/Ext',
          '{}' : '/files/extjs/{}'
        }},
        {}
        launch: function () {{
          Ext.override(Ext.draw.modifier.Target,{{
            applyChanges : function(){{
              if( this.getSprite() )
                originalApplyChanges.apply(this,arguments);
            }}
          }});
          console.log('Ext.draw.modifier.Target has been patched');
          Ext.syncRequire('{}');
          Ext.create('{}',{{
            width: '100%',
            {}
            renderTo: out
          }});
        }}
      }});
    }}
    if(typeof Ext != 'undefined')
      initUI();
    '''.format(app,app,app,"controllers: '{}',".format(controllers) if controllers is not None else '', viewClass, viewClass
               , str(config).strip('{}') + ',' if config is not None else '')
  return display( Javascript(code
                    ,css=[
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/packages/charts/classic/crisp/resources/charts-all-debug.css',
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/classic/theme-crisp/resources/theme-crisp-all_1.css',
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/classic/theme-crisp/resources/theme-crisp-all_2.css'
    ]) )

def to_message(df):
  def type(dtype):
    return 'number' if dtype == 'float64' else 'date' if issubclass(dtype.type, np.datetime64) else 'string'

  def field(name):
    return {'name': name, 'type': type(df.dtypes[name]), 'allowNull': 'true'}

  def column(name,dtype,header=None):
    retVal = {'dataIndex': name, 'header': name if header is None else header, 'flex': 1}
    if dtype == 'float64':
      retVal.update({
        'xtype' : 'numbercolumn',
        'format': '0,000.00',
        'align':'right'
      })
    return retVal

  metaData = {
    'colModel': [column('id', df.index.dtype, df.index.name)]
  }
  if isinstance(df, pd.DataFrame):
    metaData['colModel'] += [column(c,df.dtypes[c]) for c in df.columns]
    if 'Capital' not in df.columns: #todo Remove this hardcode
      metaData['fields'] = [field(c) for c in df.columns] + [{'name': 'id', 'type': type(df.index.dtype)}]
  else:
    metaData['colModel'] += [column(df, df.dtype)]

  return {
    'rows': df.to_csv(index_label='id'),
    'metaData': metaData
  }

def _jupyter_nbextension_paths():
  return [{
    'section': 'notebook',
    'src': 'static',
    'dest': 'jupyter-extjs',
    'require': 'jupyter-extjs/extension'
  }]
