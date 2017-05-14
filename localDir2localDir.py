'''What it does: 
   Takes files on local machine/server directory (source),  
   subsets the files by pattern-matching (ex. files with '.txt' extension)
   copies them on a destination directory

Learned:  
	# from itertools import product # this is for nested for loops
	# more info on itertools: https://docs.python.org/3/library/itertools.html#recipes
	# Generators are for loops/memory cach in general https://wiki.python.org/moin/Generators
	# Python allows nested functions

Input:
Output: 

Example (bash commandline run): 
Code - Status: in progress
	TODO: abs path check

Unit Testing: 
'''
import os
import shutil
import timeit

start = timeit.default_timer()

src = "readData/"
dst = "writeData-1/" # must have write permission (chmod to change if needed)

src_files = os.listdir(src)

subset_files = [name for name in src_files if '.txt' in name] # subsetting a list based on pattern in string 
# subset_files = filter(lambda name: '.txt' in name, src_files) # is slower than list based subsetting 

for file_name in subset_files:
    full_file_name = os.path.join(src, file_name) 
    if (os.path.isfile(full_file_name)):
        shutil.copy(full_file_name, dst)

# stop = timeit.default_timer()
# totalRunTime = stop - start 
# print ("filter took " + str(totalRunTime) + " seconds\n")
# print ("list took " + str(totalRunTime) + " seconds\n")
