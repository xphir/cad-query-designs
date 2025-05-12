from rackmate.model import FanType, Fan, Frame, Params, ScrewHolePattern

fan_types = {
    "200mm": FanType(
        radius=100,
        screw_hole_patterns=[
            ScrewHolePattern(spacing=(170, 170), radius=2.5),
            ScrewHolePattern(spacing=(180, 110), radius=2.5),
            ScrewHolePattern(spacing=(154, 154), radius=2.5),
        ],
    )
}

default_params = Params(
    fan=Fan(
        type=fan_types["200mm"],
        initial_radius=20,
        radius_spacing=30,
        thickness=3,
        spoke_count=8,
    ),
    frame=Frame(
        width=280,
        depth=200,
        cutout_width=220,
        cutout_depth=5,
        screw_x_offset=13,
        screw_y_offset=32.5,
        screw_radius=2.5,
        padding=20,
    ),
    height=4.5,
)
