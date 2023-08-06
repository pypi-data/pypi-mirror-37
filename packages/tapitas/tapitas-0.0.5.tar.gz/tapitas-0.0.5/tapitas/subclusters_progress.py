 # -*- coding: utf-8 -*-

## main interface

#import calc_frame
from .Diffusion_Progress import Diffusion_Progress
from .output_func import Outputs

class Point_Diffusion(object):
    def __init__(self, ptdataframe, pts_setting=None, s_radius=500, T1=12, T2=27, resample_time=99, confidence_level=0.8, critical_value=None, crs=None):

        self.ptdataframe = ptdataframe
        self.pts_setting = pts_setting
        self.crs = crs
        self.s_radius = s_radius
        self.T1 = T1
        self.T2 = T2
        self.resample_time = resample_time
        self.confidence_level = confidence_level
        self.critical_value = critical_value

        self.progression = Diffusion_Progress( self.ptdataframe, self.pts_setting, self.s_radius, self.T1, self.T2, self.resample_time, self.confidence_level, self.critical_value, crs=crs )

        self.outputs = Outputs(self.progression)
        self.results = self.outputs.oo

    def to_csv(self, filename_prefix=None):
        self.outputs.to_csv(filename_prefix)

    def get_gdf(self, crs=None, vno=16, dev_scale=1.5):
        pass

    def to_shpfile(self, filename_prefix=None, crs=None, vno=16, dev_scale=1.5):
        if crs is None:
            crs = self.crs
        self.outputs.to_shpfile(filename_prefix, crs, vno, dev_scale)

    def to_anime(self, filename_prefix=None, bg_polys=[], bbox=None):
        self.outputs.to_anime(filename_prefix, bg_polys, bbox)
    """
    def to_svgs(self, filename_prefix=None, bgfile=None, bbox=None, scale=30., widthscale=1.):
        self.outputs.to_svgs(filename_prefix, self.progression, bgfile=bgfile, bbox=bbox, scale=scale, widthscale=widthscale)

    def to_svg_event(self, filename_prefix=None, bgfile=None, title="The event of points", bbox=None, scale=30.):
        self.outputs.to_svg_event(bgfile, filename_prefix, title=title, bbox=bbox, scale=scale)

    def to_svg_animate(self, filename_prefix=None, bgfile=None, title="The progression of subcluster", bbox=None, scale=30):
        self.outputs.to_svg_animate(self.progression, bgfile, filename_prefix, title=title, bbox=bbox, scale=scale)

    def to_svg_static(self, filename_prefix=None, bgfile=None, title="The static view of subcluster", bbox=None, shape='ellipse', widthscale=1.):
        self.outputs.to_svg_static(self.progression, bgfile, filename_prefix, title=title, bbox=bbox, shape=shape, widthscale=widthscale)

    def to_svg_morph(self, filename_prefix=None, bgfile=None, title="The progression of subcluster", bbox=None, shape='ellipse', scale=30.):
        self.outputs.to_svg_morph(self.progression, bgfile, filename_prefix, title=title, bbox=bbox, shape=shape, scale=scale)
    """
