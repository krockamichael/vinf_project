import xml.etree.ElementTree as ET
from io import StringIO
import json
import re


index_dict = {}
path = '../data/final_xml_new.xml'
counter = 0
temp = 0

with open(path, 'r', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i != 0:
            counter = counter - temp
            counter = counter + 1 + i
            temp = i
        """
        logic should go something like:
            team name --> key in dict, value is position
                for player names in team --> keys in dict, team position as value (because i need "root" element)
            player name --> key in dict, value is position
                done, don't get team names because why :D no logic is tied to team names
                that raises a question, do I need to keep team names as keys?
                I probably don't, because I will never use them
                Extension of functionality if I wanted team names as keys in dict
        """
        self_enclosed_tag = re.findall(r'<(.*?)/>', line)
        if len(self_enclosed_tag) > 0:
            counter = counter - 1
            continue

        start_tag = re.findall(r'<(.*?)\s', line)  # TODO better regex, what if no attrib
        if start_tag:  # TODO solution for encapsulating tag
            start_tag = start_tag[0]
            file_strio = StringIO()
            file_strio.write(line)

            for j, page_content_line in enumerate(file): # todo there is a problem with line number!!
                end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
                if end_tag and end_tag[0] == start_tag:
                    file_strio.write(page_content_line)

                    ### LOGIC START ###
                    root = ET.fromstring(file_strio.getvalue().strip())

                    # CLUB
                    if root.tag == 'club':
                        club_name = root.attrib['name']
                        for child in root:
                            for g_child in child:   # g_child are players (names)
                                if g_child.text in index_dict:
                                    index_dict[g_child.text].extend([counter])
                                else:
                                    index_dict[g_child.text] = [counter]

                    # PLAYER
                    elif root.tag == 'player':
                        if root.attrib['name'] in index_dict:
                            index_dict[root.attrib['name']].extend([counter])
                        else:
                            index_dict[root.attrib['name']] = [counter]
                    ### LOGIC END ###
                    counter = counter + j
                    break
                file_strio.write(page_content_line)

with open('..\data\index.json', 'w', encoding='utf-8') as fp:
    json.dump(index_dict, fp, ensure_ascii=False, indent=4)
