import requests

URL = "https://livescore-api.com/api-client/scores/live.json?key=Ui1fExCJ0iBWkL5s&secret=pg2U1DmxCTvil2LglNvZl8JlrkhM5mfv&competition_id=244" 

data = requests.get(URL)
data = data.json()
n_matches = len(data['data']['match'])
home_teams = []
away_teams = []
scores = []

matches = data['data']['match']
#print(matches[1]['away_id'])

formatted_scores = []

for i in range(n_matches):
    home_teams.append(matches[i]['home_name'])

for i in range(n_matches):
    away_teams.append(matches[i]['away_name'])

for i in range(n_matches):
    scores.append(matches[i]['score'])

for i in range(n_matches):
    temp = home_teams[i] + " " + scores[i] + " " + away_teams[i] + " "
    formatted_scores.append(temp) 
f =''
for i in range(n_matches):
    f = formatted_scores[i]+ "\n" + f

#for i in range(n_matches):
    