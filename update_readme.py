from datetime import datetime
from pie_chart import create_pie_chart
from get_github_data import get_language_map
from language_colour_map import get_nice_language_colour_map

def update_readme():
    language_colour_map = get_nice_language_colour_map()
    language_map = get_language_map()
    pie_chart = create_pie_chart(400, language_map)

    with open('./README.md', 'w') as readme:
        readme.write(f'{pie_chart}\n\n{language_colour_map}\n\n<sub>Last Updated At: {datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</sub>')

if __name__ == "__main__":
    update_readme()