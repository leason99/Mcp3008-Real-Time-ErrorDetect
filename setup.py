
from distutils.core import setup, Extension
 
module1 = Extension('mcp3008', sources = ['mcp3008.c',"lfq.c"])
 
setup (name = 'mcp3008',
       version = '1.0',
       description = 'This is a mcp3008 package',
       ext_modules = [module1])
