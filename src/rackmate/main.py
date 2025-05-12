import cadquery as cq
from dataclasses import replace
from rackmate.defaults import default_params
from rackmate.geometry import sketch_cover
from rackmate.model import Params, FanType, ScrewHolePattern

def main(params: Params = default_params) -> cq.Workplane:
    return cq.Workplane("XY").add(sketch_cover(params)).extrude(params.height)


overridden = replace(
    default_params,
    fan=replace(
        default_params.fan,
        type=FanType(
            radius=100,
            screw_hole_patterns=[
                ScrewHolePattern(spacing=(170, 170), radius=2.5),
            ],
        ),
    ),
)

result = main(overridden)

# Render the solid
# show_object(result, name="box")  # type: ignore  # noqa: F821

# Export
cq.exporters.export(result, "rackmate-top.stl")
cq.exporters.export(result, "rackmate-top.step")
