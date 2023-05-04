import drawSvg as draw


class SVGHyperlink(draw.DrawingParentElement):
    TAG_NAME = "a"

    def __init__(self, href, target=None, **kwargs):
        # Other init logic...
        # Keyword arguments to super().__init__() correspond to SVG node
        # arguments: stroke_width=5 -> <a stroke-width="5" ...>...</a>
        super().__init__(href=href, target=target, **kwargs)
