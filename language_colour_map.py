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

def colour_svg(colour):
    return f'<svg width=10 height=10><rect width=10 height=10 fill="{colour}" /></svg>'

def generate_row(lang, colour):
    return f'|{lang}|{colour_svg(colour)}|'

def get_nice_language_colour_map():
    rows = [
        '| Language | Colour |',
        '|:--------:|:------:|'
    ]

    for language, colour in LC_MAP.items():
        rows.append(generate_row(language, colour))

    return "<div style='float:right;'>\n\n{}\n</div>".format('\n'.join(rows))

def get_language_colour(language):
    try:
        return LC_MAP[language]
    except KeyError:
        return "green"