from parsing.wrappers import player_xml_tree, club_xml_tree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from unidecode import unidecode
from typing import Tuple
import regex
import re


# def load_top_football_clubs() -> Tuple[list, list, list, list, list]:
#     with open('../data/top_team_names.txt', 'r', encoding='utf-8') as f:
#         # file format: league name, club names, empty line
#         f.readline()    # ignore league name
#         la_liga_ = [next(f).strip() for x in range(20)]
#         f.readline(), f.readline()  # ignore league name and empty line
#         bundesliga_ = [next(f).strip() for x in range(18)]
#         f.readline(), f.readline()
#         serie_a_ = [next(f).strip() for x in range(20)]
#         f.readline(), f.readline()
#         premier_league_ = [next(f).strip() for x in range(20)]
#         f.readline(), f.readline()
#         ligue_1_ = [next(f).strip() for x in range(20)]
#
#     return la_liga_, bundesliga_, serie_a_, premier_league_, ligue_1_


# def is_top_football_club(title, La_Liga=None, Bundesliga=None, Serie_A=None, Premier_League=None, Ligue_1=None) -> bool:
#     if not all(v is not None for v in [La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1]):
#         La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1 = load_top_football_clubs()
#
#     if [x for x in (La_Liga, Bundesliga, Serie_A, Premier_League, Ligue_1) if title in x]:
#         return True
#     else:
#         return False


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


def is_football_player(text, title) -> bool:
    # check data in short description
    short_summary_string = regex.search(r'(?=\{[sS]hort\sdescription)(\{([^{}]|(?1))*\})', text)
    if short_summary_string is not None:
        short_summary_string = short_summary_string[0].lower()

        if 'football player' in short_summary_string or 'footballer' in short_summary_string:
            return True

    elif 'footballer' in title.lower():
        return True

    return False


def is_football_club(text) -> bool:
    # check data in short description
    short_summary_string = regex.search(r'(?=\{[sS]hort\sdescription)(\{([^{}]|(?1))*\})', text)

    # check data in infobox
    infobox_string = regex.search(r'(?=\{Infobox)(\{([^{}]|(?1))*\})', text)

    for item in (short_summary_string, infobox_string):
        if item is not None:
            item = item[0][:70].lower()
            if 'football' in item:
                if 'club' in item or 'team' in item:
                    if 'american football' not in item:     # todo better?
                        return True

    return False


def parse_infobox(text, title) -> Element or None:
    player = Element('player')
    player.set('name', title)

    # select infobox and remove unwanted characters
    infobox_string = regex.search(r'(?=\{Infobox)(\{([^{}]|(?1))*\})', text)
    if infobox_string is not None:
        infobox_string = infobox_string[0]
    else:
        return

    for unwanted_chars in '{}[]*':
        infobox_string = infobox_string.replace(unwanted_chars, '')

    # parse youth clubs & years
    y_clubs_list = re.findall(r'\byouthclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    y_years_list = re.findall(r'\byouthyears\d\s*=\s*(.*?)\s*[|\n]', infobox_string)
    for youth_club, youth_year in zip(y_clubs_list, y_years_list):
        player_xml_tree(player, youth_club, youth_year.replace('–', '-'), 'youth')

    # parse senior clubs & years
    # strip '-> ' loan signs
    s_clubs_list = re.findall(r'\bclubs\d\s*=\s*(.*?)[|\n]', infobox_string)
    s_years_list = re.findall(r'\byears\d\s*=\s*(.*?)\s*[|\n]', infobox_string)
    for senior_club, senior_year in zip(s_clubs_list, s_years_list):
        player_xml_tree(player, senior_club.strip('→ '), senior_year.replace('–', '-'), 'senior')

    # parse national clubs & years
    n_clubs_list = re.findall(r'\bnationalteam\d\s*=\s*(.*?)[|\n]', infobox_string)
    n_years_list = re.findall(r'\bnationalyears\d\s*=\s*(.*?)\s*[|\n]', infobox_string)
    for national_club, national_year in zip(n_clubs_list, n_years_list):
        player_xml_tree(player, national_club, national_year.replace('–', '-'), 'national')

    return player


def parse_team_squad_text(text) -> str or None:
    if re.search(r'start', text, re.DOTALL):
        return re.findall(r'start(.*)end|$', text, re.DOTALL)[0]
    return None


def parse_table_senior(text, team_name) -> Element or None:
    squad_string = None
    club = Element('club')
    club.set('name', team_name)

    # select current senior team
    squad_list = re.findall(r'[Ss]quad\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
    if squad_list is not None and len(squad_list) > 0:
        squad_string = parse_team_squad_text(max(squad_list, key=len))
    if squad_string is None:
        squad_list = re.findall(r'[Ff]irst\steam\s*={2,3}(.*?)={2,3}', text, re.DOTALL)
        if len(squad_list) == 0:
            return
        squad_string = parse_team_squad_text(max(squad_list, key=len))
    if squad_string == '':
        squad_string = squad_list[0]
    if squad_string is None:
        return

    for unwanted_chars in '{}*':
        squad_string = squad_string.replace(unwanted_chars, '')

    # select only player names
    names_list = re.findall(r'\|\s?name=\[\[(.*?)[\]\]|\n<]', squad_string)

    # decide club type, default senior
    club_type = 'senior'
    if 'national' in team_name:
        club_type = 'national'

    club_xml_tree(club, club_type, '2020', names_list)

    return club


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
            <club_name>xxx</club_name>
            <years>yyy</years>
            <type>zzz</type>
        </club>
        <club>
            <player_name>JONATHAN</player_name>
            ...
        </club>
    </career>
"""

"""
<player name="Michael Essien">
  <youth>
    <club name="Liberty Professionals F.C.">
      <years>1998-1999</years>
    </club>
  </youth>
  <senior>
    <club name="SC Bastia">
      <years>2000-2003</years>
    </club>
  </senior>
  <national>
    <club name="Ghana national football team">
      <years>2002-2014</years>
    </club>
  </national>
</player>
"""

"""
<club name="FC Barcelona">
  <youth year="2020">
    <player>johny</player>
  </youth>
  <senior year="2020">
    <player>cash</player>
  </senior>
</club>
"""