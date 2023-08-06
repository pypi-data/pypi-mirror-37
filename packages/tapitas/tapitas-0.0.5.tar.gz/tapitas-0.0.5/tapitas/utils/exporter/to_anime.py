# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd
from descartes import PolygonPatch # for drawing base polygon

def to_anime(oo, filename_prefix=None, bg_polys=[], bbox=None):
    # oo == Output_Objects
    if filename_prefix is None:
        filename_prefix = 'temp_output/temp'

    dirname = os.path.dirname(filename_prefix)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    to_3plots(oo, filename_prefix, bg_polys, bbox)

def to_3plots(oo, filename_prefix, bg_polys, bbox):
    # animation with 3 subplots
    export_file_name = filename_prefix+"_compare_movie.mp4"
    get_anim(oo, export_file_name, bg_polys, bbox)

def get_cases(oo):
    lag_disappear = 12
    df2 = oo.node_df
    #print df2.head()
    ii = df2.node_id.tolist()
    xx = df2.xx.tolist()
    yy = df2.yy.tolist()
    tt1 = df2.time.tolist()
    tt2 = [ t+lag_disappear for t in tt1 ]
    cases_a = {}
    cases_b = {}
    cases = {}
    for a,b,c,d,e in zip(ii,xx,yy,tt1,tt2):
        cases[a] = (b,c)
        if d not in cases_a:
            cases_a[d] = []
        cases_a[d].append(a)
        if e not in cases_b:
            cases_b[e] = []
        cases_b[e].append(a)
    minx = min(xx)
    maxx = max(xx)
    miny = min(yy)
    maxy = max(yy)
    bbox = [minx,miny,maxx,maxy]
    return cases, cases_a, cases_b, bbox

def get_subclusters(oo, filename_prefix):
    #sfile = 'exports/new5/c05_y'+str(y)+'_result_clusters.csv'
    filename_prefix2 = filename_prefix.replace("_compare_movie.mp4","")
    efile = filename_prefix2+'_ellipse.shp'
    edf = None
    if os.path.exists(efile):
        edf = gpd.read_file(efile)
    else:
        import to_shpfile
        dirname = os.path.dirname(filename_prefix)
        temp_prefx = dirname+'/temp/temp'
        dirname2 = os.path.dirname(temp_prefx)
        if not os.path.isdir(dirname2):
            os.makedirs(dirname2)
        to_shpfile.to_eclipse(oo, filename_prefix=temp_prefx, crs=None, vno=16, dev_scale=1.5)
        edf = gpd.read_file(temp_prefx+'_ellipse.shp')

    ii = edf.cluster_id.tolist()
    geoms = edf.geometry.tolist()
    geom_dict = {}
    cent_dict = {}
    for k,v in zip(ii,geoms):
        geom_dict[k] = v
        a,b,c,d = v.bounds
        x = float(c - a)/2. + a
        y = float(d - b)/2. + b
        cent_dict[k] = (x,y)
        #print x,y

    t1 = edf.time_start.tolist()
    t2 = edf.time_stop.tolist()
    time_dict = { k:(a,b) for k,a,b in zip(ii,t1,t2) }
    #print edf2
    sub_a = {}
    sub_b = {}
    for k,a,b in zip(ii,t1,t2):
        if a not in sub_a:
            sub_a[a] = []
        if b not in sub_b:
            sub_b[b] = []
        sub_a[a].append(k)
        sub_b[b].append(k)
    return geom_dict, time_dict, sub_a, sub_b, cent_dict

def get_chains(oo):
    global time_dict, cent_dict
    df2 = oo.progress_df
    #print df2.head()
    i0 = df2.id0.tolist()
    i1 = df2.id1.tolist()
    x0 = []#df2.x0.tolist()
    x1 = []#df2.x1.tolist()
    y0 = []#df2.y0.tolist()
    y1 = []#df2.y1.tolist()
    t0 = []
    t1 = []
    for i in i1:
        a,b = time_dict[i]
        t0.append(a)
        t1.append(b)
        xx,yy = cent_dict[i]
        x1.append(xx)
        y1.append(yy)
    for i in i0:
        xx,yy = cent_dict[i]
        x0.append(xx)
        y0.append(yy)
    #t0 = df2.t0.tolist()
    #t1 = df2.t1.tolist()
    arrows = []
    start_arrows = {}
    stop_arrows = {}
    sets = zip(x0,x1,y0,y1,t0,t1)
    for i in range(len(sets)):
        a,b,c,d,e,f = sets[i]
        if a!='-':
            arrows.append(([a,b],[c,d]))
            if e>f:
                print(e,f)
            e = int(e)
            f = int(f)
            if e not in start_arrows:
                start_arrows[e] = []
            if f not in stop_arrows:
                stop_arrows[f] = []
            start_arrows[e].append(i)
            stop_arrows[f].append(i)
    return (arrows, start_arrows, stop_arrows)


def update(i):
    global cases, cases_a, cases_b, geom_dict, time_dict, sub_a, sub_b, cent_dict, arrows, arrows0, arrows1, time_text, ax, ax2, ax3, drawed, zup, zdown
    #global y, arrows, arrows0, arrows1, time_text, ax, ax2, ax3, current, drawed
    #this_color = colors[16]
    time_text.set_text('time: '+str(i))
    day = i

    if day in cases_a:
        for j in cases_a[day]:
            xc,yc = cases[j]
            drawed['case'][j] = ax.scatter(xc,yc, s=10, c='#f7022a', edgecolors='#f7022a', zorder=zup, alpha=0.8)

    if day in cases_b:
        for j in cases_b[day]:
            p = drawed['case'][j]
            p.remove()

            xc,yc = cases[j]
            p2 = ax.scatter(xc,yc, s=10, c='#fdc1c5', edgecolors='#fdc1c5', zorder=zdown, alpha=0.6)

    if day in sub_a:
        for j in sub_a[day]:
            gg = geom_dict[j]
            g = ax2.add_patch(PolygonPatch(gg, fc='#f7022a', lw=1.2, ec='#f7022a', alpha=0.6, zorder=zup ))
            drawed['subcluster'][j] = g

    if day in sub_b:
        for j in sub_b[day]:
            g = drawed['subcluster'][j]
            g.remove()

            gg = geom_dict[j]
            g2 = ax2.add_patch(PolygonPatch(gg, fc='#fdc1c5', lw=1.2, ec='#fdc1c5', alpha=0.5, zorder=zdown ))


    if day in arrows0:
        for j in arrows0[day]:
            #print j
            (x0,x1),(y0,y1) = arrows[j]
            drawed['arrow'][j] = ax3.arrow(x0,y0,x1-x0,y1-y0, linewidth=1.5, head_width=100., head_length=150., fc='#f7022a', ec='#f7022a', zorder=zup, alpha=0.9)

    if day in arrows1:
        for j in arrows1[day]:
            a = drawed['arrow'][j]
            a.remove()

            (x0,x1),(y0,y1) = arrows[j]
            b = ax3.arrow(x0,y0,x1-x0,y1-y0, linewidth=1.5, head_width=100., head_length=150., fc='#fdc1c5', ec='#fdc1c5', zorder=zdown, alpha=0.6)
            #prelines.append(b)

def get_anim(oo, filename_prefix, bg_polys, bbox):
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.animation import FuncAnimation
    global cases, cases_a, cases_b, geom_dict, time_dict, sub_a, sub_b, cent_dict, arrows, arrows0, arrows1, time_text, ax, ax2, ax3, drawed, zup, zdown
    #minx,maxx = 175000,186000
    #miny,maxy = 2495000,2506000
    print("start exporting movie")

    fig,(ax,ax2,ax3) = plt.subplots(1,3, figsize=(16,6), sharex=True, sharey=True)
    ax.set_aspect("equal")
    ax2.set_aspect("equal")
    ax3.set_aspect("equal")
    time_text = fig.suptitle('', fontsize=18, fontweight='bold')
    ax.set_xlabel("Case", fontsize=18)
    ax2.set_xlabel("Sub-clusters", fontsize=18)
    ax3.set_xlabel("Progression links", fontsize=18)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    #time_text = ax.text(0.02, 0.02, '', transform=ax.transAxes)
    #ax2.set_aspect("equal")
    bg = 'black'

    zo = 2
    for bgset in bg_polys:
        if len(bgset)==3:
            bgf, bgc, bgw = bgset
            bga = 0.6
        elif len(bgset)==4:
            bgf, bgc, bgw, bga = bgset
        else:
            print("background items should be a tuple with len==3 or 4")
        gdf = gpd.read_file(bgf)
        for i in range(len(gdf)):
            poly = gdf['geometry'][i]
            ax.add_patch(PolygonPatch(poly, fill=False, lw=bgw, ec=bgc, alpha=bga, zorder=zo ))
            ax2.add_patch(PolygonPatch(poly, fill=False, lw=bgw, ec=bgc, alpha=bga, zorder=zo ))
            ax3.add_patch(PolygonPatch(poly, fill=False, lw=bgw, ec=bgc, alpha=bga, zorder=zo ))
        zo+=1
    zdown = zo
    zup = zo + 1
    cases, cases_a, cases_b, bbox2 = get_cases(oo)
    geom_dict, time_dict, sub_a, sub_b, cent_dict = get_subclusters(oo, filename_prefix)
    arrows,arrows0,arrows1 = get_chains(oo)
    if bbox is None:
        bbox = bbox2
    minx,miny,maxx,maxy = bbox
    """
    for xs,ys in arrows:
        x0,x1 = xs
        y0,y1 = ys
        ax.arrow(x0,y0,x1-x0,y1-y0, linewidth=3, head_width=100., head_length=150., fc='#f7022a', ec='#f7022a', zorder=3, alpha=0.1)
    """
    drawed = {}
    drawed['case'] = {}
    drawed['subcluster'] = {}
    drawed['arrow'] = {}

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim((minx,maxx))
    ax.set_ylim((miny,maxy))

    anim = FuncAnimation(fig, update, frames=365, interval=2000)
    anim.save(filename_prefix, fps=8, extra_args=['-vcodec', 'libx264'])
    #plt.show()
    plt.close()
    print("movie exported")
