from parsing.text_parsing import *
from parsing.wrappers import get_xml_title, get_xml_text
import xml.etree.ElementTree as ET
from io import StringIO
from time import time
import re

"""
def main_test(path, player_1, player_2, list_1, list_2):
    MATCH = None

    new_root = Element('pages')

    # parse into a tree structure using xml parser
    root = ET.fromstring(open(path, 'r', encoding='utf-8').read())
    page_title = get_xml_title(root)
    xml_text = get_xml_text(root)

    if is_footballer_name(name_1, name_2, page_title):
        if is_football_player(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title, new_root)
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
                    if player_1 is None:
                        player_1 = g_child.text
                        update_player_list(child, list_1, list_2)

                    elif player_2 is None and player_1 != g_child.text:
                        player_2 = g_child.text
                        update_player_list(child, list_2, list_1)

                    elif player_1 == g_child.text:
                        update_player_list(child, list_1, list_2)

                    elif player_2 == g_child.text:
                        update_player_list(child, list_2, list_1)
                else:
                    break
"""

if __name__ == '__main__':
    """for main_test()"""
    # name_1 = 'Lionel Messi'
    # name_2 = 'Michael Essien'
    #
    # player_ONE = None
    # player_TWO = None
    # list_ONE = list()
    # list_TWO = list()
    #
    # la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()
    #
    # main_test('../data/michaelEssien.xml', player_ONE, player_TWO, list_ONE, list_TWO)
    # main_test('../data/fcBarcelona.xml', player_ONE, player_TWO, list_ONE, list_TWO)

    """how to get attribute value"""
    # root = ET.parse('../data/temp.xml').getroot()
    # print(root.attrib['name'])

    start_time = time()

    with open('C:/Users/krock/Desktop/FIIT/Inžinier/1. Semester/VINF/Projekt/result.xml', 'r', encoding='utf-8') as file:
        for line in file:
            start_tag = re.findall(r'<(.*?)\s*>', line)
            if start_tag:  # TODO, what if there's an enclosing tag <PAGES><page>...</page><page>...</page></PAGES>
                start_tag = start_tag[0]
                file_str = StringIO()
                file_str.write(line)

                for line_s in file:
                    end_tag = re.findall(r'</(.*?)\s*>', line_s)
                    if end_tag and end_tag[0] == start_tag:
                        file_str.write(line_s)
                        break
                    file_str.write(line_s)

            # we have one page in file_str
            root = ET.fromstring(file_str.getvalue().encode('utf-8'))
            page_title = get_xml_title(root)
            xml_text = get_xml_text(root)
            if xml_text is None:
                continue

            if is_football_player(xml_text, page_title):
                parse_infobox(xml_text, page_title)

            elif is_football_club(xml_text):
                parse_table_senior(xml_text, page_title)
    print(time() - start_time)
