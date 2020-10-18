from parsing.testing import parse_table_senior, is_top_football_club
import xml.etree.ElementTree as ET


if __name__ == '__main__':
    # parse incoming message into a tree structure using xml parser
    root = ET.fromstring(open('../data/only_teams.xml', 'r', encoding='utf-8').read())
    xml_texts = list()

    # cycle through 98 teams
    for i in range(98):
        temp_list = list([root[i][0].text])   # <title>
        [temp_list.append(child.text) for child in root[i][3] if child.tag == 'text']

        xml_texts.append(temp_list)

    # get squad data
    FINAL = list()
    for i in xml_texts:
        if is_top_football_club(i[0]):
            FINAL.append(parse_table_senior(i[1], i[0]))

print('a')
