# nhlly
 Simple CLI based NHL stats puller application

## usage
   python nhlly.py

#### (st)andings
   Prints current NHL standings. Sortable by (p)oints, (d)ivision, or (t)eam

#### (sc)hedule
   Prints current NHL schedule. (y)esterday takes you back a day, (t)omorrow takes you ahead one. 
   Games are assigned numbers 1-x based on how many games are on that day, enter an assigned number to get more information about that game

#### (r)oster
   Prints current team roster. 
   Sortable by (f)irst name, (g)ames, (p)oints, (+/-) plus-minus, (pim) penalty minutes, (toi) time on ice, or (fow) faceoff win pctg

#### (q)uit 
   Exits the program

### To-Do
#### Standings
- [ ] Color code if a team is in a divisional playoff slot
- [ ] Color code if a team is in a conference playoff slot
- [ ] Color code if a team is in a wildcard slot
- [ ] Add games played / left
- [ ] Add points percentage
#### Rosters
- [ ] Section off forwards from D men
- [ ] Add years played / rookie year indicator
#### Players
- [ ] I have no idea what I want to implement here.
- [ ] Add a basic player info sheet
- [ ] Add a player stats sheet
#### Teams
- [ ] Add team info sheet (fun facts maybe? LMAO)
- [ ] Add team schedule
- [ ] Add ability to access team roster (to roster page)
#### Home Menu
- [ ] Add way to search for players
- [ ] Add way to search for teams
- [ ] Add way to search for games
#### Games
- [ ] Add a way to find upcoming games for a certain team
- [ ] Maybe even ways to find individual stats from certain games
#### General
- [ ] Add a help menu
- [ ] Add images (??)


### Change Log
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