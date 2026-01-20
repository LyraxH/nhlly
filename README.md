# nhlly
 Simple CLI based NHL stats puller application

## usage
   python nhlly.py

#### (s)tandings
   Prints current NHL standings. Sortable by (p)oints, (d)ivision, or (t)eam

#### (g)ames
   Prints current NHL schedule. (y)esterday takes you back a day, (t)omorrow takes you ahead one. 
   Games are assigned numbers 1-x based on how many games are on that day, enter an assigned number to get more information about that game
   (s)tats brings up the game stats for each player on a team from that game. (x) switches which team is covered.

#### (r)oster
   Prints current team roster. Shows most relevant stats.
   Sortable by (f)irst name, (g)ames, (p)oints, (+/-) plus-minus, (pim) penalty minutes, (toi) time on ice, or (fow) faceoff win pctg

#### (q)uit 
   Exits the program

### To-Do
#### Standings
- [ ] Color code if a team is in a divisional playoff slot
- [ ] Color code if a team is in a conference playoff slot
- [ ] Color code if a team is in a wildcard slot
- [ ] Add games played / left
#### Players
- [ ] Add a basic player info sheet
- [ ] Add a player stats sheet
- [ ] Player previous teams
#### Teams
- [ ] Add team info sheet (fun facts maybe? LMAO)
- [ ] Add team schedule
- [ ] Add ability to access team roster (to roster page)
#### Home Menu
- [ ] Add way to search for players
- [ ] Add way to search for teams
- [ ] Add way to search for games
#### Games
- [ ] Maybe even ways to find individual stats from certain games
- [ ] add play by play view to game view
#### General
- [ ] Add a help menu (thats the github readme idiot)
- [ ] Add images (??)


### Change Log
20-01: leafs lose
   Implemented at a glance game view
   Implemented player stats view
   Implemented team stats view
   Added ability to toggle which team is being viewed during at a glance game view
19-01:
   Implemented usage of colors with an SQL database to hold all team info
   Changed the projects structure by compartmentalizing the code into different files
   Added ability to see schedule info as well as today/tomorrow schedules as well
   Added ability to see game score by game id based on the schedule
18-01
   Implemented basic API calling
   Implemented Standings
   Added basic roster look up
   Implemented roster sort by features