from .circle import Circle, CircleRasterized
from .cone import Cone, ConeRasterized
from .line import Line
from .square import Square

area_of_effect_shapes_to_class = {
    "circle": Circle,
    "square": Square,
    "cone": Cone,
    "line": Line,
}

area_of_effect_rasterized_shapes_to_class = {
    "circle": CircleRasterized,
    "square": Square,
    "cone": ConeRasterized,
    "line": Line,
}
