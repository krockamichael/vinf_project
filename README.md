# vinf_project
The purpose of this project is to answer whether two football players could have played together in one football team using enwiki-latest-pages-articles.xml data.

Repository structure:

data - test data used for testing parsing and / or sending using kafka

kafka/server - kafka prerequisites, zookeeper and kafka server (start in this order)

kafka - consumer, final_consumer and producer source code

parsing
- comparison.py - script for comparing two players if they played in the same team
- comparison_index.py - script for comparing two players if the played in the same team, using index
- indexing.py - script for generating index.json, inverted index
- test.py - file for testing new solutions
- text_parsing.py - functions for parsing data from text (from infobox, from senior squad tables)
- wrappers.py - helper functions for comparison and data retrieval