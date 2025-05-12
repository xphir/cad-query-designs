import cadquery as cq
from dataclasses import replace
from rackmate.defaults import default_params
from rackmate.geometry import sketch_cover
from rackmate.model import Params, FanType, ScrewHolePattern
from pathlib import Path


def top_panel(params: Params = default_params) -> cq.Workplane:
    return cq.Workplane("XY").add(sketch_cover(params)).extrude(params.height)


def export(directory: str, filename: str, shape: cq.Workplane) -> None:
    Path(directory).mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, f"{directory}/{filename}")


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

result = top_panel(overridden)

# Render the solid
# show_object(result, name="box")  # type: ignore  # noqa: F821

# Export
export("../../assets/outputs/rackmate", "top-panel.stl", result)
