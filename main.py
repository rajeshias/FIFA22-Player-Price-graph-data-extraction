from datetime import datetime
import csv
import urllib.request
import json


def convert_time(t):
    return datetime.fromtimestamp(t/1000).strftime('%Y.%m.%d')


def write_sheet(player_name, f, console):
    entry = []
    for index, time in enumerate(file[console]):
        try:
            val = file[console][index][1]
        except IndexError:
            val = 0
        entry.append([convert_time(time[0]), '00:00', val, val, val, val])

    with open(f"{player_name}-{console}.csv", "w") as fp:
        wr = csv.writer(fp, lineterminator='\n')
        wr.writerows(entry)


userInput = -1
while userInput != 0:
    userInput = int(input("What do you want to do?\n1. Search for player\n2. I have a url\n0. Exit\n-->"))
    if userInput == 1:
        search = input("Player Name:").replace(' ', '%20')
        start = urllib.request.Request(f"https://www.futbin.com/search?year=22&extra=1&v=1&term={search}", headers={'User-Agent': 'Mozilla/5.0'})
        data = json.loads(urllib.request.urlopen(start).read())
        try:
            for index, i in enumerate(data):
                print(f"{index + 1}.{i['full_name']}-{i['position']}-({i['version']})-https://www.futbin.com/22/player/{i['id']}")
            player = int(input("choose one:-->")) - 1
        except:
            print("No players found!")
            continue
        playerId = data[player]['image'].split('/')[-1].split('.')[0]
        playerName = data[player]['full_name'].replace(' ', '_')
    else:
        search = input("Enter Player URL:")
        start = urllib.request.Request(search, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(start).read().decode("utf-8")
        playerId = html[html.find("data-player-resource="):].split('"')[1]
        playerName = search.split('/')[-1]

    playerPage = urllib.request.Request(f"https://www.futbin.com/22/playerGraph?type=daily_graph&year=22&player={playerId}&set_id=", headers={'User-Agent': 'Mozilla/5.0'})
    file = json.loads(urllib.request.urlopen(playerPage).read())
    write_sheet(playerName, file, 'pc')
    write_sheet(playerName, file, 'ps')
    write_sheet(playerName, file, 'xbox')
    print('-----------------data created successfully---------------')
