# -*- coding: utf-8 -*-

from numpy import median

class SubCluster():
    ## cluster is the component in terms of
    ## nodes and neighbor_link
    def __init__(self, cid, nodeslist):
        self.cluster_id = cid
        self.node_list = nodeslist
        self.cluster_size = len(nodeslist)
        self.xcor = None
        self.ycor = None
        self.time_start = None
        self.time_stop = None
        self.time_median = None
        self.chain_id = None
        self._calculation_info()
        self.outgoings = []
        self.incomings = []
        self.behaviors = []

    def _calculation_info(self):
        xlist = [n.xcor for n in self.node_list]
        ylist = [n.ycor for n in self.node_list]
        self.xcor = sum(xlist)/float(len(xlist))
        self.ycor = sum(ylist)/float(len(ylist))

        tlist = [n.time for n in self.node_list]
        self.time_start = min(tlist)
        self.time_stop = max(tlist)
        self.time_median = median(tlist)

    def add_outgoing(self, acluster):
        self.outgoings.append(acluster)

    def add_incoming(self, acluster):
        self.incomings.append(acluster)

    def set_chain_id(self, cid):
        self.chain_id = cid

    def finalize_behaviors(self):
        if len(self.incomings)<1:
            self.behaviors.append('appearing')
        elif len(self.incomings)>1:
            self.behaviors.append('merging')
        else: ## ==1
            c0 = self.incomings[0]
            l0 = c0.cluster_size
            l1 = self.cluster_size
            if l0>l1:
                self.behaviors.append('shrinking')
            elif l0<l1:
                self.behaviors.append('growing')
            else:
                self.behaviors.append('maintained')
        if len(self.outgoings)<1:
            self.behaviors.append('disappearing')
        elif len(self.outgoings)>1:
            self.behaviors.append('splitting')


"""
class Component_Graph():
    ## component_graph is the component in terms of
    ## clusters and linked by their nodes' shifting_link
    def __init__(self):
        pass
"""
