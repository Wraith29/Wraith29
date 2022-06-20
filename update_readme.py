from pie_chart import create_pie_chart
from get_github_data import get_language_map
from language_colour_map import get_nice_language_colour_map

def update_readme():
    language_colour_map = get_nice_language_colour_map()
    language_map = get_language_map()
    pie_chart = create_pie_chart(500, language_map)

    with open('./README.md', 'w') as f:
        f.write(f"{language_colour_map}\n\n{pie_chart}")

if __name__ == "__main__":
    update_readme()