from difflib import SequenceMatcher
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from unidecode import unidecode
from xml.dom import minidom
from typing import Tuple
import re


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


def append_to_xml_tree(career_root, club_name, years, club_type, player_name):
    club = ET.SubElement(career_root, 'club')

    p_name = ET.SubElement(club, 'player_name')
    p_name.text = player_name

    c_name = ET.SubElement(club, 'club_name')
    c_name.text = club_name

    years_ = ET.SubElement(club, 'years')
    years_.text = years

    c_type = ET.SubElement(club, 'type')
    c_type.text = club_type


def parse_infobox(text, title) -> ET.Element:
    career = ET.Element('career')

    # select infobox and remove unwanted characters
    infobox_string = re.findall(r'{{Infobox.*?\n}}', text, re.DOTALL)[-1]
    for unwanted_chars in '{}[]*':
        infobox_string = infobox_string.replace(unwanted_chars, '')

    # parse youth clubs & years
    y_clubs_list = re.findall(r'\byouthclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    y_years_list = re.findall(r'\byouthyears\d\s*=\s*(.*)\n', infobox_string)
    for youth_club, youth_year in zip(y_clubs_list, y_years_list):
        append_to_xml_tree(career, youth_club, youth_year, 'youth', title)

    # parse senior clubs & years
    # TODO club string does not start with a letter (e.g. '-> ')
    s_clubs_list = re.findall(r'\bclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    s_years_list = re.findall(r'\byears\d\s*=\s*(.*)\n', infobox_string)
    for senior_club, senior_year in zip(s_clubs_list, s_years_list):
        append_to_xml_tree(career, senior_club, senior_year, 'senior', title)

    # parse national clubs & years
    n_clubs_list = re.findall(r'\bnationalteam\d\s*=\s*(.*?)[|\n]', infobox_string)
    n_years_list = re.findall(r'\bnationalyears\d\s*=\s*(.*)\n', infobox_string)
    for national_club, national_year in zip(n_clubs_list, n_years_list):
        append_to_xml_tree(career, national_club, national_year, 'senior', title)

    return career


def parse_team_squad_text(text) -> str or None:
    if re.search(r'start', text, re.DOTALL):
        return re.findall(r'start(.*)end', text, re.DOTALL)[0]
    return None


def parse_table_senior(text, team_name, _name_1, _name_2) -> ET.Element or None:
    squad_string = None
    career = None

    # select current senior team
    squad_list = re.findall(r'[Ss]quad\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
    if squad_list:
        squad_string = parse_team_squad_text(max(squad_list, key=len))
    if squad_string is None:
        squad_list = re.findall(r'[Ff]irst\steam\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
        squad_string = parse_team_squad_text(max(squad_list, key=len))

    for unwanted_chars in '{}[]*':
        squad_string = squad_string.replace(unwanted_chars, '')

    # select only player names
    names_list = re.findall(r'\|\s?name=(.*?)[|\n<]', squad_string)

    # if only of them is in the team create an xml structure with the data
    if _name_1 in names_list:
        if career is None:
            career = ET.Element('career')
        append_to_xml_tree(career, team_name, '2020', 'senior', _name_1)

    if _name_2 in names_list:
        if career is None:
            career = ET.Element('career')
        append_to_xml_tree(career, team_name, '2020', 'senior', _name_2)

    return career


def get_xml_title(tree_root) -> str:
    return [child_.text for child_ in tree_root if child_.tag == 'title'][0]


def get_xml_text(tree_root) -> str:
    return [grandchild.text
            for child_ in tree_root
            for grandchild in child_
            if grandchild.tag == 'text'][0]


def check_possibility(new_entry, other_player_list):
    club_name = new_entry[1]
    club_type = new_entry[3]

    year_1, year_2 = None, None
    if '–' in new_entry[2]:
        year_1, year_2 = re.split('–', new_entry[2])
    elif len(new_entry[2]) == 4:
        year_1 = new_entry[2]
    elif new_entry[2][-1] == '-':
        year_1 = new_entry[2][:-1]

    # x-y and a-b
    for entry in other_player_list:
        if entry[3] == club_type:
            if entry[1] == club_name:
                # xxxx-yyyy
                if '–' in entry[2] and entry[2][-1] != '–':
                    entry_year_1, entry_year_2 = re.split('–', entry[2])
                    # a <= x <= b
                    if int(entry_year_1) <= int(year_1) <= int(entry_year_2):
                        # TODO something better
                        print('They played together.')
                    # x <= a <= y
                    elif int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')
                # xxxx
                elif len(entry[2]) == 4:
                    entry_year_1 = entry[2]
                    # a == x  OR a == y
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                    # x <= a <= y
                    if year_2 is not None:
                        if int(year_1) <= int(entry_year_1) <= int(year_2):
                            print('They played together.')
                # xxxx-
                elif entry[2][-1] == '–':
                    entry_year_1 = entry[2][:-1]
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                    if year_2 is not None:
                        if int(year_1) <= int(entry_year_1) <= int(year_2):
                            print('They played together.')


def update_player_list(root_, player_list, other_player_list):
    temp_list = list()
    for child_ in root_:
        temp_list.append(child_.text)

    if len(other_player_list) > 0:
        check_possibility(temp_list, other_player_list)
    if temp_list not in player_list:
        player_list.append(temp_list)


if __name__ == '__main__':
    # parse into a tree structure using xml parser
    root = ET.fromstring(open('../data/fcBarcelona.xml', 'r', encoding='utf-8').read())
    page_title = get_xml_title(root)
    xml_text = get_xml_text(root)

    # TODO temp names
    MATCH = None
    name_1 = 'Lionel Messi'
    name_2 = 'Philippe Coutinho'
    la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()

    if is_footballer_name(name_1, name_2, page_title):
        if is_footballer(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title)
            # TODO parse_text()
    elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
        MATCH = parse_table_senior(xml_text, page_title, name_1, name_2)
        # TODO parse_table_youth()
        # TODO parse_football_squad_on_pitch()


    player_ONE = None
    player_TWO = None
    list_ONE = list()
    list_TWO = list()

    if MATCH is not None:
        for child in MATCH:
            # create list where first member is player name
            # subsequent memberss are in the form of
            # club_name, years, type

            for g_child in child:
                if g_child.tag == 'player_name':
                    if player_ONE is None:
                        player_ONE = g_child.text
                        update_player_list(child, list_ONE, list_TWO)

                    elif player_TWO is None and player_ONE != g_child.text:
                        player_TWO = g_child.text
                        update_player_list(child, list_TWO, list_ONE)

                    elif player_ONE == g_child.text:
                        update_player_list(child, list_ONE, list_TWO)

                    elif player_TWO == g_child.text:
                        update_player_list(child, list_TWO, list_ONE)
                else:
                    break

# ----------------------------------------------------------------------------------------------------------------------

    # parse into a tree structure using xml parser
    root = ET.fromstring(open('../data/michaelEssien.xml', 'r', encoding='utf-8').read())
    page_title = get_xml_title(root)
    xml_text = get_xml_text(root)

    MATCH = None

    if is_footballer_name(name_1, name_2, page_title):
        if is_footballer(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title)
            # TODO parse_text()
    elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
        MATCH = parse_table_senior(xml_text, page_title, name_1, name_2)
        # TODO parse_table_youth()
        # TODO parse_football_squad_on_pitch()

    if MATCH is not None:
        for child in MATCH:
            # create list where first member is player name
            # subsequent memberss are in the form of
            # club_name, years, type

            for g_child in child:
                if g_child.tag == 'player_name':
                    if player_ONE is None:
                        player_ONE = g_child.text
                        update_player_list(child, list_ONE, list_TWO)

                    elif player_TWO is None and player_ONE != g_child.text:
                        player_TWO = g_child.text
                        update_player_list(child, list_TWO, list_ONE)

                    elif player_ONE == g_child.text:
                        update_player_list(child, list_ONE, list_TWO)

                    elif player_TWO == g_child.text:
                        update_player_list(child, list_TWO, list_ONE)
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
    <club>
        <player_name>ALEXANDER</player_name>
        <name>xxx</name>
        <years>yyy</years>
        <type>zzz</type>
    </club>
    <club>
        <player_name>JONATHAN</player_name>
        ...
    </club>
</career>
"""