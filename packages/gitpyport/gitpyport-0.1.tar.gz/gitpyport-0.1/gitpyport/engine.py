import sys
import os
sys_offset=0

if sys.argv[sys_offset+1]=="-init":
    os.system("Fn.dll Print 0a \"Thank you for using gitpyport\"")
    print(" ")
elif sys.argv[sys_offset+1]=="-about":
    os.system("Fn.dll Print 0a \"gitpyport is Github Python Package Importer\"")
    print(" ")
elif sys.argv[sys_offset+1]=="-import":
    #print("copy "+str(sys.argv[2])+" "+str(sys.argv[3]))
    os.system("copy "+str(sys.argv[2])+" "+str(sys.argv[3]))
    os.system("unzip "+str(sys.argv[4]))
    os.system("del "+str(sys.argv[4]))
    #os.system("cd "+str(sys.argv[4]).split(".")[0])
    os.system("cd "+str(sys.argv[4]).split(".")[0]+" & python setup.py install")
    os.system("cd..")
    os.system("echo y | rmdir /s "+str(sys.argv[4]).split(".")[0])