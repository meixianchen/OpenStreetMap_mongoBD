# OpenStreetMap_mongoBD


OpenStreetMap Data Wrangle Project with MongoDB

Map area:
Zurich, Switzerland

Author:Meixian Chen


data: 
zurich_switzerland.osm: Original data downloaded from https://mapzen.com/data/metro-extracts/metro/zurich_switzerland/

clean.json: cleaned data of zurich map


code:

audit.py: checking data quality and output the problems I found from the data

clean.py: cleaning the data, and store them in a more logical representation in clean.json file. 

stats_mongodb.py: 
First run the follow command line in the system shell to import the json file into mongodb database:
mongoimport --db sample --collection sulishi --drop --file ../data/clean.json
Then run stats_mongodb.py to see the results (the expected output is also saved in stats_results.txt)


