# -*- coding: utf-8 -*-

import os
#from datetime import date,timedelta ## remove the date from output so nvm

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
from shapely.geometry.polygon import LinearRing # get ellipse

def to_shpfile(oo, filename_prefix=None, crs=None, vno=16, dev_scale=1.5):
    # oo == Output_Objects
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    to_nodes(oo, filename_prefix, crs)
    to_final_slinks(oo, filename_prefix, crs)
    to_final_nlinks(oo, filename_prefix, crs)
    to_eclipse(oo, filename_prefix, crs, vno, dev_scale)
    to_proglinks(oo, filename_prefix, crs)

def to_nodes(oo, filename_prefix, crs):
    outputfilename = filename_prefix+"_nodes.shp"
    ndf = oo.node_df
    xx = ndf.xx.tolist()
    yy = ndf.yy.tolist()
    geom = []
    for a,b in zip(xx,yy):
        p = Point(a,b)
        geom.append(p)
    node_gdf = gpd.GeoDataFrame(ndf, crs=crs, geometry=geom)
    node_gdf.to_file(filename=outputfilename, driver='ESRI Shapefile')

def to_eclipse(oo, filename_prefix, crs, vno, dev_scale):
    # start working
    outputfilename = filename_prefix+"_ellipse.shp"
    ndf = oo.node_df
    cdf = oo.cluster_df
    cdf.sort_values(by='chain_id', inplace=True)

    cids2 = cdf.chain_id.tolist()
    clids = cdf.cluster_id.tolist()
    #print cdf.head()
    #cltime = cdf.time_start.tolist()
    clx = cdf.xx.tolist()
    cly = cdf.yy.tolist()
    #basetime = date(y,4,1)
    cluster_ellipse = []
    #cluster_date = []
    for cl,mx,my in zip(clids,clx,cly):
        temp_df = ndf[ndf.cluster_id==cl]
        temp_x = temp_df.xx.tolist()
        temp_y = temp_df.yy.tolist()
        ellipse = get_ellipse(temp_x, temp_y, vno, dev_scale)
        poly = Polygon(ellipse)
        #the_date = basetime + timedelta(int(tt))
        #the_date2 = the_date.strftime('%Y/%m/%d')
        cluster_ellipse.append(poly)
        #cluster_date.append(the_date2)
    beh = cdf.behaviors.tolist()
    cdf['behaviors'] = [ str(b) for b in beh ]
    new_df = cdf.rename(columns={'cluster_size':'cls_size', 'time_median':'time_mdian'})
    #new_df['date'] = cluster_date

    geo_df = gpd.GeoDataFrame(new_df, crs=crs, geometry=cluster_ellipse)
    #print geo_df.head()
    geo_df.to_file(filename=outputfilename, driver='ESRI Shapefile')

def get_ellipse(xlist, ylist, vno, dev_scale):
    # vno is the number of vertices of the ellipse
    # dev_scale is the standard deviation scale
    size = len(xlist)
    xx = sum(xlist)/float(size)
    yy = sum(ylist)/float(size)

    xwave = [(a-xx) for a in xlist]
    ywave = [(b-yy) for b in ylist]
    xlist2 = [a**2 for a in xwave]
    ylist2 = [b**2 for a in ywave]
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
    #temp.append(temp[0])
    #print len(temp)
    return circle



def to_proglinks(oo, filename_prefix, crs):
    outputfilename = filename_prefix+'_proglinks.shp'
    edf = oo.progress_df
    if not (edf.iloc[0]['x0']=='-'):
        geom = []
        for i in range(len(edf)):
            row = edf.iloc[i]
            x0 = row['x0']
            x1 = row['x1']
            y0 = row['y0']
            y1 = row['y1']
            line = LineString(((x0,y0),(x1,y1)))
            geom.append(line)

        #crs = '+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +units=m +no_defs'

        geo_df = gpd.GeoDataFrame(edf, crs=crs, geometry=geom)
        #print geo_df.head()
        geo_df.to_file(filename=outputfilename, driver='ESRI Shapefile')
    else:
        pass


def to_final_slinks(oo, filename_prefix, crs):
    outputfilename = filename_prefix+'_slinks_final.shp'
    edf = oo.final_slinks_df
    if not (edf.iloc[0]['ooid']=='-'):
        geom = []
        for i in range(len(edf)):
            row = edf.iloc[i]
            x0 = row['oxcor']
            x1 = row['dxcor']
            y0 = row['oycor']
            y1 = row['dycor']
            line = LineString(((x0,y0),(x1,y1)))
            geom.append(line)
        geo_df = gpd.GeoDataFrame(edf, crs=crs, geometry=geom)
        #print geo_df.head()
        geo_df.to_file(filename=outputfilename, driver='ESRI Shapefile')
    else:
        pass


def to_final_nlinks(oo, filename_prefix, crs):
    outputfilename = filename_prefix+'_cluster_pairs.shp'
    edf = oo.final_nlinks_df
    if not (edf.iloc[0]['n1_id']=='-'):
        geom = []
        for i in range(len(edf)):
            row = edf.iloc[i]
            x0 = row['n1x']
            x1 = row['n2x']
            y0 = row['n1y']
            y1 = row['n2y']
            line = LineString(((x0,y0),(x1,y1)))
            geom.append(line)
        geo_df = gpd.GeoDataFrame(edf, crs=crs, geometry=geom)
        #print geo_df.head()
        geo_df.to_file(filename=outputfilename, driver='ESRI Shapefile')
    else:
        pass
