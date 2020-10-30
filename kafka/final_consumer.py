from kafka import KafkaConsumer
import xml.etree.ElementTree as ET
from parsing.text_parsing import update_player_list


final_topic = 'final_topic'
consumer = KafkaConsumer(final_topic,
                         group_id='final',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         # partition_assignment_strategy='roundrobin',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         value_deserializer=lambda x: x.decode('utf-8'))

player_ONE = None
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

        for g_child in child:
            if g_child.tag == 'player_name':
                if player_ONE is None:
                    player_ONE = g_child.text
                    update_player_list(child, list_ONE, list_TWO)

                elif player_TWO is None and player_ONE != g_child.text:
                    player_TWO = g_child.text
                    update_player_list(child, list_TWO, list_ONE)

                elif player_ONE == g_child.text:
                    update_player_list(child, list_ONE, list_TWO)

                elif player_TWO == g_child.text:
                    update_player_list(child, list_TWO, list_ONE)
            else:
                break
