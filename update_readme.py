from datetime import datetime
from pie_chart import create_pie_chart
from get_github_data import get_language_map
from language_colour_map import get_language_breakdown

def update_readme():
    language_map = get_language_map()
    language_breakdown = get_language_breakdown(language_map)
    pie_chart = create_pie_chart(400, language_map)

    with open('./README.md', 'w') as readme:
        readme.write(f'''<span align="center">

## Language Breakdown

</span>

<foreignObject>
<body xmlns="http://www.w3.org/1999/xhtml">
<table align="center">
<tr>
<td>

{pie_chart}

</td>
<td>

{language_breakdown}

</td>
</tr>
</table>
</body>
</foreignObject>

<sub>Last updated at: {datetime.now().strftime("%A %d %b %Y %H:%M:%S")}
        ''')

if __name__ == "__main__":
    update_readme()