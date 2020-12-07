from parsing.text_parsing import is_footballer_name, name_correction
from parsing.wrappers import check_possibility, update_player_list
import xml.etree.ElementTree as ET
from io import StringIO
from time import time
import json
import re


if __name__ == '__main__':
    start_time = time()
    index_dict = json.load(open('..\data\index.json', 'r', encoding='utf-8'))

    player_ONE = 'lionel messi'
    # Paul Mucureezi
    player_TWO = 'philippe coutinho'
    # Mustafa Kizza

    player_ONE = name_correction(player_ONE, index_dict)
    player_TWO = name_correction(player_TWO, index_dict)

    list_ONE = list()
    list_TWO = list()

    path = '../data/final_xml_new.xml'
    counter = 0

    with open(path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i != 0:
                counter = counter + 1

            if counter in index_dict[player_ONE] or counter in index_dict[player_TWO]:
                self_enclosed_tag = re.findall(r'<(.*?)/>', line)
                if len(self_enclosed_tag) > 0:
                    continue

                start_tag = re.findall(r'<(.*?)\s', line)   # TODO better regex, what if no attrib
                if start_tag:  # TODO solution for encapsulating tag
                    start_tag = start_tag[0]
                    file_strio = StringIO()
                    file_strio.write(line)

                    for j, page_content_line in enumerate(file):
                        end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
                        if end_tag and end_tag[0] == start_tag:
                            file_strio.write(page_content_line)

                            ### LOGIC START ###
                            root = ET.fromstring(file_strio.getvalue().strip())

                            # list member form: club_type, club_name, years
                            # CLUB
                            if root.tag == 'club':
                                club_name = root.attrib['name']
                                for child in root:
                                    for g_child in child:
                                        if is_footballer_name(g_child.text, player_ONE):
                                            temp_list = list()
                                            temp_list.append(child.tag)  # youth / senior / national
                                            temp_list.append(club_name)  # club name
                                            temp_list.append(child.attrib['year'])  # club years
                                            if temp_list not in list_ONE:
                                                list_ONE.append(temp_list)
                                                if len(list_TWO) > 0:
                                                    check_possibility(temp_list, list_TWO)

                                        elif is_footballer_name(g_child.text, player_TWO):
                                            temp_list = list()
                                            temp_list.append(child.tag)  # youth / senior / national
                                            temp_list.append(club_name)  # club name
                                            temp_list.append(child.attrib['year'])  # club years
                                            if temp_list not in list_TWO:
                                                list_TWO.append(temp_list)
                                                if len(list_ONE) > 0:
                                                    check_possibility(temp_list, list_ONE)

                            # PLAYER
                            elif root.tag == 'player':
                                # first player
                                if is_footballer_name(root.attrib['name'], player_ONE):
                                    for child in root:  # child --> youth / senior / national ( club.name (years.text), club.name (years.text), ... )
                                        update_player_list(child, list_ONE, list_TWO)
                                # second player
                                elif is_footballer_name(root.attrib['name'], player_TWO):
                                    for child in root:  # child --> youth / senior / national ( club.name (years.text), club.name (years.text), ... )
                                        update_player_list(child, list_TWO, list_ONE)
                            ### LOGIC END ###
                            counter = counter + j + 1
                            break
                        file_strio.write(page_content_line)

    print("--- %.2f seconds ---" % (time() - start_time))
