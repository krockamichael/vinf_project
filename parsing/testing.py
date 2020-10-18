from difflib import SequenceMatcher
import xml.etree.ElementTree as ET
from unidecode import unidecode
from typing import Tuple
import pandas as pd
import re
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def load_top_football_clubs() -> Tuple[list, list, list, list, list]:
    with open('../data/TopLeagueTeamNames.txt', 'r', encoding='utf-8') as f:
        # file format: league name, club names, empty line
        f.readline()    # ignore league name
        la_liga_ = [next(f).strip() for x in range(20)]
        f.readline(), f.readline()  # ignore league name and empty line
        bundesliga_ = [next(f).strip() for x in range(18)]
        f.readline(), f.readline()
        serie_a_ = [next(f).strip() for x in range(20)]
        f.readline(), f.readline()
        premier_league_ = [next(f).strip() for x in range(20)]
        f.readline(), f.readline()
        ligue_1_ = [next(f).strip() for x in range(20)]

    return la_liga_, bundesliga_, serie_a_, premier_league_, ligue_1_


def is_top_football_club(title, La_Liga=None, Bundesliga=None, Serie_A=None, Premier_League=None, Ligue_1=None) -> bool:
    if not all(v is not None for v in [La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1]):
        La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1 = load_top_football_clubs()

    if [x for x in (La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1) if title in x]:
        return True
    else:
        return False


def is_footballer_name(name1, name2, title) -> bool:
    # check if title contains () and if so remove them
    if re.search('\(.*\)', title):
        title = re.split('\(', title)[0]

    # replace language specific characters (ľščťžýáíéúäôň...) with English characters
    name1 = unidecode(name1).lower().strip()
    name2 = unidecode(name2).lower().strip()
    title = unidecode(title).lower().strip()

    # use sequence matcher to calculate the similarity of two strings
    if SequenceMatcher(None, name1, title).ratio() > 0.9:
        return True
    elif SequenceMatcher(None, name2, title).ratio() > 0.9:
        return True
    else:
        return False


def is_footballer(text, title) -> bool:
    # TODO better solution?
    # select short description and remove unwanted characters
    shortSummaryString = re.findall(r'{{short\sdescription\|(.*?)}}', text, re.DOTALL)[-1]
    if 'football player' in shortSummaryString or 'footballer' in shortSummaryString:
        return True
    elif 'football' in title.lower():
        return True
    return False


def parse_infobox(text, title) -> ET.Element:
    career = ET.Element('career')
    player_name_ = ET.SubElement(career, 'player_name')
    player_name_.text = title

    # select infobox and remove unwanted characters
    infobox_string = re.findall(r'{{Infobox.*?\n}}', text, re.DOTALL)[-1]
    for unwanted_chars in '{}[]*':
        infobox_string = infobox_string.replace(unwanted_chars, '')
    # infobox_string = infobox_string.replace('|', ' ')

    # youth, senior, national = None, None, None

    # parse youth clubs and years from infoBoxString
    y_clubs_list = re.findall(r'\byouthclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    y_years_list = re.findall(r'\byouthyears\d\s*=\s*(.*)\n', infobox_string)
    # if len(y_clubs_list) == len(y_years_list):
    #     youth = [[x.strip(), y.strip(), 'youth'] for x, y in zip(y_clubs_list, y_years_list)]
    # else:
    #     print('Error: YOUTH Club list and YOUTH Year list are not the same length.')

    for x, y in zip(y_clubs_list, y_years_list):
        club = ET.SubElement(career, 'club')
        name_ = ET.SubElement(club, 'name')
        name_.text = x
        years = ET.SubElement(club, 'years')
        years.text = y
        type_ = ET.SubElement(club, 'type')
        type_.text = 'youth'

    # parse senior clubs and years from infoBoxString
    # TODO club string does not start with a letter (e.g. '-> ')
    s_clubs_list = re.findall(r'\bclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    s_years_list = re.findall(r'\byears\d\s*=\s*(.*)\n', infobox_string)
    # if len(s_clubs_list) == len(s_years_list):
    #     senior = [[x.strip(), y.strip(), 'senior'] for x, y in zip(s_clubs_list, s_years_list)]
    # else:
    #     print('Error: SENIOR Club list and SENIOR Year list are not the same length.')

    for x, y in zip(s_clubs_list, s_years_list):
        club = ET.SubElement(career, 'club')
        name_ = ET.SubElement(club, 'name')
        name_.text = x
        years = ET.SubElement(club, 'years')
        years.text = y
        type_ = ET.SubElement(club, 'type')
        type_.text = 'senior'

    # parse national clubs and years from infoBoxString
    n_clubs_list = re.findall(r'\bnationalteam\d\s*=\s*(.*?)[|\n]', infobox_string)
    n_years_list = re.findall(r'\bnationalyears\d\s*=\s*(.*)\n', infobox_string)
    # if len(n_clubs_list) == len(n_years_list):
    #     national = [[x.strip(), y.strip(), 'national'] for x, y in zip(n_clubs_list, n_years_list)]
    # else:
    #     print('Error: NATIONAL Club list and NATIONAL Year list are not the same length.')

    for x, y in zip(n_clubs_list, n_years_list):
        club = ET.SubElement(career, 'club')
        name_ = ET.SubElement(club, 'name')
        name_.text = x
        years = ET.SubElement(club, 'years')
        years.text = y
        type_ = ET.SubElement(club, 'type')
        type_.text = 'national'

    # insert data into a dataframe
    # infobox_dataframe = pd.DataFrame(data=(youth + senior + national), columns=['Team', 'Years', 'Type'])

    return career


def parse_football_squad(text) -> str or None:
    if re.search(r'start', text, re.DOTALL):
        return re.findall(r'start(.*)end', text, re.DOTALL)[0]
    return None


def parse_table_senior(text, team_name) -> pd.DataFrame:
    squad_string = None

    # select current team
    squad_list = re.findall(r'[Ss]quad\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
    if squad_list:
        squad_string = parse_football_squad(max(squad_list, key=len))
    if squad_string is None:
        squad_list = re.findall(r'[Ff]irst\steam\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
        squad_string = parse_football_squad(max(squad_list, key=len))

    for unwanted_chars in '{}[]*':
        squad_string = squad_string.replace(unwanted_chars, '')

    # select only player names
    names_list = re.findall(r'\|\s?name=(.*?)[|\n<]', squad_string)
    club_name_list = [team_name for x in range(len(names_list))]
    senior_list = ['senior' for x in range(len(names_list))]

    # insert data into a dataframe
    senior_dataframe = pd.DataFrame(data=zip(names_list, club_name_list, senior_list), columns=['Name', 'Club', 'Type'])

    return senior_dataframe


def get_xml_title(tree_root) -> str:
    return [child_.text for child_ in tree_root if child_.tag == 'title'][0]


def get_xml_text(tree_root) -> str:
    return [grandchild.text
            for child_ in tree_root
            for grandchild in child_
            if grandchild.tag == 'text'][0]


def check_possibility(new_entry, other_player_list):
    club_name = new_entry[0]
    club_type = new_entry[2]

    year_1, year_2 = None, None
    if '–' in new_entry[1]:
        year_1, year_2 = re.split('–', new_entry[1])
    elif len(new_entry[1]) == 4:
        year_1 = new_entry[1]
    elif new_entry[1][-1] == '–':
        year_1 = new_entry[1][:-2]

    for entry in other_player_list:
        if entry[2] == club_type:
            if entry[0] == club_name:
                if '–' in entry[1]:
                    entry_year_1, entry_year_2 = re.split('–', entry[1])
                    if int(entry_year_1) <= int(year_1) <= int(entry_year_2):
                        # TODO something better
                        print('They played together.')
                    elif int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')
                elif len(entry[1]) == 4:
                    entry_year_1 = entry[1]
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                    elif int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')
                elif entry[1][-1] == '–':
                    entry_year_1 = entry[1][:-2]
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                    elif int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')


def update_player_list(root_, player_list, other_player_list):
    for child_ in root_:
        if child_.tag == 'club':
            temp_list = list()
            for g_child_ in child_:
                temp_list.append(g_child_.text)

            if len(other_player_list) > 0:
                check_possibility(temp_list, other_player_list)
            if temp_list not in player_list:
                player_list.append(temp_list)


if __name__ == '__main__':
    # parse into a tree structure using xml parser
    root = ET.fromstring(open('../data/frankLampard.xml', 'r', encoding='utf-8').read())
    page_title = get_xml_title(root)
    xml_text = get_xml_text(root)

    # TODO temp names
    MATCH = None
    name_1 = 'Frank Lampard'
    name_2 = 'Michael Essien'
    la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()

    if is_footballer_name(name_1, name_2, page_title):
        if is_footballer(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title)
            # TODO parse_text()
    elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
        senior_df = parse_table_senior(xml_text, page_title)
        for player_name in senior_df['Name']:
            if is_footballer_name(name_1, name_2, player_name):
                MATCH = (player_name, page_title)
        # TODO parse_table_youth()
        # TODO parse_football_squad_on_pitch()


    name_ONE = None
    player_TWO = None
    list_ONE = list()
    list_TWO = list()

    if MATCH is not None:
        for child in MATCH:
            # create list where first member is player name
            # subsequent memberss are in the form of
            # club_name, years, type

            if child.tag == 'player_name':
                if name_ONE is None:
                    name_ONE = child.text
                    list_ONE.append(name_ONE)
                    update_player_list(MATCH, list_ONE, list_TWO)

                elif player_TWO is None and name_ONE != child.text:
                    player_TWO = child.text
                    list_TWO.append(player_TWO)
                    update_player_list(MATCH, list_TWO, list_ONE)

                elif name_ONE == child.text:
                    update_player_list(MATCH, list_ONE, list_TWO)

                elif player_TWO == child.text:
                    update_player_list(MATCH, list_TWO, list_ONE)
            else:
                break

    # parse into a tree structure using xml parser
    root = ET.fromstring(open('../data/michaelEssien.xml', 'r', encoding='utf-8').read())
    page_title = get_xml_title(root)
    xml_text = get_xml_text(root)

    # TODO temp names
    MATCH = None
    name_1 = 'Frank Lampard'
    name_2 = 'Michael Essien'
    la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()

    if is_footballer_name(name_1, name_2, page_title):
        if is_footballer(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title)
            # TODO parse_text()
    elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
        senior_df = parse_table_senior(xml_text, page_title)
        for player_name in senior_df['Name']:
            if is_footballer_name(name_1, name_2, player_name):
                MATCH = (player_name, page_title)
        # TODO parse_table_youth()
        # TODO parse_football_squad_on_pitch()

    if MATCH is not None:
        for child in MATCH:
            # create list where first member is player name
            # subsequent memberss are in the form of
            # club_name, years, type

            if child.tag == 'player_name':
                if name_ONE is None:
                    name_ONE = child.text
                    list_ONE.append(name_ONE)
                    update_player_list(MATCH, list_ONE, list_TWO)

                elif player_TWO is None and name_ONE != child.text:
                    player_TWO = child.text
                    list_TWO.append(player_TWO)
                    update_player_list(MATCH, list_TWO, list_ONE)

                elif name_ONE == child.text:
                    update_player_list(MATCH, list_ONE, list_TWO)

                elif player_TWO == child.text:
                    update_player_list(MATCH, list_TWO, list_ONE)
            else:
                break

    print('a')

"""
{{football squad on pitch
TODO check what year --> | caption
"""

"""
===Barcelona B and Youth Academy===
{{main|FC Barcelona B|FC Barcelona (youth)}}
{{Fs start}}
{{Fs
"""

"""
MATCH structure:

<career>
    <player_name>John</player_name>
    <club>
        <name>xxx</name>
        <years>yyy</years>
        <type>zzz</type>
    </club>
    <club>...</club>
</career>
"""