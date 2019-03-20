import os
import sys

my_directory_sst = sys.argv[1]
my_directory_tide = sys.argv[2]

#read in list of files in the corresponsing directory
list_of_sst_files = os.listdir(my_directory_sst)
list_of_tide_files = os. listdir(my_directory_tide)

for sst_file in list_of_sst_files:
	date_part_sst = sst_file[-10:]
	[os.system('mv ' + my_directory_sst + sst_file + ' ' + my_directory_sst + tide_file) for tide_file in list_of_tide_files if date_part_sst in tide_file]