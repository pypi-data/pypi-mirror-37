import os
from ctypes import cdll

try:
    import rhvoice_wrapper_data

    PATH = os.path.dirname(os.path.abspath(__file__))
    LIBS_PATH = os.path.join(PATH, 'lib')

    lib_path = os.path.join(LIBS_PATH, 'RHVoice.dll' if os.name == 'nt' else 'libRHVoice.so')
    if not os.path.isfile(lib_path):
        raise RuntimeError('Library not found: {}'.format(lib_path))

    if os.name != 'nt':  # preload core library
        cdll.LoadLibrary(os.path.join(LIBS_PATH, 'libRHVoice_core.so'))

    data_path = rhvoice_wrapper_data.data_path
except Exception as e:
    print('Error in rhvoice-wrapper-bin: {}'.format(e))
    LIBS_PATH = None
    PATH = None
    data_path = None
    lib_path = None

