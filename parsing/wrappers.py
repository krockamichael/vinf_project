from xml.etree.ElementTree import SubElement
from xml.etree import ElementTree as ET
from xml.dom import minidom
import re


def get_xml_title(tree_root) -> str:
    return [child_.text for child_ in tree_root if child_.tag == 'title'][0]


def get_xml_text(tree_root) -> str:
    return [grandchild.text
            for child_ in tree_root
            for grandchild in child_
            if grandchild.tag == 'text'][0]


def prettify(elem) -> str:
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def append_to_xml_tree_Club_PName_CName_Years_Type(career_root, club_name, years, club_type, player_name):
    club = SubElement(career_root, 'club')

    p_name = SubElement(club, 'player_name')
    p_name.text = player_name

    c_name = SubElement(club, 'club_name')
    c_name.text = club_name

    years_ = SubElement(club, 'years')
    years_.text = years

    c_type = SubElement(club, 'type')
    c_type.text = club_type


def player_xml_tree(player, club_name, years, club_type):
    club_type_element = [child for child in player if child.tag == club_type]

    if len(club_type_element) == 0:
        club_type_element = SubElement(player, club_type)
    else:
        club_type_element = club_type_element[0]

    club_element = SubElement(club_type_element, 'club')
    club_element.set('name', club_name)

    years_element = SubElement(club_element, 'years')
    years_element.text = years


def club_xml_tree(club, club_type, year, player_names):
    club_type_element = [child for child in club if child.tag == club_type]

    if len(club_type_element) == 0:
        club_type_element = SubElement(club, club_type)
    else:
        club_type_element = club_type_element[0]
    club_type_element.set('year', year)

    for name in player_names:
        name_element = SubElement(club_type_element, 'player')
        name_element.text = name


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
        if entry[3] == club_type and entry[1] == club_name:

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
