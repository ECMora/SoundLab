from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# packages_list = ['numpy', 'sip', 'scipy.io.matlab.streams', 'matplotlib', 'duetto', 'pyqtgraph']
# NOTE: The following two lines substitute the above line. The above line includes full packages, what is not needed
#       when willing to include single modules (what is done through <includes> parameter)
packages_list = ['numpy', 'matplotlib', 'duetto', 'pyqtgraph']
includes_list = ['sip', 'scipy.io.matlab.streams']
excludes_list = ['Tkinter', 'tcl', 'ttk', 'tkinter??']
include_files_list = ['Utils']
buildOptions = dict(build_exe='bin_cxf',
                    packages=packages_list,
                    includes=includes_list,
                    excludes=excludes_list,
                    include_files=include_files_list,
                    optimize=2,
                    compressed=True)

executables = [
    Executable('Duetto_Sound_Lab.pyw', base='Win32GUI', targetName="duetto-SoundLab.exe")
]
#    Executable('Duetto_Sound_Lab.pyw', base='Win32GUI', icon='duetto-icon-64x64.png')

setup(name='duetto SoundLab',
      version='0.2.7.0',
      description='duetto Bioacoustics Analysis',
      options=dict(build_exe=buildOptions),
      executables=executables)
