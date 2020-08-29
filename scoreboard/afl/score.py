from datetime import datetime
from time import time, sleep
from requests import get

START = 1598965200
END = 1598718650
def template():
    scrapi = get("http://localhost:8080/api/scoreboard").text
    roundapi = get("http://localhost:8080/api/round").text
    teamsapi = get("http://localhost:8080/api/teams").text
    roundapi = get("http://localhost/api/round").text
    x="""
                              bi0s internal 28-08-2020 (blackStab)\n"""

    x+="""\n┌─ service milestones ────────────────────────────────────┬─ attack stats ──────┐"""
    x+="""\n│     time in play : 0 days, 0 hrs, 0 min, 12 sec         │  rounds done : 27   │""".format(timediffer(int(time())-START), roundsdone(scrapi, 1))
    x+="""\n│  from firstblood : 0 days, 0 hrs, 0 min, 11 sec         │flags submitted : 4  │""".format(timefirstblood(), fsubmitted(scrapi))
    x+="""\n│  firstblood team : bi0s                                 │ teams pwning : 1    │""".format(fbloodteam(scrapi), teamspwning(scrapi))
    x+="""\n│   time remaining : none seen yet                        │   teams pwned : 0   │""".format(timediffer(END-int(time())), teamspwned(scrapi))
    x+="""\n├─ round progress ─────────────────────────────┬─  status codes ────────────────┤"""
    x+="""\n│       old round: 3 (75.00%)                  │                                │""".format(roundsdone(roundapi,2))
    x+="""\n│ round began at : 0 (0.00%)                   │                                │""".format(roundbegan(roundapi))
    x+="""\n├─ stage progress ─────────────────────────────│                                │"""
    x+="""\n│     game now : team 6                        │                                │"""
    x+="""\n│   patch rule : 180/384 (46.88%)              │                                │"""
    x+="""\n│        pcaps : 55.8k                         │                                │"""
    x+="""\n├───────── total / sla / A / F+ / F- / Status ─┴─────────┬─ brought to you by ──┤"""
    x+="""\n│    team 1 :    /    /     /     /     /  Code:         │ 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥 │""".format()
    x+="""\n│    team 2 :    /    /     /     /     /  Code:         │ 🔥⚡ blackStab ⚡ 🔥 │"""
    x+="""\n│    team 3 :    /    /     /     /     /  Code:         │ 🔥          fast  🔥 │"""
    x+="""\n│    team 4 :    /    /     /     /     /  Code:         │ 🔥           as   🔥 │"""
    x+="""\n│    team 5 :    /    /     /     /     /  Code:         │ 🔥          f*ck  🔥 │"""
    x+="""\n│    team 6 :    /    /     /     /     /  Code:         │ 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥 │"""
    x+="""\n│    team 7 :    /    /     /     /     /  Code:         │ 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥 │"""
    x+="""\n│    team 8 :    /    /     /     /     /  Code:         ├──────────────────────┘"""
    x+="""\n└────────────────────────────────────────────────────────┘  [IST: 21:00]"""#.format(timeinist())
    print(x)

def roundsdone(scrapi, when):
    return eval(scrapi)['round']-when

def timefirstblood():
    return timediffer(int(time()) - int(open("blood").read()))

def fsubmitted(scrapi):
    return sum(list(map(lambda x: x['team_score']['scores'][0]['flag_captured'] , (x for x in eval(scrapi)))))

def teamspwning(scrapi):
    return len(filter((lambda x: x['team_score']['scores'][0]['attack_score'] > 0), (x for x in eval(scrapi))))

def teamspwned(scrapi):
    len(filter((lambda x: x['team_score']['scores'][0]['flag_lost'] > 0), (x for x in eval(scrapi))))

def fbloodteam(bloodapi):
    return eval(bloodapi)[0]['blood'][0]

def roundbegan(roundapi):
    _530 = (5*60)+(30)
    startat=datetime.strptime((eval(roundapi)['start_time'][:-4]), "%Y-%m-%dT%H:%M:%S.%f")
    startmins = startat.minute + (60)*(startat.hour)
    return (lambda x: str(x[0]).rjust(2,"0") + ":" + str(x[1]).rjust(2,"0"))(divmod((startmins) + _530, 60))+":"+str(startat.second).rjust(2,"0") + " IST"

def timediffer(seconds):
    intervals = (('days', 86400),('hrs', 3600),('min', 60),('sec', 1))
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    print(result)
    return ', '.join(result)

def scores(scrapi, teamsapi, position):
    teamname = eval(teamsapi[eval(scrapi)[position]['team_score']['team_id']]['name'])
    totalscore = '{0:.4g}'.format(eval(scrapi)[position]['team_score']['total_score'])
    sla = '{0:.4g}'.format(eval(scrapi)[position]['team_score']['sla'])
    ascore = '{0:.4g}'.format(eval(scrapi)[position]['team_score']['scores'][0]['attack_score'])
    fcaptured = str(eval(scrapi)[position]['team_score']['scores'][0]['flag_captured'])
    flost = str(eval(scrapi)[position]['team_score']['scores'][0]['flag_lost'])

    return [teamname, totalscore, totalscore, sla, ascore, fcaptured, flost]