from xml.etree.ElementTree import SubElement
from xml.etree import ElementTree as ET
from xml.dom import minidom
import re


def get_xml_title(tree_root: ET.Element) -> str:
    return [child_.text for child_ in tree_root if child_.tag == 'title'][0]


def get_xml_text(tree_root: ET.Element) -> str:
    return [grandchild.text
            for child_ in tree_root
            for grandchild in child_
            if grandchild.tag == 'text'][0]


def prettify(elem=None, xml_string=None) -> str:
    rough_string = None
    if elem is not None:
        rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(xml_string or rough_string)
    return reparsed.toprettyxml(indent="  ")


def write_to_xml_file(element: ET.Element, output_file):
    ET.canonicalize(prettify(elem=element), out=output_file)
    output_file.write('\n')


def player_xml_tree(player, club_name, years, club_type):
    # check if the player already has an entry for this
    # club type and if so append to it, if not create new
    club_type_element = [child for child in player if child.tag == club_type]

    if len(club_type_element) == 0:
        club_type_element = SubElement(player, club_type)
    else:
        club_type_element = club_type_element[0]

    club_element = SubElement(club_type_element, 'club')
    club_element.set('name', club_name.strip())     # attribute

    years_element = SubElement(club_element, 'years')
    years_element.text = years


def club_xml_tree(club, club_type, year, player_names):
    # check if this type of club squad already exists
    # e.g. if <senior>, <national> or <youth> exists
    club_type_element = [child for child in club if child.tag == club_type]

    if len(club_type_element) == 0:
        # does not exist, create new and set year
        club_type_element = SubElement(club, club_type)
        club_type_element.set('year', year)
    else:
        # exists, if year is not the same create new
        club_type_element = club_type_element[0]
        if club_type_element.attrib['year'] != year:
            club_type_element = SubElement(club, club_type)
            club_type_element.set('year', year)

    # append player names to club type element
    # e.g. <senior> <player>johny</player>   <player>mark</player> ... </senior>
    for name in player_names:
        # make sure player name is unique
        if name not in [child.text for child in club_type_element]:
            name_element = SubElement(club_type_element, 'player')
            name_element.text = name


def check_possibility(new_entry, other_player_list):
    club_type = new_entry[0]
    club_name = new_entry[1]

    year_1, year_2 = None, None
    if '-' in new_entry[2]:
        year_1, year_2 = re.split('-', new_entry[2])
    elif len(new_entry[2]) == 4:
        year_1 = new_entry[2]
    elif new_entry[2][-1] == '-':
        year_1 = new_entry[2][:-1]

    # x-y and a-b
    for entry in other_player_list:
        if entry[0] == club_type and entry[1] == club_name:

            # xxxx-yyyy
            if '–' in entry[2] and entry[2][-1] != '–':
                entry_year_1, entry_year_2 = re.split('-', entry[2])

                if entry_year_1 != '' and entry_year_2 != '':
                    # a <= x <= b
                    if int(entry_year_1) <= int(year_1) <= int(entry_year_2):
                        # TODO something better
                        print('They played together.')
                        print(club_type + '\t' + club_name)

                    # x <= a <= y
                    elif int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')
                        print(club_type + '\t' + club_name)

            # xxxx
            elif len(entry[2]) == 4:
                entry_year_1 = entry[2]

                if year_1 != '' and year_2 != '':
                    # a == x  OR a == y
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                        print(club_type + '\t' + club_name)

                    # x <= a <= y
                    if year_2 is not None:
                        if int(year_1) <= int(entry_year_1) <= int(year_2):
                            print('They played together.')
                            print(club_type + '\t' + club_name)

            # xxxx-
            elif entry[2][-1] == '-':
                entry_year_1 = entry[2][:-1]

                if new_entry[2][-1] == '-':
                    print('They played together.')
                    print(club_type + '\t' + club_name)

                elif year_1 != '' and year_2 != '':
                    if int(entry_year_1) == int(year_1) or int(entry_year_1) == int(year_2):
                        print('They played together.')
                        print(club_type + '\t' + club_name)

                elif year_2 is not None:
                    if int(year_1) <= int(entry_year_1) <= int(year_2):
                        print('They played together.')
                        print(club_type + '\t' + club_name)


def update_player_list(root_, player_list, other_player_list):
    # xml element format --> youth / senior / national ( club.name (years.text), club.name (years.text), ... )
    # list format --> club_type, club_name, years
    for child_ in root_:
        temp_list = list()
        temp_list.append(root_.tag)              # youth / senior / national
        temp_list.append(child_.attrib['name'])  # club name
        temp_list.append(child_[0].text)         # club years
        if temp_list not in player_list:
            player_list.append(temp_list)
            if len(other_player_list) > 0:
                check_possibility(temp_list, other_player_list)
