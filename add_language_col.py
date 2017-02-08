# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:18:37 2017

@author: simas
"""

from __future__ import print_function

from langdetect import detect
import tablib
import sys

#import dataset later

def main():    
    #Open the file and read in the data    
    f=open(sys.argv[1],'rb')    
    data = data = tablib.Dataset().load(f.read())
    f.close()    
    total = len(data)
    
    #language detection magic
    lang =[]
    for i,tweet in enumerate(data['text']):
        lang.append(detect(tweet))
        print(i,"/",total,end="\r")
        
    #append the language column
    data.append_col(lang,header='lang')
    
    #split the filename by dot
    fname = sys.argv[1].split('.')
    
    #save the output with output types' extension
    f = open('.'.join(fname[:-1])+"."+sys.argv[2],"wb")
    f.write(data.export(sys.argv[2]))
    f.close()
    
    
if __name__=="__main__":
    formats=tablib.Dataset()._formats
    inp = [fmt for fmt,funcs in formats.items() if funcs[1]!=None]
    outp = [fmt for fmt in formats.keys() if (fmt not in inp)]    
    if (('-h' in sys.argv) or ("--help" in sys.argv)):
        
        print("Usage: python ",sys.argv[0]," input_file output_type\n")
        print("Adds a language column (column name \'lang\') to tweet data.")
        print("If input and output types are the same,rewrites the original file\n")
        print("Supported input types: ", " ".join(inp))
        print("supported output types: "," ".join(formats.keys()))
    else:
        main()

