import cx_Freeze
import sys
import matplotlib
import os
import os.path

additional_mods = ['numpy.core._methods', 'numpy.lib.format']
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

include_files = [os.path.join(PYTHON_INSTALL_DIR,"DLLs","tcl86t.dll"),
os.path.join(PYTHON_INSTALL_DIR,"DLLs","tk86t.dll"),"elekta.ico"]
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("BB.py",base = base,icon = "elekta.ico")]

cx_Freeze.setup(
    name = "FindCircle",
    options = {"build_exe":{"includes":additional_mods,"packages":["tkinter","matplotlib"],"include_files":include_files}},
    version = "0.01",
    description = "First New BB Finder",
    executables = executables)
