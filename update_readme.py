from datetime import datetime
from pie_chart import create_pie_chart
from get_github_data import get_language_map
from language_colour_map import get_language_breakdown

def update_readme():
    language_map = get_language_map()
    language_breakdown = get_language_breakdown(language_map)
    pie_chart = create_pie_chart(400, language_map)
    updated_at = datetime.now().strftime("%A %d %b %Y %H:%M:%S")

    with open('./TEMPLATE.md', 'r') as template_file:
        template = template_file.readlines()

    for idx, line in enumerate(template):
        if line == '{pie_chart}\n':
            template[idx] = pie_chart
        elif line == '{language_table}\n':
            template[idx] = language_breakdown
        elif line == '{updated_at}\n':
            template[idx] = updated_at
    

    with open('./README.md', 'w') as readme:
        readme.write(''.join(template))

if __name__ == "__main__":
    update_readme()