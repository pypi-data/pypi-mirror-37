import sys
if sys.version_info[0] < 3:
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEText import MIMEText
  from email.MIMEBase import MIMEBase
  from email.MIMEImage import MIMEImage
  
else:
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText
  from email.mime.base import MIMEBase
  from email.mime.image import MIMEImage

  
import smtplib

from email import encoders 
import base64

class EnviarEmail:
  
  def __init__(self):
    self.nome = None

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

  def Enviar(self, params):
    
    obrigatorios = ['from', 'to', 'ip', 'subject', 'content']
    for o in obrigatorios:
      if not o in params:
        print "O campo "+ o + " é obrigatorio"
        return ""
    
    
    fromaddr = params["from"]
    toaddr = params["to"]
    if 'cc' in params:
      cc = params["cc"]
    else:
      cc = ""
    if 'bcc' in params:
      bcc = params["bcc"]
    else:
      bcc = ""
    
    bcc = fromaddr+";"+bcc
    
    vbcc = [] if bcc == "" else bcc.split(";")
    vcc = [] if cc == "" else cc.split(";")
    vto = [] if toaddr == "" else toaddr.split(";")
    rcpt = vbcc  + vcc + vto
    
    server = smtplib.SMTP(params['ip'], 25) 
    print rcpt
    enviados = []
    for em in rcpt:
      e = em[:].strip()
      if(len(e)>1 and e not in enviados):
        enviados.append(e)
        msg = MIMEMultipart()
        print e
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Cc'] = cc
        msg['Bcc'] = bcc
        msg['Subject'] = params["subject"]

        body = params["content"]

        body_type = 'plain'
        if(body.upper().find('<HTML>')>=0):
          body_type = 'html'
        else:
          body_type = body_type

        msg.attach(MIMEText(body, body_type))

        if 'file_name' in params:
          filename = params["file_name"][params["file_name"].rfind("/")+1:]
          attachment = open(params["file_name"], "rb")

          part = MIMEBase('application', 'octet-stream')
          part.set_payload((attachment).read())
          encoders.encode_base64(part)
          part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

          msg.attach(part)
        text = msg.as_string()
        server.sendmail(fromaddr, e, text)
        print "E-mail enviado com sucesso para "+e+"!"
    server.quit()
    return "sucesso"
    
    