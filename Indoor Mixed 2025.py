from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Hier werden die Ligen definiert. Ligen können einfach auskommentiert werden. (Name, URL, Aufsteiger, Absteiger)
leagues = {
    '1_liga': ('1. Liga', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1725', 1, 2),
    
    '2_liga_nord': ('2. Liga Nord', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1726', 1, 2),
    '2_liga_sued': ('2. Liga Süd', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1727', 1, 2),
    
    '3_liga_nord_west': ('3. Liga Nord-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1728', 1, 2),
    '3_liga_nord_ost': ('3. Liga Nord-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1729', 1, 1),
    '3_liga_sued_west': ('3. Liga Süd-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1730', 1, 3),
    '3_liga_sued_ost': ('3. Liga Süd-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1731', 1, 0),
    
    '4_liga_nord_west': ('4. Liga Nord-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1732', 2, 2),
    '4_liga_nord_ost': ('4. Liga Nord-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1733', 1, 0),
    '4_liga_sued_west': ('4. Liga Süd-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1734', 2, 1),
    '4_liga_sued_ost': ('4. Liga Süd-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1735', 2, 0),
    
    '5_liga_nord_west': ('5. Liga Nord-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1736', 2, 0),
 #  '5_liga_nord_ost': ('5. Liga Nord-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1737', 2, 2),
    '5_liga_sued_west': ('5. Liga Süd-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1737', 2, 0),
 #  '5_liga_sued_ost': ('5. Liga Süd-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1722', 2, 2),

   #'6_liga_nord_west': ('6. Liga Nord-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1723', 1, 0),
   #'6_liga_nord_ost': ('6. Liga Nord-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1723', 1, 0),
   #'6_liga_sued_west': ('6. Liga Süd-West', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1723', 1, 0),
   #'6_liga_sued_ost': ('6. Liga Süd-Ost', 'https://scores.frisbeesportverband.de/?view=seriesstatus&series=1723', 1, 0),
}

def scrape_table(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'infotable'})

        if table:
            headers = [th.text.strip() for i, th in enumerate(table.find_all('th')[:11]) if i not in [6, 7, 8, 10]]
            rows = []

            for tr in table.find_all('tr')[1:-1]:  
                cells = []
                for i, td in enumerate(tr.find_all('td')):  
                    if i not in [6, 7, 8, 10]:  
                        if i == 0:  
                            a_tag = td.find('a')  
                            if a_tag and 'href' in a_tag.attrs:
                                team_url = "https://scores.frisbeesportverband.de/" + a_tag['href']
                                team_name = a_tag.text.strip()
                                cell_value = f'<a href="{team_url}" target="_blank">{team_name}</a>'
                            else:
                                cell_value = td.text.strip()
                            cells.append(cell_value)
                        else:
                            cells.append(td.text.strip())
                if cells:
                    rows.append(cells)

            return headers, rows
    return [], []

@app.route('/')
def index():
    data = {}
    for key, values in leagues.items():
        if values:  # Nur Ligen verarbeiten, die nicht auskommentiert wurden
            name, url, top_green, bottom_red = values
            headers, rows = scrape_table(url)
            data[key] = {'name': name, 'url': url, 'headers': headers, 'rows': rows, 'top_green': top_green, 'bottom_red': bottom_red}
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
