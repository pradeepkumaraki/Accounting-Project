from cx_Freeze import setup, Executable

base = None    

executables = [Executable("home.py", base=base)]

packages = ["idna","PySimpleGUI","sqlite3"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Accounts_setup",
    options = options,
    version = "0.1",
    description = 'Customized Accounting software',
    executables = executables
)
