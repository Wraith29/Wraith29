import math
from dataclasses import dataclass
from language_colour_map import get_language_colour
from create_svg import create_svg

@dataclass
class Pos:
    x: int
    y: int

    def to_cartesian(self, radius: int, angle_in_degrees: int) -> 'Pos':
        angle_in_radians = (angle_in_degrees - 90) * math.pi / 180
        x = self.x + (radius * math.cos(angle_in_radians))
        y = self.y + (radius * math.sin(angle_in_radians))

        return Pos(x, y)

@dataclass
class Arc:
    radius: int
    start: Pos
    end: Pos
    laf: '0' or '1'

def create_arc_data(pos: Pos, radius: int, start_angle: int, end_angle: int) -> Arc:
    start = pos.to_cartesian(radius, end_angle)
    end = pos.to_cartesian(radius, start_angle)
    laf = '0' if end_angle - start_angle <= 180 else '1'

    return Arc(radius, start, end, laf)

def create_arc(center: Pos, arc_data: Arc) -> str:
    radius = arc_data.radius
    start_x = math.ceil(arc_data.start.x)
    start_y = math.ceil(arc_data.start.y)
    end_x = math.ceil(arc_data.end.x)
    end_y = math.ceil(arc_data.end.y)
    laf = arc_data.laf

    return f"M {center.x} {center.y} L {start_x} {start_y} A {radius} {radius} 0 {laf} 0 {end_x} {end_y} L {center.x} {center.y}"

def create_pie_chart(svg_size: int, lang_map: dict[str, str]) -> str:
    total = sum([v for v in lang_map.values()])
    center = Pos(svg_size // 2, svg_size // 2)
    radius = svg_size // 2
    data = []
    cumulative_total = 0
    for lang, count in lang_map.items():
        angle_coverage = round((count / total) * 360)
        arc_data = create_arc_data(center, radius, cumulative_total, cumulative_total+angle_coverage)
        colour = get_language_colour(lang)

        data.append(f'<path class="{lang}" d="{create_arc(center, arc_data)}" fill="{colour}" stroke="{colour}"><title>{lang}</title></path>')
        cumulative_total += angle_coverage

    create_svg(svg_size, svg_size, '\n'.join(data), 'pie_chart')
    return '![Pie Chart](./assets/pie_chart.svg "Pie Chart detailing languages used")'

