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
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         value_deserializer=lambda x: ET.fromstring(x.decode('utf-8')))

for message in consumer:
    MATCH = None
    page_title = get_xml_title(message.value)
    xml_text = get_xml_text(message.value)

    if xml_text is None:
        continue

    if is_football_player(xml_text, page_title):
        MATCH = parse_infobox(xml_text, page_title)

    elif is_football_club(xml_text):
        MATCH = parse_table_senior(xml_text, page_title)

    # MATCH is an element containing information about football club / player
    if MATCH is not None:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send(topic=final_topic, value=ET.tostring(MATCH, encoding='utf-8'))
