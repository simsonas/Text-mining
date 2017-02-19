# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 08:42:38 2017

@author: simas
"""
from __future__ import print_function






def clean_tweet(tweet):
   import re,string
   
   tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
   tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # Remove hyperlinks
   tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove puncutations like 's
   return tweet
   

#columns is a list of strings of names of columns of the frame
def chunks_from_r(frame,columns=None,chunksize=1000):
    import rpy2.robjects as robj
    import rpy2.rinterface
    from rpy2.robjects.lib.dplyr import DataFrame
    from rpy2.robjects import pandas2ri    
    
    df = DataFrame(robj.r[frame])
    if (columns!=None):
        df=df.select(*columns)    
    
    nrows =robj.r.nrow(df)[0]
    assert nrows!=rpy2.rinterface.NULL
    
    start=1
    end=start+chunksize-1    
    
    while(start<nrows):            
        chunk = pandas2ri.ri2py(df.slice(str(start)+':'+str(end)))
        yield chunk
        start=end+1
        end=min(start+chunksize,nrows)



