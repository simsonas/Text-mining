# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:18:37 2017

@author: simas
"""

from __future__ import print_function

from langdetect import detect
import tablib
import sys


import rpy2.robjects as robj
from rpy2.robjects import pandas2ri

pandas2ri.activate()

def lang_det(data):
    total = len(data)
    
    #language detection magic
    lang =[]
    for i,tweet in enumerate(data):
        try:            
            lang.append(detect(tweet))
        except:
            lang.append(None)
        print(i,"/",total,end="\r")
    return lang

def main():    
    #Open the file and read in the data    
    f=open(sys.argv[1],'rb')    
    data = data = tablib.Dataset().load(f.read())
    f.close()    
    
    lang = lang_det(data['text'])    
    #append the language column
    data.append_col(lang,header='lang2')
    
    #split the filename by dot
    fname = sys.argv[1].split('.')
    
    #save the output with output types' extension
    f = open('.'.join(fname[:-1])+"."+sys.argv[2],"wb")
    f.write(data.export(sys.argv[2]))
    f.close()

def r_main():
    print("Loading file.")
    robj.r['load'](sys.argv[1])
    print("importing object to pandas")
    data = robj.r[sys.argv[2]]
    print("removing R object.")
    robj.r['rm'](sys.argv[1])
    print("lang det")
    lang =lang_det(data.text)
    
    data['lang2']=lang
    
    print("exporting from pandas to r")
    robj.globalenv[sys.argv[2]] = data
    del data
    robj.r['save.image'](sys.argv[1])
    
    
if __name__=="__main__":
    formats=tablib.Dataset()._formats
    inp = [fmt for fmt,funcs in formats.items() if funcs[1]!=None]
    outp = [fmt for fmt in formats.keys() if (fmt not in inp)]
    inp.append("rda")
    outp.append("rda")    
    if (('-h' in sys.argv) or ("--help" in sys.argv)):
        
        print("Usage: python ",sys.argv[0]," {input_file output_type | rds_file dataframe}\n")
        print("Adds a language column (column name \'lang\') to tweet data.")
        print("If input and output types are the same,rewrites the original file")
        print("If the input file is .rda,we can only overwrite it.\n")
        print("Supported input types: ", " ".join(inp))
        print("supported output types: "," ".join(outp),"\n")
        print("THIS IS USELESS - TWITTER HAS DETECTED LANGUOGE IN THE API OUTPUT")
    else:
        fname = sys.argv[1].split('.')
        if ("rda" in fname[-1].lower()):
            r_main()
        else:
            main()

