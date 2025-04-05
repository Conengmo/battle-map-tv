from battle_map_tv.area_of_effect.circle import Circle, CircleRasterized
from battle_map_tv.area_of_effect.cone import Cone, ConeRasterized
from battle_map_tv.area_of_effect.line import Line
from battle_map_tv.area_of_effect.square import Square

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
