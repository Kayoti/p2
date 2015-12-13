###P2
A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

###Structure
```
p1/
├── tournament.py
├── tournament.py
├── .gitignore.swp
├── .README.md
├── tournament.sql/

```		
###Installation

To install this app you need to have the following prerequests first:
* Python environment running on your machine (windows,mac,linux) if you do not have python installed please search (python download) using your favorite search engine and follow the instructions.
* You will also need to have postgresql installed.
for windows make sure you have correctly setup postgresql environment variable on your machine
* make sure you replace the database info in tournament.sql to match yours
* On windows launch pgadmin GUI connect to server and create your database, you will also need to configure users and database permissions--> (youtube is your best here friend)
* You also need to add postgre module in python you can use `pip install psycopg2` make sure pip is setup as well
* A word from the wise---> DO NOT EVER TRY TO USE/WORK WITH VIGRANT ON WINDOWS MACHINES IT IS A NIGHTMARE!!!


###License
Code released under the MIT license.
