# -*- coding: utf-8 -*-

### svg output functions are still in experiment

import os
from shutil import copyfile
import numpy as np
from shapely.geometry.polygon import LinearRing
from shapely.geometry import Point

"""
from vmapper import make_svg as svg_making
from vmapper import svg
from vmapper import fromShpfile
"""

def to_svgs(oo, filename_prefix=None, pgraph=None, bgfile=None, bbox=None, scale=30., widthscale=1.):
    pass
"""
def to_svgs(oo, filename_prefix=None, pgraph=None, bgfile=None, bbox=None, scale=30., widthscale=1.):
    to_svgs_all(oo, filename_prefix, pgraph, bgfile, bbox, scale, widthscale)

def to_svgs_all(oo, filename_prefix=None, pgraph=None, bgfile=None, bbox=None, scale=30., widthscale=1.):
    # oo == Output_Objects

    to_svg_event(oo, bgfile, filename_prefix, title="The event of points", bbox=bbox, scale=scale)
    to_svg_animate(oo, pgraph, bgfile, filename_prefix, title="The progression of subcluster", bbox=bbox, scale=scale)
    to_svg_static(oo, pgraph, bgfile, filename_prefix, title="The static view of subcluster", bbox=bbox, shape='ellipse', widthscale=widthscale)
    to_svg_morph(oo, pgraph, bgfile, filename_prefix, title="The progression of subcluster", bbox=bbox, shape='ellipse', scale=scale)

def to_svg_event(oo, bgfile, filename_prefix, title="The event of points", bbox=None, scale=30.):
    if bbox is None:
        bbox = [None, None, None, None]
    xmin,ymin,xmax,ymax = bbox
    event_to_animate_svg(oo, bgfile, filename_prefix, title=title, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, scale=scale)

def to_svg_animate(oo, pgraph, bgfile, filename_prefix, title="The progression of subcluster", bbox=None, scale=30.):
    if bbox is None:
        bbox = [None, None, None, None]
    xmin,ymin,xmax,ymax = bbox
    pg_to_animate_svg(oo, pgraph, bgfile, filename_prefix, title=title, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, scale=scale)

def to_svg_static(oo, pgraph, bgfile, filename_prefix, title="The static view of subcluster", bbox=None, shape='ellipse', widthscale=1.):
    if bbox is None:
        bbox = [None, None, None, None]
    xmin,ymin,xmax,ymax = bbox
    pg_to_static_svg(oo, pgraph, bgfile, filename_prefix, title=title, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, shape=shape, widthscale=widthscale)

def to_svg_morph(oo, pgraph, bgfile, filename_prefix, title="The progression of subcluster", bbox=None, shape='ellipse', scale=30.):
    if bbox is None:
        bbox = [None, None, None, None]
    xmin,ymin,xmax,ymax = bbox
    pg_to_morph_svg(oo, pgraph, bgfile, filename_prefix, title=title, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, shape=shape, scale=scale)

def _get_background(bgf, layername=None, labelby=None,
    dcolor=(5,5,5), dopacity=0.7, dscolor=(255,255,255), dswidth=5, widthscale=1.):
    if not(bgf is None):
        ss = fromShpfile.fromShp(bgf)
        shps = ss.shapedict
        bbox = ss.bbox()
        layer = svg.Layer()
        layer.addtoLayer(svg.initLayer(key=layername, dcolor=dcolor, dopacity=dopacity,
            dscolor=dscolor, dswidth=dswidth*widthscale))
        for shp_key, shp_val in shps.iteritems():
            if labelby is not None:
                label = labels[shp_key]
            else:
                label = shp_key
            layer.addtoLayer(svg.MultiPolygons(key=shp_key, label=label, multiPolygons=shp_val))
        layer.addtoLayer(svg.closeLayer())
        return (layer.items, bbox)
    else:
        return None

def _get_circle(node_list, vno=16, scale=30.):
    size = len(node_list)
    xlist = [a.xcor for a in node_list]
    ylist = [a.ycor for a in node_list]
    xx = sum(xlist)/float(size)
    yy = sum(ylist)/float(size)
    circle = list(Point(xx,yy).buffer(size*scale).exterior.coords)
    temp = []
    skip = int(np.floor(len(circle[:-1])/float(vno-1)))
    for i in range(vno):
        j = skip*i
        temp.append(circle[j])
    temp.append(temp[0])
    #print len(temp)
    return temp

def _get_ellipse(node_list, vno=16, dev_scale=1.5):
    size = len(node_list)
    xlist = [a.xcor for a in node_list]
    ylist = [a.ycor for a in node_list]
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
    circle = []
    if C != 0:
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

    #print circle
    skip = int(np.floor(len(circle[:-1])/float(vno-1)))
    temp = []
    #print vno
    for i in range(vno):
        j = skip*i
        #print j
        temp.append(circle[j])
    temp.append(temp[0])
    #print len(temp)
    return temp

def event_to_animate_svg(oo, bgfile, filename_prefix=None, title="The event points", xmin=None, ymin=None, xmax=None, ymax=None, scale=30.):
    ###
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    svgpanfile = dirname+"/SVGPan.js"
    if not os.path.exists(svgpanfile):
        svgpanfile_ori = os.path.dirname(__file__)+"/vmapper/SVGPan.js"
        copyfile(svgpanfile_ori, svgpanfile)

    filename = filename_prefix+'_event_map.svg'
    ###

    node_df = oo.node_df

    iis = node_df.node_id.tolist()
    xxs = node_df.xx.tolist()
    yys = node_df.yy.tolist()
    if xmin is None:
        xmin = min(xxs)
        ymin = min(yys)
        xmax = max(xxs)
        ymax = max(yys)
    boxwidth = xmax-xmin
    boxheight = ymax-ymin
    buffer_x = boxwidth*0.025
    buffer_y = boxheight*0.025
    tts = node_df.time.tolist()
    tt0 = min(tts)-1

    param_dict = {"title":title, "title_in_page":title, "xmin":xmin-buffer_x, "ymin":ymin-buffer_y, "boxwidth":boxwidth+2*buffer_x, "boxheight":boxheight+2*buffer_y, "bgcolor":"#000000", "textcolor":"#FFFFFF"}

    scene = svg_making.simple_scene(param_dict)
    bg,bbox = _get_background(bgf=bgfile, layername='background')
    if not(bg is None):
        scene.add_simpleLayer(bg)
        x1, y1, x2, y2 = bbox
        bw = x2-x1
        bh = y2-y1
        bx = bw*0.025
        by = bh*0.025
        scene.update_param({'xmin':x1-bx,'boxwidth':bw+2*bx,'ymin':y1-by,'boxheight':bh+2*by})

    for ii,xx,yy,tt in zip(iis,xxs,yys,tts):
        t0 = tt - tt0
        t1 = t0
        t2 = t1 + 1
        size = 1
        item = svg.Appear_Circle(center=(xx,yy), radius=size*scale, color=(255,0,0), idd=ii, t0=t0, t1=t1, t2=t2)
        scene.add_simpleLayer([item])
    outputText = scene.render()
    f = open(filename, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()

def pg_to_animate_svg(oo, pgraph, bgfile, filename_prefix=None, title="The progression of subcluster", xmin=None, ymin=None, xmax=None, ymax=None, scale=30.):
    ###
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    svgpanfile = dirname+"/SVGPan.js"
    if not os.path.exists(svgpanfile):
        svgpanfile_ori = os.path.dirname(__file__)+"/vmapper/SVGPan.js"
        copyfile(svgpanfile_ori, svgpanfile)

    filename = filename_prefix+'_prog_map.svg'
    ###

    node_df = oo.node_df
    xxs = node_df.xx.tolist()
    yys = node_df.yy.tolist()
    if xmin is None:
        xmin = min(xxs)
        ymin = min(yys)
        xmax = max(xxs)
        ymax = max(yys)
    boxwidth = xmax-xmin
    boxheight = ymax-ymin
    buffer_x = boxwidth*0.025
    buffer_y = boxheight*0.025
    tts = node_df.time.tolist()
    tt0 = min(tts)-1

    param_dict = {"title":title, "title_in_page":title, "xmin":xmin-buffer_x, "ymin":ymin-buffer_y, "boxwidth":boxwidth+2*buffer_x, "boxheight":boxheight+2*buffer_y, "bgcolor":"#000000", "textcolor":"#FFFFFF"}

    scene = svg_making.simple_scene(param_dict)
    bg,bbox = _get_background(bgf=bgfile, layername='background')
    if not(bg is None):
        scene.add_simpleLayer(bg)
        x1, y1, x2, y2 = bbox
        bw = x2-x1
        bh = y2-y1
        bx = bw*0.025
        by = bh*0.025
        scene.update_param({'xmin':x1-bx,'boxwidth':bw+2*bx,'ymin':y1-by,'boxheight':bh+2*by})

    for chain in pgraph.isolated_clusters:
        for cluster in chain:
            idd = cluster.cluster_id
            xx = cluster.xcor
            yy = cluster.ycor
            t0 = cluster.time_start - tt0
            t1 = cluster.time_median - tt0
            t2 = cluster.time_stop - tt0
            size = cluster.cluster_size

            item = svg.Appear_Circle(center=(xx,yy), radius=size*scale, color=(255,0,0), idd=idd, t0=t0, t1=t1, t2=t2)

            scene.add_simpleLayer([item])

    for chain in pgraph.long_chains:
        for cluster in chain:
            idd = cluster.cluster_id
            xx = cluster.xcor
            yy = cluster.ycor
            t0 = cluster.time_start - tt0
            t1 = cluster.time_median - tt0
            t2 = cluster.time_stop - tt0
            size = cluster.cluster_size

            item = svg.Appear_Circle(center=(xx,yy), radius=size*scale, color=(255,0,0), idd=idd, t0=t0, t1=t1, t2=t2)

            scene.add_simpleLayer([item])

    for link in pgraph.pg.progress:
        idda = link.origin.cluster_id
        xxa = link.origin.xcor
        yya = link.origin.ycor
        t0a = link.origin.time_start - tt0
        t1a = link.origin.time_median - tt0
        t2a = link.origin.time_stop - tt0

        iddb = link.destination.cluster_id
        xxb = link.destination.xcor
        yyb = link.destination.ycor
        t0b = link.destination.time_start - tt0
        t1b = link.destination.time_median - tt0
        t2b = link.destination.time_stop - tt0

        idd=str(idda)+'-'+str(iddb)
        start = (xxa,yya)
        end = (xxb,yyb)
        t0=t0a
        t1=t0b
        item = svg.animated_line(idd=idd, start=start, end=end, t0=t0, t1=t1)
        scene.add_simpleLayer([item])
    outputText = scene.render()
    f = open(filename, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()

def pg_to_static_svg(oo, pgraph, bgfile, filename_prefix=None, title="The static view of subcluster", xmin=None, ymin=None, xmax=None, ymax=None, shape='ellipse', widthscale=1.):
    ###
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    svgpanfile = dirname+"/SVGPan.js"
    if not os.path.exists(svgpanfile):
        svgpanfile_ori = os.path.dirname(__file__)+"/vmapper/SVGPan.js"
        copyfile(svgpanfile_ori, svgpanfile)

    filename = filename_prefix+'_prog_map_static.svg'
    ###===
    node_df = oo.node_df

    iis = node_df.node_id.tolist()
    xxs = node_df.xx.tolist()
    yys = node_df.yy.tolist()
    if xmin is None:
        xmin = min(xxs)
        ymin = min(yys)
        xmax = max(xxs)
        ymax = max(yys)
    boxwidth = xmax-xmin
    boxheight = ymax-ymin
    buffer_x = boxwidth*0.025
    buffer_y = boxheight*0.025
    tts = node_df.time.tolist()
    tt0 = min(tts)-1

    param_dict = {"title":title, "title_in_page":title, "xmin":xmin-buffer_x, "ymin":ymin-buffer_y, "boxwidth":boxwidth+2*buffer_x, "boxheight":boxheight+2*buffer_y, "bgcolor":"#000000", "textcolor":"#FFFFFF"}

    noise = []
    for anode in pgraph.sg.nodes:
        clid = anode.cluster_id
        #tt = anode.time
        if clid == -1:
            noise.append(anode)

    solo = []
    chain = []
    for ac in pgraph.pg.clusters:
        if ac.chain_id == -1:
            solo.append(ac)
        else:
            chain.append(ac)

    scene = svg_making.simple_scene(param_dict)
    bg,bbox = _get_background(bgfile, layername='background')
    if not(bg is None):
        scene.add_simpleLayer(bg)
        x1, y1, x2, y2 = bbox
        bw = x2-x1
        bh = y2-y1
        bx = bw*0.025
        by = bh*0.025
        scene.update_param({'xmin':x1-bx,'boxwidth':bw+2*bx,'ymin':y1-by,'boxheight':bh+2*by})

    for anode in noise:
        xx = anode.xcor
        yy = anode.ycor
        ii = str(anode.idd)
        tt = anode.time
        size = 1
        circle = []
        if shape=='ellipse':
            circle = _get_ellipse([anode], vno=16)
        else:
            circle = _get_circle([anode], vno=16)
        shpstr = svg.get_pathstring(vertexlist=circle)
        pid = 'noise_'+ii
        item = svg.linePath(shpstr, path_id=pid, stroke_width=8*widthscale, stroke_color=(50,50,50), fill_color=(200,200,200), stroke_opacity=1.0)
        scene.add_simpleLayer([item])

    for acluster in solo:
        xx = acluster.xcor
        yy = acluster.ycor
        tt = acluster.time_median
        size = acluster.cluster_size
        node_list = acluster.node_list
        circle = []
        if shape=='ellipse':
            circle = _get_ellipse(node_list, vno=16)
        else:
            circle = _get_circle(node_list, vno=16)
        shpstr = svg.get_pathstring(vertexlist=circle)
        pid = 'noise_'+ii
        item = svg.linePath(shpstr, path_id=pid, stroke_width=8*widthscale, stroke_color=(200,200,200), fill_color=(250,250,0), stroke_opacity=0.7)
        scene.add_simpleLayer([item])

    for link in pgraph.pg.progress:
        idda = link.origin.cluster_id
        xxa = link.origin.xcor
        yya = link.origin.ycor
        t0a = link.origin.time_start - tt0
        t1a = link.origin.time_median - tt0
        t2a = link.origin.time_stop - tt0

        iddb = link.destination.cluster_id
        xxb = link.destination.xcor
        yyb = link.destination.ycor
        t0b = link.destination.time_start - tt0
        t1b = link.destination.time_median - tt0
        t2b = link.destination.time_stop - tt0

        idd=str(idda)+'-'+str(iddb)
        start = (xxa,yya)
        end = (xxb,yyb)
        t0=t0a
        t1=t0b
        item = svg.Line(start, end, strokewidth=60*widthscale)
        scene.add_simpleLayer([item])

    for acluster in chain:
        xx = acluster.xcor
        yy = acluster.ycor
        tt = acluster.time_median
        size = acluster.cluster_size
        node_list = acluster.node_list
        circle = []
        if shape=='ellipse':
            circle = _get_ellipse(node_list, vno=16)
        else:
            circle = _get_circle(node_list, vno=16)
        shpstr = svg.get_pathstring(vertexlist=circle)
        pid = 'noise_'+ii
        item = svg.linePath(shpstr, path_id=pid, stroke_width=8*widthscale, stroke_color=(200,200,200), fill_color=(255,0,0), stroke_opacity=0.7)
        scene.add_simpleLayer([item])
    ### add legend text
    scene.add_text(svg_making.add_textbox())

    ### rendering
    outputText = scene.render()

    ### outputing
    f = open(filename, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()
    ###===

def pg_to_morph_svg(oo, pgraph, bgfile, filename_prefix=None, title="The progression of subcluster", xmin=None, ymin=None, xmax=None, ymax=None, shape='ellipse', scale=30.):
    ###
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    svgpanfile = dirname+"/SVGPan.js"
    if not os.path.exists(svgpanfile):
        svgpanfile_ori = os.path.dirname(__file__)+"/vmapper/SVGPan.js"
        copyfile(svgpanfile_ori, svgpanfile)

    filename = filename_prefix+'_morph_map.svg'
    ####


    node_df = oo.node_df

    iis = node_df.node_id.tolist()
    xxs = node_df.xx.tolist()
    yys = node_df.yy.tolist()
    if xmin is None:
        xmin = min(xxs)
        ymin = min(yys)
        xmax = max(xxs)
        ymax = max(yys)
    boxwidth = xmax-xmin
    boxheight = ymax-ymin
    buffer_x = boxwidth*0.025
    buffer_y = boxheight*0.025
    tts = node_df.time.tolist()
    tt0 = min(tts)-1

    param_dict = {"title":title, "title_in_page":title, "xmin":xmin-buffer_x, "ymin":ymin-buffer_y, "boxwidth":boxwidth+2*buffer_x, "boxheight":boxheight+2*buffer_y, "bgcolor":"#000000", "textcolor":"#FFFFFF"}

    time_noise = {}
    time_solo = {}
    time_chain = {}
    for anode in pgraph.sg.nodes:
        clid = anode.cluster_id
        tt = anode.time
        chid = anode.chain_id
        if clid == -1:
            if tt not in time_noise:
                time_noise[tt] = []
            time_noise[tt].append(anode)
        elif chid == -1:
            if clid not in time_solo:
                time_solo[clid] = {}
            if tt not in time_solo[clid]:
                time_solo[clid][tt] = []
            time_solo[clid][tt].append(anode)
        else:
            if chid not in time_chain:
                time_chain[chid] = {}
            if clid not in time_chain[chid]:
                time_chain[chid][clid] = {}
            if tt not in time_chain[chid][clid]:
                time_chain[chid][clid][tt] = []
            time_chain[chid][clid][tt].append(anode)

    ctime_noise = {}
    ctime_solo = {}
    ctime_chain = {}
    for tt, node_list in time_noise.iteritems():
        for tx in range(pgraph.T1):
            tt_delay = tt+tx
            if tt_delay not in ctime_noise:
                ctime_noise[tt_delay] = []
            ctime_noise[tt_delay].extend(node_list)

    for clid, cluster_dict in time_solo.iteritems():
        for tt, node_list in cluster_dict.iteritems():
            for tx in range(pgraph.T1):
                tt_delay = tt+tx
                if clid not in ctime_solo:
                    ctime_solo[clid] = {}
                if tt_delay not in ctime_solo[clid]:
                    ctime_solo[clid][tt_delay] = []
                ctime_solo[clid][tt_delay].extend(node_list)

    for chid, chain_dict in time_chain.iteritems():
        for clid, cluster_dict in chain_dict.iteritems():
            for tt, node_list in cluster_dict.iteritems():
                for tx in range(pgraph.T1):
                    tt_delay = tt+tx
                    if chid not in ctime_chain:
                        ctime_chain[chid] = {}
                    if clid not in ctime_chain[chid]:
                        ctime_chain[chid][clid] = {}
                    if tt_delay not in ctime_chain[chid][clid]:
                        ctime_chain[chid][clid][tt_delay] = []
                    ctime_chain[chid][clid][tt_delay].extend(node_list)

    clusters_dict = {}
    for ac in pgraph.pg.clusters:
        clid = ac.cluster_id
        clusters_dict[clid] = ac

    scene = svg_making.simple_scene(param_dict)
    bg,bbox = _get_background(bgfile, layername='background')
    if not(bg is None):
        scene.add_simpleLayer(bg)
        x1, y1, x2, y2 = bbox
        bw = x2-x1
        bh = y2-y1
        bx = bw*0.025
        by = bh*0.025
        scene.update_param({'xmin':x1-bx,'boxwidth':bw+2*bx,'ymin':y1-by,'boxheight':bh+2*by})

    for tt,node_list in ctime_noise.iteritems():
        for anode in node_list:
            xx = anode.xcor
            yy = anode.ycor
            ii = 'n_'+str(anode.idd)
            t0 = tt - tt0
            t1 = t0
            t2 = t1 + 1
            size = 1
            item = svg.Appear_Circle(center=(xx,yy), radius=size*scale, color=(200,200,200), idd=ii, t0=t0, t1=t1, t2=t2)
            scene.add_simpleLayer([item])


    temp_solo = {}
    for clid, ttcluster_dict in ctime_solo.iteritems():
        #this_cluster = clusters_dict[clid]
        if clid not in temp_solo:
            temp_solo[clid] = {}
        for tt, node_list in ttcluster_dict.iteritems():
            circle = []
            if shape=='ellipse':
                circle = _get_ellipse(node_list, vno=16)
            else:
                circle = _get_circle(node_list, vno=16)
            tt2 = tt - tt0
            temp_solo[clid][tt2] = circle
        temp_t = sorted(temp_solo[clid].keys())
        tot = max(temp_t)-min(temp_t)
        mint = min(temp_t)
        initv = temp_solo[clid][mint]
        initss = svg.get_pathstring(vertexlist=initv)
        ii = 'cl_'+str(clid)
        item = svg.Morphing_Shapes(idd=ii, init_str=initss, begin=mint, total_time=tot, fading_duration=1, color=(250,250,0))
        for i in temp_t:
            #if i!=mint:
            t0 = i-mint
            tx = t0/float(tot)
            this_c = temp_solo[clid][i]
            ss = svg.get_pathstring(vertexlist=this_c)
            item.add_shape(vertexstr=ss, tt=tx)
        scene.add_simpleLayer([item])

    temp_chain = {}
    for chid, ttchain_dict in ctime_chain.iteritems():
        for clid, ttcluster_dict in ttchain_dict.iteritems():
            if chid not in temp_chain:
                temp_chain[chid] = {}
            if clid not in temp_chain[chid]:
                temp_chain[chid][clid] = {}
            for tt, node_list in ttcluster_dict.iteritems():
                circle = []
                if shape=='ellipse':
                    circle = _get_ellipse(node_list, vno=16)
                else:
                    circle = _get_circle(node_list, vno=16)
                tt2 = tt - tt0
                temp_chain[chid][clid][tt2] = circle
                #break
            #break
            temp_t = sorted(temp_chain[chid][clid].keys())
            tot = max(temp_t)-min(temp_t)
            mint = min(temp_t)
            initv = temp_chain[chid][clid][mint]
            initss = svg.get_pathstring(vertexlist=initv)
            ii = 'cl_'+str(clid)
            item = svg.Morphing_Shapes(idd=ii, init_str=initss, begin=mint, total_time=tot, fading_duration=1, color=(250,0,0))
            for i in temp_t:
                #if i!=mint:
                t0 = i-mint
                tx = t0/float(tot)
                this_c = temp_chain[chid][clid][i]
                ss = svg.get_pathstring(vertexlist=this_c)
                item.add_shape(vertexstr=ss, tt=tx)
            scene.add_simpleLayer([item])

    ### add legend text
    scene.add_text(svg_making.add_textbox())

    ### rendering
    outputText = scene.render()

    ### outputing
    f = open(filename, 'w')
    f.write(outputText.encode("utf-8"))
    f.close()
"""
