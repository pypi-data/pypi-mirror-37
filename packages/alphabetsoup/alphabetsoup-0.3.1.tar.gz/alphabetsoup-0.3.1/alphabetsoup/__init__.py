# -*- coding: utf-8 -*-
"""alphabetsoup -- fix alphabet and other problems in protein FASTA files.

Here are some common problems in protein-coding sequences and fixes:
Presence of stop codons at end - strip
Ambiguous residues at end - strip
Codes other than IUPAC + 'X' elsewhere - change to X
Length shorter than MINLEN - delete whole entry
"""
#
# standard library imports
#
import functools
import locale
import logging
import sys
from pathlib import Path
from datetime import datetime
#
# third-party imports
#
import click
import coverage
import dask.bag as db
import pandas as pd
from dask.diagnostics import ProgressBar
#
# package imports
#
from .version import version as VERSION
from .process_file import process_file
from .process_logs import process_logs
from .common import *
#
# Start coverage
#
coverage.process_startup()
# set locale so grouping works
for localename in ['en_US', 'en_US.utf8', 'English_United_States']:
    try:
        locale.setlocale(locale.LC_ALL, localename)
        break
    except:
        continue

PROGRAM_NAME = 'alphabetsoup'
AUTHOR = 'Joel Berendzen'
EMAIL = 'joelb@ncgr.org'
COPYRIGHT = """Copyright (C) 2018, The National Center for Genome Resources.  All rights reserved.
"""
PROJECT_HOME = 'https://github.com/ncgr/alphabetsoup'

DEFAULT_FILE_LOGLEVEL = logging.DEBUG
DEFAULT_STDERR_LOGLEVEL = logging.INFO
DEFAULT_FIRST_N = 0 # only process this many files
STARTTIME = datetime.now()
DEFAULT_MINLEN = 0 # minimum gene size in residues
DEFAULT_MINSEQS = 0 # minimum number of sequences per file
DEFAULT_MAXAMBIG = 0 # maximum number of ambiguous characters per gene, (0 = all)
DEFAULT_FILETYPES = ('*.faa', '*.fa', '*.fasta')
LOG_PATH = Path('.')/ 'logs'
#
# global logger object
#
logger = logging.getLogger(PROGRAM_NAME)
#
# private context function
#
_ctx = click.get_current_context
#
# Classes
#
class CleanInfoFormatter(logging.Formatter):
    def __init__(self, fmt = '%(levelname)s: %(message)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        if record.levelno == logging.INFO:
            return record.getMessage()
        return logging.Formatter.format(self, record)


#
# Helper functions
#
def init_dual_logger(file_log_level=DEFAULT_FILE_LOGLEVEL,
                     stderr_log_level=DEFAULT_STDERR_LOGLEVEL):
    '''Log to stderr and to a log file at different levels
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            global logger
            # find out the verbose/quiet level
            if _ctx().params['verbose']:
                _log_level = logging.DEBUG
            elif _ctx().params['quiet']:
                _log_level = logging.ERROR
            else:
                _log_level = stderr_log_level
            logger.setLevel(file_log_level)
            stderrHandler = logging.StreamHandler(sys.stderr)
            stderrFormatter = CleanInfoFormatter()
            stderrHandler.setFormatter(stderrFormatter)
            stderrHandler.setLevel(_log_level)
            logger.addHandler(stderrHandler)
            if _ctx().params['logs']: # start a log file in LOG_PATH
                logfile_path = LOG_PATH / (PROGRAM_NAME + '.log')
                if not LOG_PATH.is_dir():  # create LOG_PATH
                    try:
                        logfile_path.parent.mkdir(mode=0o755, parents=True)
                    except OSError:
                        logger.error('Unable to create logfile directory "%s"',
                                     logfile_path.parent)
                        raise OSError
                else:
                    if logfile_path.exists():
                        try:
                            logfile_path.unlink()
                        except OSError:
                            logger.error('Unable to remove existing logfile "%s"',
                                         logfile_path)
                            raise OSError
                logfileHandler = logging.FileHandler(str(logfile_path))
                logfileFormatter = logging.Formatter('%(levelname)s: %(message)s')
                logfileHandler.setFormatter(logfileFormatter)
                logfileHandler.setLevel(file_log_level)
                logger.addHandler(logfileHandler)
            logger.debug('Command line: "%s"', ' '.join(sys.argv))
            logger.debug('%s version %s', PROGRAM_NAME, VERSION)
            logger.debug('Run started at %s', str(STARTTIME)[:-7])
            return f(*args, **kwargs)
        return wrapper
    return decorator

def init_user_context_obj(initial_obj=None):
    '''Put info from global options into user context dictionary
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            global config_obj
            if initial_obj is None:
                _ctx().obj = {}
            else:
                _ctx().obj = initial_obj
            ctx_dict = _ctx().obj
            if _ctx().params['verbose']:
                ctx_dict['logLevel'] = 'verbose'
            elif _ctx().params['quiet']:
                ctx_dict['logLevel'] = 'quiet'
            else:
                ctx_dict['logLevel'] = 'default'
            for key in ['progress', 'first_n']:
                ctx_dict[key] = _ctx().params[key]
            return f(*args, **kwargs)
        return wrapper
    return decorator


@click.command(epilog=AUTHOR+' <'+EMAIL+'>.  '+COPYRIGHT)
@click.option('-v', '--verbose', is_flag=True, show_default=True,
              default=False, help='Debug info to stderr.')
@click.option('-q', '--quiet', is_flag=True, show_default=True,
              default=False, help='Suppress logging to stderr.')
@click.option('--progress', is_flag=True, show_default=True,
              default=False, help='Show a progress bar.')
@click.option('--first_n', default=DEFAULT_FIRST_N,
               help='Process only this many files. [default: all]')
@click.option('--minlen', default=DEFAULT_MINLEN,show_default=True,
               help='Minimum sequence length.')
@click.option('--minseqs', default=DEFAULT_MINSEQS,show_default=True,
               help='Minimum number of sequences in file.')
@click.option('--maxambig', default=DEFAULT_MAXAMBIG,
               help='Maximum # of ambiguous residues. [default:any]')
@click.option('--logs/--no-logs', is_flag=True, show_default=True,
              default=True, help='Write analysis in ./logs.')
@click.option('--log_lengths/--no-log_lengths', is_flag=True,
              show_default=True, default=False, help='Write lengths to log.')
@click.option('--dedup/--no-dedup', is_flag=True, show_default=True,
              default=False, help='De-duplicate sequences.')
@click.option('--defrag/--no-defrag', is_flag=True, show_default=True,
              default=False, help='Remove exact substrings.')
@click.option('--histbeginning/--no-histbeginning', is_flag=True, show_default=True,
              default=False, help='Show only beginning of histograms.')
@click.option('--stripdash/--no-stripdash', is_flag=True, show_default=True,
              default=True, help='Remove "-" characters.')
@click.option('--overwrite/--no-overwrite', is_flag=True, show_default=True,
              default=False, help='Overwrite input files.')
@click.argument('in_path', type=click.Path(exists=True,
                                           writable=True,
                                           resolve_path=True,
                                           allow_dash=True,
                                           ))
@click.version_option(version=VERSION, prog_name=PROGRAM_NAME)
@init_dual_logger()
@init_user_context_obj()
def cli(in_path,
        verbose,
        quiet,
        progress,
        first_n,
        logs,
        overwrite,
        minlen,
        minseqs,
        maxambig,
        dedup,
        histbeginning,
        stripdash,
        defrag,
        log_lengths):
    """alphabetsoup -- fix alphabet and other problems in protein FASTA files
    """
    if quiet or verbose:
        progress = False
    if defrag:
        dedup = True

    logger.debug('')
    in_path = Path(in_path)
    files = []
    for ext in DEFAULT_FILETYPES:
        files.extend(in_path.rglob(ext))
    if first_n > 0 and len(files) > first_n:
        files = files[:first_n]
    if progress:
        logger.info('Processing %d files in parallel:', len(files))
    if progress:
        ProgressBar().register()
    bag = db.from_sequence(files)
    results = bag.map(process_file,
                      logger=logger,
                      write=overwrite,
                      min_len=minlen,
                      min_seqs=minseqs,
                      max_ambiguous=maxambig,
                      remove_duplicates=dedup,
                      remove_dashes=stripdash,
                      remove_substrings=defrag,
                      lengths=log_lengths).compute()
    if logs:
        process_logs(LOG_PATH, results, logger, beginning_only=histbeginning)
    #
    # Transpose results and put Name as first column
    #
    max_qty_len = max([len(s) for s in STAT_COLS])
    df = pd.DataFrame(results,
                      columns=STAT_COLS)
    if not quiet:
        print('Quantity\tSum\tMean')
        print('%s:\t%d\t0' %('Files'.rjust(max_qty_len), len(files)))
        for col_name in STAT_COLS[1:]:
            column = df[col_name]
            print('%s:\t%d\t%.3f'%(col_name.rjust(max_qty_len),column.sum(),column.mean()))
    sys.exit(0)
