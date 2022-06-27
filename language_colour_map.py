from create_svg import create_svg

LC_MAP = {
    "Nim": "#FFC200",
    "Python": "#FFD343",
    "HTML": "#E34C26",
    "JavaScript": "#F1E05A",
    "CSS": "#563D7C",
    "Shell": "#89E051",
    "Less": "#1D365D",
    "TypeScript": "#3178C6",
    "C++": "#f34b7d",
    "Makefile": "#427819"
}

def generate_row(language, colour, count):
    create_svg(10, 10, f'<rect width="10" height="10" fill="{colour}" />', language)
    return f'![{language}](./assets/{language}.svg) {language}|{count}|'

def get_language_breakdown(language_map: dict[str, int]):
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

def get_language_colour(language):
    try:
        return LC_MAP[language]
    except KeyError:
        return "green"