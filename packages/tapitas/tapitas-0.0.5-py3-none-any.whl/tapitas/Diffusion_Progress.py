# -*- coding: utf-8 -*-
#from __future__ import absolute_import

#import time

import pandas as pd
import geopandas as gpd

from .core_objs import Shift_Graph, Progression_Graph
from .utils import wqu
#import core_objs as core
#from .utils.weightedquickunion import GenericWeightedQuickUnion as wqu
#from utils.exporter import exporter as exporting

class Diffusion_Progress(object):
    def __init__(self, ptdataframe, pts_setting, s_radius, T1, T2, resample_time, confidence_level, critical_value, crs=None):
        self.T1 = T1
        self.T2 = T2
        #pts = gpd.read_file(pointfile)
        pts = ptdataframe
        self.sg = Shift_Graph()
        self.crs = crs
        #self.points = []
        ## ===============
        print('construction of shifting graph - start')
        ## ===============
        pts_setting_default = {'xcor':'xcor', 'ycor':'ycor', 'time':'time'}
        if pts_setting is None:
            pts_setting = {'xcor':'xcor', 'ycor':'ycor', 'time':'time'}
        else:
            for k,v in pts_setting_default.items():
                if not(k in pts_setting):
                    pts_setting[k] = v
        self.__get_points(pts, pts_setting)

        ## ===============
        print('construction of shifting graph - stop')
        print('making links - start')
        ## ===============
        self.__make_links(s_radius, T1, T2)

        ## ===============
        print('making links - stop')
        print('bootstraping - start')
        ## ===============

        if not(critical_value is None):
            self.critical_value = self.sg.skip_bootstraping(critical_value)
        else:
            self.critical_value = self.sg.bootstraping(resample_time, confidence_level)
        print('critical value is: ', self.critical_value)

        self.sg.finalize_nlinks() # must calculate before finalize slink
        self.sg.finalize_slinks() # must calculate after finalize nlink
        #print 'final nlinks count:', str(len(self.sg.nlinks_final))
        #print 'final slinks count:', str(len(self.sg.slinks_final))

        ## ===============
        print('bootstraping - stop')
        print('detection of subclusters - start')
        ## ===============

        self.pg = Progression_Graph()
        self.__subcluster_detection() # can run after nlinks are finalized
        self.__find_progression_links() # can run after slinks are finalized
        self.chain_list_full = None
        self.long_chains = None
        self.isolated_clusters = None
        self.__get_progression_chain()

        print('number of subcluster found:', str(len(self.pg.clusters)))

        ## component graph construction
        ## track progression
        #self.exporter = exporting.Export_Main_Result(self)

    def __get_points(self, pts, pts_setting):
        pts = pts.sort_values(by=pts_setting['time'])
        xs = []
        ys = []
        ts = pts[pts_setting['time']].tolist()
        if isinstance(pts, gpd.GeoDataFrame):
            geoms = pts.geometry.tolist()
            xs = [ p.x for p in geoms ]
            ys = [ p.y for p in geoms ]
            self.crs = pts.crs
        elif isinstance(pts, pd.DataFrame):
            xs = pts[pts_setting['xcor']].tolist()
            ys = pts[pts_setting['ycor']].tolist()
        i = 0
        for xcor,ycor,time in list(zip(xs,ys,ts)):
            #this_point = pts.iloc[i]
            #time = this_point[pts_setting['time']]
            #xcor = this_point[pts_setting['xcor']]
            #ycor = this_point[pts_setting['ycor']]
            self.sg.add_node(i, time, xcor, ycor)
            i+=1

    def __make_links(self, s_radius, T1, T2):
        self.sg.prepare(s_radius, T2)
        self.sg.find_links(s_radius, T1, T2)

    def __subcluster_detection(self):
        cluster_wqu = wqu(init_list=self.sg.nodes)
        for npair in self.sg.nlinks_final:
            cluster_wqu.union(npair.one, npair.two)
        clusters_list = cluster_wqu.get_currentcomponents(form='list')
        j = 0
        for i in range(len(clusters_list)):
            nodes = clusters_list[i]
            if len(nodes)>1:
                for anode in nodes:
                    anode.set_clusterid(j)
                self.pg.add_cluster_node(j, nodes)
                j = j + 1
            else:
                for anode in nodes:
                    anode.set_clusterid(-1)
        self.pg.finalize_clusters()

    def __find_progression_links(self):
        #clusters = self.pg.clusters
        for spair in self.sg.slinks_final:
            #if not (spair is None):
            s_ori = spair.origin.cluster_id
            s_des = spair.destination.cluster_id
            ori_possibility = spair.ori_possibility ###
            if (s_ori>=0) and (s_des>=0) and (s_ori!=s_des):
                #c1 = clusters[s_ori]
                #c2 = clusters[s_des]
                t1 = self.pg.clusters_dict[s_ori].time_start
                t2 = self.pg.clusters_dict[s_des].time_start
                if t1<t2:
                    self.pg.add_progressionlink(s_ori, s_des, ori_possibility)
        for ac in self.pg.clusters:
            ac.finalize_behaviors()

    def __get_progression_chain(self):
        chain_wqu = wqu(init_list=self.pg.clusters)
        for spair in self.pg.progress:
            chain_wqu.union(spair.origin, spair.destination)
        chain_list = chain_wqu.get_currentcomponents(form='list')
        self.chain_list_full = chain_list
        #print len(chain_list)
        sizes = []
        long_chains = []
        isol_chain = []
        j = 0
        for i in range(len(chain_list)):
            clusters = chain_list[i]
            if len(clusters) > 1:
                sizes.append(len(clusters))
                for ac in clusters:
                    ac.set_chain_id(j)
                    for anode in ac.node_list:
                        anode.set_chain_id(j)
                long_chains.append(clusters)
                j = j + 1
            else:
                for ac in clusters:
                    ac.set_chain_id(-1)
                    for anode in ac.node_list:
                        anode.set_chain_id(-1)
                isol_chain.append(clusters)
        self.long_chains = long_chains
        self.isolated_clusters = isol_chain
        #print sizes
        #print len(sizes)
