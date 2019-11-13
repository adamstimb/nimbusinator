import inspect
import sys

logo = """

     _  ___       __            _           __          
    / |/ (_)_ _  / /  __ _____ (_)__  ___ _/ /____  ____
   /    / /  ' \/ _ \/ // (_-</ / _ \/ _ `/ __/ _ \/ __/
  /_/|_/_/_/_/_/_.__/\_,_/___/_/_//_/\_,_/\__/\___/_/   
                                                      
  RM Nimbus SUB-BIOS Emulator for Python
                                            
"""

def message(text):
    caller = inspect.stack()[1][3]
    print('[nimbusinator] {}: {}'.format(caller, text))

def fatal():
    message('Fatal error')
    sys.exit()
