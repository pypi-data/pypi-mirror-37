# -*- coding: utf-8 -*-
# stdlib imports
import zlib
from collections import defaultdict
from operator import itemgetter
# third-party imports
from Bio import SeqIO
from Bio.Data import IUPACData
# package imports
from .common import *

ALPHABET = IUPACData.protein_letters + 'X' + '-'
LOGINT_FMT = '%s\t%s\t%s\t%d'
LOGSTR_FMT = '%s\t%s\t%s\t%s'

class DuplicateIDDict(defaultdict):
    """A dictionary of lists with a get() that returns a mangled ID
    """
    def __init__(self):
        super().__init__(list)

    def get(self,k):
        dup_list = [k] + self[k]
        # Make a prefixed list with bracked, discarded because too complex later
        #char_tuples = zip(*dup_list)
        #prefix_tuples = itertools.takewhile(lambda x: all(x[0] == y for y in x),
        #                                    char_tuples)
        #prefix = ''.join(x[0] for x in prefix_tuples)
        #prefix_len = len(prefix)
        #mangled = prefix + '{' + '|'.join(id[prefix_len:] for id in dup_list)+ '}'
        return '|'.join(dup_list)


def process_file(file,
                 logger=None,
                 write=False,
                 min_len=0,
                 min_seqs=0,
                 max_ambiguous=0,
                 remove_duplicates=False,
                 remove_dashes=False,
                 remove_substrings=False,
                 lengths=False):
    if logger:
        logger.debug('processing %s', file)
    out_sequences = []
    out_len = 0
    n_interior_ambig = 0
    seq_hash_dict = {}
    n_dups = 0
    n_substrings = 0
    n_seqs_in = 0
    n_short = 0
    duplicate_ID_dict = DuplicateIDDict()
    with file.open('rU') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            n_seqs_in += 1
            seq = record.seq.upper().tomutable()
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
                n_short += 1
                if logger:
                    logger.debug(LOGINT_FMT,
                                 file.name,
                                 record.id,
                                 SHORT_NAME,
                                 min_len - len(record.seq) + 1)
                continue
            # count duplicates and optionally discard
            seq_hash = zlib.adler32(bytearray(str(seq),'utf-8'))
            if seq_hash not in seq_hash_dict:
                seq_hash_dict[seq_hash] = record.id
            else:
                n_dups += 1
                first_ID = seq_hash_dict[seq_hash]
                duplicate_ID_dict[first_ID].append(record.id)
                logger.debug(LOGSTR_FMT,
                             file.name,
                             record.id,
                             DUP_NAME,
                             first_ID)
                if remove_duplicates:
                    continue
            # count interior X's and discard if more than max_ambiguous
            ambig = sum([i =='X' for i in seq])
            if ambig > max_ambiguous:
                n_interior_ambig += 1
                if logger:
                    logger.debug(LOGINT_FMT,
                                 file.name,
                                 record.id,
                                 AMBIG_NAME,
                                 ambig)
                continue
            record.seq = seq.toseq()
            out_sequences.append(record)
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
                if logger:
                    logger.debug(LOGSTR_FMT,
                                 file.name,
                                 test_id,
                                 SUBSTRING_NAME,
                                 record.id)
                break
    # Optionally remove exact substring matches
    if remove_substrings and len(subst_removal_list) > 0:
        subst_removal_list.sort()
        for item_num, idx in enumerate(subst_removal_list):
            out_sequences.pop(idx-item_num)
    # Count length of output residues
    for record in out_sequences:
        out_len += len(record.seq)
    # Indicate (in ID) records deduplicated
    if (remove_duplicates or remove_substrings) and len(duplicate_ID_dict) > 0:
        for record in out_sequences:
            if record.id in duplicate_ID_dict:
                record.id = duplicate_ID_dict.get(record.id)
                record.description = ''
    # If file is small, log it.  Else write lengths if requested.
    if len(out_sequences) < min_seqs:
        logger.debug(LOGINT_FMT,
                     file.name,
                     record.id,
                     FILESMALL_NAME,
                     len(out_sequences))
        small = 1
    else:
        if lengths and logger:
            for record in out_sequences:
                logger.debug(LOGINT_FMT,
                             file.name,
                             record.id,
                             LENGTH_NAME,
                             len(record.seq))
        if logger:
            logger.debug(LOGINT_FMT,
                         file.name,
                         record.id,
                         SEQS_NAME,
                         len(out_sequences))
        small = 0
    if write:
        if not small:
            with file.open('w') as output_handle:
                SeqIO.write(out_sequences,output_handle,'fasta')
        else:
            logger.warn('file %s has only %d sequences after processing, removed',
                        file.name, len(out_sequences))
            file.unlink()
    return (file.name,
            n_seqs_in,
            len(out_sequences),
            out_len,
            n_interior_ambig,
            n_short,
            small,
            n_dups,
            n_substrings)
