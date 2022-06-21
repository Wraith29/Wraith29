from create_svg import create_svg

LC_MAP = {
    "Nim": "#FFC200",
    "Python": "#3572A5",
    "HTML": "#E34C26",
    "JavaScript": "#F1E05A",
    "CSS": "#563D7C",
    "Shell": "#89E051",
    "Less": "#1D365D",
    "TypeScript": "#3178C6"
}

def generate_row(language, colour, count):
    create_svg(10, 10, f'<rect width="10" height="10" fill="{colour}" />', language)
    return f'![{language}](./assets/{language}.svg) {language}|{count}|'

# def get_nice_language_colour_map():
#     rows = [
#         "|Language|Count|",
#         "|:-:|:-:|"
#     ]

#     for language, colour in LC_MAP.items():
#         rows.append(generate_row(language, colour))

#     return '\n'.join(rows)

def get_language_breakdown(language_map: dict[str, int]):
    rows = [
        "|Language|Count|",
        "|:-:|:-:|",
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