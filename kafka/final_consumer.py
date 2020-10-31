from kafka import KafkaConsumer
from parsing.wrappers import prettify

out_path = '../data/final_xml_ENWIKI.xml'
final_topic = 'final_topic'
consumer = KafkaConsumer(final_topic,
                         group_id='final',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         value_deserializer=lambda x: x.decode('utf-8'))

with open(out_path, 'a', encoding='utf-8') as out_file:
    for message in consumer:
        # get string value, leave out opening <xml version="1.0"..../> tag
        a = prettify(xml_string=message.value)[23:-1]
        out_file.write(a)
        out_file.write('\n')

        # print out player / club name
        print(message.value[:40])
