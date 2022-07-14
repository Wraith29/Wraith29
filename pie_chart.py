import math
from dataclasses import dataclass
from language_colour_map import get_language_colour
from create_svg import create_svg

@dataclass
class Pos:
    x: int
    y: int

@dataclass
class Arc:
    radius: int
    start: Pos
    end: Pos
    laf: '0' or '1'

def get_pos_in_circle(center_x: int, center_y: int, radius: int, angle_in_degrees: int) -> Pos:
    x = center_x + (radius * math.cos(angle_in_degrees))
    y = center_y + (radius * math.sin(angle_in_degrees))
    return Pos(x, y)

def polar_to_cartesian(center_x: int, center_y: int, radius: int, angle_in_degrees: int) -> Pos:
    angle_in_radians = (angle_in_degrees-90) * math.pi / 180
    x = center_x + (radius * math.cos(angle_in_radians))
    y = center_y + (radius * math.sin(angle_in_radians))

    return Pos(x, y)

def create_arc_data(x_pos: int, y_pos: int, radius: int, start_angle: int, end_angle: int) -> Arc:
    start = polar_to_cartesian(x_pos, y_pos, radius, end_angle)
    end = polar_to_cartesian(x_pos, y_pos, radius, start_angle)
    laf = "0" if end_angle - start_angle <= 180 else "1"

    return Arc(radius, start, end, laf)

def create_arc(center_x: int, center_y: int, arc_data: Arc) -> str:
    radius = arc_data.radius
    start_x = math.ceil(arc_data.start.x)
    start_y = math.ceil(arc_data.start.y)
    end_x = math.ceil(arc_data.end.x)
    end_y = math.ceil(arc_data.end.y)
    laf = arc_data.laf

    return f"M {center_x} {center_y} L {start_x} {start_y} A {radius} {radius} 0 {laf} 0 {end_x} {end_y} L {center_x} {center_y}"

def create_pie_chart(svg_size: int, lang_map: dict[str, str]) -> str:
    total = sum([v for v in lang_map.values()])
    center_x = svg_size // 2
    center_y = svg_size // 2
    radius = svg_size // 2
    data = []
    cumulative_total = 0
    for lang, count in lang_map.items():
        angle_coverage = round((count / total) * 360)
        arc_data = create_arc_data(center_x, center_y, radius, cumulative_total, cumulative_total+angle_coverage)
        colour = get_language_colour(lang)

        data.append(f'<path class="{lang}" d="{create_arc(center_x, center_y, arc_data)}" fill="{colour}" stroke="{colour}"><title>{lang}</title></path>')
        cumulative_total += angle_coverage

    create_svg(svg_size, svg_size, '\n'.join(data), 'pie_chart')
    return '![Pie Chart](./assets/pie_chart.svg "Pie Chart detailing languages used")'

