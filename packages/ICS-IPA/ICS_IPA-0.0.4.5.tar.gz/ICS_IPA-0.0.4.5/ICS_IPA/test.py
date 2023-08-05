"""
Usage:
  script.py
  script.py <IPA_FILE>
  script.py --data_files=<FILE>... --config_files=<FILE>... --output_dir=<FILE>
  script.py (-h | --help)
  script.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -d FILE --data_files=<FILE>   the data files that are used
  -c FILE --config_files=<FILE> the confie files that are used
  -o FILE --output_dir=<FILE>   the output directory
"""

from docopt import docopt

from importlib import import_module

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
    tk = import_module('tkinter')
    tk_filedialog = import_module('tkinter.filedialog')
    print(tk)
    print(tk_filedialog)