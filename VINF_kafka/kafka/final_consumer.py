from kafka import KafkaConsumer
import xml.etree.ElementTree as ET
from parsing.testing import update_player_list


final_topic = 'final_topic'
consumer = KafkaConsumer(final_topic,
                         group_id='abc',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         # partition_assignment_strategy='roundrobin',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         value_deserializer=lambda x: x.decode('utf-8'))

name_ONE = None
player_TWO = None
list_ONE = list()
list_TWO = list()

for message in consumer:
    root = None

    try:
        root = ET.fromstring(message.value)
    except Exception as e:
        print(e)

    for child in root:
        # create list where first member is player name
        # subsequent memberss are in the form of
        # club_name, years, type

        if child.tag == 'player_name':
            if name_ONE is None:
                name_ONE = child.text
                list_ONE.append(name_ONE)
                update_player_list(root, list_ONE, list_TWO)

            elif player_TWO is None and name_ONE != child.text:
                player_TWO = child.text
                list_TWO.append(player_TWO)
                update_player_list(root, list_TWO, list_ONE)

            elif name_ONE == child.text:
                update_player_list(root, list_ONE, list_TWO)

            elif player_TWO == child.text:
                update_player_list(root, list_TWO, list_ONE)
        else:
            break
