"""Get bets from Nike.sk. 0th version."""

import datetime
import requests
import pandas as pd

local_path = "v0/"

event_id = 42866077

# load dataframe
df = pd.read_csv(local_path + f'data/{event_id}.csv')

# download data
# url = f"https://api.nike.sk/api/nikeone/v1/boxes/extended/sport-event-id?boxId=bi-137-4-26076&sportEventId={event_id}"
url = f"https://api.nike.sk/api/nikeone/v1/boxes/extended/sport-event-id?sportEventId={event_id}"

r = requests.get(url, verify=True)
downloaded_at = datetime.datetime.now().isoformat()

data = r.json()

# parse data
for bet in data['bets']:
  b = {
    'date': downloaded_at,
    'header': bet['header'],
    'name': bet['participantOrder'],
    'odds_order': bet['oddsOrder'],
  }
  for row in bet['selectionGrid']:
    for r in row:
      if ('odds' in r.keys()):
        bc = b.copy()
        bc['odds_name'] = r['name']
        bc['odds'] = r['odds']
        bc['odds_enabled'] = r['enabled']
        df = pd.concat([df, pd.DataFrame(bc, index=[0])])

df.to_csv(local_path + f'data/{event_id}.csv', index=False)
