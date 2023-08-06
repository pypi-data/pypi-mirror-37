# -*- coding: utf-8 -*-

#import .utils.exporter as exporter
from .utils import oo, to_csv, to_shpfile, to_anime

class Outputs(object):
    def __init__(self, progression):
        #self.oo = exporter.Output_Objects(progression)
        self.oo = oo(progression)

    def to_csv(self, filename_prefix):
        #exporter.to_csv(self.oo, filename_prefix)
        to_csv(self.oo, filename_prefix)

    def to_shpfile(self, filename_prefix, crs, vno, dev_scale):
        #exporter.to_shpfile(self.oo, filename_prefix, crs, vno, dev_scale)
        to_shpfile(self.oo, filename_prefix, crs, vno, dev_scale)

    def to_anime(self, filename_prefix, bg_polys, bbox):
        #exporter.to_anime(self.oo, filename_prefix, bg_polys, bbox)
        to_anime(self.oo, filename_prefix, bg_polys, bbox)
    """
    def to_svgs(self, filename_prefix, pgraph, bgfile, bbox, scale, widthscale):
        exporter.to_svgs_all(self.oo, filename_prefix, pgraph, bgfile, bbox, scale, widthscale)

    def to_svg_event(self, bgfile, filename_prefix, title, bbox, scale):
        exporter.to_svg_event(self.oo, bgfile, filename_prefix, title=title, bbox=bbox, scale=scale)

    def to_svg_animate(self, pgraph, bgfile, filename_prefix, title, bbox, scale):
        exporter.to_svg_animate(self.oo, pgraph, bgfile, filename_prefix, title=title, bbox=bbox, scale=scale)

    def to_svg_static(self, pgraph, bgfile, filename_prefix, title, bbox, shape, widthscale):
        exporter.to_svg_static(self.oo, pgraph, bgfile, filename_prefix, title=title, bbox=bbox, shape=shape, widthscale=widthscale)

    def to_svg_morph(self, pgraph, bgfile, filename_prefix, title, bbox, shape, scale):
        exporter.to_svg_morph(self.oo, pgraph, bgfile, filename_prefix, title=title, bbox=bbox, shape=shape, scale=scale)
    """
