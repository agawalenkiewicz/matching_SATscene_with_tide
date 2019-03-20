import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import os
import pandas as pd
from datetime import datetime
from scipy import interpolate


def get_metadata(Filepath, Filename):
    myfile = os.path.join(Filepath, Filename)
    meta = {}
    with open(myfile) as file:
        for line in file:
            name, var = line.partition("=")[::2]
            meta[name.strip()] = var
    return meta


the_metafile = sys.argv[1]
the_folder = sys.argv[2]
metadata = get_metadata(the_folder, the_metafile)
 
date = str(metadata['DATE_ACQUIRED'])
m = re.search('\d{4}.\d{2}.\d{2}', date)
date = m.group(0)
date_new = datetime.strptime(date, '%Y-%m-%d').strftime('%Y/%m/%d')

time = str(metadata['SCENE_CENTER_TIME'])
n = re.search('\d{2}.\d{2}.\d{2}', time)
time = n.group(0)

print date_new, time


"""
in bash:
path=/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/hunterston_10_50/*
code=/home/users/mp877190/getting_netcdf/tide_tables/find_all_dates_times_of_netcdf_files.py
for f in $path ; do [ -d $f ] && cd "$f/scenes" ; meta=`find *_MTL.txt`  ; python $code $meta "$f/scenes"; cd .. ; done
"""