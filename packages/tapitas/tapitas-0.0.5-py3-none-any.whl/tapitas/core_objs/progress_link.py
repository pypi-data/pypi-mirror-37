# -*- coding: utf-8 -*-

class Progress_Link():
    ## the directed links between clusters in each progression_graph
    def __init__(self, cluster1, cluster2, op):
        self.origin = cluster1
        self.destination = cluster2
        self.ori_pos = op
        self.no_slink = 1

    def set_op(self, ori_pos):
        if ori_pos>self.ori_pos:
            self.ori_pos = ori_pos
        self._add_no_slink()

    def _add_no_slink(self):
        self.no_slink += 1
