import sys, os.path

__version__ = '0.1.2'
torch_version_required = '0.4.1'


###########################################################
#              Compilation options
###########################################################

from .common.get_options import set_build_folder

script_folder = os.path.dirname(os.path.abspath(__file__))
build_folder  = set_build_folder()

verbose = False # display output of compilations
build_type = "Release" # 'Release' or 'Debug'

default_cuda_type = 'float32' # 'float32' or 'float64'

sys.path.append(build_folder)

