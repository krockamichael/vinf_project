from kafka import KafkaProducer
from time import sleep
import re

pattern = re.compile('[\W_]')
topic = 'vinf'  # or test
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# write to pesudofile..? --> works probably, TODO DOCUMENT PROPERLY
from io import StringIO

with open('../data/playedTogether.xml', 'r', encoding='utf-8') as file:
    for line in file:
        if re.search('^<.*>$', line.strip()):  # TODO, what if there's an attribute or enclosing tag
            tag = pattern.sub('', line)
            file_str = StringIO()
            file_str.write(line)
            for line_s in file:
                if re.search('^</.*>$', line_s.strip()) and pattern.sub('', line_s) == tag:  # TODO, what if there's an attribute
                    file_str.write(line_s)
                    try:
                        producer.send(topic=topic, value=file_str.getvalue().encode('utf-8'))
                        sleep(10)
                    except Exception as e:
                        print(e)
                    break
                file_str.write(line_s)
