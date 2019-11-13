import inspect
import sys

logo = """

____  _   _ _  _______  _  ___________  _  _________  _  _________________           
     | \ | (_)_ __ ___ | |__  _   _ ___(_)_ __   __ _| |_ ___  _ __ 
____ |  \| | | '_ ` _ \| '_ \| | | / __| | '_ \ / _` | __/ _ \| '__| _____
     | |\  | | | | | | | |_) | |_| \__ \ | | | | (_| | || (_) | |   
____ |_| \_|_|_| |_| |_|_.__/ \__,_|___/_|_| |_|\__,_|\__\___/|_| ________
   
            The RM Nimbus PC186 SUB-BIOS emulator for Python
__________________________________________________________________________                                                
"""

def message(text):
    caller = inspect.stack()[1][3]
    print('[nimbusinator] {}: {}'.format(caller, text))

def fatal():
    message('Fatal error')
    sys.exit()
