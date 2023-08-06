# -*- coding: utf-8 -*-

from .subcluster import SubCluster
from .progress_link import Progress_Link


class Progression_Graph():
    ## the total picture, and the combinations of all clusters
    def __init__(self):
        self.clusters = []
        self.clusters_dict = {}
        self.progress = []
        self.progress_pair = []
        self.prog_dict = {}

    #def get_clusters(self):
    #    newlist = sorted(self.clusters, key=lambda x: x.time_start, reverse=False)
    #    return newlist

    def add_cluster_node(self, j, nodes):
        a_cluster = SubCluster(j, nodes)
        self.clusters.append(a_cluster)
        self.clusters_dict[j] = a_cluster

    def finalize_clusters(self):
        self.clusters.sort(key=lambda x: x.time_start, reverse=False)

    def add_progressionlink(self, cid1, cid2, op):
        #cid1 = cluster1.cluster_id
        #cid2 = cluster2.cluster_id
        cluster1 = self.clusters_dict[cid1]
        cluster2 = self.clusters_dict[cid2]
        #if (cid1,cid2) not in self.progress_pair:
        if cluster2 not in cluster1.outgoings:
            PL = Progress_Link(cluster1, cluster2, op)
            self.progress.append(PL)
            self.progress_pair.append((cid1,cid2))
            self.prog_dict[(cid1,cid2)] = PL
            cluster1.add_outgoing(cluster2)
            cluster2.add_incoming(cluster1)
        else:
            PL = self.prog_dict[(cid1,cid2)]
            PL.set_op(op)
