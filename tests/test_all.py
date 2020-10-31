import sys
import os


sys.dont_write_bytecode = True
sys.path.insert(0, "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts")
init_file = "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\ClyphX_Pro\__init__.py"
with open(init_file, "a"):
    from .fixtures import *

from .actions_tests import *
from .entities_tests import *

os.remove(init_file)
from shutil import copyfile
copyfile("C:\\Users\\thiba\\Google Drive\\music\\software presets\\clyphx pro\\Manual Setup\\MIDI Remote Scripts\\ClyphX_Pro\\__init__.pyc", "C:\ProgramData\Ableton\Live 10 Suite\Resources\MIDI Remote Scripts\ClyphX_Pro\__init__.pyc")