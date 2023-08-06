
# -*- coding: utf-8 -*-
"""alphabetsoup -- fix alphabet and length problems in protein FASTA files.

Here are some common problems in protein-coding sequences and fixes:
Presence of stop codons at end - strip
Ambiguous residues at end - strip
Codes other than IUPAC + 'X' elsewhere - change to X
Length shorter than MINLEN - delete whole entry
"""
#
# standard library imports
#
import csv
import functools
import itertools
import locale
import logging
import sys
import zlib
from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from datetime import datetime
#
# third-party imports
#
import click
import coverage
import dask.bag as db
from Bio import SeqIO
from Bio.Data import IUPACData
from dask.diagnostics import ProgressBar
#
# package imports
#
from .version import version as VERSION
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
DEFAULT_MINLEN = 10 # minimum gene size in residues
DEFAULT_FILETYPES = ('*.faa', '*.fa', '*.fasta')
ALPHABET = IUPACData.protein_letters + 'X' + '-'
LOG_DIR = 'logs'
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


class DuplicateIDDict(defaultdict):
    """A dictionary of lists with a get() that returns a mangled ID
    """
    def __init__(self):
        super().__init__(list)

    def get(self,k):
        dup_list = [k] + self[k]
        char_tuples = zip(*dup_list)
        prefix_tuples = itertools.takewhile(lambda x: all(x[0] == y for y in x),
                                            char_tuples)
        prefix = ''.join(x[0] for x in prefix_tuples)
        prefix_len = len(prefix)
        mangled = prefix + '{' + ','.join(id[prefix_len:] for id in dup_list)+ '}'
        return mangled


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
            if _ctx().params['log']: # start a log file
                logfile_name = PROGRAM_NAME + '.log'
                logfile_path = Path('.') / LOG_DIR / logfile_name
                if not logfile_path.parent.is_dir():  # create logs/ dir
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


def process_file(file,
                 write=True,
                 min_len=0,
                 remove_duplicates=False,
                 remove_dashes=False,
                 remove_substrings=True):
    logger.debug('processing %s', file)
    out_sequences = []
    out_len = 0
    n_interior_ambig = 0
    seq_hash_dict = {}
    n_dups = 0
    n_substrings = 0
    n_seqs_in = 0
    duplicate_ID_dict = DuplicateIDDict()
    with file.open('rU') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            n_seqs_in += 1
            seq = record.seq.tomutable()
            if remove_dashes:
                # delete '-' as insertion characters in an alignment
                [ seq.pop(dash_pos-k) for k, dash_pos in
                    enumerate([i for i,j in enumerate(seq) if j == '-'])]
            # replace everything else out of alphabet with 'X'-
            [seq.__setitem__(i, 'X')
             for i, j in enumerate(seq) if j not in ALPHABET]
            # remove trailing ambiguous/stop
            while seq[-1] == 'X':
                seq.pop()
            # remove leading ambiguous
            while seq[0] == 'X':
                seq.pop(0)
            # discard if too short
            if len(record.seq) < min_len:
                logger.debug('%s\t%s\tlength\t%d',
                             file.name, record.id, len(record.seq))
                continue
            # count duplicates and optionally discard
            seq_hash = zlib.adler32(bytearray(str(seq),'utf-8'))
            if seq_hash not in seq_hash_dict:
                seq_hash_dict[seq_hash] = record.id
            else:
                n_dups += 1
                first_ID = seq_hash_dict[seq_hash]
                duplicate_ID_dict[first_ID].append(record.id)
                logger.debug('%s\t%s\tduplicates\t%s',
                             file.name, record.id, first_ID)
                if remove_duplicates:
                    continue
            # count interior X's but don't do anything to them
            X_arr = [i =='X' for i in seq]
            if any(X_arr):
                n_interior_ambig += 1
                logger.debug('%s\t%s\tambiguous\t%d',
                             file.name, record.id, sum(X_arr))
            record.seq = seq.toseq()
            out_sequences.append(record)
            out_len += len(record.seq)
    # Search for exact substring matches in the set
    length_idx = [(i,len(record.seq))
                  for i, record in enumerate(out_sequences)]
    length_idx.sort(key=itemgetter(1))
    ascending = [idx for idx,length in length_idx]
    subst_removal_list = []
    for item_num,idx in enumerate(ascending):
        test_seq = out_sequences[idx].seq
        test_id = out_sequences[idx].id
        # traverse from biggest to smallest to find the biggest match
        for record in [out_sequences[i] for i in reversed(ascending[item_num+1:])]:
            if str(test_seq) in str(record.seq):
                n_substrings += 1
                duplicate_ID_dict[record.id].append(test_id)
                subst_removal_list.append(idx)
                logger.debug('%s\t%s\tsubstring\t%s',
                             file.name, test_id, record.id)
                break
    # Optionally remove exact substring matches
    if remove_substrings and len(subst_removal_list) > 0:
        subst_removal_list.sort()
        for item_num, idx in enumerate(subst_removal_list):
            out_sequences.pop(idx-item_num)
    # Indicate (in ID) records deduplicated
    if (remove_duplicates or remove_substrings) and len(duplicate_ID_dict) > 0:
        for record in out_sequences:
            if record.id in duplicate_ID_dict:
                record.id = duplicate_ID_dict.get(record.id)
                record.description = ''
    if write:
        with file.open('w') as output_handle:
            SeqIO.write(out_sequences,output_handle,'fasta')
    return (n_seqs_in,
            len(out_sequences),
            out_len,
            n_interior_ambig,
            n_dups,
            n_substrings,
            file.name)

@click.command(epilog=AUTHOR+' <'+EMAIL+'>.  '+COPYRIGHT)
@click.option('-v', '--verbose', is_flag=True, show_default=True,
              default=False, help='Log debugging info to stderr.')
@click.option('-q', '--quiet', is_flag=True, show_default=True,
              default=False, help='Suppress logging to stderr.')
@click.option('--progress', is_flag=True, show_default=True,
              default=False, help='Show a progress bar, if supported.')
@click.option('--first_n', default=DEFAULT_FIRST_N,
               help='Process only this many files. [default: all]')
@click.option('--minlen', default=DEFAULT_MINLEN,
               help='Minimum sequence length.')
@click.option('--log/--no-log', is_flag=True, show_default=True,
              default=True, help='Log to file.')
@click.option('--dedup/--no-dedup', is_flag=True, show_default=True,
              default=False, help='De-duplicate sequences.')
@click.option('--defrag/--no-defrag', is_flag=True, show_default=True,
              default=False, help='Remove exact-match substrings.')
@click.option('--stripdash/--no-stripdash', is_flag=True, show_default=True,
              default=False, help='Remove "-" alignment characters.')
@click.option('--write_file/--no-write-file', is_flag=True, show_default=True,
              default=True, help='Write to files.')
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
        first_n, log,
        write_file,
        minlen,
        dedup,
        stripdash,
        defrag):
    """alphabetsoup -- fix alphabet problems in protein FASTA files
    """
    if quiet or verbose:
        progress = False
    if defrag:
        dedup = True
    in_path = Path(in_path)
    files = []
    for ext in DEFAULT_FILETYPES:
        files.extend(in_path.rglob(ext))
    if first_n > 0 and len(files) > first_n:
        files = files[:first_n]
    logger.info('Processing %d files found in %s:', len(files), in_path)
    if progress:
        ProgressBar().register()
    bag = db.from_sequence(files)
    results = bag.map(process_file,
                      write=write_file,
                      min_len=minlen,
                      remove_duplicates=dedup,
                      remove_dashes=stripdash,
                      remove_substrings=defrag).compute()
    resultfile_name = PROGRAM_NAME + '.tsv'
    resultfile_path = Path('.') / LOG_DIR / resultfile_name
    if log:
        with resultfile_path.open('w', newline='') as resultfh:
            writer = csv.writer(resultfh, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['#SeqsIn','SeqsOut', 'Chars', 'Ambig', 'Dups','Substr', 'Name'])
            for row in results:
                writer.writerow(row)
        logger.info('Results written to %s.', resultfile_path)
    sys.exit(0)

