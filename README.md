# vinf_project
The purpose of this project is to answer whether two football players could have played together in one football team using enwiki-latest-pages-articles.xml data.

Repository structure:
data - test data used for testing parsing and / or sending using kafka
kafka/server - kafka prerequisites, zookeeper and kafka server (start in this order)
kafka - consumer, final_consumer and producer source code
parsing - testing contains majority of application logic for parsing wikipedia pages, parsing teams is a script to parse teams from top 5 leagues into a dataframe in the form [player_name, club_name, club_type (youth, senior, national)], input_file is a script for parsing enwiki-latest-pages-articles to produce a resulting file which contains pages about football  
