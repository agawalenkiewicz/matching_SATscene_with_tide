import os
import sys

my_directory_sst = sys.argv[1]
my_directory_tide = sys.argv[2]

#read in list of files in the corresponsing directory
list_of_sst_files = os.listdir(my_directory_sst)
list_of_tide_files = os. listdir(my_directory_tide)

#for tide_file in list_of_tide_files:
#date_part_sst = sst_file[-10:]
[os.system('rm ' + my_directory_tide + tide_file) for tide_file in list_of_tide_files if tide_file not in list_of_sst_files]