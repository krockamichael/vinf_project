import re
from parsing.testing import load_top_football_clubs

source = '../data/result.xml'
target = '../data/only_teams.xml'
la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()

with open(source, 'r', encoding='utf8') as s_file, open(target, 'w', encoding='utf8') as t_file:
    t_file.write('<pages>')
    for line in s_file:
        if '<page>' in line:
            football_indicator = False
            whole_page = list()
            whole_page.append(line)

            for line_1 in s_file:
                if '<title>' in line_1:
                    # get title
                    title = re.findall(r'<title>(.*?)</title>', line_1)[0]
                    # check if title in top football club names
                    if [x for x in (la_liga, bundesliga, serie_a, premier_league, ligue_1) if title in x]:
                        football_indicator = True
                    else:
                        break
                # if not end of page append line from file to list
                if '</page>' not in line_1:
                    whole_page.append(line_1)
                else:
                    break

            # if it is a top football club page, write to file
            if football_indicator:
                whole_page.append(line_1)
                t_file.writelines(whole_page)
    t_file.write('</pages>')
