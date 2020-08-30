from os import path
from datetime import datetime
from time import time, sleep
from requests import get

START = 1598706000
END = 1598734800
def template():
    scrapi = get("http://localhost:8080/api/scoreboard").text
    roundapi = get("http://localhost:8080/api/round").text
    teamsapi = get("http://localhost:8080/api/teams").text
    roundapi = get("http://localhost:8080/api/round").text
    x="""
                             \x1b[1;93mbi0s internal \x1b[1;96m28-08-2020 \x1b[1;92m(blackStab)\n"""

    x+="""\n    \x1b[1;90m┌─\x1b[0;36m service milestones \x1b[1;90m────────────────────────────────────┬─ \x1b[0;36mattack stats \x1b[1;90m──────┐"""
    x+="""\n    \x1b[1;90m│     time in play : \x1b[37m{}\x1b[1;90m│    rounds done :\x1b[0;37m{}\x1b[1;90m│""".format(timediffer(int(time())-START), roundsdone(roundapi, 1))
    x+="""\n    \x1b[1;90m│  from firstblood : \x1b[37m{}\x1b[1;90m│flags submitted :\x1b[0;37m{}\x1b[1;90m│""".format(timefirstblood(), fsubmitted(scrapi))
    x+="""\n    \x1b[1;90m│  firstblood team : \x1b[37m{}\x1b[1;90m│   teams pwning :\x1b[31m{}\x1b[1;90m│""".format(fbloodteam(scrapi), teamspwning(scrapi))
    x+="""\n    \x1b[1;90m│   time remaining : \x1b[37m{}\x1b[1;90m│    teams pwned :\x1b[37m{}\x1b[1;90m│""".format(timediffer(END-int(time())), teamspwned(scrapi))
    x+="""\n    \x1b[1;90m├─ \x1b[0;36mround progress \x1b[1;90m─────────────────────────────┬─ \x1b[0;36mstatus codes\x1b[1;90m ─────────────────┤"""
    x+="""\n    \x1b[1;90m│       old round: \x1b[37m{}\x1b[1;90m│                                │""".format(roundsdone(roundapi,2))
    x+="""\n    \x1b[1;90m│ round began at : \x1b[37m{}\x1b[1;90m│                                │""".format(roundbegan(roundapi))
    x+="""\n    \x1b[1;90m├─ \x1b[0;36mstage progress \x1b[1;90m─────────────────────────────│                                │"""
    x+="""\n    \x1b[1;90m│     game now : \x1b[37mno data\x1b[1;90m                       │                                │"""
    x+="""\n    \x1b[1;90m│   patch rule : \x1b[37mblackStab policy\x1b[1;90m              │                                │"""
    x+="""\n    \x1b[1;90m│        pcaps : \x1b[37mwe're not providing those\x1b[1;90m     │                                │"""
    x+="""\n    \x1b[1;90m├───────── \x1b[32mtotal \x1b[90m/\x1b[32m sla \x1b[90m/ \x1b[32mattack \x1b[90m/ \x1b[32mflg+ \x1b[90m/ \x1b[32mflg-  \x1b[1;90m┴─────────┬─\x1b[0;36m brought to you by\x1b[1;90m ──┤"""
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │                      │""".format(**(scores(scrapi, teamsapi, 0)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │   ⚡ blackStab ⚡    │""".format(**(scores(scrapi, teamsapi, 1)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │                      │""".format(**(scores(scrapi, teamsapi, 2)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │             fast     │""".format(**(scores(scrapi, teamsapi, 3)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │   🔥         as      │""".format(**(scores(scrapi, teamsapi, 4)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │     🔥      f*ck     │""".format(**(scores(scrapi, teamsapi, 5)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     │       🔥             │""".format(**(scores(scrapi, teamsapi, 6)))
    x+="""\n    \x1b[1;90m│\x1b[0;31m{team}\x1b[90m:{total}/{sla}/{attack}/{fcap}/{flost}/  \x1b[32mcode:\x1b[1;90m     ├──────────────────────┘""".format(**(scores(scrapi, teamsapi, 7)))
    x+="""\n    \x1b[1;90m└────────────────────────────────────────────────────────┘  [IST: 21:00]"""#.format(timeinist())
    print(x+"\n\n")

def roundsdone(roundapi, when):
    return str((eval(roundapi)['round']-when)).rjust(4) if when==1 else str((eval(roundapi)['round']-when)).ljust(28)

def timefirstblood():
    return timediffer(int(time()) - int(open("blood").read())) if path.exists("blood") else "No one has seen it yet".ljust(37)

def fsubmitted(scrapi):
    return str(sum(list(map(lambda x: x['team_score']['scores'][0]['flag_captured'] , (x for x in eval(scrapi)))))).center(4)

def teamspwning(scrapi):
    return str(len(list(filter((lambda x: x['team_score']['scores'][0]['attack_score'] > 0), (x for x in eval(scrapi)))))).center(4)

def teamspwned(scrapi):
    return str(len(list(filter((lambda x: x['team_score']['scores'][0]['flag_lost'] > 0), (x for x in eval(scrapi)))))).center(4)

def fbloodteam(bloodapi):
    return eval(bloodapi)[0]['blood'][0].ljust(37) if path.exists("blood") else "No one has seen yet".ljust(37)

def roundbegan(roundapi):
    _530 = (5*60)+(30)
    startat=datetime.strptime((eval(roundapi)['start_time'][:-4]), "%Y-%m-%dT%H:%M:%S.%f")
    startmins = startat.minute + (60)*(startat.hour)
    return ((lambda x: str(x[0]%24).rjust(2,"0") + ":" + str(x[1]).rjust(2,"0"))(divmod((startmins) + _530, 60))+":"+str(startat.second).rjust(2,"0") + " IST").ljust(28)

def timediffer(seconds):
    intervals = (('days', 86400),('hrs', 3600),('min', 60),('sec', 1))
    result = []
    for name, count in intervals:
        value = seconds // count
        seconds -= value * count
        if value == 1:
            name = name.rstrip('s')
        result.append("{} {}".format(int(value), name))
    # print(result)
    return ', '.join(result).ljust(37)

def scores(scrapi, teamsapi, position):
    teamname = eval(teamsapi)[ eval(scrapi)[position]['team_score']['team_id']]['name']
    totalscore = '{0:.3g}'.format(eval(scrapi)[position]['team_score']['total_score'])
    sla = str(eval(scrapi)[position]['team_score']['sla'])[:4]
    ascore = str(eval(scrapi)[position]['team_score']['scores'][0]['attack_score'])[:4]
    fcaptured = str(eval(scrapi)[position]['team_score']['scores'][0]['flag_captured'])
    flost = str(eval(scrapi)[position]['team_score']['scores'][0]['flag_lost'])

    return {"team": teamname.rjust(10), "total":totalscore.center(6), "sla": sla.center(6), "attack": ascore.center(6), "fcap": fcaptured.center(5), "flost": flost.center(5)}

def main():
    while True:
        print("\033[H\033[2J\033[25l")
        template()
        sleep(0.3)

if __name__ == '__main__':
    main()
