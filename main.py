import argparse
import distutils.util
import re 
import pickle
from philter import Philter
import gzip
import json


def main():
    # get input/output/filename
    run_eval = False
    verbose = True
    # filters = "./configs/philter_alpha.json"
    philter_config = {
        "verbose":verbose,
        "run_eval":run_eval,
        "finpath":"./data/i2b2_notes/",
        "foutpath":"./data/i2b2_results/",
        "outformat":"asterisk",
        "filters":"./configs/philter_delta.json",
        "cachepos":None
    }
   
    filterer = Philter(philter_config)

    #map any sets, pos and regex groups we have in our config
    filterer.map_coordinates()

    
    #transform the data 
    #Priority order is maintained in the pat 


# error analysis
        
if __name__ == "__main__":
    main()
