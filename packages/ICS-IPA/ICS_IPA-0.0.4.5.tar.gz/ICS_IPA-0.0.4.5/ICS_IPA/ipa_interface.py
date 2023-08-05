import sys  #allows access to command line
import glob #allows searching for files
import os
import json
from docopt import docopt
from importlib import import_module

def ipa_init(script_name='script.py', version='script.py 1.0'):
    '''
    * The ipa_init function allows you to set the the name and version information of
    * your script. This is allows command line help to display the information accurately.

    * Note ipa_init function must be called before any other ipa function for the change to
    * take affect
    '''
    __read_args(script_name, version)

def get_data_files():
    '''
    * The get_data_files function returns the data files used.

    * Note: If you are in desktop mode this function will display a the
    * file dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    '''
    if get_data_files.data_files is not None:
        return get_data_files.data_files
    desktop_options = {}
    #options['initialdir'] = '{0}'.format(os.path.expanduser('~'))
    desktop_options['filetypes'] = [("Data files", "*.dat;*.log;*.mdf;*.mf4;*.db"), ('all files', '.*')]
    desktop_options['title'] = 'Select list of input data files and click open.'
    desktop_options['defaultextension'] = '.db'
    get_data_files.data_files = __get_files('data_files', desktop_options)
    return get_data_files.data_files

def get_config_files():
    '''
    * The get_config_files function returns the config files used.

    * Note: If you are in desktop mode this function will display a the
    * file dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    '''
    if get_config_files.config_files is not None:
        return get_config_files.config_files
    desktop_options = {}
    desktop_options['filetypes'] = [("Lookup files", "*.sl;*.asl"), ("Signal Lookup files", "*.sl"),  ("Aliased Signal Lookup files", "*.asl"), ("All files", "*.*")] 
    desktop_options['title'] = "Select script config file (*.als) and click open."
    get_config_files.config_files = __get_files('config_files', desktop_options)
    return get_config_files.config_files

def get_output_dir():
    '''
    * The get_output_dir function returns the output directory that must be used.

    * Note: If you are in desktop mode this function will display a the
    * directory dialog the first time it's called. After being called
    * a cached version of the results will be returned from then on.
    '''
    if get_output_dir.output_dir is not None:
        return get_output_dir.output_dir
    get_output_dir.output_dir = __get_files('output_dir', {})
    return get_output_dir.output_dir

def update_progress(name='Master', percent=None, message=None):
    #pylint: disable=unused-argument
    '''
    * Allows the user to identify the prograss of the script

    * name: Is the of the progress bar master being the full script progress
    * percent: is a optional way to update progress.
    * message: is a optional way to update progress.
    '''
    # TODO
    pass


def __read_args(script_name='script.py', version='script.py 1.0'):
    if __read_args.args is None:
        args = '''
Usage:
  {scriptPy}
  {scriptPy} <IPA_FILE>
  {scriptPy} [--data_files=<FILE>...] [--config_files=<FILE>...] [--output_dir=<FILE>]
  {scriptPy} (-h | --help)
  {scriptPy} --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -d FILE --data_files=<FILE>   The data files that are used.
  -c FILE --config_files=<FILE> The config files that are used. 
  -o FILE --output_dir=<FILE>   The output directory. This is required if the script output directory.
'''
        __read_args.args = docopt(args.format(scriptPy=script_name), version=version)
    return __read_args.args

def __arrayafy(argument):
    if not isinstance(argument, list):
        argument = [argument]
    return argument

def __is_strings(argument):
    return isinstance(argument, str)

def __is_array_of_strings(argument):
    if not isinstance(argument, list):
        return False
    return all(isinstance(item, str) for item in argument)


def __get_args():
    if __read_args()['<IPA_FILE>'] is not None:
        return json.load(open(__read_args()['<IPA_FILE>']))
    else:
        return __read_args()


def __get_files(file_arg, desktop_options):
    args = __get_args()
    if file_arg in args:
        files = __arrayafy(args[file_arg])
        if __is_array_of_strings(files):
            return files
        else:
            raise TypeError("the {files} argument is invalid".format(files=file_arg))
    elif __read_args()['<IPA_FILE>'] is not None:
        raise TypeError("the {files} argument is not included in IPA_FILE".format(files=file_arg)) 
    else:
        mtk = None
        mtk_filedialog = None
        try:
            mtk = import_module('tkinter')
            mtk_filedialog = import_module('tkinter.filedialog')
        except ModuleNotFoundError as err:
            raise err

        root = mtk.Tk()
        root.withdraw()
        root.focus_force()
        root.wm_attributes('-topmost', 1)
        #filenames = tkFileDialog.askopenfilenames(parent=self.parent, **options)
        return list(mtk_filedialog.askopenfilenames(**desktop_options))

def __get_dir(dir_arg, desktop_options):
    args = __get_args()
    if dir_arg in args:
        if __is_strings(args[dir_arg]):
            return args[dir_arg]
        else:
            raise TypeError("the {dir_arg} argument is invalid".format(dir_arg=dir_arg))
    elif __read_args()['<IPA_FILE>'] is not None:
        raise TypeError("the {dir_arg} argument is not included in IPA_FILE".format(dir_arg=dir_arg)) 
    else:
        mtk = None
        mtk_filedialog = None
        try:
            mtk = import_module('tkinter')
            mtk_filedialog = import_module('tkinter.filedialog')
        except ModuleNotFoundError as err:
            raise err

        root = mtk.Tk()
        root.withdraw()
        root.focus_force()
        root.wm_attributes('-topmost', 1)
        #filenames = tkFileDialog.askopenfilenames(parent=self.parent, **options)
        return list(mtk_filedialog.askdirectory(**desktop_options))


