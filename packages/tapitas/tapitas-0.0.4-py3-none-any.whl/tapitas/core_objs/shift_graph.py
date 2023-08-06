# -*- coding: utf-8 -*-

## the shifting graph object,
## compose by nodes, neighboring pair, and shifting link

# import dependencies
import time
from random import randint
from scipy import spatial
from scipy.stats import norm
from numpy import std as nstd
# import local objects
from .node import Node
from .neighbor_pair import Neighbor_Pair
from .shifting_link import Shifting_Link

class Shift_Graph():
    ## the total picture of all nodes, neighbor_pair, and shifting_link
    def __init__(self):
        self.nodes = []
        self.isolated_nodes = []
        self.nlinks = []
        self.slinks = []
        self.nlinks_final = []
        self.slinks_final = []
        self.spatial_neighbor_list = None
        self.spatial_neighbor_dicts = None
        self.critical_value = None

    def add_node(self, idd, dd, xx, yy):
        anode = Node(idd, dd,xx,yy)
        self.nodes.append(anode)
        #self.nodes_dict[dd] = anode

    def _add_nlink(self, n1, n2):
        if not n1.check_isneighbor(n2):
            a_nlink = Neighbor_Pair(n1, n2)
            self.nlinks.append(a_nlink)
            n1.add_neighbor(a_nlink)
            n2.add_neighbor(a_nlink)

    def _add_slink(self, n1, n2, s_radius, T1, T2):
        a_slink = Shifting_Link(n1, n2, s_radius, T1, T2)
        self.slinks.append(a_slink)
        n2.add_incoming(a_slink)
        n1.add_outgoing(a_slink)

    def prepare(self, s_radius, T2):
        xlist = []
        ylist = []
        for n in self.nodes:
            xlist.append(n.xcor)
            ylist.append(n.ycor)
        pts = list(zip(xlist, ylist))
        #print('debug this:', len(pts))
        tree = spatial.KDTree(pts)
        nlist = tree.query_ball_point(x=pts, r=s_radius)
        self.spatial_neighbor_list = []
        self.spatial_neighbor_dicts = []
        for i in range(len(nlist)):
            nns = nlist[i]
            nns.remove(i)
            self.spatial_neighbor_list.append(nns)
            temp_dict = {}
            a_node = self.nodes[i]
            a_t = a_node.time
            for j in nns:
                b_node = self.nodes[j]
                b_t = b_node.time
                if( b_t <= (a_t + T2)) and (b_t >= a_t):
                    if b_t not in temp_dict:
                        temp_dict[b_t] = []
                    temp_dict[b_t].append(b_node)
            self.spatial_neighbor_dicts.append(temp_dict)


    def find_links(self, s_radius, T1, T2):
        ## ===============
        print('find links - start')
        #print 'calculate passing possibility - start'
        ## ===============
        nodes = self.nodes
        spatial_neighbor_list = self.spatial_neighbor_list

        for i in range(len(nodes)):
            a_node = nodes[i]
            t_i = a_node.time
            this_sns = self.spatial_neighbor_dicts[i]
            for tt in range(T1):
                tx = tt + t_i
                if tx in this_sns:
                    #print tx
                    #x = [ self._add_nlink(a_node, b) for b in this_sns[tx] ]
                    for b_node in this_sns[tx]:
                        self._add_nlink(a_node,b_node)
            for tt in range(T1,T2+1):
                tx = tt + t_i
                if tx in this_sns:
                    #x = [ self._add_slink(a_node, b, s_radius, T1, T2) for b in this_sns[tx] ]
                    for b_node in this_sns[tx]:
                        self._add_slink(a_node, b_node, s_radius, T1, T2)

        ## ===============
        print('find links - stop')
        print('calculate passing possibility - start')
        ## ===============
        self._calculate_passing_possibility()
        ## ===============
        print('calculate passing possibility - stop')
        print('calculate propensity - start')
        ## ===============
        self._calculate_propensity() ## maybe this part slow
        ## ===============
        print('calculate propensity - stop')
        #print 'calculate propensity - start'
        ## ===============

    def _calculate_passing_possibility(self):
        nodes = self.nodes
        origins = []
        for n in nodes:
            incomings = n.incoming
            if len(incomings)>0:
                #print len(incomings)
                iws = [i.combine_risk for i in incomings]
                tot = float(sum(iws))
                ori_rate = [w/tot for w in iws]
                #n.set_ori_weight(iws)
                #n.set_ori_rate(ori_rate)
                for ll,oo in zip(incomings, ori_rate):
                    ll.set_ori_pos(oo)
                    n.set_slink_orp(ll,oo)
            else:
                if len(n.outgoing)<=0:
                    self.isolated_nodes.append(n)
                else:
                    origins.append(n)
        #print "isolated nodes count:", str(len(self.isolated_nodes))
        #print "origins nodes count:", str(len(origins))

    def _calculate_propensity(self):
        nlinks = self.nlinks
        for a_link in nlinks:
            a_link.calculate_cop()
            #break

    def bootstraping(self, resample_time, confidence_level):
        sample_list = []
        #print nsize
        for i in range(resample_time):
            boot_list = []
            nsize = len(self.nlinks)
            if nsize>0:
                for j in range(nsize):
                    k = randint(0,nsize-1)
                    this_nlink = self.nlinks[k]
                    if not (this_nlink.cop is None):
                        boot_list.append(this_nlink.cop)
                    else:
                        boot_list.append(0)
                nboot = sum(boot_list) / float(len(boot_list))
                sample_list.append(nboot)
            else:
                nboot = None
        """
        cv = 0
        if confidence_level == 0.80:
            cv = 1.28
        elif confidence_level == 0.85:
            cv = 1.44
        elif confidence_level == 0.90:
            cv = 1.64
        elif confidence_level == 0.95:
            cv = 1.96
        elif confidence_level == 0.99:
            cv = 2.566
        """
        p = 1.-(1.-float(confidence_level))/2.
        cv = norm.ppf(p)
        if len(sample_list)>0:
            cop_mean = sum(sample_list)/float(len(sample_list))
            cop_std = nstd(sample_list)
            critical_value = cop_mean + cv*cop_std
        else:
            critical_value = None

        self.critical_value = critical_value
        return critical_value

    def skip_bootstraping(self, critical_value):
        self.critical_value = critical_value
        return critical_value

    def finalize_nlinks(self):
        ### filtering the nlinks that is lower than critical value, save the "cluster link" to final nlink set
        if self.critical_value is None:
            print("error: critical value is None")
            return
        #check = 0
        for nlin in self.nlinks:
            if not (nlin.cop is None):
                #check=check+1
                if nlin.cop >= self.critical_value:
                    self.nlinks_final.append(nlin)
        #print 'check: ', str(check)
        for anode in self.nodes:
            for nl in anode.neighbors:
                if not (nl.cop is None):
                    if nl.cop >= self.critical_value:
                        anode.add_finalnlink(nl)

    def finalize_slinks(self):
        # filtering slink, save to final slink set
        #print 'final nlinks count: ', str(len(self.nlinks_final))
        s_links_final = []
        origin_set = []
        for anode in self.nodes:
            # for those node with no cluster link neighbor
            # get the most probable shifting link that might happen
            if len(anode.neighbors_final)<=0:
                s_incoming = anode.incoming
                if len(s_incoming)>0:
                    s_poss = [x.ori_possibility for x in s_incoming]
                    M_inc = None
                    M_pos = 0
                    temp_dict = {}
                    for sl, sp in zip(s_incoming, s_poss):
                        if sp not in temp_dict:
                            temp_dict[sp] = []
                        temp_dict[sp].append(sl)
                        #if sp > M_pos:
                        #    M_inc = sl
                        #    M_pos = sp
                    M_pos = max(temp_dict.keys())
                    M_inc = temp_dict[M_pos]
                    s_links_final.extend(M_inc)
                else:
                    origin_set.append(anode)
            else:
                # for those with cluster link
                # get the highest common origin node
                # save the slinks from that node to the both end of the nlink
                n_links = anode.neighbors_final
                for nl in n_links:
                    if nl.max_cop is not None:
                        s_links_final.extend(nl.link1_max)
                        s_links_final.extend(nl.link2_max)
        #s_links_final2 = [x for x in s_links_final if x is not None]
        self.slinks_final = list(set(s_links_final))
