from kafka import KafkaProducer
from io import StringIO
import re

# TODO parse_table_youth()
# TODO parse_football_squad_on_pitch()

topic = 'vinf'
producer = KafkaProducer(bootstrap_servers='localhost:9092')
path = 'C:/Users/krock/OneDrive/Documents/FIIT/Inžinier/1. Semester/VINF/Projekt/result.xml'

with open(path, 'r', encoding='utf-8') as file:
    for line in file:
        start_tag = re.findall(r'<(.*?)\s*>', line)
        if start_tag and start_tag[0] == 'page':       # TODO better solution for encapsulating tag
            start_tag = start_tag[0]
            file_strio = StringIO()
            file_strio.write(line)

            for page_content_line in file:
                end_tag = re.findall(r'</(.*?)\s*>', page_content_line)
                if end_tag and end_tag[0] == start_tag:
                    file_strio.write(page_content_line)
                    try:
                        producer.send(topic=topic, value=file_strio.getvalue().encode('utf-8'))
                    except Exception as e:
                        print(e)
                    break
                file_strio.write(page_content_line)
