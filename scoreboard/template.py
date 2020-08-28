from requests import get
from os import path
from time import time, sleep
from datetime import datetime
from random import randrange
# servicemilestoneswindow = ''.ljust(len("0 days, 0 hrs, 0 min, 11 sec        "))
# attackstatuswindow = ''.ljust(len("27   "))
# roundprogresswindow =  ''.ljust(len("26                   "))
# serviceprogresswindow = ''.ljust(len("planting flags         "))

# teamnames = ''.rjust(len("     black"))
# sla = ''.center(len("       "))
# attackscore, flag+, flag- = ''.center(len("     "))
# statuswindow = ''.ljust("       ")

starttime = 1597415400
endtime = 1598657400
template="""
                            \x1b[1;93mbi0s internal \x1b[1;96m28-08-2020\x1b[1;92m (blackStab)\033[0m
  
  \033[90m┌─\033[0m \x1b[0;36mservice milestones\033[90m ───────────────────────────────────┬─ \033[0;36mattack stats\033[90m ──────┐\033[0m
  \033[90m│  time in play    :\033[0m {timefstart}\033[90m│  rounds done :\033[0m {roundsdone}\033[90m│\033[0m
  \033[90m│  from firstblood :\033[0m {timefblood}\033[90m│ flags stolen :\033[0m {totalflags}\033[90m│\033[0m
  \033[90m│  firstblood team :\033[31m {bloodteam}\033[90m│ teams pwning :\033[0m {expteams}\033[90m│\033[0m
  \033[90m│  last flag steal :\033[0m {lastfsteal}\033[90m│  teams pwned :\033[0m {pwnedteams}\033[90m│\033[0m
  \033[90m├─ \x1b[0;36mround progress\033[0m\033[90m ──────────────────────┬─\033[0m\033[0;36m patch status\033[0m\033[90m ─┴─────────────────────┤
  \033[90m│       old round:\033[0m {lastround}\033[90m│\033[0m                                      \033[90m│\033[0m
  \033[90m│ round began at :\033[0m {roundbeganat}\033[90m│\033[0m                                      \033[90m│\033[0m
  \033[90m├─ \033[0m\033[0;36mservive progress\033[0m\033[90m ────────────────────┼─\033[0m\033[0;36m what is this thing?!?\033[0m\033[90m ──────────────┤\033[0m
  \033[90m│     game now :\033[0m {gamestate}         \033[90m│\033[0m                                      \033[90m│\033[0m
  \033[90m│   patch rule :\033[0m blackStab policy       \033[90m│\033[0m                                      \033[90m│\033[0m
  \033[90m│        pcaps :\033[0m do it on your own      \033[90m│\033[0m                                      \033[90m│\033[0m
  \033[90m├─── \033[0m\033[0;36mteam / sla / A / F+ / F- / Status \033[0m\033[90m─┴───────────────┬─\033[0m\033[0;36m brought to you by\033[0m \033[90m──┤\033[0m
  \033[90m│\033[0m\033[31m{team1}\033[0m :{team1t}/{team1sla}/{team1a}/{team1f1}/{team1f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team2}\033[0m :{team2t}/{team2sla}/{team2a}/{team2f1}/{team2f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team3}\033[0m :{team3t}/{team3sla}/{team3a}/{team3f1}/{team3f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m   \033[1m  blackStab \033[0m       \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team4}\033[0m :{team4t}/{team4sla}/{team4a}/{team4f1}/{team4f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team5}\033[0m :{team5t}/{team5sla}/{team5a}/{team5f1}/{team5f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m             fast     \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team6}\033[0m :{team6t}/{team6sla}/{team6a}/{team6f1}/{team6f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m    ︻デ┳═ー  as       \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team7}\033[0m :{team7t}/{team7sla}/{team7a}/{team7f1}/{team7f2}/  \033[31mCode:\033[0m          \033[90m│\033[0m             f*ck     \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team8}\033[0m :{team8t}/{teams8la}/{teamsa}/{teamsf1}/{teamsf2}/  \033[31mCode:\033[0m          \033[90m├──────────────────────┘
  \033[90m└───────────────────────────────────────────────────────┘         \033[90m[IST: \033[0m\033[1;92m21:00\033[0m\033[90m]\033[0m\033[90m
"""
def bloodtime(blood):
	if(path.exists("blood")):
		return(int(open('blood').read()))
	else:
		if(len(blood) == 0):
			return "Notyet"
		else:
			open('blood','w').write(str(int(time())))
			return time()

def setvals( team, template):
	# scr = eval(get("http://localhost:8080/api/scoreboard").text)
	scr = [{'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 1, 'team_score': {'team_id': 1, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}, {'position': 0, 'team_score': {'team_id': 0, 'total_score': 0.0, 'sla': 0.0, 'scores': [{'attack_score': 0.0, 'flag_captured': 0, 'flag_lost': 0, 'sla': 0.0}]}, 'service_states': ['Other']}]
	rounds = eval(get("http://localhost:8080/api/round").text)
	blood = eval(get("http://localhost:8080/api/round").text)
	bloodteam = bloodtime(blood)
	for i in range(len(scr)):
		exec("team{}='{}'".format(i+1,team[scr[i]['team_score']['team_id']]))
		exec("team{}t='{}'".format(i+1, str(scr[i]['team_score']['total_score'])))
		exec("team{}sla='{}'".format(i+1, str(scr[i]['team_score']['scores'][0]['sla'])))
		exec("team{}a='{}'".format(i+1, str(scr[i]['team_score']['scores'][0]['attack_score'])))
		exec("team{}f1='{}'".format(i+1, str(scr[i]['team_score']['scores'][0]['flag_captured'])))
		exec("team{}f2='{}'".format(i+1, str(scr[i]['team_score']['scores'][0]['flag_lost'])))
	from IPython import embed;embed()
	allf1 = [team1f1 , team2f1 , team3f1 , team4f1 , team5f1 , team6f1 , team7f1 , team8f1]
	allf2 = [team1f2 , team2f2 , team3f2 , team4f2 , team5f2 , team6f2 , team7f2 , team8f2]
	alla = [team1a , team2a , team3a , team4a , team5a , team6a , team7a , team8a]
	timefstart = ""
	timefblood = ""
	bloodteam = ""
	timetoend = ""
	roundsdone = str(rounds['round']-1)
	lastround = str(rounds['round']-2)
	totalflags = sum(allf1)
	expteams = len(list(filter(lambda x: (x>0), list(map(lambda x: x if x>0 else 0,alla)))))
	pwnedteams = len(list(filter(lambda x: (x<0), list(map(lambda x: x if x<0 else 0,allf2)))))





	return template


print("\n\n")
while True:
	print("\033[H\033[2J")
	setvals({0:' ', 1:' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' '}, template)
	print("\n\n")
	sleep(1)