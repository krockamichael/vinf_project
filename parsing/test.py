from parsing.text_parsing import *
from parsing.wrappers import get_xml_title, get_xml_text, update_player_list, check_possibility
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
#             # TODO parse_text()
#     elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
#         MATCH = parse_table_senior(xml_text, page_title, name_1, name_2)
#         # TODO parse_table_youth()
#         # TODO parse_football_squad_on_pitch()
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


"""parsing logic"""
# def main_parsing_logic(file_str_: StringIO) -> Element or None:
#     # we have one page in file_str_
#     root_ = ET.fromstring(file_str_.getvalue().encode('utf-8'))
#     page_title_ = get_xml_title(root_)
#     xml_text_ = get_xml_text(root_)
#     if xml_text_ is None:
#         return
#
#     if is_football_player(xml_text_, page_title_):
#         return parse_infobox(xml_text_, page_title_)
#
#     elif is_football_club(xml_text_):
#         return parse_table_senior(xml_text_, page_title_)



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
    # main_test('../data/club_example_page.xml', player_ONE, player_TWO, list_ONE, list_TWO)

    """how to get attribute value"""
    # root = ET.parse('../data/final_xml_RESULT.xml').getroot()
    # print(root.attrib['name'])

    """parse 'result' file into final xml file"""
    # start_time = time()
    # path = 'C:/Users/krock/OneDrive/Documents/FIIT/Inžinier/1. Semester/VINF/Projekt/result.xml'
    # with open(path, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         start_tag = re.findall(r'<(.*?)\s*>', line)
    #         if start_tag and start_tag[0] != 'pages':
    #             start_tag = start_tag[0]
    #             file_strio = StringIO()
    #             file_strio.write(line)
    #
    #             for page_content_line in file:
    #                 end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
    #                 if end_tag and end_tag[0] == start_tag:     # closing tag
    #                     file_strio.write(page_content_line)
    #                     break
    #                 file_strio.write(page_content_line)
    #
    #         # we have one page in file_str
    #         out_path = '../data/final_xml_RESULT.xml'
    #         with open(out_path, 'a', encoding='utf-8') as out_file:
    #             result = main_parsing_logic(file_strio)
    #             if result is not None:
    #                 out_file.writelines(prettify(xml_string=ET.tostring(result, encoding='utf-8'))[23:-1])
    #                 out_file.write('\n')
    #
    # print(time() - start_time)

    """read final input file and check if players played together"""
    # player_ONE = 'Lionel Messi'
    # player_TWO = 'Philippe Coutinho'
    # list_ONE = list()
    # list_TWO = list()
    #
    # path = '../data/final_xml_RESULT.xml'
    #
    # with open(path, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         self_enclosed_tag = re.findall(r'<(.*?)/>', line)
    #         if len(self_enclosed_tag) > 0:
    #             continue
    #
    #         start_tag = re.findall(r'<(.*?)\s', line)
    #         if start_tag:  # TODO solution for encapsulating tag
    #             start_tag = start_tag[0]
    #             file_strio = StringIO()
    #             file_strio.write(line)
    #
    #             for page_content_line in file:
    #                 end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
    #                 if end_tag and end_tag[0] == start_tag:
    #                     file_strio.write(page_content_line)
    #
    #                     ### LOGIC START ###
    #                     root = ET.fromstring(file_strio.getvalue().strip())
    #
    #                     # create list where first member is player name
    #                     # subsequent memberss are in the form of
    #                     # list member form: club_type, club_name, years
    #                     if root.tag == 'club':
    #                         club_name = root.attrib['name']
    #                         for child in root:
    #                             for g_child in child:
    #                                 if g_child.text == player_ONE:
    #                                     temp_list = list()
    #                                     temp_list.append(child.tag)  # youth / senior / national
    #                                     temp_list.append(club_name)  # club name
    #                                     temp_list.append(child.attrib['year'])  # club years
    #                                     if temp_list not in list_ONE:
    #                                         list_ONE.append(temp_list)
    #                                         if len(list_TWO) > 0:
    #                                             check_possibility(temp_list, list_TWO)
    #
    #                                 elif g_child.text == player_TWO:
    #                                     temp_list = list()
    #                                     temp_list.append(child.tag)  # youth / senior / national
    #                                     temp_list.append(club_name)  # club name
    #                                     temp_list.append(child.attrib['year'])  # club years
    #                                     if temp_list not in list_TWO:
    #                                         list_TWO.append(temp_list)
    #                                         if len(list_ONE) > 0:
    #                                             check_possibility(temp_list, list_ONE)
    #
    #                     # PLAYER
    #                     elif root.tag == 'player':
    #                         # first player
    #                         if root.attrib['name'] == player_ONE:
    #                             for child in root:  # child --> youth / senior / national
    #                                 update_player_list(child, list_ONE, list_TWO)
    #                         # second player
    #                         elif root.attrib['name'] == player_TWO:
    #                             for child in root:  # child --> youth / senior / national
    #                                 update_player_list(child, list_TWO, list_ONE)
    #                     ### LOGIC END ###
    #                     break
    #                 file_strio.write(page_content_line)
