from dataclasses import dataclass
from typing import Tuple, List


@dataclass(frozen=True)
class ScrewHolePattern:
    spacing: Tuple[int, int]
    radius: float


@dataclass(frozen=True)
class FanType:
    radius: int
    screw_hole_patterns: List[ScrewHolePattern]


@dataclass(frozen=True)
class Fan:
    type: FanType
    initial_radius: int
    radius_spacing: int
    thickness: int
    spoke_count: int


@dataclass(frozen=True)
class Frame:
    width: int
    depth: int
    cutout_width: int
    cutout_depth: int
    screw_x_offset: int
    screw_y_offset: int
    screw_radius: int
    padding: int


@dataclass(frozen=True)
class Params:
    fan: Fan
    frame: Frame
    height: int
