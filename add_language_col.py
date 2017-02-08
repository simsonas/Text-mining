# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:18:37 2017

@author: simas
"""

from __future__ import print_function

from langdetect import detect
import tablib
import sys

def main():    
    f=open(sys.argv[1],'rb')    
    data = data = tablib.Dataset().load(f.read())
    f.close()    
    
    lang = map(lambda tweet:detect(tweet),data['text'])
    
    data.append_col(lang,header='lang')
    
    fname = sys.argv[1].split('.')
    
    f = open('.'.join(fname[:-1])+"."+sys.argv[2],"wb")
    f.write(data.export(sys.argv[2]))
    f.close()
    
    
if __name__=="__main__":
    if (('-h' in sys.argv) or ("--help" in sys.argv)):
        formats=tablib.Dataset()._formats
        inp = [fmt for fmt,funcs in formats.items() if funcs[1]!=None]
        outp = [fmt for fmt in formats.keys() if (fmt not in inp)]
        print("Usage: python ",sys.argv[0]," input_file output_type\n")
        print("If input and output types are the same,rewrites the original file\n")
        print("Supported input types: ", " ".join(inp))
        print("supported output types: "," ".join(formats.keys()))
    else:
        main()

