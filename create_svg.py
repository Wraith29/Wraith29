def create_svg(width, height, data, filename):
    with open(f"./assets/{filename}.svg", "w") as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n{data}\n</svg>')