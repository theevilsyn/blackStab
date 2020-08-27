from time import sleep

# servicemilestoneswindow = ''.ljust(len("0 days, 0 hrs, 0 min, 11 sec        "))
# attackstatuswindow = ''.ljust(len("27   "))
# roundprogresswindow =  ''.ljust(len("26                   "))
# serviceprogresswindow = ''.ljust(len("planting flags         "))

# teamnames = ''.rjust(len("     black"))
# sla = ''.center(len("         "))
# attackscore, flag+, flag- = ''.center(len("     "))
# statuswindow = ''.ljust("       ")


d="""
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
  \033[90m├─── \033[0m\033[0;36mteam / sla / A / F+ / F- / Status \033[0m\033[90m─┴───────────────┬─\033[0m\033[0;36m brought to you by ──┤\033[0m
  \033[90m│\033[0m\033[31m{team1}\033[0m :{team1sla}/{team1a}/{team1f1}/{team1f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team2}\033[0m :{team2sla}/{team2a}/{team2f1}/{team2f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team3}\033[0m :{team3sla}/{team3a}/{team3f1}/{team3f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m   \033[1m  blackStab \033[0m       \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team4}\033[0m :{team4sla}/{team4a}/{team4f1}/{team4f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m                      \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team5}\033[0m :{team5sla}/{team5a}/{team5f1}/{team5f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m             fast     \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team6}\033[0m :{team6sla}/{team6a}/{team6f1}/{team6f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m    ︻デ┳═ー  as       \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team7}\033[0m :{team7sla}/{team7a}/{team7f1}/{team7f2}/  \033[31mCode:\033[0m        \033[90m│\033[0m             f*ck     \033[90m│\033[0m
  \033[90m│\033[0m\033[31m{team8}\033[0m :{teams8la}/{teamsa}/{teamsf1}/{teamsf2}/  \033[31mCode:\033[0m        \033[90m├──────────────────────┘
  \033[90m└───────────────────────────────────────────────────────┘         \033[90m[IST: \033[0m\033[1;92m21:00\033[0m\033[90m]\033[0m\033[90m
"""
print("\n\n")
while True:
    print("\033[H\033[2J")
    print(d)
    print("\n\n")
    sleep(1)