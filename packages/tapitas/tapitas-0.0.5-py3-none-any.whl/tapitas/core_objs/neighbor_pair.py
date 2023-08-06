# -*- coding: utf-8 -*-

## neigboring pair

class Neighbor_Pair():
    ## the connection between neighboring nodes (both time and space)
    def __init__(self, node1, node2):
        self.one = node1
        self.two = node2
        self.cop = None
        self.max_cop = None
        self.link1_max = None
        self.link2_max = None
        self.copmax_links = None

    def other_end(self, anode):
        if anode == self.one:
            return self.two
        else:
            return self.one

    def calculate_cop(self):
        # cop: common origin propensity
        Pcops = {}
        Pcops_list = []
        in_1 = self.one.origin_pos_dict
        in_2 = self.two.origin_pos_dict
        len1 = len(in_1)
        len2 = len(in_2)
        base_in = in_1
        check_in = in_2
        if len2<len1:
            base_in = in_2
            check_in = in_1
        for k in base_in.keys():
            if k in check_in:
                l1,orp1 = base_in[k]
                l2,orp2 = check_in[k]
                pcop = orp1*orp2
                Pcops_list.append(pcop)
                #Pcops[ori1] = pcop
                if pcop not in Pcops:
                    Pcops[pcop] = []
                Pcops[pcop].append((l1,l2))

        if len(Pcops)>0:
            cops = Pcops.keys()
            self.cop = sum(Pcops_list)
            #print cop_max == max(cops)
            self.max_cop = max(cops)
            self.copmax_links = Pcops[self.max_cop]
            self.link1_max = []
            self.link2_max = []
            for a,b in self.copmax_links:
                self.link1_max.append(a)
                self.link2_max.append(b)
