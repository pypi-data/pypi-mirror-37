# -*- coding: utf-8 -*-

import os

def to_csv(oo, filename_prefix=None):
    # oo == Output_Objects
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    filename1 = filename_prefix+"_nodes.csv"
    filename2 = filename_prefix+"_clusters.csv"
    filename3 = filename_prefix+"_proglinks.csv"
    filename4 = filename_prefix+"_summary.csv"
    filename5 = filename_prefix+"_slinks_final.csv"
    filename6 = filename_prefix+"_cluster_pairs.csv"
    
    oo.node_df.to_csv(filename1, index_label='ind')
    oo.cluster_df.to_csv(filename2, index_label='ind')
    oo.progress_df.to_csv(filename3, index_label='ind')
    oo.summary_df.to_csv(filename4, index_label='ind')
    oo.final_slinks_df.to_csv(filename5, index_label='ind')
    oo.final_nlinks_df.to_csv(filename6, index_label='ind')
