# -*- coding: utf-8 -*-

## shifting link

from numpy import exp, sqrt

class Shifting_Link():
    ## connection between nodes near to each other in space, but between a range of T1 to T2 starting from the origin node's time to destination node
    def __init__(self, node1, node2, s_radius, T1, T2):
        self.origin = node1
        self.destination = node2
        dd = self._get_distance(node1, node2)
        tt = node2.time - node1.time
        self.spatial_risk = self._get_spatial_risk(dd, s_radius)
        self.temporal_risk = self._get_temporal_risk(tt, T1, T2)
        self.combine_risk = self.spatial_risk * self.temporal_risk
        self.ori_possibility = None

    def _get_distance(self, node1, node2):
        dx = node2.xcor-node1.xcor
        dy = node2.ycor-node1.ycor
        dd = sqrt(dx**2+dy**2)
        return dd

    def _get_spatial_risk(self, spatial_distance, s_radius):
        Rs = float((1 - spatial_distance/float(s_radius))**2)
        return Rs

    def _get_temporal_risk(self, temporal_distance, T1, T2):
        #Rt = float(exp(-(temporal_distance-(T1+T2)/2.0)**2/2.0))
        Rt = float(exp(-(temporal_distance-float(T1+T2)/2.0)**2/float(T2-T1))) # modified 2017/2/10
        return Rt

    def set_ori_pos(self, arate):
        self.ori_possibility = arate
