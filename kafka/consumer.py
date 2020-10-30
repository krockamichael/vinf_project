from kafka import KafkaConsumer, KafkaProducer
from parsing.text_parsing import *
from parsing.wrappers import get_xml_title, get_xml_text
import xml.etree.ElementTree as ET

topic = 'vinf'
final_topic = 'final_topic'
consumer = KafkaConsumer(topic,
                         group_id='abc',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         # partition_assignment_strategy='roundrobin',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         value_deserializer=lambda x: ET.fromstring(x.decode('utf-8')))

for message in consumer:
    page_title = get_xml_title(message.value)
    xml_text = get_xml_text(message.value)

    # TODO temp names
    MATCH = None
    name_1 = 'Lionel Messi'
    name_2 = 'Philippe Coutinho'
    la_liga, bundesliga, serie_a, premier_league, ligue_1 = load_top_football_clubs()

    if is_footballer_name(name_1, name_2, page_title):
        if is_footballer(xml_text, page_title):
            MATCH = parse_infobox(xml_text, page_title)
            # TODO parse_text()
    elif is_top_football_club(page_title, la_liga, bundesliga, serie_a, premier_league, ligue_1):
        MATCH = parse_table_senior(xml_text, page_title, name_1, name_2)
        # TODO parse_table_youth()
        # TODO parse_football_squad_on_pitch()

    if MATCH is not None:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send(topic=final_topic, value=ET.tostring(MATCH, encoding='utf-8'))
