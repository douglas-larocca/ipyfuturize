import os
import json
import shlex
from tempfile import NamedTemporaryFile
from datetime import datetime
from IPython.core.display import Javascript
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magics import DisplayMagics
from subprocess import Popen, PIPE


class CellInject(object):
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, cell, extrajs=''):
        if not isinstance(cell, str):
            cell = json.dumps(cell)
        if not cell.startswith('"'):
            cell = json.dumps(cell)
        cell = '''
        var cell = IPython.notebook.get_selected_cell();
        var content = {0};
        {extrajs}
        cell.code_mirror.setValue(content);
        '''.format(cell, extrajs=extrajs)
        DisplayMagics().javascript('', cell)


@magics_class
class IPythonFuturize(Magics):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @line_magic('futurize')
    def ipython_futurize(self, line):
        raise NotImplementedError()
    
    @cell_magic('futurize')
    def ipython_futurize(self, line, cell):
        """        
        Usage: futurize [options] file|dir ...

        Options:
          -h, --help            show this help message and exit
          -V, --version         Report the version number of futurize
          -a, --all-imports     Add all __future__ and future imports to 
                                each module
          -1, --stage1          Modernize Python 2 code only; no compatibility 
                                with Python 3 (or dependency on ``future``)
          -2, --stage2          Take modernized (stage1) code and add a dependency 
                                on ``future`` to provide Py3 compatibility.
          -0, --both-stages     Apply both stages 1 and 2
          -u, --unicode-literals
                                Add ``from __future__ import unicode_literals`` 
                                to implicitly convert all unadorned string literals 
                                '' into unicode strings
          -f FIX, --fix=FIX     Each FIX specifies a transformation; default: all. 
                                Either use '-f division -f metaclass' etc. or use the 
                                fully-qualified module name: '-f lib2to3.fixes.fix_types 
                                -f libfuturize.fixes.fix_unicode_keep_u'
          -j PROCESSES, --processes=PROCESSES
                                Run 2to3 concurrently
          -x NOFIX, --nofix=NOFIX
                                Prevent a fixer from being run.
          -l, --list-fixes      List available transformations
          -p, --print-function  Modify the grammar so that print() is a function
          -v, --verbose         More verbose logging
          --no-diffs            Don't show diffs of the refactoring
          -w, --write           Write back modified files
          -n, --nobackups       Don't write backups for modified files.
          -o OUTPUT_DIR, --output-dir=OUTPUT_DIR
                                Put output files in this directory instead of overwriting the 
                                input files. Requires -n. For Python >= 2.7 only.
          -W, --write-unchanged-files
                                Also write files even if no changes were required 
                                (useful with --output-dir); implies -w.
          --add-suffix=ADD_SUFFIX
                                Append this string to all output filenames. Requires -n 
                                if non-empty. For Python >= 2.7 only.ex: --add-suffix='3' 
                                will generate .py3 files.
        """
        
        try:
            futurize = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/futurize')
        except KeyError:
            futurize = 'futurize'
            
        with NamedTemporaryFile(delete=False, suffix='.py') as f:
            f.write(cell.encode('utf-8'))
            filename = f.name
        
        args = shlex.split(' '.join((futurize, '-w', line, filename)))
        
        p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out, err = p.communicate()
        
        with open(filename, 'r') as f:
            rf = f.read()
        
        inj = CellInject()
        inj(rf)