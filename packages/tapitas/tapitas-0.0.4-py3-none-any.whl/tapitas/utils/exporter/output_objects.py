# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
from shapely.geometry.polygon import LinearRing # get ellipse

def get_dist(pt0, pt1):
    x0, y0 = pt0
    x1, y1 = pt1
    d = np.sqrt((x1-x0)**2+(y1-y0)**2)
    return d

class Output_Objects(object):
    def __init__(self, parent):
        self.parent = parent
        self.node_df = self.get_node_df()
        self.cluster_df = self.get_cluster_df()
        self.progress_df = self.get_progress_df()
        self.summary_df = self.get_summary_df()
        self.final_slinks_df = self.get_final_slinks_df()
        self.final_nlinks_df = self.get_final_nlinks_df()

    def get_summary_df(self):
        ## working 11/04
        nodes = self.parent.sg.nodes
        nlinks = self.parent.sg.nlinks
        slinks = self.parent.sg.slinks
        final_slinks = self.parent.sg.slinks_final
        cluster_pairs = self.parent.sg.nlinks_final
        clusters = self.parent.pg.clusters
        lines = self.parent.pg.progress
        cv = self.parent.critical_value
        dic = dict(
            nodes=len(nodes),
            npair=len(nlinks),
            slink=len(slinks),
            final_cpair=len(cluster_pairs),
            final_slink=len(final_slinks),
            clusterno=len(clusters),
            progressno=len(lines),
            critical_value=cv)
        df_summary = pd.DataFrame.from_dict(dict(attribute=dic))
        return df_summary

    def get_node_df(self):
        nodes = self.parent.sg.nodes
        ii = []#[c.idd for c in nodes]
        xx = []#[c.xcor for c in nodes]
        yy = []#[c.ycor for c in nodes]
        tt = []#[c.time for c in nodes]
        cl = []#[c.cluster_id for c in nodes]
        ch = []#[c.chain_id for c in nodes]
        nc = []#[len(c.incoming) for c in nodes]
        ou = []#[len(c.outgoing) for c in nodes]
        ne = []#[len(c.neighbors) for c in nodes]
        for n in nodes:
            ii.append(n.idd)
            xx.append(n.xcor)
            yy.append(n.ycor)
            tt.append(n.time)
            cl.append(n.cluster_id)
            ch.append(n.chain_id)
            nc.append(len(n.incoming))
            ou.append(len(n.outgoing))
            ne.append(len(n.neighbors))

        df_nodes = pd.DataFrame.from_dict({'node_id':ii, 'xx':xx, 'yy':yy, 'time':tt, 'subcluster_id':cl, 'chain_id':ch, 'in_size':nc, 'out_size':ou, 'neig_size':ne})
        df_nodes = df_nodes[['node_id', 'xx', 'yy', 'time', 'subcluster_id', 'chain_id', 'in_size', 'out_size', 'neig_size']]
        #self.node_df = df_nodes
        return df_nodes

    def get_cluster_df(self):
        clusters = self.parent.pg.clusters
        xx = []#[c.xcor for c in clusters]
        yy = []#[c.ycor for c in clusters]
        ss = []#[c.cluster_size for c in clusters]
        tt = []#[c.time_median for c in clusters]
        t0 = []#[c.time_start for c in clusters]
        t1 = []#[c.time_stop for c in clusters]
        cl = []#[c.cluster_id for c in clusters]
        ch = []#[c.chain_id for c in clusters]
        bvr = []
        ins = []
        ous = []
        for c in clusters:
            xx.append(c.xcor)
            yy.append(c.ycor)
            ss.append(c.cluster_size)
            tt.append(c.time_median)
            t0.append(c.time_start)
            t1.append(c.time_stop)
            cl.append(c.cluster_id)
            ch.append(c.chain_id)
            bvr.append(c.behaviors)
            ins.append(len(c.incomings))
            ous.append(len(c.outgoings))
        df_clusters = pd.DataFrame.from_dict({'subcluster_id':cl, 'chain_id':ch, 'xx':xx, 'yy':yy, 'cluster_size':ss, 'time_median':tt, 'time_start':t0, 'time_stop':t1, 'behaviors':bvr, 'in_count':ins, 'out_count':ous})
        df_clusters = df_clusters[['subcluster_id', 'chain_id', 'xx', 'yy', 'cluster_size', 'time_median', 'time_start', 'time_stop', 'behaviors', 'in_count', 'out_count']]
        #self.cluster_df = df_clusters
        return df_clusters

    def get_progress_df(self):
        #progress = self.pg.progress
        lines = self.parent.pg.progress
        ii = 0
        lines_dict = {}
        for line in lines:
            i0 = line.origin.cluster_id
            i1 = line.destination.cluster_id
            s0 = line.origin.cluster_size
            s1 = line.destination.cluster_size
            x0 = line.origin.xcor
            x1 = line.destination.xcor
            y0 = line.origin.ycor
            y1 = line.destination.ycor
            z0 = line.origin.time_start
            z1 = line.destination.time_stop
            clid = line.destination.cluster_id
            chid = line.destination.chain_id
            op = line.ori_pos
            no_SL = line.no_slink
            dist = get_dist((x0,y0),(x1,y1))
            lag = z1 - z0
            lines_dict[ii] = {'id0':i0, 'id1':i1, 'clid':clid, 'chid':chid, 'size0':s0, 'size1':s1, 'x0':x0, 'x1':x1, 'y0':y0, 'y1':y1, 't0':z0, 't1':z1, 'op':op, 'no_SL':no_SL, 'distance':dist, 'timelag':lag}
            ii=ii+1
        if len(lines)<=0:
            lines_dict[ii] = {'id0':'-', 'id1':'-', 'clid':'-', 'chid':'-', 'size0':'-', 'size1':'-', 'x0':'-', 'x1':'-', 'y0':'-', 'y1':'-',
            't0':'-',  't1':'-',  'op':'-', 'no_SL':'-', 'distance':'-', 'timelag':'-'}
        df_progress = pd.DataFrame.from_dict(lines_dict, orient='index')
        df_progress = df_progress[['id0','id1','clid','chid','size0','size1','x0','x1','y0','y1','t0','t1','op','no_SL', 'distance','timelag']]
        #self.progress_df = df_progress
        return df_progress

    def get_final_slinks_df(self):
        final_slinks = self.parent.sg.slinks_final
        final_dict = {}
        i = 0
        if len(final_slinks)>0:
            for sl in final_slinks:
                oo = sl.origin
                dd = sl.destination
                sldic = dict(
                    ooid = oo.idd,
                    ddid = dd.idd,
                    srisk = sl.spatial_risk,
                    trisk = sl.temporal_risk,
                    crisk = sl.combine_risk,
                    opossi = sl.ori_possibility,
                    oxcor = oo.xcor,
                    oycor = oo.ycor,
                    otime = oo.time,
                    dxcor = dd.xcor,
                    dycor = dd.ycor,
                    dtime = dd.time,
                    clid = dd.cluster_id,
                    chid = dd.chain_id,
                    distance = get_dist((oo.xcor,oo.ycor),(dd.xcor,dd.ycor)),
                    timelag = dd.time - oo.time,
                )
                final_dict[i] = sldic
                i+=1
        else:
            sldic = dict(
                ooid = '-',
                ddid = '-',
                srisk = '-',
                trisk = '-',
                crisk = '-',
                opossi = '-',
                oxcor = '-',
                oycor = '-',
                otime = '-',
                dxcor = '-',
                dycor = '-',
                dtime = '-',
                clid = '-',
                chid = '-',
                distance = '-',
                timelag = '-',
            )
            final_dict[i] = sldic
        f_sls = pd.DataFrame.from_dict(final_dict, orient='index')
        f_sls = f_sls[['ooid','ddid','clid','chid','srisk','trisk','crisk','opossi','oxcor','oycor','otime','dxcor','dycor','dtime', 'distance', 'timelag']]
        return f_sls

    def get_final_nlinks_df(self):
        cluster_pairs = self.parent.sg.nlinks_final
        final_dict = {}
        i = 0
        if len(cluster_pairs)>0:
            for cp in cluster_pairs:
                n1 = cp.one
                n2 = cp.two
                cpdic = dict(
                    n1_id = n1.idd,
                    n2_id = n2.idd,
                    clid = n1.cluster_id,
                    chid = n1.chain_id,
                    max_cop = cp.max_cop,
                    n1x = n1.xcor,
                    n1y = n1.ycor,
                    n2x = n2.xcor,
                    n2y = n2.ycor,
                    n1t = n1.time,
                    n2t = n2.time,
                    distance = get_dist((n1.xcor,n1.ycor),(n2.xcor,n2.ycor)),
                    timelag = n2.time - n1.time,
                )
                final_dict[i] = cpdic
                i+=1
        else:
            cpdic = dict(
                n1_id = '-',
                n2_id = '-',
                clid = '-',
                chid = '-',
                max_cop = '-',
                n1x = '-',
                n1y = '-',
                n2x = '-',
                n2y = '-',
                n1t = '-',
                n2t = '-',
                distance = '-',
                timelag = '-',
            )
            final_dict[i] = cpdic
        f_nps = pd.DataFrame.from_dict(final_dict, orient='index')
        f_nps = f_nps[['n1_id', 'n2_id', 'clid', 'chid', 'max_cop','n1x','n1y','n2x','n2y', 'n1t', 'n2t', 'distance', 'timelag']]
        return f_nps

    def get_node_gdf(self):
        ndf = self.get_node_df()
        xx = ndf.xx.tolist()
        yy = ndf.yy.tolist()
        geom = []
        for a,b in zip(xx,yy):
            p = Point(a,b)
            geom.append(p)
        geo_df = gpd.GeoDataFrame(ndf, crs=self.parent.crs, geometry=geom)
        return geo_df

    def get_cluster_gdf(self, vno=16, dev_scale=1.5):
        ndf = self.get_node_df()
        cdf = self.get_cluster_df()
        cdf.sort_values(by='chain_id', inplace=True)
        cids2 = cdf.chain_id.tolist()
        clids = cdf.cluster_id.tolist()
        cluster_ellipse = []
        cluster_area = []
        for cl in clids:
            temp_df = ndf[ndf.cluster_id==cl]
            temp_x = temp_df.xx.tolist()
            temp_y = temp_df.yy.tolist()
            ellipse = self.__get_ellipse(temp_x, temp_y, vno, dev_scale)
            poly = Polygon(ellipse)
            cluster_ellipse.append(poly)
            cluster_area.append(poly.area)
        beh = cdf.behaviors.tolist()
        cdf['behaviors'] = [ str(b) for b in beh ]
        new_df = cdf.rename(columns={'cluster_size':'cls_size', 'time_median':'time_mdian'})
        geo_df = gpd.GeoDataFrame(new_df, crs=self.parent.crs, geometry=cluster_ellipse)
        geo_df['cls_area'] = cluster_area
        return geo_df

    def __get_ellipse(self, xlist, ylist, vno, dev_scale):
        # vno is the number of vertices of the ellipse
        # dev_scale is the standard deviation scale
        size = len(xlist)
        xx = sum(xlist)/float(size)
        yy = sum(ylist)/float(size)
        xwave = [(a-xx) for a in xlist]
        ywave = [(b-yy) for b in ylist]
        xlist2 = [a**2 for a in xwave]
        ylist2 = [b**2 for b in ywave]
        xylist2 = [(a)*(b) for a,b in zip(xwave,ywave)]
        sumx2 = sum(xlist2)
        sumy2 = sum(ylist2)
        sumxy2 = sum(xylist2)
        A = sumx2 - sumy2
        B = np.sqrt((sumx2 - sumy2)**2 + 4*(sumxy2)**2)
        C = 2*sumxy2
        #circle = []
        if C!=0:
            theta = np.arctan((A+B)/C)
            cxlist = [a*np.cos(theta) for a in xwave]
            sylist = [b*np.sin(theta) for b in ywave]
            sxlist = [a*np.sin(theta) for a in xwave]
            cylist = [b*np.cos(theta) for b in ywave]
            partx = [(a-b)**2 for a,b in zip(cxlist,sylist)]
            party = [(a-b)**2 for a,b in zip(sxlist,cylist)]
            devx = np.sqrt(sum(partx)/float(size))*dev_scale
            devy = np.sqrt(sum(party)/float(size))*dev_scale
            #print devx

            n = 64
            t = np.linspace(0, 2*np.pi, n, endpoint=False)
            st = np.sin(t)
            ct = np.cos(t)
            sa = np.sin(theta)
            ca = np.cos(theta)
            p = np.empty((n, 2))
            p[:, 0] = xx + devx * ca * ct - devy * sa * st
            p[:, 1] = yy + devx * sa * ct + devy * ca * st
            circle = list(LinearRing(p).coords)
            #circle = LinearRing(p)
        else:
            dev = (np.sqrt(sum(xlist2)/float(size)) + 1)*dev_scale
            #print dev
            theta = 1
            n = 64
            t = np.linspace(0, 2*np.pi, n, endpoint=False)
            st = np.sin(t)
            ct = np.cos(t)
            sa = np.sin(theta)
            ca = np.cos(theta)
            p = np.empty((n, 2))
            p[:, 0] = xx + dev * ca * ct - dev * sa * st
            p[:, 1] = yy + dev * sa * ct + dev * ca * st
            circle = list(LinearRing(p).coords)
            #circle = LinearRing(p)
        #print circle
        skip = int(np.floor(len(circle[:-1])/float(vno-1)))
        temp = []
        #print vno
        for i in range(vno):
            j = skip*i
            #print j
            temp.append(circle[j])
        return circle

    def get_progress_gdf(self):
        #outputfilename = filename_prefix+'_proglinks.shp'
        edf = self.get_progress_df()
        if not (edf.iloc[0]['x0']=='-'):
            geom = []
            #dist = []
            #lags = []
            for i in range(len(edf)):
                row = edf.iloc[i]
                x0 = row['x0']
                x1 = row['x1']
                y0 = row['y0']
                y1 = row['y1']
                #t0 = row['t0']
                #t1 = row['t1']
                #lags.append(float(t1)-float(t0))
                #dist.append(get_dist((x0,y0),(x1,y1)))
                line = LineString(((x0,y0),(x1,y1)))
                geom.append(line)
            #crs = '+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +units=m +no_defs'
            #edf['time_lag'] = lags
            #edf['distance'] = dist
            geo_df = gpd.GeoDataFrame(edf, crs=self.parent.crs, geometry=geom)
            #print geo_df.head()
            return geo_df
        else:
            pass

    def get_final_slinks_gdf(self):
        #outputfilename = filename_prefix+'_slinks_final.shp'
        edf = self.get_final_slinks_df()
        if not (edf.iloc[0]['ooid']=='-'):
            geom = []
            #dist = []
            #lags = []
            for i in range(len(edf)):
                row = edf.iloc[i]
                x0 = row['oxcor']
                x1 = row['dxcor']
                y0 = row['oycor']
                y1 = row['dycor']
                #t0 = row['otime']
                #t1 = row['dtime']
                #lags.append(float(t1)-float(t0))
                #dist.append(get_dist((x0,y0),(x1,y1)))
                line = LineString(((x0,y0),(x1,y1)))
                geom.append(line)
            #edf['time_lag'] = lags
            #edf['distance'] = dist
            geo_df = gpd.GeoDataFrame(edf, crs=self.parent.crs, geometry=geom)
            #print geo_df.head()
            return geo_df
        else:
            pass

    def get_final_nlinks_gdf(self):
        #outputfilename = filename_prefix+'_cluster_pairs.shp'
        edf = self.get_final_nlinks_df()
        if not (edf.iloc[0]['n1_id']=='-'):
            geom = []
            #dist = []
            #lags = []
            for i in range(len(edf)):
                row = edf.iloc[i]
                x0 = row['n1x']
                x1 = row['n2x']
                y0 = row['n1y']
                y1 = row['n2y']
                #t0 = row['n1t']
                #t1 = row['n2t']
                #lags.append(float(t1)-float(t0))
                #dist.append(get_dist((x0,y0),(x1,y1)))
                line = LineString(((x0,y0),(x1,y1)))
                geom.append(line)
            #edf['time_lag'] = lags
            #edf['distance'] = dist
            geo_df = gpd.GeoDataFrame(edf, crs=self.parent.crs, geometry=geom)
            #print geo_df.head()
            return geo_df
        else:
            pass
