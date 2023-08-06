# -*- coding: utf-8 -*-

## node file

class Node():
    ## incident point in the data
    def __init__(self, idd, time, xcor, ycor):
        self.idd = idd
        self.time = time
        self.xcor = xcor
        self.ycor = ycor
        self.neighbors = []
        self.neighbor_nodes = []
        self.neighbors_final = []
        self.incoming = []
        #self.ori_weight = None # the combine risks of incoming
        #self.ori_rate = None # the combine risk / total combine risks
        self.outgoing = []
        self.cluster_id = None
        self.chain_id = None
        self.origin_pos_dict = {}

    def add_neighbor(self, a_nlink):
        self.neighbor_nodes.append(a_nlink.other_end(self))
        self.neighbors.append(a_nlink)

    def check_isneighbor(self, anode):
        if anode in self.neighbor_nodes:
            return True
        else:
            return False

    def add_incoming(self, a_slink):
        self.incoming.append(a_slink)

    def add_outgoing(self, a_slink):
        self.outgoing.append(a_slink)

    def add_finalnlink(self, a_nlink):
        self.neighbors_final.append(a_nlink)

    def set_clusterid(self, cid):
        self.cluster_id = cid

    def set_chain_id(self, cid):
        self.chain_id = cid

    def set_slink_orp(self, slink, oripos):
        self.origin_pos_dict[slink.origin.idd] = (slink, oripos)
