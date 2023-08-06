# -*- coding: utf-8 -*-
import csv
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .common import *
MIN_HIST_LEN = 50
PLOT_TYPES = ['png','svg']
HIST_MAX_VAL = {LENGTH_NAME: 100,
                AMBIG_NAME: 20,
                SEQS_NAME: 50,
                FILESMALL_NAME: 10,
                SHORT_NAME: 50}

def process_logs(path, stats, logger, beginning_only=False):
    logger.info('Processing log files serially')
    #
    # write overall stats
    #
    with (path / 'alphabetsoup_stats.tsv').open('w', newline='') as resultfh:
        writer = csv.writer(resultfh, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['#'+ STAT_COLS[1]] + list(STAT_COLS[2:]) + [STAT_COLS[0]])
        for row in stats:
            writer.writerow(list(row[1:]) + [row[0]])
    #
    # get path to logfile
    #
    logfile_names = []
    for handler in logger.handlers:
        try:
            logfile_names.append(handler.stream.name)
        except:
            pass
    logfile_names.remove('<stderr>')
    logfile_path = Path(logfile_names[0])
    #
    # Shut down logging and parse log file
    #
    logging.shutdown()
    stat_dict = {}
    graph_dict = {}
    for stat_name in STAT_TYPES:
        stat_dict[stat_name] = []
    for graph_name in GRAPH_TYPES:
        graph_dict[graph_name] = []
    tmpfile_path = logfile_path.parent/(logfile_path.name + 'tmp')
    with tmpfile_path.open('w') as tmpfh:
        with logfile_path.open('rU') as logfh:
            line = logfh.readline()
            while line:
                line = logfh.readline()
                parts = line.split('\t')
                if len(parts) > 2 and parts[2] in (GRAPH_TYPES + STAT_TYPES):
                    file = parts[0].strip('DEBUG: ')
                    record = parts[1]
                    rec_type = parts[2]
                    if rec_type in STAT_TYPES:
                        value = int(parts[3])
                        stat_dict[rec_type].append((file, record, value))
                    else:
                        id = parts[3].strip()
                        graph_dict[rec_type].append((file, id, record))
                else:
                    tmpfh.write(line)
            logfh.close()
    tmpfile_path.rename(logfile_path)
    for stat_name in STAT_TYPES:
        stat_frame = pd.DataFrame(stat_dict[stat_name],
                                            columns=['file', 'record', 'value'])
        stat_len = len(stat_frame)
        if stat_len > 0:
            stat_frame = stat_frame.sort_values(['file', 'record', 'value']
                                                ).reindex(index=list(range(stat_len)))
            stat_frame.to_csv(path/(stat_name+'.tsv'), sep='\t')
            if stat_len > MIN_HIST_LEN:
                dist = np.array(stat_frame['value'])
                mean = dist.mean()
                if beginning_only:
                    dist = dist[dist < HIST_MAX_VAL[stat_name]]
                    label = 'low'
                else:
                    label = '%d' % stat_len
                # do histogram plot with kernel density estimate
                sns.distplot(dist,
                             rug=True,
                             rug_kws={'color': 'b'},
                             kde_kws={'color': 'k', 'lw': 1, 'label': 'KDE'},
                             hist_kws={'histtype': 'step',
                                       'linewidth': 2,
                                       'alpha': 1,
                                       'color': 'b'}
                )
                plt.title('%s histogram of %s values, overall mean=%.1f'
                          %(stat_name, label, mean))
                plt.xlabel(stat_name)
                plt.ylabel('Frequency')
                for ext in PLOT_TYPES:
                   plt.savefig(path/('%s-hist.'%(stat_name) + ext), bbox_inches='tight')
    for graph_name in GRAPH_TYPES:
        graph_frame = pd.DataFrame(graph_dict[graph_name],
                                   columns=['file','id','duplicate'])
        graph_len = len(graph_frame)
        if graph_len > 0:
            graph_frame = graph_frame.sort_values(['file', 'id', 'duplicate']
                                                  ).reindex(index=list(range(graph_len)))
            graph_frame.to_csv(path/(graph_name+'.tsv'), sep='\t')
