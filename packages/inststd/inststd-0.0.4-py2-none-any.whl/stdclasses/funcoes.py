import sys
import socket

class Funcoes:
  def __init__ (self):
    self.nome = None
    
    
  def GetMaxCarga(self, spark, db, table, aspas=""):
    ssql = '''
      select max(dat_ref_carga) as dt from 
      ''' + db+'''.'''+table
    return aspas+str(spark.sql(ssql).toPandas()['dt'][0])+aspas
  
  def DeletaTabela(self, spark, db, table):
    return spark.sql('drop table if exists '+db+'.'+table)
  
  def RemoverAcentos(self, text):
    import unicodedata
    try:
      text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
  
  def ReplaceDicionario(self, replacements, string):
    for i in replacements:
        string = string.replace(i, replacements[i])
    return string
  
  def VerificaCarga(self, spark, arr):
      x = True
      result = []
      for i in arr:
        dt = str(np.datetime64(str(np.datetime64('today'))) - np.timedelta64(i[2], 'D'))
        max_dt = GetMaxCarga(spark, i[0], i[1])
        result.append(i[1], '| carga: ' + max_dt, '| esperado: ' + dt)
        
        if max_dt != dt:
          x = False
          break

      return [x, result]
    
    
  def GetIpFromHost(self, hostname):
    return socket.gethostbyname(hostname)
  
  
  def Version(self):
    return '0.0.73'