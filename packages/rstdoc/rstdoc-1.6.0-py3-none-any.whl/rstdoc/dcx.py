#!/usr/bin/env python
#encoding: utf-8

##### THIS GETS EXECUTED VIA GEN FILE #######
##lns=open(__file__).readlines()
##list(gen_head(lns))
#def gen_head(lns,**kw):
#    b,e = list(rindices('^"""',lns))[:2]
#    return lns[b+1:e]
#def gen_head
##list(gen_api(lns))
#def gen_api(lns,**kw):
#    yield from doc_parts(lns,signature='py',prefix='dcx.')
#def gen_api
##### THIS GETS EXECUTED VIA GEN FILE #######

"""
.. _`rstdcx`:

rstdcx
======

Support script to create documentation (PDF, HTML, DOCX)
from restructuredText (RST, reST) using either

- `Pandoc <https://pandoc.org>`__
- `Sphinx <http://www.sphinx-doc.org>`__
- Docutils `configurable <http://docutils.sourceforge.net/docs/user/config.html>`__

Usage
-----

``rstdoc`` installs the ``rstdcx`` command line tool that calls ``dcx.py``.
It

- processes ``gen`` files (see examples produced by --rest)

- handles `.stpl <https://bottlepy.org/docs/dev/stpl.html>`__ files

- creates ``.tags`` to jump around with the editor

- creates links files like ``_links_pdf.rst``, ``_links_docx.rst``, ``_links_sphinx.rst``

- forwards known files to either Pandoc, Sphinx or Docutils

See example at the end of ``dcx.py``.

It is supposed to be used with a build tool. ``make`` and ``waf`` examples are included.

- Initialize example tree.
  This copies ``dcx.py`` into the example tree to be independent from possible future changes.

  $ ./dcx.py --rest tmp #.rest files OR
  $ ./dcx.py --stpl tmp #.rest.stpl files

- Only create .tags and _links_xxx.rst::

  $ cd tmp/src/doc
  $ ./dcx.py

- Create the docs (and .tags and _links_xxx.rst) with **make**::

  $ make html #OR
  $ make epub #OR
  $ make latex #OR
  $ make docx #OR
  $ make pdf

  The latter two are done by Pandoc, the others by Sphinx.

- Create the docs (and .tags and _links_xxx.rst) with **waf** (preferred):

  Instead of using ``make`` one can load ``dcx.py`` in `waf <https://github.com/waf-project/waf>`__.
  ``waf`` also considers all recursively included files,
  such that a change in any of them results in a rebuild of the documentation. 
  All files can have an additional ``.stpl`` extension to use `SimpleTemplate <https://bottlepy.org/docs/dev/stpl.html#simpletemplate-syntax>`__.

    $ waf configure #copies the latest version of waf in here
    $ waf --docs docx,sphinx_html,rst_odt

  - ``rst_xxx`` via `rst2xxx.py <http://docutils.sourceforge.net/docs/user/tools.html>`__
  - ``sphinx_xxx`` via `Sphinx <http://www.sphinx-doc.org>`__ and
  - just ``xxx`` via `Pandoc <https://pandoc.org>`__.


The following image language files should be parallel to the ``.rest`` files.
They are automatically converted to ``.png`` and placed into ``./_images`` or ``../_images``.

- ``.tikz`` or ``.tikz.stpl``. 
  This needs LaTex.

- `.svg <http://svgpocketguide.com/book/>`__ or ``.svg.stpl``

- ``.dot`` or ``.dot.stpl``
  
  This needs `graphviz <https://graphviz.gitlab.io/gallery/>`__.

- `.uml <http://plantuml.com/command-line>`__ or ``.uml.stpl``

  This needs `plantuml <http://plantuml.com/command-line>`__ .
  Provide either 

  - ``plantuml.bat`` with e.g. ``java -jar "%~dp0plantuml.jar" %*``  or
  - ``plantuml`` sh script with ``java -jar `dirname $BASH_SOURCE`/plantuml.jar "$@"``

- ``.eps`` or ``.eps.stpl`` embedded postscript files.

  This needs `inkscape <https://inkscape.org/en/>`__.

- ``.pyg`` contains python code that produces a graphic.
  If the python code defines a ``save_to_png`` function,
  then that is used, which allows to use whatever python library you want 
  (`graph_tool <https://graph-tool.skewed.de/static/doc/quickstart.html>`__,
  `igraph <http://igraph.org/python/doc/tutorial/tutorial.html>`__,...)
  Else the following is tried

  - ``pyx.canvas.canvas`` from the `pyx <http://pyx.sourceforge.net/manual/graphics.html>`__ library or 
  - ``cairocffi.Surface`` from `cairocffi <https://cairocffi.readthedocs.io/en/stable/overview.html#basic-usage>`__
  - ``pygal.Graph`` from `pygal <https://pygal.org>`__
  - `matplotlib <https://matplotlib.org>`__. If ``matplotlib.pyplot.get_fignums()>1`` the figures result ``<name><fignum>.png`` 
    
Conventions
-----------

- Files 

  - main docs end in ``.rest``
  - ``.rst`` are included and ignored by Sphinx (see conf.py).
  - ``.txt`` are literally included (use :literal: option).
  - templates ``x.rest.stpl`` and ``y.rst.stpl`` are rendered separately.
  - ``some.rst.tpl`` are template included
    Template lookup is done in in ``.`` and ``..`` with respect to the current file.

    - with ``%include('some.rst.tpl',param="test")`` with optional parameters
    - with ``%globals().update(include('utility.rst.tpl'))`` if it contains only definitions

- ``.. _`id`:`` are *reST targets*.
  reST targets should not be template-generated. 
  The template files should have a higher or equal number of targets than the generated file,
  in order for tags to jump to the template original.
  If one wants to generate also reST targets, then this should happen in a previous step, 
  e.g. with ``gen`` files mentioned above. 

- References use replacement `substitutions`_ : ``|id|``.

- Add ``.. include:: _traceability_file.rst`` to ``index.rest`` or another ``.rest`` file to get traceability information generated
  
See the example created with ``--rest`` of ``--stpl`` at the end of this file and the sources of the documentation of 
`rstdoc <https://github.com/rpuntaie/rstdoc>`__.

.. _`substitutions`: http://docutils.sourceforge.net/docs/ref/rst/directives.html#replacement-text

"""


'''
API
---

.. code-block:: py

   import rstdoc.dcx as dcx


The functions in ``dcx.py`` are available to the ``gen_xxx(lns,**kw)`` functions (|dhy|).

'''

import sys
import re
import io
import os
import shutil
import contextlib
import atexit
import subprocess as sp
import tempfile
from threading import RLock
from urllib import request
from functools import lru_cache, wraps, partial, reduce
from collections import OrderedDict,defaultdict
from itertools import chain, tee
from types import GeneratorType
from argparse import Namespace
from docutils.core import publish_file, publish_string

import stpl

try:
    import svgwrite.drawing
except:
    print('Warning: no svgwrite')
    svgwrite = None

try:
    import pyfca
except:
    print('Warning: no pyfca for traceability diagram')
    pyfca = None

import pyx
import pygal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cairocffi
import cairosvg

from hashlib import sha1 as sha

import sphinx_bootstrap_theme
_commajoinslash = lambda x: ','.join(x).replace('\\','/')
html_theme_path = _commajoinslash(sphinx_bootstrap_theme.get_html_theme_path())

class RstDocError(Exception):
    pass

'''
Increase output if set to True.
'''
verbose = False

_plus = '+'
_indent = '    '

class _Tools:
    def svg2png(self,*args,**kwargs):
        cairosvg.svg2png(*args,**kwargs)
    def run(self,*args,**kwargs):
        if 'outfile' in kwargs:
            del kwargs['outfile']
        return sp.run(*args,**kwargs)
class _DryTools: #together with FakeFs
    def svg2png(self,*args,**kwargs):
        pass
    def run(self,*args,**kwargs):
        return sp.CompletedProcess([],0,'')
class _Verbose:
    def __init__(self, tools):
        self.tools = tools
    def svg2png(self,*args,**kwargs):
        print(_plus, relpath(kwargs['write_to']))
        return self.tools.svg2png(*args,**kwargs)
    def run(self,*args,**kwargs):
        print('run',args,kwargs)
        if 'outfile' in kwargs:
            print(_plus, kwargs['outfile'])
        return self.tools.run(*args,**kwargs)

from pyfakefs.fake_filesystem_unittest import TestCaseMixin
class _FakeFs(TestCaseMixin):
    def __init__(self):
        self.stack = []
    def is_setup(self):
        return self.stack != []
    def addCleanup(self, function, *args, **kwargs):
        self.stack.append((function, args, kwargs))
    def doCleanups(self):
        while self.stack:
            function, args, kwargs = self.stack.pop()
            function(*args, **kwargs)
    def setup(self):
        if self.stack:
            return
        self.setUpPyfakefs()
    def teardown(self):
        self.doCleanups()

fakefs = _FakeFs()

tools = None
def dry_run(
    dry=None #None: initialize with False if not yet, else keep as is.
             #True: fake fs and dry-run
             #False: use real tools
    ):
    '''
    Adjusts ``dcx`` classes to produce a dry run.

    '''
    
    global tools
    if dry:
        if not fakefs.is_setup():
            rstdir = os.path.dirname(os.path.dirname(__file__))
            cdir = os.getcwd()
            fakefs.setup()
            try:
                try:
                    fakefs.fs.add_real_directory(rstdir)
                    if verbose:
                        print('Added %s to fake fs'%rstdir)
                except Exception as e:
                    print('Error %s '%rstdir,e)
                try:
                    fakefs.fs.add_real_directory(cdir)
                    if verbose:
                        print('Added %s to fake fs'%cdir)
                except Exception as e:
                    print('Error %s '%cdir,e)
                cd(cdir)
                if verbose:
                    print('Fake %s'%cwd())
                tools = _Verbose(_DryTools())
            except Exception as e:
                tools = _Tools()
                fakefs.teardown()
                raise e
    else:
        if dry!=None or tools==None:
            fakefs.teardown()
            if verbose:
                tools = _Verbose(_Tools())
            else:
                tools = _Tools()

dry_run(None)

def opnwrite(filename):
    if verbose:
        print(_plus,filename)
    return open(filename,'w',encoding='utf-8',newline='\n')

isfile = os.path.isfile
abspath = lambda x: os.path.abspath(x).replace('\\','/')
isabs = os.path.isabs
def relpath(x,start=None):
    try:
        return os.path.relpath(x,start=start).replace('\\','/')
    except ValueError:
        return abspath(x)
dir = lambda x: os.path.dirname(x).replace('\\','/')
base = os.path.basename
dir_base = lambda x: [e.replace('\\','/') for e in os.path.split(x)]
stem = lambda x: os.path.splitext(x)[0].replace('\\','/')
stem_ext = lambda x: [e.replace('\\','/') for e in os.path.splitext(x)]
exists = os.path.exists
cwd = lambda: os.getcwd().replace('\\','/')
mkdir = partial(os.makedirs,exist_ok=True)
cd = os.chdir
cp = shutil.copy
ls = lambda x='.': [e for e in sorted(os.listdir(x))]
def rmrf(x):
    try:
        if os.path.isdir(x):
            shutil.rmtree(x)
        else:
            os.remove(x)
    except: pass
def filenewer(infile,outfile):
    res = True
    try:
        res = os.path.getmtime(infile) > os.path.getmtime(outfile)
    except: pass
    return res
normjoin = lambda *x: os.path.normpath(os.path.join(*x)).replace("\\","/")
updir = lambda fn: normjoin(dir(fn),'..',base(fn))
#fn='x/y/../y/a.b'
#updir(fn)#x\a.b
#updir('a.b')#..\a.b
#updir('a.b/a.b')#a.b
#normjoin(fn)#x\y\a.b

'''
Used for png creation.
'''
DPI = 600

#text files
_stpl = '.stpl'
_tpl = '.tpl'
_rest = '.rest'
_rst = '.rst'
_txt = '.txt'

is_rest = lambda x: x.endswith(_rest) or x.endswith(_rest+_stpl)
is_rst = lambda x: x.endswith(_rst) or x.endswith(_rst+_stpl) or x.endswith(_rst+_tpl)

#graphic files
_svg = '.svg'
_tikz = '.tikz'
_tex = '.tex'
_dot = '.dot'
_uml = '.uml'
_eps = '.eps'
_pyg = '.pyg'
_png = '.png' #target of all others

_is_rest_type = lambda t: any(x.endswith(t) for x in [_rest,_rst,_txt])
_is_graphic_type = lambda t: any(x.endswith(t) for x in graphic_extensions)

rextgt = re.compile(r'(?:^|^[^\.\%\w]*\s|^\s*\(?\w+[\)\.]\s)\.\. _`?(\w[^:`]*)`?:\s*$')
rexsubtgt = re.compile(r'(?:^|^[^\.\%\w]*\s|^\s*\(?\w+[\)\.]\s)\.\. \|(\w[^\|]*)\|\s\w+::')#no need to consider those not starting with \w, because rexlinksto starts with \w
rextitle = re.compile(r'^([!"#$%&\'()*+,\-./:;<=>?@[\]^_`{|}~])\1+$')
rexitem = re.compile(r'^\s*:?\**(\w[^:\*]*)\**:\s*.*$')
rexoneword = re.compile(r'^\s*(\w+)\s*$')
rexname = re.compile(r'^\s*:name:\s*(\w.*)*$')
rexlnks = re.compile(r'(?:^|[^a-zA-Z`])\|(\w+)\|(?:$|[^a-zA-Z`])')
reximg = re.compile(r'(?:image|figure):: ((?:\.|/|\\|\w).*)')
rerstinclude = re.compile(r'\.\. include::\s*([\./\w\\].*)')
restplinclude = re.compile(r'''%\s*include\s*\(\s*["']([^'"]+)['"].*\)\s*''')

@lru_cache()
def here_or_updir(fldr,file):
    """
    return type:
      - fldr/file or fldr/../file, depending on where file is
      - 0 not there, 1 in fldr, 2 updir
    """
    filepth = normjoin(fldr,file)
    there = 1
    if not exists(filepth):
        filepth = updir(filepth)
        if exists(filepth):
            there = 2
        else:
            there = 0
    return (filepth,there)

#master_doc and latex_documents is determined automatically
sphinx_config_keys = '''
    project
    author
    copyright
    version
    release
    html_theme
    html_theme_path
    latex_elements
    html_extra_path
    '''.split()

latex_elements = {'preamble':r"""
\usepackage{pgfplots}
\usepackage{unicode-math}
\usepackage{tikz}
\usepackage{caption}
\captionsetup[figure]{labelformat=empty}
\usetikzlibrary{arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks,intersections}
"""
}

tex_wrap = r"""
\documentclass[12pt,tikz]{standalone}
\usepackage{amsmath}
"""+latex_elements['preamble']+r"""
\pagestyle{empty}
\begin{document}
%s
\end{document}
"""

target_id_group = lambda targetid: targetid[0]
target_id_color = {"ra":("r","lightblue"), "sr":("s","red"), "dd":("d","yellow"), "tp":("t","green")}

_images = '_images'
_traceability_file = '_traceability_file' #used for _traceability_file.rst and _traceability_file.svg
html_extra_path = ['doc'+'/'+_images+'/'+_traceability_file+'.svg'] #IF YOU DID ``.. include:: _traceability_file.rst``
pandoc_doc_optref = {'latex': '--template reference.tex',
                 'html': {},#each can also be dict of file:template
                 'pdf': '--template reference.tex',
                 'docx': '--reference-doc reference.docx',
                 'odt': '--reference-doc reference.odt'
                 }
_pandoc_latex_pdf = ['--listings','--number-sections','--pdf-engine','xelatex','-V','titlepage','-V','papersize=a4','-V','toc','-V','toc-depth=3','-V','geometry:margin=2.5cm']
pandoc_opts = {'pdf':_pandoc_latex_pdf,'latex':_pandoc_latex_pdf,'docx':[],'odt':[],'html':['--mathml','--highlight-style','pygments']}
rst_opts = { #http://docutils.sourceforge.net/docs/user/config.html
            'strip_comments':True
            ,'report_level':3
            ,'raw_enabled':True
            }
#``list-table`` and ``code-block`` are converted to ``table`` and ``code``
make_counters = lambda: {".. figure":1,".. math":1,".. table":1,".. code":1}
name_from_directive = lambda directive,count: directive[0].upper()+directive[1:]+' '+str(count)

config_defaults = {
    'project': 'rstdoc'
    ,'author': 'rstdoc'
    ,'copyright': '2018, rstdoc'
    ,'version': '1.0'
    ,'release': '1.0.0'
    ,'html_theme': 'bootstrap'
    ,'html_theme_path': html_theme_path
    ,'latex_elements': latex_elements
    ,'html_extra_path': html_extra_path
    ,'tex_wrap': tex_wrap
    ,'target_id_group': target_id_group
    ,'target_id_color': target_id_color
    ,'pandoc_doc_optref': pandoc_doc_optref
    ,'pandoc_opts': pandoc_opts
    ,'rst_opts': rst_opts
    ,'name_from_directive': name_from_directive
    }

sphinx_enforced = {
    'numfig': 0
    ,'smartquotes': 0
    ,'source_suffix': '.rest'
    ,'templates_path': []
    ,'language': None
    ,'highlight_language': "none"
    ,'default_role': 'math'
    ,'latex_engine': 'xelatex'
    ,'pygments_style': 'sphinx'
    ,'exclude_patterns': ['_build', 'Thumbs.db', '.DS_Store']
    }

@lru_cache()
def conf_py(fldr):
    """
    ``conf.py`` or ``../conf.py`` is used for both sphinx and pandoc.

    """
    confpy,_ = here_or_updir(fldr,'conf.py')
    config={}
    config.update(config_defaults)
    try:
        with open(confpy,encoding='utf-8') as f:
            eval(compile(f.read(),abspath(confpy),'exec'),config)
        global DPI
        if 'dpi' in config:
            DPI = config['dpi']
    except: 
        pass
    config.update(sphinx_enforced)
    config['confpy'] = confpy #for SphinxTask
    try:
        config['html_theme_path'] = _commajoinslash(config['html_theme_path'])
    except: pass
    return config

_fillwith = lambda u,v: [x or v for x in u]

def _joinlines(lns):
    if lns[0].endswith('\n'):
        tmp = ''.join(lns)
    else:
        tmp = '\n'.join(lns)
    return tmp.replace('\r\n', '\n')

#x=b'a\r\nb'
#_nbstr(x)==b'a\nb'
_nbstr = lambda x: x and x.replace(b'\r\n',b'\n') or b''
#x=x.decode()
#_nstr(x)=='a\nb'
_nstr = lambda x: x and x.replace('\r\n','\n') or ''
def cmd(
    cmdlist #command as list
    ,**kwargs #arguments forwarded to subprocess.run()
    ):
    '''
    Runs ``cmdlist`` via subprocess.run and return stdout.
    In case of problems RstDocError is raised.

    '''

    cmdstr = ' '.join(cmdlist)
    try:
        for x in 'out err'.split():
            kwargs['std'+x]=sp.PIPE
        r = tools.run(cmdlist,**kwargs)
        try:
            stdout,stderr = _nstr(r.stdout),_nstr(r.stderr)
        except:
            stdout,stderr = _nbstr(r.stdout).decode('utf-8'),_nbstr(r.stderr).decode('utf-8')
        if r.returncode != 0:
            raise RstDocError('Error code %s returned from \n%s\nin\n%s\n'%(r.returncode 
                ,cmdstr,cwd())
                +'\n[stdout]\n%s\n[stderr]\n%s'%(stdout,stderr))
        return stdout
    except OSError as err:
        if err.errno != os.errno.ENOENT:   # No such file or directory
            raise
        raise RstDocError('Error: Cannot run '
            +cmdstr+' in '+cwd() + str(err))

def _imgout(inf): 
    inp,inname = dir_base(inf)
    infn,infe = stem_ext(inname)
    if not _is_graphic_type(infe):
        raise ValueError('%s is not an image source'%inf)
    outp,there = here_or_updir(inp,_images)
    if not there:
        outp = inp
    outname = infn+_png
    nout = normjoin(outp,outname)
    return nout

def _unioe(args): 
    i,o,e = [None]*3
    try:
        (i,o,e),a = args[:3],args[3:]
    except:
        try:
            (i,o),a = args[:2],args[2:]
        except:
            i,a = args[:1],args[1:]
    return i,o,e,a

def png_post_process_if_any(f):
    @wraps(f)
    def png_post_processor(*args,**kwargs):
        infile,outfile,e,args = _unioe(args)
        if isinstance(infile,str):
            config = conf_py(dir(infile))
            pp = config.get('png_post_processor',None)
            if pp:
                pngfile = f(infile,outfile,e,*args,**kwargs)
                if verbose:
                    print('png_post_processor','(',pngfile,')')
                return pp(pngfile)
            else:
                return f(infile, outfile, e, *args, **kwargs)
        return f(infile, outfile, e, *args, **kwargs)
    return png_post_processor

_ext = lambda x: x[0]=='.' and x or '.'+x
def normoutfile(f,suffix=None):
    """
    Make outfile from infile by appending suffix, or, if None,
    ``.png`` in ``./_images`` or ``../_images``  or ``./`` from infile directory.
    The outfile is returned.
    """
    @wraps(f)
    def normoutfiler(*args, **kwargs):
        infile,outfile,e,args = _unioe(args)
        if isinstance(infile,str):
            if not outfile:
                if suffix:
                    infn,infe = stem_ext(infile)
                    outfile = infn + _ext(suffix)
                else:
                    outfile = _imgout(infile)
        f(infile, outfile, e, *args, **kwargs)
        return outfile
    return normoutfiler

_cdlock = RLock()
@contextlib.contextmanager
def new_cwd(apth):
    prev_cwd = cwd()
    _cdlock.acquire()
    cd(apth)
    try:
        yield
    finally:
        cd(prev_cwd)
        _cdlock.release()

def infilecwd(f):
    """
    Changes into the directory of the infile if infile is a file name string.
    """
    @wraps(f)
    def infilecwder(*args, **kwargs):
        infile,outfile,e,args = _unioe(args)
        if isinstance(infile,str):
            ndir,inf = dir_base(infile)
        else:
            ndir,inf = '',infile
        if ndir:
            if outfile:
                outfile = relpath(outfile,start=ndir)
            with new_cwd(ndir):
                return f(inf, outfile, e, *args, **kwargs)
        return f(infile, outfile, e, *args, **kwargs)
    return infilecwder

def mkdtemp():
    '''
    Make temporary directory and register it to be removed with ``atexit``.
    '''

    atmpdir = tempfile.mkdtemp()
    if not fakefs.is_setup():
        atexit.register(rmrf,atmpdir)
    return atmpdir

def intmpiflist(f
    ,suffix=None #.dot, .uml, ... or rst.stpl,...
    ):
    """
    Wraps f(infile,outfile) returning None
    to produce a temporary directory/file for when infile is a list of strings.
    The temporary directory/file is removed only via atexit. 

    To make this have an effect use after ``readin``

    - includes ``normoutfile``

    If outfile is None, outfile is derived from suffix,
    which can be `rest.stpl`, `png.svg`;
    If suffix is `.svg`, ..., png is assumed and will be placed into ``_images``.

    """

    @wraps(f)
    def intmpiflister(*args, **kwargs):
        infile,outfile,e,args = _unioe(args)
        suf0,suf1 = suffix.split('.')
        if isinstance(infile,list) and infile:
            if outfile:
                outfile = abspath(outfile)
            atmpdir = mkdtemp()
            content = _joinlines(infile).encode('utf-8')
            if outfile:
                infn = stem(base(outfile))
            else:
                infn = sha(content).hexdigest()
            infile = normjoin(atmpdir,infn+'.'+suf1)
            with open(infile,'bw') as ff:
                ff.write(content)
            return normoutfile(f,suf0)(infile, outfile, e, *args, **kwargs)
        return normoutfile(f,suf0)(infile, outfile, e, *args, **kwargs)
    return intmpiflister

def readin(f):
    """
    Decorator to read in file content and pass it on to the wrapped function.

    The third parameter is replaced by the config.
    """

    @wraps(f)
    def readiner(*args, **kwargs):
        infile,outfile,e,args = _unioe(args)
        if isinstance(infile,str):
            config = conf_py(dir(infile))
            with open(infile) as inf:
                return f(inf.readlines(),outfile, config, *args,**kwargs)
        return f(infile, outfile, e, *args, **kwargs)
    return readiner

def run_inkscape(
    infile #.svg, .eps, .pdf filename string or list with actual .eps or .svg data
    ,outfile #.png file name
    ):
    '''
    Uses ``inkscape`` commandline to convert to ``.png``

    '''
    cmd(
        ['inkscape','-z','--export-dpi=%s'%DPI,
         '--export-area-drawing','--export-background-opacity=0',
         infile,'--export-png='+outfile]
      ,outfile=outfile
      )

def rst_sphinx(
    infile #.txt, .rst, .rest filename (normally index.rest)
    ,outfile #the path to the target file (not target directory)
    ,outtype=None #html,... or any other sphinx writer
    ,**config #keys from config_defaults
    ):
    '''
    Run Sphinx on infile.

    >>> cd(dir(__file__))
    >>> cd('../doc')

    >>> dry_run(True)
    #>>> ls()
    #>>> fakefs.is_setup()

    >>> infile,outfile = ('index.rest','../../build/doc/sphinx_html/index.html') # doctest: +ELLIPSIS
    >>> rst_sphinx(infile,outfile)
    run (['sphinx-build', '-b', 'html', '.', 'build/doc/sphinx_html', '-C', ... 'master_doc=index.rest'],) ...

    >>> rst_sphinx('dd.rest','../../build/doc/sphinx_html/dd.html') # doctest: +ELLIPSIS
    run (['sphinx-build', '-b', 'singlehtml', ..., '-D', 'master-doc=dd.rest'],) ...

    >>> rst_sphinx('dd.rest','../../build/doc/sphinx_latex/dd.tex') # doctest: +ELLIPSIS
    run (['sphinx-build', '-b', 'latex', ..., '-D', 'project=rstdoc', ...],) ...

    >>> dry_run(False)

    '''
    cfgt = {}
    cfgt.update(config_defaults)
    cfgt.update(config)
    dfn = lambda n,v:['-D',n+'='+v]
    indr,infn = dir_base(infile)
    if not indr:
        indr = '.'
    outdr,outn = dir_base(outfile)
    outnn,outne = stem_ext(outn)
    cfg = {}
    cfg.update({k:v for k,v in cfgt.items() if k in sphinx_config_keys and 'latex' not in k and k!='html_extra_path'})
    #html_extra_path is done here below
    cfg.update({k:v for k,v in sphinx_enforced.items() if 'latex' not in k})
    cfg['master_doc'] = steminfn = stem(infn)
    if not outtype:
        if outne=='.html':
            if infn.startswith('index.'):
                outtype = 'html'
            else:
                outtype = 'singlehtml'
        elif outne=='tex':
            outtype = 'latex'
        else:
            outtype = outne.strip('.')
    latex_elements = []
    latex_documents = []
    if 'latex' in outtype:
        cfg.update({k:v for k,v in cfgt.items() if k in sphinx_config_keys and 'latex' in k})
        cfg.update({k:v for k,v in sphinx_enforced.items() if 'latex' in k})
        try:
            latex_elements = ([['-D',"latex_elements.%s=%s"%(k,v.replace('\n',''))] for k,v in cfg['latex_elements'].items()]+
                [['-D','latex_engine=xelatex']])
        except: pass
        del cfg['latex_elements']
        del cfg['latex_engine']
        project = cfg.get('project',stem(infn))
        author = cfg.get('author','')
        #there seems to be a sphinx bug when this is in command line
        latex_documents = []#[['-D',"latex_documents=[(%s,%s,%s,%s,%s,%s)]"%(
                            #    infn,steminfn+'.latex',project,author,'manual',0
                            #    )]]
    extras = ['-C']+reduce(lambda x,y:x+y,
        [['-D',"%s=%s"%(k,(','.join(v)if isinstance(v,list) else v))
          ] for k,v in cfg.items()]+ latex_elements + latex_documents)
    sphinxcmd = ['sphinx-build','-b',outtype,indr,outdr]+extras
    cmd(sphinxcmd,outfile=outfile)
    if 'latex' in outtype:
        texfile = next(x  for x in os.listdir(outdr) if x.endswith('.tex'))
        os.rename(normjoin(outdr,texfile),outfile)
    if 'html' in outtype and 'html_extra_path' in cfgt:
        for epth in cfgt['html_extra_path']:
            try:
                cp(epth,outdr)
            except FileNotFoundError:
                pass

def _copy_images_for(infile,outfile):
    imgdir,there = here_or_updir(dir(infile),_images)
    if there==1:
        imgdir_tgt = normjoin(dir(outfile),_images)
    elif there==2:
        imgdir_tgt = normjoin(dir(dir(outfile)),_images)
    else:
        return
    if exists(imgdir) and imgdir!=imgdir_tgt:
        if not exists(imgdir_tgt):
            mkdir(imgdir_tgt)
        for x in os.listdir(imgdir):
            frm,twd =  normjoin(imgdir,x),normjoin(imgdir_tgt,x)
            docpy = filenewer(frm,twd)
            if docpy:
                cp(frm,twd)

def PageBreakHack(destination_path):
    '''
    This introduces a ``PageBreak`` style into ``content.xml``
    to allow the following raw page break of opendocument odt::

      .. raw:: odt

          <text:p text:style-name="PageBreak"/>

    This is no good solution, as it introduces an empty line at the top of the new page.

    Unfortunately the following does not work
    with or without ``text:use-soft-page-breaks="true"``

        .. for docutils
        .. raw:: odt

            <text:p text:style-name="PageBreak"/>

        .. for pandoc
        .. raw:: opendocument

            <text:p text:style-name="PageBreak"/>

    According to C066363e.pdf it should work.

    See ``utility.rst.tpl`` in the ``--stpl`` samples.
    '''

    from zipfile import ZipFile
    odtzip = OrderedDict()
    with ZipFile(destination_path) as z:
        for n in z.namelist():
          with z.open(n) as f:
              content = f.read()
              if n =='content.xml':
                  #break-after produces two page breaks
                  content = content.replace(
                      b'</office:automatic-styles>',
                      b' '.join(x.strip() for x in b'''<style:style
                      style:name="PageBreak"
                      style:family="paragraph"
                      style:master-page-name="rststyle-pagedefault"
                      style:parent-style-name="Standard">
                      <style:paragraph-properties fo:break-before="page"/>
                      </style:style>
                      </office:automatic-styles>'''.splitlines())
                      )
                  content = content.replace(
                      b'<office:text>',
                      b'<office:text text:use-soft-page-breaks="true">'
                      )
          odtzip[n]=content
    with ZipFile(destination_path,'w') as z:
        for n,content in odtzip.items():
            with z.open(n,mode='w',force_zip64=True) as f:
                f.write(content)

def rst_pandoc(
    infile #.txt, .rst, .rest filename
    ,outfile #the path to the target document
    ,outtype #html,... 
    ,**config  #keys from config_defaults
    ):
    '''
    Run Pandoc on infile.

    '''
    cfg = {}
    cfg.update(config_defaults)
    cfg.update(config)
    pandoccmd = ['pandoc','--standalone','-f','rst']+cfg.get('pandoc_opts',{}).get(outtype,[]
        )+['-t','latex' if outtype=='pdf' else outtype,infile,'-o',outfile]
    opt_refdoc = cfg.get('pandoc_doc_optref',{}).get(outtype,'')
    if opt_refdoc:
        if isinstance(opt_refdoc,dict):
            opt_refdoc = opt_refdoc.get(base(infile),'')
        if opt_refdoc:
            refoption,refdoc = opt_refdoc.split()
            refdoc,there = here_or_updir('.',refdoc)
            if there:
                pandoccmd.append(refoption)
                pandoccmd.append(abspath(refdoc))
    stdout = cmd(pandoccmd,outfile=outfile)
    if outtype.endswith('html') or outtype.endswith('latex'):
        _copy_images_for(infile,outfile)
    elif outtype.endswith('odt'):
        PageBreakHack(outfile)
    return stdout

def rst_rst2(
    infile #.txt, .rst, .rest filename
    ,outfile #the path to the target document
    ,outtype #html,... 
    ,**config  #keys from config_defaults
    ):
    '''
    Run the rst2xxx docutils fontend tool on infile.

    '''
    cfg = {}
    cfg.update(config_defaults)
    cfg.update(config)
    destination_path=outfile if outfile!='-' else None
    if outtype=='odt':
        outtype='odf_odt'
    stdout = None
    if isinstance(infile,list):
        source = '.. default-role:: math\n'+_joinlines(infile)
        stdout = publish_string(
            source
            ,destination_path=destination_path
            ,writer_name=outtype
            ,settings_overrides = cfg['rst_opts']
            )
    else:
        publish_file(
            source_path=infile
            ,destination_path=destination_path
            ,writer_name=outtype
            ,settings_overrides = cfg['rst_opts']
            )
    if destination_path:
        if outtype.endswith('html') or outtype.endswith('latex'):
            _copy_images_for(infile,outfile)
        elif outtype.endswith('odt'):
            PageBreakHack(destination_path)
    return stdout

#sphinx_html,rst_html,[pandoc_]html
rst_tools = {
    'pandoc': rst_pandoc
    ,'sphinx': rst_sphinx
    ,'rst': rst_rst2
    }

@png_post_process_if_any
@normoutfile
@readin
def svgpng(
    infile #a .svg file name or list of lines
    ,outfile=None #if not provided the input file with new extension ``.png`` either in ``./_images`` or ``../_images`` or ``.``
    ,*args #needed by decorators
    ):
    '''
    Converts a .svg file to a png file.

    '''
    tools.svg2png(bytestring=_joinlines(infile),write_to=outfile,dpi=DPI)

@png_post_process_if_any
@partial(intmpiflist,suffix='.tex')
@infilecwd
def texpng(
    infile #a .tex file name or list of lines (provide outfile in the latter case)
    ,outfile=None #if not provided, the input file with .png either in ``./_images`` or ``../_images`` or ``.``
    ,*args #needed by decorators
    ):
    '''
    Latex has several graphic packages, like

    - tikz
    - chemfig

    that can be converted to .png with this function.

    For ``.tikz`` file use |tikzpng|.

    '''

    pdffile = stem(infile)+'.pdf'
    try:
        cmd(['xelatex', '-interaction=nonstopmode', infile],outfile=pdffile)
    except RstDocError as e:
        with open(infile) as latex:
            raise RstDocError(str(e)+'\n[latex]\n'+latex.read())
    run_inkscape(pdffile,outfile)

def _texwrap(f):
    @wraps(f)
    def _texwraper(*args, **kwargs):
        texlns,outfile,config,args = _unioe(args)
        content = _joinlines(texlns)
        latex = config['tex_wrap']%content
        return f(latex.splitlines(),outfile,config,*args, **kwargs)
    return _texwraper

def _tikzwrap(f):
    @wraps(f)
    def _tikzwraper(*args, **kwargs):
        tikzlns,outfile,e,args = _unioe(args)
        content = _joinlines(tikzlns).strip()
        tikzenclose = [r'\begin{tikzpicture}','%s',r'\end{tikzpicture}']
        if not content.startswith(tikzenclose[0]):
            content = _joinlines(tikzenclose)%content
        return f(content.splitlines(),outfile,e,*args, **kwargs)
    return _tikzwraper

'''
Converts a .tikz file to a png file.
'''
tikzpng = normoutfile(readin(_tikzwrap(_texwrap(texpng))))

@png_post_process_if_any
@partial(intmpiflist,suffix='.dot')
@infilecwd
def dotpng(
    infile #a .dot file name or list of lines (provide outfile in the latter case)
    ,outfile=None #if not provided the input file with new extension ``.png`` either in ``./_images`` or ``../_images`` or ``./``
    ,*args #needed by decorators
    ):
    '''
    Converts a .dot file to a png file.

    '''

    cmd(
        ['dot','-Tpng',infile,'-o',outfile]
        ,outfile=outfile
        )

@png_post_process_if_any
@partial(intmpiflist,suffix='.uml')
@infilecwd
def umlpng(
    infile #a .uml file name or list of lines (provide outfile in the latter case)
    ,outfile=None #if not provided the input file with new extension ``.png`` either in ``./_images`` or ``../_images`` or ``./``
    ,*args #needed by decorators
    ):
    '''
    Converts a .uml file to a png file.

    '''

    cmd(
        ['plantuml','-tpng',infile,'-o'+dir(outfile)]
        ,shell=sys.platform=='win32'
        ,outfile=outfile
        )

@png_post_process_if_any
@partial(intmpiflist,suffix='.eps')
@infilecwd
def epspng(
    infile #a .eps file name or list of lines (provide outfile in the latter case)
    ,outfile=None #if not provided the input file with new extension ``.png`` either in ``./_images`` or ``../_images`` or ``./``
    ,*args #needed by decorators
    ):
    '''
    Converts an .eps file to a png file using inkscape.

    '''

    run_inkscape(infile,outfile)

@png_post_process_if_any
@normoutfile
@infilecwd
@readin
def pygpng(
    infile #a .pyg file name or list of lines (provide outfile in the latter case)
    ,outfile=None #if not provided the input file with new extension ``.png`` either in ``./_images`` or ``../_images`` or ``./``
    ,*args #needed by decorators
    ):
    '''
    Converts a .pyg file to a png file.

    ``.pyg`` contains python code that produces a graphic.
    If the python code defines a ``save_to_png`` function, then that is used.
    Else the following is tried

    - ``pyx.canvas.canvas`` from the `pyx <http://pyx.sourceforge.net/manual/graphics.html>`__ library or 
    - ``svgwrite.drawing.Drawing`` from the `svgwrite <https://svgwrite.readthedocs.io>`__ library or 
    - ``cairocffi.Surface`` from `cairocffi <https://cairocffi.readthedocs.io/en/stable/overview.html#basic-usage>`__
    - ``pygal.Graph`` from `pygal <https://pygal.org>`__
    - `matplotlib <https://matplotlib.org>`__. If ``matplotlib.pyplot.get_fignums()>1`` the figures result ``<name><fignum>.png`` 

    '''

    pygcode = _joinlines(infile)
    pygvars={}
    eval(compile(pygcode,outfile,'exec'),pygvars)
    if 'save_to_png' in pygvars:
        pygvars['save_to_png'](outfile)
    else:
        for k,v in pygvars.items():
            if isinstance(v,pyx.canvas.canvas):
                tools.svg2png(bytestring=v._repr_svg_(),write_to=outfile, dpi=DPI)
                break
            elif isinstance(v,pygal.Graph):
                tools.svg2png(bytestring=v.render(),write_to=outfile, dpi=DPI)
                break
            elif isinstance(v,cairocffi.Surface):
                v.write_to_png(target=outfile)
                break
            elif svgwrite and isinstance(v,svgwrite.drawing.Drawing):
                svgio = io.StringIO()
                d.write(svgio)
                svgio.seek(0)
                svgsrc= svgio.read()
                tools.svg2png(bytestring=svgsrc,write_to=outfile, dpi=DPI)
                break
            else: #try matplotlib.pyplot
                try:
                    fignums = plt.get_fignums()
                    if len(fignums) == 0: 
                        continue
                    if len(fignums) > 1: 
                        #makename('a.b',1)#a1.b
                        makename=lambda x,i: ('{0}%s{1}'%i).format(*stem_ext(x))
                    else:
                        makename=lambda x,i: x
                    for i in fignums:
                        plt.figure(i).savefig(makename(outfile,i),format='png')
                        plt.close(i)
                    break
                except: 
                    continue

@infilecwd
def dostpl(
    infile #a .stpl file name or list of lines
    ,outfile=None #if not provided the expanded is returned
    ,lookup=None #lookup paths must be relative to infile
    ,**kwargs
    ):
    '''
    Expands an `.stpl <https://bottlepy.org/docs/dev/stpl.html>`__ file.

    >>> infile = ['hi {{2+3}}!']
    >>> dostpl(infile)
    ['hi 5!']

    The whole ``rstdoc.dcx`` namespace is forwarded to the template code.


    '''
    if not lookup:
        lookup = ['.','..']
    if isinstance(infile,list):
        lookup = [abspath(x) for x in lookup]
        try:
            filename = abspath(outfile)
        except: 
            filename = None
        infile = _joinlines(infile)
    else:
        lookup = [abspath(normjoin(dir(infile),x)) for x in lookup]
        filename = abspath(infile)
    variables = {}
    variables.update(globals())
    variables.update(kwargs)
    variables.update({'__file__':filename})
    if filenewer(infile,outfile):
        st=stpl.template(infile
                ,template_settings={'escape_func':lambda x:x}
                ,template_lookup = lookup
                ,**variables
                #,__file__ = filename
                #,**kwargs
                )
        if outfile:
            with opnwrite(outfile) as f:
                f.write(st)
        else:
            return st.replace('\r\n','\n').splitlines(keepends=True)

def dorst(
    infile #a .rest, .rst, .txt file name or list of lines
    ,outfile=None #None and '-' mean standard out
                  #for .rest |xxx| substitutions for reST link targets in infile are appended if no ``_links_sphinx.rst`` there
    ,outinfo=None #specifies the tool to use 
                  #'html', 'docx', 'odt',... via pandoc if output 
                  #'sphinx_html',... via sphinx
                  #'rst_html',... via rst2xxx frontend tools
                  #'[infile/][substitution.]docx[.]' substitutions stands for the file used in substitutions if no ``_links_sphinx.rst``
                  #The infile is used, if the actual infile are lines. The final dot tells to stop after substitutions.
    ,fn_i_ln=None #(fn,i,ln) of the .stpl with all stpl includes sequenced (used by convert())
    ):
    '''
    Default interpreted text role is set to math.
    The link lines are added to a .rest file.

    >>> cd(dir(__file__))
    >>> cd('../doc')

    >>> dorst('dd.rest') # doctest: +ELLIPSIS
    .. default-role:: math...

    >>> dorst('ra.rest.stpl') # doctest: +ELLIPSIS
    .. default-role:: math...

    >>> dorst(['hi there']) # doctest: +ELLIPSIS
    .. default-role:: math...
    hi there

    >>> dorst(['hi there'],None,'html') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', '-'],) ...

    >>> dorst('ra.rest.stpl','ra.docx') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', 'ra.docx'],) ...

    >>> dorst(['hi there'],'test.html') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', 'test.html'],) ...

    >>> dorst(['hi there'],'test.html','sphinx_html') # doctest: +ELLIPSIS
    run (['sphinx-build',...

    >>> dorst(['hi there'],'test.html','sphinx') # doctest: +ELLIPSIS
    run (['sphinx-build',...

    >>> dorst(['hi there'],'test.odt','rst') # doctest: +ELLIPSIS
    run (['rst2odt.py', ...
    
    '''

    rsttool = rst_tools['pandoc']
    dinfo,binfo = None,None
    if outinfo:
        dinfo,binfo = dir_base(outinfo)
        outinfo = binfo
    try:
        rsttool,outinfo = outinfo.split('_')
        try:
            rsttool = rst_tools[rsttool]
        except:
            rsttool = None
    except: pass
    if isinstance(infile,str):
        infile = abspath(infile)
        if rsttool!=rst_sphinx:
            with open(infile) as f:
                filelines = f.readlines()
    else:
        filelines = infile
        infile = dinfo
        if not infile:
            infile = 'rest'
        infile = abspath(infile+_rest)
    sysout = None
    finalsysout = None
    try:
        if outfile is None or outfile=='-':
            try:
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            except: pass
            sysout = sys.stdout
            if not outinfo:
                outinfo = 'rest'
            if outinfo.strip('.').find('.')<0:
                outfile = stem(base(infile))+'.'+outinfo.strip('.') #- - infile.docx
            else:
                outfile = outinfo.strip('.') #- - otherfile.docx
        else:
            _,ofext = stem_ext(outfile)
            ofext = ofext.strip('.')
            if not outinfo: #x.rst a/b/c.docx
                outinfo = ofext
            elif outinfo in rst_tools: #x.rst a/b/c.docx pandoc
                rsttool = rst_tools[outinfo]
                outinfo = ofext
        if outinfo.endswith('.'):   #x.rest - docx.
            rsttool = None          #... will output the rest code with links for docx
        #drop file info from outinfo
        outinfo = outinfo.strip('.')
        t,outinfo = stem_ext(outinfo)
        if not outinfo:
            outinfo = t
        outinfo = outinfo.strip('.')
        if _is_rest_type(outinfo):
            rsttool = None #no further processing wanted, sysout is final
        if not rsttool and not sysout:
            sysout  = opnwrite(outfile)
        tmprestindir = None

        if rsttool!=rst_sphinx: #sphinx can read substitutions from included files
            if rsttool:
                finalsysout = sysout
                tmprestindir = normjoin(dir(infile),base(outfile)+'.rest')
                sysout = opnwrite(tmprestindir)
                infile = tmprestindir
                if not fakefs.is_setup():
                    atexit.register(rmrf,tmprestindir)
            if sysout:
                sysout.write('.. default-role:: math\n')
                links_done = False
                for x in filelines:
                    if x.startswith('.. include:: _links_sphinx.rst'):
                        linksfilename = normjoin(dir(infile),'_links_'+outinfo+'.rst')
                        if exists(linksfilename):
                            with open(linksfilename) as f:
                                sysout.write(f.read())
                                links_done = True
                    else:
                        sysout.write(x)
                if not links_done:
                    sysout.write('\n')
                    filenoext=stem(outfile)
                    for tgt in RstFile.make_tgts(filelines,infile
                        ,make_counters()
                        ,fn_i_ln):
                        sysout.write(tgt.create_link(outinfo.replace('rest','html'),filenoext))

        if rsttool:
            if finalsysout and rsttool!=rst_sphinx:
                outfile = '-'
            config = conf_py(dir(infile))
            if sysout:
                sysout.close()
                sysout = None
            stdout = rsttool(infile,outfile,outinfo,**config)
            if stdout!=None and finalsysout and rsttool!=rst_sphinx:
                finalsysout.write(stdout)
    finally:
        for x in [sysout,finalsysout]:
            if x is not None and x != sys.stdout:
                x.close()

converters = {
    _svg:   svgpng
    ,_tikz: tikzpng
    ,_tex:  texpng
    ,_dot:  dotpng
    ,_uml:  umlpng
    ,_eps:  epspng
    ,_pyg:  pygpng
    ,_stpl:  dostpl
    ,_rst:  dorst
    ,_rest:  dorst
    ,_txt:  dorst
}
graphic_extensions = {_svg,_tikz,_tex,_dot,_uml,_eps,_pyg}

def convert(
    infile #any of '.tikz' '.svg' '.dot' '.uml' '.eps' '.pyg' or else stpl is assumed
    ,outfile = None  #'-' means standard out, else a file name, or None for automatic
    ,outinfo = None  #'html', 'sphinx_html', 'docx', 'odt', 'file.docx',... interpet input as rest, else specifies graph type
    ):
    '''
    Converts the known files.

    Stpl files are immediately forwarded to the next converter.

    The main job is to normalized the input params, because this is called from main() and via Python.
    The it forwards to the right converter.

    >>> cd(dir(__file__))
    >>> cd('../doc')

    >>> convert(['hi {{2+3}}!'])
    ['hi 5!']

    >>> dry_run(True)

    >>> infile,outfile,outinfo = (["newpath {{' '.join(str(i)for i in range(4))}} rectstroke showpage"],'tst.png','eps')
    >>> convert(infile,outfile,outinfo) # doctest: +ELLIPSIS
    run (['inkscape', ...tst.png'],) ...

    >>> convert('ra.rest.stpl') # doctest: +ELLIPSIS
    .. default-role:: math
    ...

    >>> convert('ra.rest.stpl','ra.docx') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', 'ra.docx'],) ...

    >>> convert('ra.rest.stpl','ra.docx','sphinx') # doctest: +ELLIPSIS
    run (['sphinx-build', ...

    >>> convert('dd.rest',None,'html') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', '-'],) ...

    >>> convert('dd.rest','html') # doctest: +ELLIPSIS
    run (['pandoc', ..., '-o', 'dd.html'],) ...

    >>> convert('index.rest','../../build/doc/sphinx_singlehtml') # doctest: +ELLIPSIS
    run (['sphinx-build', '-b', 'singlehtml', ..., '../../build/doc', ...],) ...

    >>> dry_run(False)

    '''

    afile = False
    try:
        afile = infile and isfile(infile) or False
    except:
        pass
    if not afile and infile == '-':
        try:
            sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach()) 
        except: pass
        infile = sys.stdin.readlines()
    if infile:
        if outinfo==None:
            if outfile=='-':
                outinfo = 'rest'
            elif outfile==None:
                outinfo = 'html'
        if isinstance(infile,str):
            nextinfile,fext = stem_ext(infile)
        else:
            fext = _stpl
            if outinfo and _is_graphic_type(outinfo):
                nextinfile = outinfo.strip('.')+'.'+outinfo.strip('.')
            else:
                nextinfile = 'rest'+_rest
                if not outinfo:
                    outinfo = 'rest'
        fn_i_ln = None
        while fext in converters:
            try:
                nextinfile,fextnext = stem_ext(nextinfile)
            except:
                fextnext = None
            thisconverter = converters[fext]
            if  thisconverter == dorst:
                infile = thisconverter(infile, outfile if not fextnext else None, outinfo, fn_i_ln)
            else:
                if thisconverter == dostpl:
                    if fextnext and converters[fextnext]==dorst: #save infile for dorst() in outinfo as "infile/outinfo"
                        if isinstance(infile,list):
                            fn_i_ln = list(_flatten_stpl_includes_it(infile))
                        else:
                            fn_i_ln = _flatten_stpl_includes(infile)
                        outinfo = nextinfile+'/'+(outinfo or '')
                infile = thisconverter(infile, outfile if not fextnext else None)
            if not infile:
                break
            if not fextnext:
                break
            if not outfile:
                if _is_graphic_type(fextnext):
                    outfile = _imgout(nextinfile+fextnext)
            fext = fextnext
        return infile

def rindices(
    r #regular expression string or compiled
    ,lns #lines
    ):
    r'''
    Return the indices matching the regular expression ``r``.

    ::

      >>> lns=['a','ab','b','aa']
      >>> [lns[i] for i in rindices(r'^a\w*',lns)]==['a', 'ab', 'aa']
      True

    '''

    if isinstance(r,str):
        r = re.compile(r)
    for i,ln in enumerate(lns):
        if r.search(ln):
            yield i 

def rlines(
    r #regular expression string or compiled
    ,lns #lines
    ):
    '''
    Return the lines matched by ``r``.

    '''

    return [lns[i] for i in rindices(r,lns)]

def intervals(
    nms #list of indices
    ):
    """
    Return intervals between numbers.

    ::

      >>> intervals([1,2,3])==[(1, 2), (2, 3)]
      True

    """
    return list(zip(nms[:],nms[1:]))

def in2s(
    nms #list of indices
    ):
    """
    Convert the list into a list of couples of two elements.
    
    ::

      >>> in2s([1,2,3,4])==[(1, 2), (3, 4)]
      True

    """
    return list(zip(nms[::2],nms[1::2]))

#re.search(reid,'OpenDevices = None').groups()
#re.search(reid,'def OpenDevices(None)').groups()
#re.search(reid,'class OpenDevices:').groups()
#re.search(reid,'    def __init__(a,b):').groups()
#re.search(relim,"  '''prefix. ").groups()
#re.search(relim,"  '''").groups()

def doc_parts(
    lns #list of lines
    ,relim=r"^\s*'''([\w.:]*)\s*\n*$" #regular expression marking lines enclosing the documentation. The group is a prefix.
    ,reid=r"\s(\w+)[(:]|(\w+)\s\=" #extract id from preceding or succeeding non-empty lines
    ,reindent=r'[^#/\s]' #determines start of text
    ,signature=None #if signature language is given the preceding or succeeding lines will be included
    ,prefix='' #prefix to make id unique, e.g. module name. Include the dot.
    ):
    '''
    ``doc_parts()`` yields doc parts delimeted by ``relim`` regular expression
    possibly with id, if ``reid`` matches 

    If start and stop differ use regulare expression ``|`` in ``relim``.

    ::

      >>> with open(__file__) as f:
      ...     lns = f.readlines()
      ...     docparts = list(doc_parts(lns,signature='py'))
      ...     doc_parts_line = rlines('doc_parts',docparts)
      >>> doc_parts_line[1]
      'doc_parts(\n'

    - There is no empty line between doc string and preceding code lines that should be included.
    - There is no empty line between doc string and succeeding code lines that should be included.
    - Included code lines end with an empty line.

    In case of ``__init__()`` the ID can come from the ``class`` line
    and the included lines can be those of ``__init__()``,
    if there is no empty line between the doc string and ``class`` above as well as ``_init__()`` below.

    If the included code comes only from one side of the doc string, have an empty line at the other side.

    Immediately after the initial doc string marker there can be a prefix, e.g. ``classname.``.

    '''

    rlim = re.compile(relim)
    rid = re.compile(reid)
    rindent = re.compile(reindent)
    def foundid(lnsi):
        if not lnsi.strip():#empty
            return False
        id = rid.search(lnsi)
        if id and id.groups():
            ids = [x for x in id.groups() if x is not None]
            if len(ids) > 0:
                return ids[0]
    ids = []
    def checkid(rng):
        i = None
        for i in rng:
            testid = foundid(lns[i])
            if testid is False:
                break
            elif not ids and isinstance(testid,str):
                ids.append(testid)
        return i
    for a,b in in2s(list(rindices(rlim,lns))):
        try:
            thisprefix = rlim.search(lns[a]).groups()[0]
        except:
            thisprefix = ''
        ids.clear()
        i = checkid(range(a-1,0,-1))
        j = checkid(range(b+1,len(lns)))
        if ids:
            yield ''
            yield '.. _`'+prefix+thisprefix+ids[0]+'`:\n'
            yield ''
            yield ':'+prefix+thisprefix+ids[0]+':\n'
            yield ''
        if signature:
            if i is not None and i < a and i > 0:
                if not lns[i].strip():#empty
                    i = i+1
                if i < a:
                    yield '.. code-block:: '+signature+'\n'
                    yield ''
                    yield from ('   '+x for x in lns[i:a])
                    yield ''
            if j is not None and j > b+1 and j < len(lns):
                if not lns[j].strip():#empty
                    j = j-1
                if j > b:
                    yield '.. code-block:: '+signature+'\n'
                    yield ''
                    yield from ('   '+x for x in lns[b+1:j+1])
                    yield ''
        indent = 0
        for ln in lns[a+1:b]:
            lnst = rindent.search(ln)
            if lnst and lnst.span():
                indent = lnst.span()[0]
                break;
        yield from (x[indent:] for x in lns[a+1:b])

#for generator function, instead of lru_cache()
_Tee = tee([], 1)[0].__class__
def _memoized(f):
    cache={}
    def ret(*args):
        if args not in cache:
            cache[args]=f(*args)
        if isinstance(cache[args], (GeneratorType, _Tee)):
            cache[args], r = tee(cache[args])
            return r
        return cache[args]
    return ret

@lru_cache()
def _read_lines(fn):
    lns = []
    with open(fn) as f:
        lns = f.readlines()
    return lns

@_memoized
def rstincluded(
    fn #file name without path
    ,paths=() #paths where to look for fn
    ,withimg=False #also yield image files, not just other rst files
    ,withrest=False #rest files are not supposed to be included
    ):
    '''
    Yield the files recursively included from an RST file.

    >>> cd(dir(__file__))
    >>> list(rstincluded('ra.rest',paths=('../doc',)))
    ['ra.rest.stpl', '_links_sphinx.rst']
    >>> list(rstincluded('sr.rest',paths=('../doc',)))
    ['sr.rest', '_links_sphinx.rst']
    >>> list(rstincluded('meta.rest',paths=('../doc',)))
    ['meta.rest', 'files.rst', '_traceability_file.rst', '_links_sphinx.rst']
    >>> 'dd.rest'in list(rstincluded('index.rest',paths=('../doc',)))
    True

    '''

    p = ''
    for p in paths:
        nfn = normjoin(p,fn)
        if exists(nfn+_stpl): #first, because original
            nfn = nfn+_stpl
            yield fn+_stpl
            break
        elif exists(nfn): #while this might be generated
            yield fn
            break
    else:
        nfn = fn
        yield fn
    lns = _read_lines(nfn)
    toctree = False
    if lns:
        for e in lns:
            if toctree:
                toctreedone = False
                if e.startswith(' '):
                    fl=e.strip()
                    if fl.endswith(_rest) and exists(normjoin(p,fl)):
                        toctreedone = True
                        yield from rstincluded(fl,paths)
                    continue
                elif toctreedone:
                    toctree = False
            if e.startswith('.. toctree::'):
                if withrest:
                    toctree = True
            elif e.strip().startswith('.. '):
                #e = '  .. include:: some.rst'
                #e = '  .. include:: ../some.rst'
                #e = '.. include:: some.rst'
                #e = '.. include:: ../some.rst'
                #e = '  .. image:: some.png'
                #e = '.. image:: some.png'
                #e = '  .. figure:: some.png'
                #e = '  .. |x y| image:: some.png'
                try:
                    f,t,_ = rerstinclude.split(e)
                    nf = not f.strip() and t
                    if nf:
                        if is_rest(nf) and not withrest:
                            continue
                        yield from rstincluded(nf.strip(),paths)
                except:
                    if withimg:
                        m = reximg.search(e)
                        if m:
                            yield m.group(1)
            elif restplinclude.match(e): 
                #e="%include('some.rst.tpl',v='param')"
                #e="   %include('some.rst.tpl',v='param')"
                f,t,_=restplinclude.split(e)
                nf = not f.strip() and t
                if nf:
                    thisnf = normjoin(p,nf)
                    if not exists(thisnf):
                        parntnf = normjoin(p,'..',nf)
                        if exists(parntnf): 
                            nf = parntnf
                        else:
                            continue
                    yield from rstincluded(nf.strip(),paths)

_traceability_instance = None
class Traceability:
    def __init__(self,tracehtmltarget):
        self.tracehtmltarget= tracehtmltarget
        self.fcaobjsets = [] #in FCA sense: set of target tgt with all its links to other targets 
        global _traceability_instance
        _traceability_instance = self
        self.counters = None
    def append(self,aset):
        self.fcaobjsets.append(aset)
    def isempty(self):
        return len(self.fcaobjsets)==0
    def create_traceability_file(self,directory): #returns the rst lines of _traceability_file
        if not pyfca:
            return
        if not self.fcaobjsets:
            return []
        config = conf_py(directory)
        target_id_group = config['target_id_group']
        target_id_color = config['target_id_color']
        def _drawnode(canvas,node,parent,center,radius): 
            fillcolors = []
            nodetgtgrps = {target_id_group(x) for x in node.intent}
            for _,(groupid,groupcolor) in target_id_color.items():
                if groupid in nodetgtgrps:
                    fillcolors.append(groupcolor)
            n_grps = len(fillcolors)
            for i in range(n_grps-1,-1,-1):
                rr = int(radius*(i+1)/n_grps)
                parent.add(canvas.circle(center,rr,fill=fillcolors[i],stroke='black'))
        fca = pyfca.Lattice(self.fcaobjsets,lambda x:x)
        tr = 'tr'
        #|trXX|, |trYY|, ...
        reflist = lambda x,pfx=tr: ('|'+pfx+('|, |'+pfx).join([str(e)for e in sorted(x)])+'|') if x else ''
        trace = [(".. _`"+tr+"{0}`:\n\n:"+tr+"{0}:\n\n{1}\n\nUp: {2}\n\nDown: {3}\n\n").format(
                n.index, reflist(n.intent,''), reflist(n.up), reflist(n.down))
                for n in fca.nodes]
        tlines = ''.join(trace).splitlines(keepends=True)
        imgpath,there = here_or_updir(directory,_images)
        if not there:
            imgpath = normjoin(directory,_images)
            mkdir(imgpath)
        trcpath = normjoin(relpath(imgpath,start=directory),_traceability_file)
        tlines.extend(['.. _`trace`:\n','\n','.. figure:: '+trcpath+'.png\n','   :name:\n','\n',
          '   |trace|: `FCA <https://en.wikipedia.org/wiki/Formal_concept_analysis>`__ diagram of dependencies'])
        if target_id_color is not None:
            legend=', '.join([fnm+" "+clr for fnm,(_,clr) in target_id_color.items()])
            tlines.extend([': '+legend,'\n'])
        tlines.append('\n')
        with opnwrite(normjoin(directory,_traceability_file+_rst)) as f:
            f.write('.. raw:: html\n\n')
            f.write('    <object data="'+_traceability_file+'.svg" type="image/svg+xml"></object>\n')
            if target_id_color is not None:
                f.write('    <p><a href="https://en.wikipedia.org/wiki/Formal_concept_analysis">FCA</a> diagram of dependencies with clickable nodes: '+legend+'</p>\n\n')
            f.writelines(tlines)
        ld = pyfca.LatticeDiagram(fca,4*297,4*210)
        tracesvg = abspath(normjoin(imgpath,_traceability_file+'.svg'))
        ttgt = lambda : self.tracehtmltarget.endswith(_rest) and stem(self.tracehtmltarget) or self.tracehtmltarget
        ld.svg(target=ttgt()+'.html#'+tr,drawnode=_drawnode).saveas(tracesvg)
        tracepng = stem(tracesvg)+_png
        svgpng(tracesvg,tracepng)
        return tlines


def pair(
    alist #first list
    ,blist #second list longer or equal to alist
    ,cmp #compare function
    ):
    ''' 
    pair two sorted lists where the second must be at least as long as the first
    
    >>> alist=[1,2,4,7]
    >>> blist=[1,2,3,4,5,6,7]
    >>> cmp = lambda x,y: x==y
    >>> list(pair(alist,blist,cmp))
    [(1, 1), (2, 2), (None, 3), (4, 4), (None, 5), (None, 6), (7, 7)]

    >>> alist=[1,2,3,4,5,6,7]
    ... blist=[1,2,3,4,5,6,7]
    ... cmp = lambda x,y: x==y
    ... list(pair(alist,blist,cmp))
    [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

    '''

    i = 0
    for aa,bb in zip(alist,blist):
        if not cmp(aa,bb):
            break
        i = i+1
        yield aa,bb
    alen = len(alist)
    tlen = max(alen,len(blist))
    d = 0
    for j in range(i+1,alen):
        for dd in range(tlen-j-d):
            bb = blist[j+d+dd]
            if not cmp(alist[j],bb):
                yield None,bb
            else:
                yield alist[j],bb
                d = d+dd
                break
        else:
            return

def gen(
    source #either a list of lines of a path to the source code
    ,target=None #either save to this file or return the generated documentation
    ,fun=None #use ``#gen_<fun>(lns,**kw):`` to extract the documtenation
    ,**kw #kw arguments to the gen_<fun>() function
    ):
    r''' 
    Take the ``gen_[fun]`` functions enclosed by ``#def gen_[fun](lns,**kw)`` to create a new file.

    Example::

        >>> source=[i+'\\n' for i in """
        ...        #def gen(lns,**kw):
        ...        #  return [l.split('#@')[1] for l in rlines(r'^\s*#@',lns)]
        ...        #def gen
        ...        #@some lines
        ...        #@to extrace
        ...        """.splitlines()]
        >>> [l.strip() for l in gen(source)]
        ['some lines', 'to extrace']

    '''

    if isinstance(source,list):
        lns = source
        source = ""
    else:
        lns = []
        try:
            lns = _read_lines(source)
        except:
            sys.stderr.write("ERROR: {} cannot be opened\n".format(source))
            return
    if '.' not in sys.path:
        sys.path.append('.')
    if fun:
        gen_regex = r'#def gen_'+fun+r'(\w*(lns,\*\*kw):)*'
    else:
        gen_regex = r'#def gen(\w*(lns,\*\*kw):)*'
    iblks = list(rindices(gen_regex,lns))
    py3 = '\n'.join([lns[k][lns[i].index('#')+1:] 
            for i,j in in2s(iblks) 
            for k in range(i,j)])
    eval(compile(py3,source+'#gen','exec'),globals())
    if fun:
        gened = list(eval('gen_'+fun+'(lns,**kw)'))
    else:#else eval all gen_ funtions
        gened = []
        for i in iblks[0::2]:
            gencode = re.split("#def |:",lns[i])[1]#gen(lns,**kw)
            gened += list(eval(gencode))
    if target:
        drn = dir(target)
        if drn and not exists(drn):
            mkdir(drn)
        with opnwrite(target) as o:
            o.write(''.join(((x or '\n') for x in gened)))
    else:
        return gened

def parsegenfile(
    genpth #path to gen file
    ):
    '''
    Parse the file ``genpth`` which has format ::

      sourcefile | targetfile | suffix | kw paramams or {}

    ``suffix`` refers to ``gen_<suffix>``.

    The yields are used for the |dcx.gen| function.
    '''

    try:
        genfilelns = _read_lines(genpth)
    except:
        sys.stderr.write("ERROR: {} cannot be opened\n".format(genpth))
        return
        
    for ln in genfilelns:
        if ln[0] != '#':
            try:
              f,t,d,a = [x.strip() for x in ln.split('|')]
              kw=eval(a)
              yield f,t,d,kw
            except: pass

def _flatten_stpl_includes_it(fn):
    """
    This flattens the .stpl includes to have all targets align to those in the .rest file.
    Targets must be *explicit* in all ``.stpl`` and ``.tpl``, i.e. they must not be created by stpl code.
    This is needed to make the .tags jump to the original and not the generated file.
    """
    flns = []
    if isinstance(fn,str):
        if exists(fn):
            flns = _read_lines(fn)
        else:
            parnt = updir(fn)
            if exists(parnt):
                flns = _read_lines(parnt)
    else:
        flns = fn
        fn = '-'
    for i,ln in enumerate(flns):
        #ln = '% include("../test.rst.stpl",v="aparam")'
        m = restplinclude.match(ln)
        if m: 
            includedtpl = m.group(1)
            yield from _flatten_stpl_includes(normjoin(dir(fn),includedtpl))
        else:
            yield fn,i,ln

@lru_cache()
def _flatten_stpl_includes(fn):
    return list(_flatten_stpl_includes_it(fn))

class Tgt:
    
    line_search_range = 8

    def __init__(self
        ,lnidx #line index 
        ,target #target name
        ):
        self.lnidx = lnidx
        self.target = target
        self.tagentry = None #(path,line index)
        self.lnkname = None #link name

    def is_inside_literal(self,lns):
        try:#skip literal blocks
            indentation = re.search(r'\w',lns[self.lnidx]).span()[0]-3 
            if indentation>0:
                for iprev in range(self.lnidx-1,0,-1):
                   prev = lns[iprev]
                   if prev:
                       newspc,_ = next((ich,ch) for ich,ch in enumerate(prev) if ch!=' ' and ch!='\t')
                       if newspc<indentation:
                           prev = prev.strip()
                           if prev:
                               if not prev.startswith('.. ') and prev.endswith('::'):
                                   return True
                               return False
        except:
            pass

    def find_lnkname(self,lns,counters):
        lenlns = len(lns)
        lnkname = self.target
        for j in range(self.lnidx+2,self.lnidx+self.line_search_range):
            #j=i+2
            if j > lenlns-1:
                break
            lnj = lns[j]
            if rextitle.match(lnj):
                lnkname=lns[j-1].strip()
                if not lnkname:
                    lnkname=lns[j+1].strip()
                break
            #j,lns=1,".. figure::\n  :name: linkname".splitlines();lnj=lns[j]
            #j,lns=1,".. figure::\n  :name:".splitlines();lnj=lns[j]
            #j,lns=1,".. math::\n  :name: linkname".splitlines();lnj=lns[j]
            itm = rexname.match(lnj)
            if itm:
                lnkname, = itm.groups()
                lnj1 = lns[j-1].split('::')[0].replace('list-table','table').replace('code-block','code').strip()
                if counters and not lnkname and lnj1 in counters:
                    lnkname = name_from_directive(lnj1.strip('. '),counters[lnj1])
                    counters[lnj1]+=1
                    break
                elif lnkname:
                    lnkname = lnkname.strip()
                    break
            #lnj=":linkname: words"
            itm = rexitem.match(lnj)
            if itm:
                lnkname, = itm.groups()
                break
            itm = rexoneword.match(lnj)
            if itm:
                lnkname, = itm.groups()
                break
            lnkname = self.target
        self.lnkname = lnkname

    def create_link(self,linktype,reststem):
        if linktype == 'latex':
            linktype = 'pdf'
        if linktype=='sphinx':
            tgte = ".. |{0}| replace:: :ref:`{1}<{0}>`\n".format(self.target,self.lnkname)
        elif linktype=='odt':
            #https://github.com/jgm/pandoc/issues/3524
            tgte = ".. |{0}| replace:: `{1} <../{2}#{0}>`__\n".format(self.target,self.lnkname,reststem+'.'+linktype)
        else:
            tgte = ".. |{0}| replace:: `{1} <{2}#{0}>`__\n".format(self.target,self.lnkname,reststem+'.'+linktype)
        return tgte

    def create_tag(self):
        return r'{0}	{1}	/\.\. _`\?{0}`\?:/;"		line:{2}'.format(
            self.target,self.tagentry[0],self.tagentry[1])

class RstFile:
    '''
    Represents an .rst or .rest file.

    :reststem: ``.rest`` file this ``.rst`` belongs to (without extension)
    :doc:  doc of this doc included by that rest file
    :nlns: number of lines of the doc
    :lnks: list of (line index, target name (``|target|``)) tuples
    :tgts: list of Tgt objects yielded by |make_tgts|.

    '''

    def __init__(self
          ,reststem # .rest file this .rst belongs to (without extension)
          ,doc
          ,tgts
          ,lnks
          ,nlns
          ):
        self.reststem = reststem
        self.doc = doc
        self.tgts = tgts
        self.lnks = lnks
        self.nlns = nlns

    def __str__(self):
        return str((self.doc,self.restname))

    def add_links_and_tags(self, add_tgt, add_linksto):
        iterlnks = iter(self.lnks)
        prevtgt = None
        #unknowntgts = []
        tgt = None
        for tgt in self.tgts:
            if tgt.lnidx is not None:
                add_linksto(prevtgt,tgt.lnidx,iterlnks)#,unknowntgts)
                add_tgt(tgt,self.reststem)
                prevtgt = tgt
        if tgt:
            add_linksto(prevtgt,tgt.lnidx,iterlnks)#,unknowntgts)
        if verbose:
            if '/'+self.reststem+'.' in self.doc:
                print(_indent+self.doc)
            else:
                print(2*_indent+self.doc)

    @staticmethod
    def make_lnks(
        lns  #lines of the document
        ):
        '''Yields (index, link name) for ``lns``'''

        for i,ln in enumerate(lns):
            mo = rexlnks.findall(ln)
            for g in mo:
                yield i,g

    @staticmethod
    def make_tgts(
        lns  #lines of the document
        ,doc #the rst document
        ,counters=None # if None, the starts with {".. figure":1,".. math":1,".. table":1,".. code":1}
        ,fn_i_ln=None #(fn,i,ln) of the .stpl with all stpl includes sequenced
        ):
        '''
        Yields ``((line index, tag address), target, link name)`` of ``lns`` of a restructureText file.
        For a .stpl file the linkname comes from the generated .rest file.

        '''

        if counters == None:
            counters = make_counters()
        itgts = list(rindices(rextgt,lns))
        if fn_i_ln:
            lns1 = [x[2] for x in fn_i_ln]
            itgts1 = list(rindices(rextgt,lns1))
        else:
            lns1 = lns
            itgts1 = itgts
        if len(itgts)<len(itgts1):
            paired_itgts_itgts1 = pair(itgts,itgts1,lambda x,y:lns[x]==lns1[y])
        elif len(itgts)>len(itgts1):
            paired_itgts_itgts1 = ((i,j) for (j,i) in pair(itgts1,itgts,lambda x,y:lns1[x]==lns[y]))
        else:
            paired_itgts_itgts1 = zip(itgts,itgts1)
        lenlns = len(lns)
        lenlns1 = len(lns1)
        for i,i1 in paired_itgts_itgts1:
            ii,iis,iilen = (i,lns,lenlns) if i else (i1,lns1,lenlns1)
            cur = iis[ii]
            tgt = Tgt(ii,rextgt.search(cur).group(1))
            if tgt.is_inside_literal(iis):
                continue
            tgt.find_lnkname(iis,counters)
            tgt.lnkidx = i
            if i1:
                if fn_i_ln:
                    tgt.tagentry = fn_i_ln[i1][:2]
                else:
                    tgt.tagentry = (doc,ii)
            else:
                tgt.tagentry = (doc.replace(_stpl,''),ii)
            yield tgt

    @staticmethod
    def substs(
        lns  #lines of the rst document
        ):
        '''
        Return all substitution targets in the rst lns

        >>> list(substs("""
        ...   .. |sub| image:: xx
        ...   .. |s-b| date::
        ...   """.splitlines()))
        ['sub', 's-b']

        '''

        for i,ln in enumerate(lns):
            asub = rexsubtgt.search(ln)
            if asub:
                yield asub.group(1)


class Fldr(OrderedDict):
    '''
    Represents a directory.

    It is an ordered list of {rst file: RstFile object}.

    :folder: is the directory path
    :allfiles: set of all files in the directory
    :alltgts: set of all targets in the directory
    :allsubsts: set of all substitutions in the directory

    '''

    def __init__(self
        ,folder #as returned by ``os.walk()``
        ):

        self.folder = folder
        self.allfiles = set()
        self.alltgts = set()
        self.allsubsts = set()
        self.counters = defaultdict(dict)

    def __str__(self):
        return str(list(sorted(self.keys())))

    def scan(self
        ,fs #all files in the directory as returned by ``os.walk()``
        ):
        '''
        Scans the directory for rest files.
        All files (.rest and included .rst) are added.

        Sphinx index.rest is processed last.

        ``allfiles``, ``alltgts`` and ``allsubsts`` get filled.

        '''

        sofar=set([])
        sphinx_index = None
        for afs in reversed(sorted(fs)):#reversed puts the rest.stpl before the .rest
            fullpth=normjoin(self.folder,afs).replace("\\","/")
            if is_rest(afs):
                if afs.startswith('index.rest'):
                    sphinx_index = (afs,fullpth)
                    continue
                fullpth_nostpl = fullpth.replace(_stpl,'')
                if fullpth_nostpl in sofar:
                    continue
                sofar.add(fullpth_nostpl)
                self.add_rest(afs,fullpth)
        if sphinx_index:
            self.add_rest(*sphinx_index)

    def add_rest(self
        ,restfile
        ,fullpth
        ,exclude_paths_substrings = ['_links_']
        ):

        pths = []
        has_traceability = False
        for restinc in rstincluded(restfile,(self.folder,)):
            if _traceability_file+_rst in restinc:
                if pyfca and _traceability_instance is None:#THERE CAN BE ONLY ONE
                    Traceability(stem(restfile)) 
                    has_traceability = True
                    continue
            pth=normjoin(self.folder,restinc).replace("\\","/")
            if any(x in pth for x in exclude_paths_substrings):
                continue
            pths.append(pth)

        reststem = pths[0]
        reststem = stem(stem(reststem))
        if reststem not in self.counters:
            self.counters[reststem] = make_counters()
        counters = self.counters[reststem]
        if has_traceability:
              _traceability_instance.counters = counters

        self.allfiles |= set(pths)

        for doc in pths:
            rstpath = doc.replace(_stpl,'')
            if doc.endswith(_stpl) and exists(rstpath):
                lns = _read_lines(doc.replace(_stpl,''))
                fn_i_ln = _flatten_stpl_includes(doc)
                tgts = list(RstFile.make_tgts(lns,doc,counters,fn_i_ln))
            elif not doc.endswith(_tpl) and not doc.endswith(_txt) and exists(doc):
                lns = _read_lines(doc)
                tgts = list(RstFile.make_tgts(lns,doc,counters))
            else:
                continue
            lnks = list(RstFile.make_lnks(lns))
            rstfile = RstFile(base(reststem),doc,tgts,lnks,len(lns))
            self[doc]= rstfile
            self.alltgts |= set([t.target for t in rstfile.tgts])
            self.allsubsts |= set(RstFile.substs(lns)) 

    def create_links_and_tags(self,scanroot):
        '''
        Creates links_xxx.rst and .tags files for a directory at scanroot/directory

        The target IDs are grouped. To every group a color is associated. See ``conf.py``.
        This is used to color an FCA lattice diagram in "_traceability_file.rst".
        The diagram nodes are clickable in HTML.

        '''

        tagentries = []
        upcnt = 0
        if self.folder.strip():
           relfolder = relpath(self.folder,start=scanroot)
           upcnt = len(relfolder.split('/'))
        links_types = "sphinx latex html pdf docx odt".split()
        linkfiles = [(linktype,[]) for linktype in links_types]
        def add_tgt(tgt,reststem):
            for linktype,linklines in linkfiles:
                linklines.append(tgt.create_link(linktype,reststem))
            if isabs(tgt.tagentry[0]):
                tgt.tagentry = (relpath(tgt.tagentry[0],start=scanroot),tgt.tagentry[1])
            tgt.tagentry = ("../"*upcnt+tgt.tagentry[0],tgt.tagentry[1])
            tagentries.append(tgt.create_tag())
        def add_links_comments(comment):
            for _,linklines in linkfiles:
                linklines.append(comment)
        def add_linksto(prevtgt,lnidx,iterlnks,ojlnk=[0,None]):
            #all the links from the block following prevtgt up to this tgt
            linksto = []
            def chkappend(x):
                if x!=prevtgt.target: 
                    linksto.append(x)
            if ojlnk[1] and ojlnk[0] < lnidx:#for the first link in the new prevtgt
                if ojlnk[1] in self.alltgts:
                    chkappend(ojlnk[1])
                elif ojlnk[1] not in self.allsubsts:
                    linksto.append('-'+ojlnk[1])
                    #unknowntgts.append(ojlnk[1])
                ojlnk[1] = None
            if ojlnk[1] is None:#the remaining links in prevtgt up to this tgt
                for j, lnk in iterlnks:
                    if j > lnidx:#links upcnt to this target
                        ojlnk[:] = j,lnk
                        break
                    else:
                        if lnk in self.alltgts:
                            chkappend(lnk)
                        elif lnk not in self.allsubsts:
                            linksto.append('-'+lnk)
                            #unknowntgts.append(lnk)
            if _traceability_instance:
                if prevtgt and linksto:
                    _traceability_instance.append(set([x for x in linksto if not x.startswith('-') and not x.startswith('_')]+[prevtgt.target]))
            if linksto:
                linksto = '.. .. ' + ','.join(linksto) + '\n\n'
                add_links_comments(linksto)
        for rstfile in self.values():
            add_links_comments('\n.. .. {0}\n\n'.format(rstfile.doc))
            rstfile.add_links_and_tags(add_tgt,add_linksto)
        if _traceability_instance:
            tlns = _traceability_instance.create_traceability_file(self.folder)
            trcrst = normjoin(self.folder,_traceability_file+_rst)
            if tlns:
                for tgt in RstFile.make_tgts(tlns,trcrst,_traceability_instance.counters) :
                    add_tgt(tgt,_traceability_instance.tracehtmltarget)
        for linktype,linklines in linkfiles:
            with opnwrite(normjoin(self.folder,'_links_%s.rst'%linktype)) as f:
                f.write('\n'.join(linklines));
        ctags_python = ""
        try:
            ctags_python = cmd(
                ['ctags','-R','--sort=0','--fields=+n','--languages=python','--python-kinds=-i','-f','-','*']
                ,cwd=self.folder
                )
        finally:
            with opnwrite(normjoin(self.folder,'.tags')) as f:
                f.write(ctags_python)
                f.write('\n'.join(tagentries))

class Fldrs(OrderedDict):
    '''
    Represents a directory hierarchy below ``scanroot``.
    The paths are relative to ``scanroot``.

    It is a dict ordere by insertion of {directory: Fldr objects}

    '''

    def __init__(self
        ,scanroot = '.' #root path to start scanning for independent doc directories
        ):
        self.scanroot = scanroot

    def __str__(self):
        return super().__str__()

    def scan(self):
        for p,ds,fs in os.walk(self.scanroot):
            if not p.endswith(_images):
                directory = normjoin(p)
                fldr = Fldr(directory)
                fldr.scan(fs)
                if len(fldr):
                    self[directory] = fldr

def links_and_tags(
    adir #directory name
    ):
    '''
    Creates _links_xxx.rst`` files and a ``.tags``.

    >>> cd(dir(__file__))
    >>> rmrf('../doc/_links_sphinx.rst')
    >>> '_links_sphinx.rst' in ls('../doc')
    False

    >>> links_and_tags('../doc')
    >>> '_links_sphinx.rst' in ls('../doc')
    True

    '''
    
    fldrs = Fldrs(adir)
    fldrs.scan()
    for fldr in fldrs.values():
        fldr.create_links_and_tags(fldrs.scanroot)

#==============> for building with WAF

try:
    from waflib import TaskGen, Task

    @lru_cache()
    def _ant_glob_stpl(bldpath,*stardotext):
        res = []
        already = set([])
        for an_ext in stardotext:
          stplsfirst = bldpath.ant_glob(an_ext+_stpl)
          for anode in stplsfirst:
              already.add(stem(anode.name))
              res.append(anode)
          nonstpls = bldpath.ant_glob(an_ext)
          for anode in nonstpls:
              if anode.name not in already:
                  res.append(anode)
        return res
    gensrc={}
    @TaskGen.feature('gen_files')
    @TaskGen.before('process_rule')
    def gen_files(self):
        global gensrc
        gensrc={}
        for f,t,fun,kw in parsegenfile(self.path.make_node('gen').abspath()):
            gensrc[t]=f
            frm = self.path.find_resource(f)
            twd = self.path.make_node(t)
            self.create_task('GENTSK',frm,twd,fun=fun,kw=kw)
    class GENTSK(Task.Task):
        def run(self):
            frm = self.inputs[0]
            twd = self.outputs[0]
            twd.parent.mkdir()
            gen(frm.abspath(),twd.abspath(),fun=self.fun,**self.kw)
    def get_docs(bld):
        docs = [x.lower() for x in bld.options.docs]
        if not docs:
            docs = [x.lower() for x in bld.env.docs]
        return docs
    @lru_cache()
    def get_files_in_doc(path,node):
        srcpath = node.parent.get_src()
        orgd = node.parent.abspath()
        d = srcpath.abspath()
        n = node.name
        nod = None
        if node.is_bld() and not node.name.endswith(_stpl) and not x.endswith(_tpl):
            nod = srcpath.find_node(node.name+_stpl)
        if not nod:
            nod = node
        ch = rstincluded(n,(d,orgd),True,True)
        deps = []
        nodeitself=True
        for x in ch:
            if nodeitself:
                nodeitself = False
                continue
            isrst = is_rst(x)
            if isrst and x.startswith('_links_'):#else cyclic dependency for _links_xxx.rst
                    continue
            nd = srcpath.find_node(x)
            if not nd:
                if isrst and not x.endswith(_stpl) and not x.endswith(_tpl):
                    nd = srcpath.find_node(x+_stpl)
            deps.append(nd)
        depsgensrc = [path.find_node(gensrc[x]) for x in deps if x and x in gensrc] 
        rs = [x for x in deps if x]+depsgensrc
        return (list(sorted(set(rs),key=lambda a:a.name)),[])
    @TaskGen.feature('gen_links')
    @TaskGen.after('gen_files')
    def gen_links(self):
        docs=get_docs(self.bld)
        if docs:
            for so in self.path.ant_glob('*.stpl'):
                tsk = Namespace()
                tsk.inputs=(so,)
                tsk.env = self.env
                tsk.generator = self
                render_stpl(tsk,self.bld)
            links_and_tags(self.path.abspath())
    def render_stpl(tsk,bld):
        bldpath = bld.path.get_bld()
        ps = tsk.inputs[0].abspath()
        try:
            pt = tsk.outputs[0].abspath()
        except:
            if ps.endswith(_stpl):
                pt = stem(ps)
            else:
                raise RstDocError('No target for %s'%ps)
        env = dict(tsk.env)
        env.update(tsk.generator.__dict__)
        dostpl(ps,pt,**env)
    class STPL(Task.Task):
        always_run = True
        def run(self):
            render_stpl(self,self.generator.bld)
    @TaskGen.extension(_stpl)
    def stpl_taskgen(self,node):#expand into same directory
        nn = node.parent.make_node(stem(node.name))
        self.create_task('STPL',node,nn)
        try:
            self.get_hook(nn)(self, nn)
        except:
            pass
    def gen_ext_tsk(self,node,ext):#into _images or ../_images in source path
        srcfldr = node.parent.get_src()
        _imgpath,_ = here_or_updir(srcfldr.abspath(),_images)
        imgpath = relpath(_imgpath,start=srcfldr.abspath())
        outnode = srcfldr.make_node(normjoin(imgpath,stem(node.name)+'.png'))
        self.create_task(ext[1:].upper(),node,outnode)
    @TaskGen.extension(_tikz)
    def tikz_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,_tikz)
    class TIKZ(Task.Task):
        def run(self):
            tikzpng(self.inputs[0].abspath(),self.outputs[0].abspath())
    @TaskGen.extension('.svg')
    def svg_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,'.svg')
    class SVG(Task.Task):
        def run(self):
            svgpng(self.inputs[0].abspath(),self.outputs[0].abspath())
    @TaskGen.extension('.dot')
    def dot_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,'.dot')
    class DOT(Task.Task):
        run_str = "${dot} -Tpng ${SRC} -o${TGT}"
    @TaskGen.extension('.uml')
    def uml_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,'.uml')
    class UML(Task.Task):
        run_str = "${plantuml} ${SRC} -o${TGT[0].parent.abspath()}"
    @TaskGen.extension('.eps')
    def eps_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,'.eps')
    class EPS(Task.Task):
        run_str = "${inkscape} -z --export-dpi=%s --export-area-drawing --export-background-opacity=0 ${SRC} --export-png=${TGT}"%DPI
    @TaskGen.extension('.pyg')
    def pyg_to_png_taskgen(self,node):
        gen_ext_tsk(self,node,'.pyg')
    class PYG(Task.Task):
        def run(self):
            pygpng(self.inputs[0].abspath(),self.outputs[0].abspath())
    @TaskGen.extension(_rest)
    def docs_taskgen(self,node):
        docs=get_docs(self.bld)
        d = get_files_in_doc(self.path,node)
        rstscan = lambda: d
        if node.name != "index.rest":
            for doctgt in docs:
                if doctgt.startswith('sphinx_'):
                    continue
                try:
                    #doctgt = 'html'
                    _,doctype = doctgt.split('_')
                except:
                    doctype = doctgt
                out_node = node.parent.find_or_declare("{0}/{1}.{2}".format(doctgt,stem(node.name),doctype))
                self.create_task('NonSphinxTask', [node], out_node, scan=rstscan, doctgt=doctgt)
        else:
            for doctgt in docs:
                if not doctgt.startswith('sphinx_'):
                    continue
                doctype = doctgt.split('_')[1]
                out_node = node.parent.find_or_declare("{0}/{1}.{2}".format(doctgt,stem(node.name),doctype.replace('latex','tex')))
                self.create_task('SphinxTask',[node],out_node,scan=rstscan,doctype=doctype,config_path=self.bld.path.get_src().abspath())
    class NonSphinxTask(Task.Task):
        def run(self):
            dorst(
                self.inputs[0].abspath()
                ,self.outputs[0].abspath()
                ,self.doctgt
                )
    class SphinxTask(Task.Task):
        always_run = True
        def run(self):
            config = conf_py(self.config_path)
            config['html_extra_path'] = [normjoin(self.config_path,x) for x in config['html_extra_path']]
            rst_sphinx(self.inputs[0].abspath(),self.outputs[0].abspath(),self.doctype,**config)
    def options(opt):
        def docscb(option, opt, value, parser):
            setattr(parser.values, option.dest, value.split(','))
        opt.add_option("--docs", type='string', action="callback", callback= docscb, dest='docs', default=[],
            help="Comma-separated list of html,docx,pdf,sphinx_html (default) or any other of http://www.sphinx-doc.org/en/master/usage/builders") 

    def configure(cfg):
        cfg.env['docs'] = cfg.options.docs
        for x in 'plantuml dot inkscape'.split():
            try:
                cfg.env[x] = cfg.find_program(x)
            except cfg.errors.ConfigurationError:
                cfg.to_log(x+' was not found (ignoring)')

    def build(bld):
        bld.src2bld = lambda f: bld(features='subst',source=f,target=f,is_copy=True)
        def gen_files():
            bld(name="process gen file",features="gen_files")
        bld.gen_files = gen_files
        def gen_links():
            bld(name="create links and .tags",features="gen_links")
        bld.gen_links = gen_links
        bld.stpl = lambda tsk: render_stpl(tsk,bld) #use like bld(rule=bld.stpl,source='x.h.stpl') to compile stpl only, else do without rule
        def build_docs():
            docs=get_docs(bld)
            if docs:
                bld.gen_files()
                bld.gen_links()
                for anext in '*.tikz *.svg *.dot *.uml *.pyg *.eps'.split():
                    for anextf in _ant_glob_stpl(bld.path,anext):
                        bld(name='build '+anext,source=anextf)
                bld.add_group()
                bld(name='build all rest',source=[x for x in _ant_glob_stpl(bld.path,'*.rest','*.rst')if not x.name.endswith(_rst)])
                bld.add_group()
        bld.build_docs = build_docs

except:
    pass

#==============< for building with WAF

#pandoc --print-default-data-file reference.docx > reference.docx
#pandoc --print-default-data-file reference.odt > reference.odt
#pandoc --print-default-template=latex
#then modified in format and not to use figure labels
#this is for mktree(): first line of file content must not be empty!
example_tree = r'''
       build/
       src
        ├ dcx.py << file:///__file__
        ├ reference.tex << file:///__tex_ref__
        ├ reference.docx << file:///__docx_ref__
        ├ reference.odt << file:///__odt_ref__
        ├ wafw.py << file:///__wafw__
        ├ waf
            #!/usr/bin/env sh
            shift
            ./wafw.py "$@"
        ├ waf.bat
            @setlocal
            @set PYEXE=python
            @where %PYEXE% 1>NUL 2>NUL
            @if %ERRORLEVEL% neq 0 set PYEXE=py
            @%PYEXE% -x "%~dp0wafw.py" %*
            @exit /b %ERRORLEVEL%
        ├ wscript
            from waflib import Logs
            Logs.colors_lst['BLUE']='\x1b[01;36m'
            
            top='.'
            out='../build'
            
            def options(opt):
              opt.load('dcx',tooldir='.')
            
            def configure(cfg):
              cfg.load('dcx',tooldir='.')
            
            def build(bld):
              #defines bld.gen_files(), bld.gen_links(), bld.build_docs()
              bld.load('dcx',tooldir='.')
              bld.recurse('doc')
        ├ docutils.conf
            [general]
            halt_level: severe
            report_level: error
        ├ conf.py
            project = 'sample'
            author = project+' Project Team'
            copyright = '2018, '+author
            version = '1.0'
            release = '1.0.0'
            html_theme = 'bootstrap'
            import sphinx_bootstrap_theme
            html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

            #these are enforced by rstdoc, but you need to keep them here if you call sphinx-build directly
            numfig = 0
            smartquotes = 0
            source_suffix = '.rest'
            templates_path = []
            language = None
            highlight_language = "none"
            default_role = 'math'
            latex_engine = 'xelatex'
            pygments_style = 'sphinx'
            exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
            master_doc = 'index'
            
            #You can postprocess pngs. Here an example. default: png_post_processor = None
            def png_post_processor(filename):
                from PIL import Image, ImageChops
                def trim(im):
                    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
                    diff = ImageChops.difference(im, bg)
                    diff = ImageChops.add(diff, diff, 2.0, -100)
                    bbox = diff.getbbox()
                    if bbox:
                        return im.crop(bbox)
                im = Image.open(filename)
                im = trim(im)
                im.save(filename)
                return filename
            
            #remove the following, if you don't change them, because they are default anyway
            latex_elements = {'preamble':r"""
            \usepackage{pgfplots}
            \usepackage{unicode-math}
            \usepackage{tikz}
            \usepackage{caption}
            \captionsetup[figure]{labelformat=empty}
            \usetikzlibrary{arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks,intersections}
            """
            }
            
            #new in rstdcx/dcx/py
            tex_wrap = r"""
            \documentclass[12pt,tikz]{standalone}
            \usepackage{amsmath}
            """+latex_elements['preamble']+r"""
            \pagestyle{empty}
            \begin{document}
            %s
            \end{document}
            """
            dpi = 600
            target_id_group = lambda targetid: targetid[0]
            target_id_color={"ra":("r","lightblue"), "sr":("s","red"), "dd":("d","yellow"), "tp":("t","green")}
            html_extra_path=["doc/_images/_traceability_file.svg"] #IF YOU DID ``.. include:: _traceability_file.rst``
            pandoc_doc_optref={'latex': '--template ../reference.tex',
                             'html': {},#each can also be dict of file:template
                             'pdf': '--template ../reference.tex',
                             'docx': '--reference-doc ../reference.docx',
                             'odt': '--reference-doc ../reference.odt'
                             }
            _pandoc_latex_pdf = ['--listings','--number-sections','--pdf-engine','xelatex','-V','titlepage','-V','papersize=a4','-V','toc','-V','toc-depth=3','-V','geometry:margin=2.5cm']
            pandoc_opts = {'pdf':_pandoc_latex_pdf,'latex':_pandoc_latex_pdf,'docx':[],'odt':[],'html':['--mathml','--highlight-style','pygments']}
            rst_opts = { #http://docutils.sourceforge.net/docs/user/config.html
                        'strip_comments':True
                        ,'report_level':3
                        ,'raw_enabled':True
                        }
            name_from_directive = lambda directive,count: directive[0].upper()+directive[1:]+' '+str(count)
        ├ Makefile
            SPHINXOPTS  = -c .
            SPHINXBLD   = sphinx-build
            SPHINXPROJ  = sample
            SRCDIR      = ./doc
            SRCBACK     = ../
            BLDDIR      = ../build/doc
            STPLS       = $(wildcard $(SRCDIR)/*.stpl)
            STPLTGTS    = $(STPLS:%.stpl=%)
            SRCS        = $(filter-out $(SRCDIR)/index.rest,$(wildcard $(SRCDIR)/*.rest))
            SRCSTPL     = $(wildcard $(SRCDIR)/*.rest.stpl)
            IMGS        = \
            	$(wildcard $(SRCDIR)/*.pyg)\
            	$(wildcard $(SRCDIR)/*.eps)\
            	$(wildcard $(SRCDIR)/*.tikz)\
            	$(wildcard $(SRCDIR)/*.svg)\
            	$(wildcard $(SRCDIR)/*.uml)\
            	$(wildcard $(SRCDIR)/*.dot)\
            	$(wildcard $(SRCDIR)/*.eps.stpl)\
            	$(wildcard $(SRCDIR)/*.tikz.stpl)\
            	$(wildcard $(SRCDIR)/*.svg.stpl)\
            	$(wildcard $(SRCDIR)/*.uml.stpl)\
            	$(wildcard $(SRCDIR)/*.dot.stpl)
            PNGS=$(subst $(SRCDIR),$(SRCDIR)/_images,\
            	$(patsubst %.eps,%.png,\
            	$(patsubst %.pyg,%.png,\
            	$(patsubst %.tikz,%.png,\
            	$(patsubst %.svg,%.png,\
            	$(patsubst %.uml,%.png,\
            	$(patsubst %.dot,%.png,\
            	$(patsubst %.eps.stpl,%.png,\
            	$(patsubst %.dot.stpl,%.png,\
            	$(patsubst %.tikz.stpl,%.png,\
            	$(patsubst %.svg.stpl,%.png,\
            	$(patsubst %.uml.stpl,%.png,$(IMGS)))))))))))))
            DOCXS = $(subst $(SRCDIR),$(BLDDIR)/docx,$(SRCS:%.rest=%.docx))\
            	$(subst $(SRCDIR),$(BLDDIR)/docx,$(SRCSTPL:%.rest.stpl=%.docx))
            PDFS  = $(subst $(SRCDIR),$(BLDDIR)/pdf,$(SRCS:%.rest=%.pdf))\
            	$(subst $(SRCDIR),$(BLDDIR)/pdf,$(SRCSTPL:%.rest.stpl=%.pdf))
            .PHONY: docx help Makefile docxdir pdfdir stpl index imgs
            stpl: $(STPLTGTS)
            %:%.stpl
            	@cd $(SRCDIR) && stpl "$(<F)" "$(@F)"
            imgs: $(PNGS)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.pyg
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.eps
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.tikz
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.svg
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.uml
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            $(SRCDIR)/_images/%.png:$(SRCDIR)/%.dot
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py $(<F)
            docxdir: ${BLDDIR}/docx
            pdfdir: ${BLDDIR}/pdf
            MKDIR_P = mkdir -p
            ${BLDDIR}/docx:
            	@${MKDIR_P} ${BLDDIR}/docx
            ${BLDDIR}/pdf:
            	@${MKDIR_P} ${BLDDIR}/pdf
            index:
            	@python ./dcx.py
            help:
            	@$(SPHINXBLD) -M help "$(SRCDIR)" "$(BLDDIR)" $(SPHINXOPTS) $(O)
            	@echo "  docx        to docx"
            	@echo "  pdf         to pdf"
            #http://www.sphinx-doc.org/en/stable/usage/builders/
            html dirhtml singlehtml htmlhelp qthelp applehelp devhelp epub latex text man texinfo pickle json xml pseudoxml: Makefile index stpl imgs
            	@$(SPHINXBLD) -M $@ "$(SRCDIR)" "$(BLDDIR)" $(SPHINXOPTS) $(O)
            docx:  docxdir index stpl imgs $(DOCXS)
            $(BLDDIR)/docx/%.docx:$(SRCDIR)/%.rest
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py "$(<F)" "$(SRCBACK)/$@"
            pdf: pdfdir index stpl imgs $(PDFS)
            $(BLDDIR)/pdf/%.pdf:$(SRCDIR)/%.rest
            	@cd $(SRCDIR) && python $(SRCBACK)/dcx.py "$(<F)" "$(SRCBACK)/$@"
        ├ code
            └ some.h
                /*
                #def gen_tst(lns,**kw):
                #  return [l.split('@')[1] for l in rlines(r'^\s*@',lns)]
                #def gen_tst
                #def gen_tstdoc(lns,**kw):
                #  return ['#) '+l.split('**')[1] for l in rlines(r'^/\*\*',lns)]
                #def gen_tstdoc
                
                @//generated from some.h
                @#include <assert.h>
                @#include "some.h"
                @int main()
                @{
                */
                
                /**Test add1()
                @assert(add1(1)==2);
                */
                int add1(int a)
                {
                  return a+1;
                }
                
                /**Test add2()
                @assert(add2(1)==3);
                */
                int add2(int a)
                {
                  return a+2;
                }
                
                /*
                @}
                */
        └ doc
           ├ _images/
           ├ wscript_build
               bld.build_docs()
           ├ index.rest
               ============
               Project Name
               ============
               
               .. toctree::
                  ra.rest
                  sr.rest
                  dd.rest
                  tp.rest
               
               One can also have a
               
               - issues.rest for issues
               
               - pp.rest for the project plan
                 (with backlog, epics, stories, tasks)
               
               .. include:: _traceability_file.rst
               
               .. include:: _links_sphinx.rst
               
           ├ ra.rest
               Risk Analysis
               =============
               
               .. _`rz7`:
               
               :rz7: risk calculations
               
               Risk calculations are done with python in the ``.stpl`` file.
               
               .. include:: _links_sphinx.rst
               
           ├ sr.rest
               Software/System Requirements
               ============================
               
               .. _`s97`:
               
               Requirements are testable (see |t9a|). 
               
               .. _`su7`:
               
               ``dcx.py`` produces its own labeling consistent across DOCX, PDF, HTML.
               
               .. _`sy7`:
               
               A Requirement Group
               -------------------
               
               .. _`s3a`:
               
               :s3a: brief description
               
               Don't count the ID, since the order will change.
               The IDs have the first letter of the file and 2 or more random letters of ``[0-9a-z]``.
               Use an editor macro to generate IDs.

               A link: |s3a|
               
               If one prefers ordered IDs, one can use templates::
               
                 %id = lambda x=[0]: x.append(x[-1]+1) or "s{:0>2}".format(x[-1])
               
                 .. _`soi`:
               
                 :{{id()}}: auto numbered.
               
               The disadvantage is that the id will differ between rst and final doc.
               When this is needed in an included file use template include: ``%include('x.rst.tpl`)``
               See the the ``test/stpl`` directory.
               
               Every ``.rest`` has this line at the end::
               
                  .. include:: _links_sphinx.rst
               
               .. include:: _links_sphinx.rst
               
           ├ dd.rest
               Design Description
               ==================
               
               .. _`d97`:
               
               :d97: Independent DD IDs
               
                 The relation with RS IDs is m-n. Links like |s3a| can be scattered over more DD entries.  
               
               .. _`dx3`:
               
               .. figure:: _images/egtikz1.png
                  :name:
                  :width: 30%
               
                  |dx3|: Create from egtikz1.tikz
               
               .. _`dz3`:
               
               .. figure:: _images/egtikz.png
                  :name:
                  :width: 50%
               
                  |dz3|: Create from egtikz.tikz
               
                  The usage of ``:name:`` produces: ``WARNING: Duplicate explicit target name: ""``. Ignore.

               Reference via |dz3|.
               
               ``.tikz``, ``.svg``, ``.dot``,  ``.uml``, ``.eps`` or ``.stpl`` thereof and ``.pyg``, are converted to ``.png``.
               
               .. _`dz4`:
               
               .. figure:: _images/egsvg.png
                  :name:
               
                  |dz4|: Created from egsvg.svg.stpl
               
               .. _`dz5`:
               
               .. figure:: _images/egdot.png
                  :name:
               
                  |dz5|: Created from egdot.dot.stpl
               
               .. _`dz6`:
               
               .. figure:: _images/eguml.png
                  :name:
               
                  |dz6|: Created from eguml.uml
               
               .. _`dz7`:
               
               .. figure:: _images/egplt.png
                  :name:
                  :width: 30%
               
                  |dz7|: Created from egplt.pyg
               
               .. _`dz8`:
               
               .. figure:: _images/egpyx.png
                  :name:
               
                  |dz8|: Created from egpyx.pyg
               
               .. _`dr8`:
               
               .. figure:: _images/egcairo.png
                  :name:
               
                  |dr8|: Created from egcairo.pyg
               
               .. _`ds8`:
               
               .. figure:: _images/egpygal.png
                  :name:
                  :width: 30%
               
                  |ds8|: Created from egpygal.pyg
               
               .. _`dsx`:
               
               .. figure:: _images/egother.png
                  :name:
               
                  |dsx|: Created from egother.pyg
               
               .. _`du8`:
               
               .. figure:: _images/egeps1.png
                  :name:
               
                  |du8|: Created from egeps1.eps
               
               .. _`d98`:
               
               .. figure:: _images/egeps.png
                  :name:
               
                  |d98|: Created from egeps.eps
               
               .. _`dua`:
               
               |dua|: Table legend
               
               .. table::
                  :name:
               
                  +--------+--------+
                  | A      | B      |
                  +========+========+
                  | |eps1| | |eps|  |
                  +--------+--------+
               
               .. _`dta`:
               
               |dta|: Table legend
               
               .. list-table::
                  :name:
                  :widths: 20 80
                  :header-rows: 1
               
                  * - Bit
                    - Function
               
                  * - 0
                    - afun
               
               Reference |dta| does not show ``dta``.
               
               .. _`dyi`:
               
               |dyi|: Listing showing struct.
               
               .. code-block:: cpp
                  :name:
               
                  struct astruct{
                     int afield; //afield description 
                  }
               
               .. _`d9x`:
               
               .. math:: 
                  :name:
               
                  V = \frac{K}{r^2}
               
               ``:math:`` is the default inline role: `mc^2`
               
               .. _`d99`:
               
               :OtherName: Keep names the same all over.
               
               Here instead of ``d99:`` we use ``:OtherName:``, but now we have two synonyms for the same item.
               This is no good. If possible, keep ``d99`` in the source and in the final docs.
               
               The item target must be in the same file as the item content. The following would not work::
               
                 .. _`dh5`:
                 
                 .. include:: somefile.rst   
               
               .. |eps1| image:: _images/egeps1.png
               .. |eps| image:: _images/egeps.png
               
               .. include:: _links_sphinx.rst
              
           ├ tp.rest
               Test Plan
               =========
               
               .. _`t9a`:
               
               Requirement Tests
               -----------------
               
               No duplication. Only reference the requirements to be tested.
               
               - |s97|
               - |su7|
               - |s3a|
               - |rz7|
               
               Or better: reference the according SR chapter, else changes there would need an update here.
               
               - Test |sy7|
               
               Unit Tests
               ----------
               
               Use ``.rst`` for included files and start the file with ``_`` if generated.
               
               - |d97|
               - |dx3|
               - |dz4|
               - |dz5|
               - |dz6|
               - |dz7|
               - |dz8|
               - |dsx|
               - |du8|
               - |d98|
               - |dua|
               - |dta|
               - |dyi|
               - |d9x|
               - |d99|
               
               .. include:: _sometst.rst
               
               .. include:: _links_sphinx.rst
               
           ├ egtikz.tikz
               [thick,red]
               \draw (0,0) grid (3,3);
               \foreach \c in {(0,0), (1,0), (2,0), (2,1), (1,2)}
                   \fill \c + (0.5,0.5) circle (0.42);
           ├ egtikz1.tikz
               \begin{scope}[blend group = soft light]
               \fill[red!30!white]   ( 90:1.2) circle (2);
               \fill[green!30!white] (210:1.2) circle (2);
               \fill[blue!30!white]  (330:1.2) circle (2);
               \end{scope}
               \node at ( 90:2)    {Typography};
               \node at ( 210:2)   {Design};
               \node at ( 330:2)   {Coding};
               \node [font=\Large] {\LaTeX};
           ├ egsvg.svg.stpl
               <?xml version="1.0" encoding="utf-8"?>
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" version="1.1" width="110pt" height="60pt" stroke-width="0.566929" stroke-miterlimit="10.000000">
               %for i in range(10):
                 <path fill="none" stroke="#f00" stroke-width="1" d="M10,55 C15,5 100,5 100,{{i*5}}" />
               %end
               %for i in range(10):
                 <path fill="none" stroke="#f40" stroke-width="1" d="M10,{{i*5}} C15,5 100,5 100,55" />
               %end
               <text x="50" y="50" fill="red">Hi!</text>
               </svg>
           ├ egdot.dot.stpl
               digraph {
               %for i in range(3):    
                   "From {{i}}" -> "To {{i}}";
               %end
                   }
           ├ eguml.uml
               @startuml
               'style options 
               skinparam monochrome true
               skinparam circledCharacterRadius 0
               skinparam circledCharacterFontSize 0
               skinparam classAttributeIconSize 0
               hide empty members
               Class01 <|-- Class02
               Class03 *-- Class04
               Class05 o-- Class06
               Class07 .. Class08
               Class09 -- Class10
               @enduml
           ├ egplt.pyg
               #vim: syntax=python
               import matplotlib.pyplot as plt
               import numpy as np
               x = np.random.randn(1000)
               plt.hist( x, 20)
               plt.grid()
               plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
               plt.show()
           ├ egpyx.pyg
               import pyx
               c = pyx.canvas.canvas()
               c.stroke(pyx.path.circle(0,0,2),[pyx.style.linewidth.Thick,pyx.color.rgb.red])
               c.text(1, 1, 'Hi',[pyx.color.rgb.red])
           ├ egpygal.pyg
               import pygal
               diagram=pygal.Bar()(1, 3, 3, 7)(1, 6, 6, 4)
           ├ egother.pyg
               from PIL import Image, ImageDraw, ImageFont
               im = Image.new("RGBA",size=(50,50),color=(155,0,100))
               draw = ImageDraw.Draw(im)
               draw.rectangle(((0, 0), (40, 40)), fill="red")
               draw.text((20, 20), "123")
               save_to_png = lambda out_file: im.save(out_file, "PNG")
           ├ egeps.eps
               1 0 0 setrgbcolor
               newpath 6 2 36 54 rectstroke
               showpage
           ├ egeps1.eps
               0 0 1 setrgbcolor
               newpath 6 2 36 54 rectstroke
               showpage
           ├ egcairo.pyg
               import cairocffi as cairo
               surface = cairo.SVGSurface(None, 200, 200)
               context = cairo.Context(surface)
               x, y, x1, y1 = 0.1, 0.5, 0.4, 0.9
               x2, y2, x3, y3 = 0.6, 0.1, 0.9, 0.5
               context.set_source_rgba(1, 0.2, 0.2, 0.6)
               context.scale(200, 200)
               context.set_line_width(0.04)
               context.move_to(x, y)
               context.curve_to(x1, y1, x2, y2, x3, y3)
               context.stroke()
               context.set_line_width(0.02)
               context.move_to(x, y)
               context.line_to(x1, y1)
               context.move_to(x2, y2)
               context.line_to(x3, y3)
               context.stroke()
           ├ gen
               #from|to|gen_xxx|kwargs
               ../code/some.h | _sometst.rst                | tstdoc | {}
               ../code/some.h | ../../build/code/some_tst.c | tst    | {}'''

#replaces from '├ index.rest' to '├ egtikz.tikz'
example_stp_subtree = r'''
           ├ model.py
               """
               This contains definitions used in template files ending in ``.stpl``.
               """
               from pint import UnitRegistry
               u = UnitRegistry()
               u.define('percent = 0.01*count = %')
               def U(*k,sep=", "):
                   """
                   Returns string where pint quantities are formatted with units, if possible, else normally.
                   """
                   try:
                       return sep.join(["{:~P}"]*len(k)).format(*k)
                   except:
                       res = sep.join(["{}"]*len(k)).format(*k)
                       if res == 'None':
                           res = '-'
                       return res
               # Definitions
               max_charging_time = 3.5*u.hour #in |hw_charger|
           ├ utility.rst.tpl
               % import sys
               % import os
               % sys.path.append(os.path.dirname(__file__))
               % from model import *
               % cntr = lambda alist0,prefix='',width=2: alist0.append(alist0[-1]+1) or ("{}{:0>%s}"%width).format(prefix,alist0[-1])
               % II=lambda prefix,alist0,short:':{}: **{}**'.format(cntr(alist0,prefix),short)
               % #define in file e.g. ``SR=lambda short,alist0=[0]:II('SR',alist0,short)`` and use like ``{{SR('Item Title')}}``
               %def pagebreak():
               .. raw:: openxml
               
                   <w:p>
                     <w:r>
                       <w:br w:type="page"/>
                     </w:r>
                   </w:p> 
               
               .. raw:: html
               
                   <p style="page-break-before: always;">&nbsp;</p>
               
               .. raw:: latex
               
                   \pagebreak
               
               .. for docutils
               .. raw:: odt
               
                   <text:p text:style-name="PageBreak"/>
               
               .. for pandoc
               .. raw:: opendocument
               
                   <text:p text:style-name="PageBreak"/>
               
               %end
           ├ index.rest
               .. encoding: utf-8
               .. vim: syntax=rst
               
               ============
               Project Name
               ============
               
               .. toctree::
                  sy.rest
                  ra.rest
                  sr.rest
                  dd.rest
                  tp.rest
               
               One can also have a
               
               - issues.rest for issues
               
               - pp.rest for the project plan
                 (with backlog, epics, stories, tasks)
               
               .. include:: _traceability_file.rst
               
               .. include:: _links_sphinx.rst
               
           ├ sy.rest.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               % globals().update(include('utility.rst.tpl'))
               % SY=lambda short,alist0=[0]:II('SY',alist0,short)
               
               .. _`sy_system_scope`:
               
               ############
               System Scope
               ############
               
               .. _`sy_general_idea`:
               
               {{SY('General Idea')}}
               
                 Source code is text done in a good editor.
                 Use the same editor also for documentation.
                 Jump around like in hypertext.
               
               .. include:: _links_sphinx.rst
           ├ ra.rest.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               % globals().update(include('utility.rst.tpl'))
               % RA=lambda short,alist0=[0]:II('RA',alist0,short)
               
               .. _`ra_risk_analysis`:
               
               #############
               Risk Analysis
               #############
               
               .. _`r_restructured_text`:
               
               Advantages
               ==========
               
               {{RA('Restructured Text')}}
               
                 We use `restructuredText <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_
                 together with `SimpleTemplate <https://bottlepy.org/docs/dev/stpl.html#simpletemplate-syntax>`_.
               
                 This is very flexible:
               
                 - it allows to generate boilerplate text with python
                 - it allows to link the text across documents
                 - it allows to have many final formats (html, docx, pdf, odt, ...)
                 - ...
               
               .. _`ra_risks`:
               
               Risks
               =====
               
               .. _`r_editor`:
               
               {{RA('Wrong Editor')}}
               
                 This is not for people that only know how to edit in MS Words.
                 Users should have embraced a good text editor.
                 Software guys normally have.
               
                 One needs a good text editor that supports ctags.
                 These have been tested
               
                 - `atom <https://atom.io/>`_
                 - `vim <https://www.vim.org/>`_
               
               .. include:: _links_sphinx.rst
           ├ sr.rest.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               % globals().update(include('utility.rst.tpl'))
               % SR=lambda short,alist0=[0]:II('SR',alist0,short)
               
               .. _`sr_software_system_requirements`:
               
               ############################
               Software/System Requirements
               ############################
               
               .. _`sr_general`:
               
               General
               =======
               
               .. _`sr_testable`:
               
               {{SR('Testable')}}
               
                 Requirements are testable (see |tp_requirement_tests|). 
               
               .. _`sr_style`:
               
               {{SR('Style')}}
               
                 In a restructuredText file, have one sentence in one line.
               
                 Make long sentences into 
               
                 - lists
               
                   - with sub items, if needed
               
                 - or simply make more sentences out of it

                 A link: |sr_style|.
               
               .. _`sr_a_requirement_group`:
               
               A Requirement Group
               ===================
               
               .. _`sr_id`:
               
               {{SR('ID')}}
               
                 The ID seen in the final document is numbered by a python function.
                 In the restructuredText files there is no numbering.
                 The targets use key words instead.
                 This way one can rearrange the items keeping the items sorted and still referentially consistent.
                 
                 The ID shall not contain any hyphens or dots or other non-identifier characters,
                 as some final formats, like DOCX, demand that.
               
               .. include:: _links_sphinx.rst
           ├ dd.rest.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               % globals().update(include('utility.rst.tpl'))
               % DD=lambda short,alist0=[0]:II('DD',alist0,short)
               
               .. _`dd_design_description`:
               
               ##################
               Design Description
               ##################
               
               .. _`dd_traceability`:
               
               {{DD('Traceability')}}
               
                 ``dcx.py`` associates all links between two targets to the first target.
                 This can be used as traceability.
               
                 Warnings issued during conversion to final documents help to keep the documents consistent.  
               
               .. _`dd_name`:
               
               {{DD('Name')}}
               
                 For targeted ``.. table::``, ``.. list-table::``, ``.. figure::``, ``.. code-block::`` and ``.. math::`` use ``:name:``.
                 In the legend use the same ID as in the target definition.
               
                 .. _`dd_figure`:
               
                 .. figure:: _images/egtikz.png
                    :name:
                    :width: 50%
               
                    |dd_figure|: Caption here.
                    Reference this via ``|dd_figure|``.
               
               For testing purpose the following is rendered via include files.
               
               Include normal .rst way, where the .rst might be gnerated by a ``.rst.stpl``
               
               .. include:: dd_included.rst
               
               Include the stpl way
               
               %include('dd_diagrams.tpl',DD=DD)#you optionally can provide python definitions
               
               Pandoc does not know about `definitions in included files <https://github.com/jgm/pandoc/issues/4160>`__.
               
               .. |eps1| image:: _images/egeps1.png
               .. |eps| image:: _images/egeps.png
               
               .. include:: _links_sphinx.rst
               
           ├ dd_included.rst.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               .. _`dd_code`:
               
               |dd_code|: Listing showing struct.
               
               .. code-block:: cpp
                  :name:
               
                  struct xxx{
                     int yyy; //yyy for zzz
                  }
               
               Include normal ``.rst``.
               
               .. include:: dd_tables.rst
               
               Again include the stpl way.
               
               %include('dd_math.tpl')
               
           ├ dd_tables.rst
               .. encoding: utf-8
               .. vim: syntax=rst
               
               .. _`dd_table`:
               
               |dd_table|: Table legend
               
               .. table::
                  :name:
               
                  +--------+--------+
                  | A      | B      |
                  +========+========+
                  | |eps1| | |eps|  |
                  +--------+--------+
               
               .. _`dd_list_table`:
               
               |dd_list_table|: Table legend
               
               .. list-table::
                  :name:
                  :widths: 20 80
                  :header-rows: 1
               
                  * - Bit
                    - Function
               
                  * - 0
                    - xxx
               
               Reference |dd_table| or |dd_list_table| does not show ``dd_table`` or ``dd_list_table``.
               
           ├ dd_math.tpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               .. _`dd_math`:
               
               .. math:: 
                  :name:
               
                  V = \frac{K}{r^2}
               
               ``:math:`` is the default inline role: `mc^2`
               
               With `sympy <www.sympy.org>`_ one can have formulas in ``some.py`` that are usable for calculation.
               The formulas can be converted to latex in the ``.stpl`` or ``.tpl`` file.
               
               %def hyp(a,b):
               %    return a**2+b**2
               %end
               
               The long side of a rectangular triangle with legs {{3}} and {{4}} is {{hyp(3,4)**0.5}}. See |hyp|.
               
               .. _`hyp`:
               
               .. math::
                   :name:
               
                   %import sympy
                   %from sympy.abc import a,b,c
                   {{sympy.latex(sympy.Eq(c,hyp(a,b)))}}
               
           ├ dd_diagrams.tpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               .. _`dd_diagrams`:
               
               {{DD('Diagrams')}}
               
                 .. _`exampletikz1`:
                 
                 .. figure:: _images/egtikz1.png
                    :name:
                    :width: 30%
                 
                    |exampletikz1|: Create from egtikz1.tikz
                 
                    The usage of ``:name:`` produces: ``WARNING: Duplicate explicit target name: ""``. Ignore.
                 
                 Reference via |exampletikz1|.
                 
                 ``.tikz``, ``.svg``, ``.dot``,  ``.uml``, ``.eps`` or ``.stpl`` thereof and ``.pyg``, are converted to ``.png``.
                 
                 .. _`examplesvg`:
                 
                 .. figure:: _images/egsvg.png
                    :name:
                 
                    |examplesvg|: Created from egsvg.svg.stpl
                 
                 .. _`exampledot`:
                 
                 .. figure:: _images/egdot.png
                    :name:
                 
                    |exampledot|: Created from egdot.dot.stpl
                 
                 .. _`exampleuml`:
                 
                 .. figure:: _images/eguml.png
                    :name:
                 
                    |exampleuml|: Created from eguml.uml
                 
                 .. _`exampleplt`:
                 
                 .. figure:: _images/egplt.png
                    :name:
                    :width: 30%
                 
                    |exampleplt|: Created from egplt.pyg
                 
                 .. _`examplepyx`:
                 
                 .. figure:: _images/egpyx.png
                    :name:
                 
                    |examplepyx|: Created from egpyx.pyg
                 
                 .. _`examplecairo`:
                 
                 .. figure:: _images/egcairo.png
                    :name:
                 
                    |examplecairo|: Created from egcairo.pyg
                 
                 .. _`examplepygal`:
                 
                 .. figure:: _images/egpygal.png
                    :name:
                    :width: 30%
                 
                    |examplepygal|: Created from egpygal.pyg
                 
                 .. _`exampleother`:
                 
                 .. figure:: _images/egother.png
                    :name:
                 
                    |exampleother|: Created from egother.pyg
                 
                 .. _`exampleeps1`:
                 
                 .. figure:: _images/egeps1.png
                    :name:
                 
                    |exampleeps1|: Created from egeps1.eps
                 
                 .. _`exampleeps`:
                 
                 .. figure:: _images/egeps.png
                    :name:
                 
                    |exampleeps|: Created from egeps.eps
                 
                 %if False:
                 .. _`target_more_than_in_rest`:
                 
                    It is OK to have more targets in the .stpl file.
                 %end
               
           ├ tp.rest.stpl
               .. encoding: utf-8
               .. vim: syntax=rst
               
               % globals().update(include('utility.rst.tpl'))
               % TP=lambda short,alist0=[0]:II('TP',alist0,short)
               
               .. _`tp_test_plan`:
               
               #########
               Test Plan
               #########
               
               .. _`tp_requirement_tests`:
               
               Requirement Tests
               =================
               
               .. _`tp_test_types`:
               
               {{TP('Test Types')}}
               
                 Performance tests are only one kind of tests.
                 
               .. _`tp_no_duplication`:
               
               {{TP('No duplication')}}
               
                 Since items in other documents are phrased as tests, there is no need to repeat the text here.
               
                 - |sr_id|
               
                 Or better: Reference the according chapter:
               
                 - Test |sr_a_requirement_group|
               
               .. _`tp_unit_tests`:
               
               Unit Tests
               ==========
               
               .. _`tp_gen_file`:
               
               {{TP('gen file')}}
               
                 Use ``.rst`` for included files and start the file with ``_`` if generated.
                 How test documentation files are generated from test source code can be specified in the ``gen`` file.
               
               .. include:: _links_sphinx.rst
               '''

def mktree(
    tree #tree string as list of lines
    ):
    ''' 

    Build a directory tree from a string as returned by the tree tool.

    The level is determined by the identation.

    This is not thread-safe.

    Leafs:

    - ``/`` or ``\\`` to make a directory leaf

    - ``<<`` to copy file from internet using ``http://`` or locally using ``file:://``

    - use indented lines as file content

    Example::

        >>> tree="""
        ...          a
        ...          ├aa.txt
        ...            this is aa
        ...          └u.txt<<http://docutils.sourceforge.net/docs/user/rst/quickstart.txt
        ...          b
        ...          ├c
        ...          │└d/
        ...          ├e  
        ...          │└f.txt
        ...          └g.txt
        ...            this is g
        ...       """.splitlines()
        >>> #mktree(tree) 

    '''

    for treestart,t in enumerate(tree):
        try:
            ct = re.search(r'[^\s├│└]',t).span()[0]
            break
        except:
            continue
    t1 = [t[ct:] for t in tree[treestart:]]
    entry_re = re.compile(r'^(\w[^ </\\]*)(\s*<<\s*|\s*[\\/]\s*)*(\w.*)*')
    it1 = list(rindices(entry_re,t1))
    lt1 = len(t1)
    it1.append(lt1)
    for c,f in intervals(it1):
        ef,ed,eg = entry_re.match(t1[c]).groups()
        if ef:
            if c<f-1:
                p1 = t1[c+1].find('└')+1
                p2 = t1[c+1].find('├')+1
                ix = (p1>=0 and p1 or p2)-1
                if ix >= 0 and ix <= len(ef):
                    mkdir(ef)
                    with new_cwd(ef):
                        mktree(
                          t1[c+1:f]
                          )
                else:
                    t0 = t1[c+1:f]
                    try:
                        ct = re.search(r'[^\s│]',t0[0]).span()[0]
                    except:
                        print(c,f,'\n'.join(t0[:10]))
                        print("FIRST LINE OF FILE CONTENT MUST NOT BE EMPTY!")
                    tt = [t[ct:]+'\n' for t in t0]
                    with opnwrite(ef) as fh:
                        fh.writelines(tt)
            elif eg:
                try:
                    request.urlretrieve(eg,ef)
                except Exception as e:
                    print("Error ", e)
            elif ed and (('\\' in ed) or ('/' in ed)):
                mkdir(ef)
            else:
                with opnwrite(ef) as f:
                    f.write('')

def tree(
    path #path of which to create the tree string
    ,with_content=False #use this only if all the files are text
    ,with_files=True #else only directories are listed
    ,with_dot_files=True #also include files starting with .
    ,max_depth=100 #max directory depth to list
    ):
    '''
    Inverse of mktree.
    Like the linux tree tool, but optionally with content of files

    ::

      >>> path='.'
      >>> tree(path,False)
      >>> tree(path,True)

    '''

    subprefix = ['│  ', '   '] 
    entryprefix = ['├─', '└─']
    def _tree(path, prefix):
        for p,ds,fs in os.walk(path):
            #p,ds,fs = path,[],os.listdir()
            lends = len(ds)
            lenfs = len(fs)
            if len(prefix)/3 >= max_depth:
                return
            for i,d in enumerate(sorted(ds)):
                yield prefix + entryprefix[i==lends+lenfs-1] + d
                yield from _tree(normjoin(p,d),prefix+subprefix[i==lends+lenfs-1])
            del ds[:]
            if with_files:
                for i,f in enumerate(sorted(fs)):
                    if with_dot_files or not f.startswith('.'):
                        yield prefix + entryprefix[i==lenfs-1] + f
                        if with_content:
                            for ln in _read_lines(normjoin(p,f)):
                                yield prefix + subprefix[1] + ln
    return '\n'.join(_tree(path, ''))


def initroot(
    rootfldr #directory name that becomes root of the sample tree
    ,sampletype #either 'stpl' for the templated sample tree, or 'rest'
    ):
    '''
    Creates a sample tree in the file system 
    based on the ``example_tree`` and the ``example_stp_subtree`` in dcx.py.

    >>> dry_run(True)
    >>> initroot('tmp','stpl')
    >>> cd('tmp/src')
    >>> ls()
    ['Makefile', 'code', 'conf.py', 'dcx.py', 'doc', 'docutils.conf', 'reference.docx', 'reference.odt', 'reference.tex', 'waf', 'waf.bat', 'wafw.py', 'wscript']
    >>> cd('doc')
    >>> ls()
    ['_images', 'dd.rest.stpl', 'dd_diagrams.tpl', 'dd_included.rst.stpl', 'dd_math.tpl', 'dd_tables.rst', 'egcairo.pyg', 'egdot.dot.stpl', 'egeps.eps', 'egeps1.eps', 'egother.pyg', 'egplt.pyg', 'egpygal.pyg', 'egpyx.pyg', 'egsvg.svg.stpl', 'egtikz.tikz', 'egtikz1.tikz', 'eguml.uml', 'gen', 'index.rest', 'model.py', 'ra.rest.stpl', 'sr.rest.stpl', 'sy.rest.stpl', 'tp.rest.stpl', 'utility.rst.tpl', 'wscript_build']
    >>> dry_run(False)

    '''
    #rootfldr ,sampletype = 'tmp','rest'
    stpltype = sampletype == 'stpl'
    thisfile = __file__.replace('\\','/')
    tex_ref = normjoin(dir(thisfile),'..','reference.tex')
    docx_ref = normjoin(dir(thisfile),'..','reference.docx')
    odt_ref = normjoin(dir(thisfile),'..','reference.odt')
    wafw = normjoin(dir(thisfile),'..','wafw.py')
    inittree=[l for l in example_tree.replace(
        '__file__',thisfile).replace(
        '__tex_ref__',tex_ref).replace(
        '__docx_ref__',docx_ref).replace(
        '__odt_ref__',odt_ref).replace(
        '__wafw__',wafw).splitlines()]
    if stpltype:
        _replace_lines = lambda origlns,start,stop,insertlns: origlns[
            :list(rindices(start,origlns))[0]]+insertlns+origlns[list(rindices(stop,origlns))[0]:]
        inittree = _replace_lines(inittree,'├ index.rest','├ egtikz.tikz',example_stp_subtree.splitlines())
    mkdir(rootfldr)
    with new_cwd(rootfldr):
        mktree(inittree)

def index_dir(
    root #all sub directories of ``root`` are indexed
    ):
    ''' 
    - expands the .stpl files
    - generates the files as defined in the ``gen`` file (see example in dcx.py) 
    - generates ``_links_xxx.rst`` for xxx = {sphinx latex html pdf docx odt}
    - generates ``.tags`` with jumps to reST targets

    If dcx.verbose is set to True the indexed files are printed.

    >>> dry_run(True)
    >>> fakefs.is_setup()
    True

    >>> initroot('tmp','rest')
    >>> cd('tmp/src')
    >>> ls()
    ['Makefile', 'code', 'conf.py', 'dcx.py', 'doc', 'docutils.conf', 'reference.docx', 'reference.odt', 'reference.tex', 'waf', 'waf.bat', 'wafw.py', 'wscript']

    >>> cd('doc')
    >>> ls()
    ['_images', 'dd.rest', 'egcairo.pyg', 'egdot.dot.stpl', 'egeps.eps', 'egeps1.eps', 'egother.pyg', 'egplt.pyg', 'egpygal.pyg', 'egpyx.pyg', 'egsvg.svg.stpl', 'egtikz.tikz', 'egtikz1.tikz', 'eguml.uml', 'gen', 'index.rest', 'ra.rest', 'sr.rest', 'tp.rest', 'wscript_build']

    >>> index_dir('.')
    svg2png ...
    >>> [x for x in ls() if x.startswith('_links_') or x=='.tags']
    ['.tags', '_links_docx.rst', '_links_html.rst', '_links_latex.rst', '_links_odt.rst', '_links_pdf.rst', '_links_sphinx.rst']

    >>> dry_run(False)
    >>> fakefs.is_setup()
    False

    '''

    #we need to do the templates here, because ``create_links_and_tags()`` needs them
    for p,ds,fs in os.walk(root):
        for f in fs:
            if f.endswith(_stpl):
                fullpth = normjoin(p,f)
                outpth = stem(fullpth)
                dostpl(fullpth,outpth)
    #link, gen and tags per directory
    fldrs = Fldrs(root)
    fldrs.scan()
    for directory,fldr in fldrs.items():
        if verbose:
            print(directory)
        genpth = normjoin(directory,'gen')
        if exists(genpth):
            for f,t,d,kw in parsegenfile(genpth):
                gen(normjoin(directory,f),target=normjoin(directory,t),fun=d,**kw)
        fldr.create_links_and_tags(root)


description='''\
``rstdcx`` CLI
--------------

Without parameters: creates |substitution| links and .tags ctags for reST targets.

With two or three parameters: process files through Pandoc, Sphinx, Docutils  (.rest);
Inkscape (.eps, .svg), Dot (.dot), Planuml (.uml), latex (.tex,.tikz) 
are converted to .png into ``./_images`` or ``../_images``.
Any of the files can be a SimpleTemplate templates (xxx.yyy.stpl).

Configuration is in ``conf.py`` or ``../conf.py``.

Examples with the files generated with the ``--stpl tmp``:

.. code-block:: sh

    cd tmp/src/doc
    rstdcx   #expand .stpl and produce _links_xxx.rst and .tags

    #expand stpl and append substitutions (for simple expansion use ``stpl <file> .``)
    rstdcx dd.rest.stpl - rest           # expand to stdout, appending dd.html substitutions, to pipe to Pandoc
    rstdcx dd.rest.stpl - html.          # as before
    rstdcx dd.rest.stpl - docx.          # expand to stdout, appending dd.docx substitutions, to pipe to Pandoc
    rstdcx dd.rest.stpl - newname.docx.  # expand template, appending substitutions for target newname.docx
    rstdcx dd.rest.stpl - html           # expand to stdout, already process through Pandoc to produce html on stdout
    rstdcx dd.rest.stpl                  # as before
    rstdcx sy.rest.stpl - rst_html       # expand template, already process through Docutils to produce html on stdout
    stpl sy.rest.stpl | rstdcx - - sy.html. # appending sy.html substitutions, e.g. to pipe to Pandoc
    stpl dd.rest.stpl | rstdcx - - dd.html  # appending tp.html substitutions and produce html on stdout via Pandoc
    rstdcx dd.rest.stpl dd.rest          # expand into dd.rest, appending substitutions for target dd.html
    rstdcx dd.rest.stpl dd.html html     # expand template, process through Pandoc to produce dd.html
    rstdcx dd.rest.stpl dd.html          # as before
    rstdcx dd.rest.stpl dd.html rst_html # expand template, already process through Docutils to produce dd.html
    rstdcx dd.rest.stpl dd.docx          # expand template, process through Pandoc to produce dd.docx
    rstdcx dd.rest.stpl dd.odt pandoc    # expand template, process through Pandoc to produce dd.odt
    rstdcx dd.rest.stpl dd.odt           # as before
    rstdcx dd.rest.stpl dd.odt rst_odt   # expand template, process through Docutils to produce dd.odt
    rstdcx dd.rest.stpl dd.odt rst       # as before

    #Sphinx is not file-oriented
    #but with rstdcx you need to provide the files to give Sphinx ``master_doc`` (normally: index.rest)
    #Directly from ``.stpl`` does not work with Sphinx
    rstdcx index.rest ../../build/index.html sphinx_html   # via Sphinx the output directory must be different

    #convert the graphics and place the into _images or ../_images
    #if no _images directory exists they will placed into the same folder
    rstdcx egcairo.pyg
    rstdcx egdot.dot.stpl
    rstdcx egeps.eps
    rstdcx egeps1.eps
    rstdcx egother.pyg
    rstdcx egplt.pyg
    rstdcx egpygal.pyg
    rstdcx egpyx.pyg
    rstdcx egsvg.svg.stpl
    rstdcx egtikz.tikz
    rstdcx egtikz1.tikz
    rstdcx eguml.uml

    #convert graphics to a png here (even if _images directory exists)
    rstdcx eguml.uml eguml.png

'''


def main(**args):
    '''
    This corresponds to the |rstdcx| shell command.

    '''
  
    import codecs
    import argparse
  
    if not args:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--rest', dest='restroot', action='store',
                            help='Create a sample directory structure with .rest files.')
        parser.add_argument('--stpl', dest='stplroot', action='store',
                            help='Create a sample directory structure with .rest.stpl files.')
        parser.add_argument('-v','--verbose', action='store_true',
                            help='''Show files recursively included by each rest''')
        parser.add_argument('-n','--dry-run', action='store_true',
                            help='''Don't actually run, just print.''')
        parser.add_argument('infile', nargs='?',
                help='''\
Integrates Sphinx, Pandoc and Docutils to produce output supported by any of them.
To use all three, document must not use Sphinx extensions.
Input file or - for stdin.''')
        parser.add_argument('outfile', nargs='?',
                help='Output file or - or nothing to print to std out.')
        parser.add_argument('outtype', nargs='?',default=None,
                help='One of {pandoc,sphinx,}x{html,docx,...} or omitted for default (pandoc) (- if further code paramters are given).')
        parser.add_argument('code', nargs='*',
                help='Further parameters are python code, to define variables that can be used in templates.')
        args = parser.parse_args().__dict__

    if 'code' in args and args['code'] is not None:
        code = '\n'.join(args['code'])
        eval(compile(code,'<string>','exec'),globals())

    global verbose
    verbose = False
    if 'verbose' in args:
        verbose = args['verbose']

    if 'dry_run' in args and dry_run(args['dry_run']):
        dry_run(args['dry_run'])

    if 'stplroot' in args and args['stplroot']:
        initroot(args['stplroot'],'stpl')
    elif 'restroot' in args and args['restroot']:
        initroot(args['restroot'],'rest')
    elif 'infile' in args and args['infile']:
        for x in 'infile outfile'.split():
            if x not in args: args[x] = None
        convert(args['infile'],args['outfile'],args['outtype'] if args['outtype']!='-' else None)
    else:
        index_dir('.')
  

if __name__=='__main__':
    main()

