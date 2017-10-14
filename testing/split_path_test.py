from utils import *
import os


dir_name, file_name = split_path('data')
print os.path.join(dir_name, file_name)