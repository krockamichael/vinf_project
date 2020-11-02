from parsing.wrappers import check_possibility, update_player_list
import xml.etree.ElementTree as ET
from io import StringIO
import re


if __name__ == '__main__':
    player_ONE = 'Lionel Messi'
    player_TWO = 'Philippe Coutinho'
    list_ONE = list()
    list_TWO = list()

    path = '../data/final_xml_RESULT.xml'

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            self_enclosed_tag = re.findall(r'<(.*?)/>', line)
            if len(self_enclosed_tag) > 0:
                continue

            start_tag = re.findall(r'<(.*?)\s', line)
            if start_tag:  # TODO solution for encapsulating tag
                start_tag = start_tag[0]
                file_strio = StringIO()
                file_strio.write(line)

                for page_content_line in file:
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
                                    if g_child.text == player_ONE:
                                        temp_list = list()
                                        temp_list.append(child.tag)  # youth / senior / national
                                        temp_list.append(club_name)  # club name
                                        temp_list.append(child.attrib['year'])  # club years
                                        if temp_list not in list_ONE:
                                            list_ONE.append(temp_list)
                                            if len(list_TWO) > 0:
                                                check_possibility(temp_list, list_TWO)

                                    elif g_child.text == player_TWO:
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
                            if root.attrib['name'] == player_ONE:
                                for child in root:  # child --> youth / senior / national ( club.name (years.text), club.name (years.text), ... )
                                    update_player_list(child, list_ONE, list_TWO)
                            # second player
                            elif root.attrib['name'] == player_TWO:
                                for child in root:  # child --> youth / senior / national ( club.name (years.text), club.name (years.text), ... )
                                    update_player_list(child, list_TWO, list_ONE)
                        ### LOGIC END ###
                        break
                    file_strio.write(page_content_line)
