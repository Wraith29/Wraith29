import json
from create_svg import create_svg

def get_language_colour(language: str) -> str:
    with open('./colours.json', 'r') as colours_file:
        colours = json.loads(colours_file.read())

    try:
        return colours[language]
    except KeyError:
        return "green"

def generate_row(language: str, colour: str, count: int):
    create_svg(10, 10, f'<rect width="10" height="10" fill="{colour}" />', language)
    return f'![{language}](./assets/{language}.svg) {language}|{count}|'

def get_language_breakdown(language_map: dict[str, int]) -> str:
    total = sum([v for v in language_map.values()])
    rows = [
        "|Language|Bytes|",
        "|:-:|:-:|",
        f"|Total|{total}"
    ]

    for language, count in language_map.items():
        colour = get_language_colour(language)
        rows.append(generate_row(language, colour, count))

    return '\n'.join(rows)
