import cadquery as cq
import math
from typing import Tuple, List
from rackmate.model import FanType, Fan, Frame, Params


def top_frame(frame: Frame) -> cq.Sketch:
    return cq.Sketch().rect(frame.width, frame.depth)


def frame_cutout(frame: Frame) -> cq.Sketch:
    cutout = cq.Sketch().rect(frame.cutout_width, frame.cutout_depth)
    offset = (frame.depth - frame.cutout_depth) / 2
    return cutout.moved(y=offset).face(cutout.moved(y=-offset), mode="a")


def holes_at_positions(
    positions: List[Tuple[float, float]], radius: float
) -> cq.Sketch:
    sketch = cq.Sketch()
    for x, y in positions:
        sketch = sketch.face(cq.Sketch().circle(radius).moved(x=x, y=y), mode="a")
    return sketch


def frame_screw_holes(frame: Frame) -> cq.Sketch:
    w, d = frame.width, frame.depth
    x_off, y_off = frame.screw_x_offset, frame.screw_y_offset
    positions = [
        (w / 2 - x_off, d / 2 - y_off),
        (-w / 2 + x_off, d / 2 - y_off),
        (w / 2 - x_off, -d / 2 + y_off),
        (-w / 2 + x_off, -d / 2 + y_off),
    ]
    return holes_at_positions(positions, frame.screw_radius)


def fan_mount_holes(fan_type: FanType) -> cq.Sketch:
    sketch = cq.Sketch()
    for pattern in fan_type.screw_hole_patterns:
        x_spacing, y_spacing = pattern.spacing
        positions = [
            (-x_spacing / 2, -y_spacing / 2),
            (x_spacing / 2, -y_spacing / 2),
            (-x_spacing / 2, y_spacing / 2),
            (x_spacing / 2, y_spacing / 2),
        ]
        sketch = sketch.face(holes_at_positions(positions, pattern.radius), mode="a")
    return sketch


def fan_cutout(fan: Fan, frame: Frame) -> cq.Sketch:
    usable_width = frame.width - 2 * (frame.screw_x_offset + frame.screw_radius)
    usable_depth = frame.depth - 2 * frame.cutout_depth
    needs_padding = (
        fan.type.radius * 2 + frame.padding > usable_width
        or fan.type.radius * 2 + frame.padding > usable_depth
    )
    fan_hole = cq.Sketch().circle(fan.type.radius)
    if needs_padding:
        limit = cq.Sketch().rect(
            usable_width - frame.padding, usable_depth - frame.padding
        )
        fan_hole = fan_hole.face(limit, mode="i")
    return fan_hole


def ring(radius: int, thickness: int) -> cq.Sketch:
    return (
        cq.Sketch()
        .circle(radius)
        .face(cq.Sketch().circle(radius - thickness), mode="s")
    )


def polar_point(radius: float, angle: float) -> Tuple[float, float]:
    return radius * math.cos(angle), radius * math.sin(angle)


def create_single_spoke(
    inner_radius: float,
    outer_radius: float,
    center_angle: float,
    spoke_width: float,
    buffer_ratio: float = 0.01,
) -> cq.Sketch:
    buffered_inner = inner_radius * (1 - buffer_ratio)
    buffered_outer = outer_radius * (1 + buffer_ratio)

    half_angle_inner = (spoke_width / 2) / buffered_inner
    half_angle_outer = (spoke_width / 2) / buffered_outer

    angle_inner_left = center_angle - half_angle_inner
    angle_inner_right = center_angle + half_angle_inner
    angle_outer_left = center_angle - half_angle_outer
    angle_outer_right = center_angle + half_angle_outer

    p1 = polar_point(buffered_inner, angle_inner_left)
    p2 = polar_point(buffered_outer, angle_outer_left)
    p3 = polar_point(buffered_outer, angle_outer_right)
    p4 = polar_point(buffered_inner, angle_inner_right)

    return cq.Sketch().polygon([p1, p2, p3, p4])


def create_grill_spokes(fan: Fan) -> cq.Sketch:
    sketch = cq.Sketch()
    angle_step = 2 * math.pi / fan.spoke_count

    for i in range(fan.spoke_count):
        angle = i * angle_step
        spoke = create_single_spoke(
            fan.initial_radius, fan.type.radius, angle, fan.thickness
        )
        sketch = sketch.face(spoke, mode="a")

    return sketch


def fan_grill_rings(fan: Fan) -> cq.Sketch:
    sketch = cq.Sketch()
    r = fan.initial_radius
    while r + fan.thickness <= fan.type.radius:
        sketch = sketch.face(ring(r, fan.thickness), mode="a")
        r += fan.radius_spacing
    return sketch


def fan_grill(fan: Fan) -> cq.Sketch:
    rings = fan_grill_rings(fan)
    spokes = create_grill_spokes(fan)
    return rings.face(spokes, mode="a")


def sketch_cover(params: Params) -> cq.Sketch:
    cutout = fan_cutout(params.fan, params.frame)
    sketch = (
        top_frame(params.frame)
        .face(frame_cutout(params.frame), mode="s")
        .face(cutout, mode="s")
    )

    sketch = sketch.face(fan_grill(params.fan).face(cutout, mode="i"), mode="a")
    sketch = sketch.face(frame_screw_holes(params.frame), mode="s")
    sketch = sketch.face(fan_mount_holes(params.fan.type), mode="s")

    return sketch
