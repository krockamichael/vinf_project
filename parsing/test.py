from parsing.text_parsing import is_football_player, parse_infobox, is_football_club, parse_table_senior
from parsing.wrappers import prettify, get_xml_title, get_xml_text
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from io import StringIO
import re

"""parsing and comparison logic 1.0"""
# def main_test(path, player_1, player_2, list_1, list_2):
#     MATCH = None
#
#     new_root = Element('pages')
#
#     # parse into a tree structure using xml parser
#     root = ET.fromstring(open(path, 'r', encoding='utf-8').read())
#     page_title = get_xml_title(root)
#     xml_text = get_xml_text(root)
#
#     if is_footballer_name(name_1, name_2, page_title):
#         if is_football_player(xml_text, page_title):
#             MATCH = parse_infobox(xml_text, page_title, new_root)

#     elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
#         MATCH = parse_table_senior(xml_text, page_title, name_1, name_2)
#
#     if MATCH is not None:
#         for child in MATCH:
#             # create list where first member is player name
#             # subsequent memberss are in the form of
#             # club_name, years, type
#
#             for g_child in child:
#                 if g_child.tag == 'player_name':
#                     if player_1 is None:
#                         player_1 = g_child.text
#                         update_player_list(child, list_1, list_2)
#
#                     elif player_2 is None and player_1 != g_child.text:
#                         player_2 = g_child.text
#                         update_player_list(child, list_2, list_1)
#
#                     elif player_1 == g_child.text:
#                         update_player_list(child, list_1, list_2)
#
#                     elif player_2 == g_child.text:
#                         update_player_list(child, list_2, list_1)
#                 else:
#                     break


def main_parsing_logic(file_str_: StringIO) -> Element or None:
    # we have one page in file_str_
    root_ = ET.fromstring(file_str_.getvalue().encode('utf-8'))
    page_title_ = get_xml_title(root_)
    xml_text_ = get_xml_text(root_)
    if xml_text_ is None:
        return

    if is_football_player(xml_text_, page_title_):
        return parse_infobox(xml_text_, page_title_)

    elif is_football_club(xml_text_):
        return parse_table_senior(xml_text_, page_title_)


if __name__ == '__main__':

    """parse 'result' file into final xml file"""
    path = 'C:/Users/krock/OneDrive/Documents/FIIT/Inžinier/1. Semester/VINF/Projekt/result.xml'
    temp_path = '../data/example_club_page.xml'
    with open(temp_path, 'r', encoding='utf-8') as file:
        for line in file:
            start_tag = re.findall(r'<(.*?)\s*>', line)
            if start_tag and start_tag[0] != 'pages':
                start_tag = start_tag[0]
                file_strio = StringIO()
                file_strio.write(line)

                for page_content_line in file:
                    end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
                    if end_tag and end_tag[0] == start_tag:  # closing tag
                        file_strio.write(page_content_line)
                        break
                    file_strio.write(page_content_line)

            # we have one page in file_str
            out_path = '../data/temp.xml'
            with open(out_path, 'a', encoding='utf-8') as out_file:
                result = main_parsing_logic(file_strio)
                if result is not None:
                    out_file.writelines(prettify(xml_string=ET.tostring(result, encoding='utf-8'))[23:-1])
                    out_file.write('\n')
