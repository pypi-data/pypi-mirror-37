from .enviaremail import EnviarEmail
from .spark import Spark
from .funcoes import Funcoes

#import pip
#import sys
#import pkg_resources
#
#
#latest_version = '0.0.56'
#
#def install(package):
#    if hasattr(pip, 'main'):
#        pip.main(['install', package])
#    else:
#        pip._internal.main(['install', package])
#
#
#while not pkg_resources.get_distribution("stdclasses").version == latest_version:
#  install('stdclasses')
#  if 'stdclasses' in sys.modules:
#    del sys.modules["stdclasses"]
#  import stdclasses
