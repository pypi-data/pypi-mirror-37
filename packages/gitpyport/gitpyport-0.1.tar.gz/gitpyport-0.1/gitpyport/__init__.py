import os
from os import path

realpath=os.getcwd()
new_module = __import__('gitpyport')
os.chdir(os.path.dirname(new_module.__file__))

compatibility="Windows Platform"

def about():
	os.system("engine.py -about")

def pyport(file):
	os.system("engine.py -import "+"\""+realpath+"\\"+file+"\" "+os.path.dirname(new_module.__file__)+"\\ "+file)

os.system("engine.py -init")