import math
from language_colour_map import get_language_colour

def get_pos_in_circle(center_x, center_y, radius, angle_in_degrees):
    x = center_x + (radius * math.cos(angle_in_degrees))
    y = center_y + (radius * math.sin(angle_in_degrees))
    return x, y

def polar_to_cartesian(center_x, center_y, radius, angle_in_degrees):
    angle_in_radians = (angle_in_degrees-90) * math.pi / 180
    x = center_x + (radius * math.cos(angle_in_radians))
    y = center_y + (radius * math.sin(angle_in_radians))

    return x, y

def create_arc_data(x_pos, y_pos, radius, start_angle, end_angle):
    start_x, start_y = polar_to_cartesian(x_pos, y_pos, radius, end_angle)
    end_x, end_y = polar_to_cartesian(x_pos, y_pos, radius, start_angle)
    laf = "0" if end_angle - start_angle <= 180 else "1"

    return {
        'radius': radius,
        'start_x': start_x,
        'start_y': start_y,
        'end_x': end_x,
        'end_y': end_y,
        'laf': laf
    }

def create_arc(center_x, center_y, arc_data):
    radius = arc_data['radius']
    start_x = math.ceil(arc_data['start_x'])
    start_y = math.ceil(arc_data['start_y'])
    end_x = math.ceil(arc_data['end_x'])
    end_y = math.ceil(arc_data['end_y'])
    laf = arc_data['laf']

    return f"M {center_x} {center_y} L {start_x} {start_y} A {radius} {radius} 0 {laf} 0 {end_x} {end_y} L {center_x} {center_y}"

def create_pie_chart(svg_size, lang_map):
    total = sum([v for v in lang_map.values()])
    center_x = svg_size // 2
    center_y = svg_size // 2
    radius = (svg_size // 2) - 50
    data = []
    cumulative_total = 0
    for lang, count in lang_map.items():
        angle_coverage = round((count / total) * 360)
        arc_data = create_arc_data(center_x, center_y, radius, cumulative_total, cumulative_total+angle_coverage)
        colour = get_language_colour(lang)

        data.append(f'<path class="{lang}" d="{create_arc(center_x, center_y, arc_data)}" fill="{colour}" stroke="{colour}" />')
        cumulative_total += angle_coverage

    return '<svg width="{0}" height="{0}">\n{1}\n</svg>'.format(svg_size, '\n'.join(data))

