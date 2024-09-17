from django.shortcuts import render, redirect
from datetime import datetime
from random import shuffle

players_list = []
def index(request):
    today = datetime.now()
    is_christmas = "Yes!" if today.month == 12 and today.day == 25 else "No!"
    return render(request, 'christmas/index.html', {'is_christmas': is_christmas})

def get_players():
    return players_list

def validate_players(players):
    if len(players) < 2:
        return 'Add at least two players'
    if len(players) % 2 != 0:
        return 'The number of players must be even'
    return None

def generate_pairs(players):
    shuffled_players = players[:]
    shuffle(shuffled_players)
    pairs = {}
    num_players = len(shuffled_players)
    for i in range(num_players):
        giver = shuffled_players[i]
        receiver = shuffled_players[(i + 1) % num_players]
        pairs[giver] = receiver
    return pairs

def secret_santa_home(request):
    global players_list
    players = get_players()

    if request.method == 'POST':
        name = request.POST.get('name')
        if name and name not in players:
            players.append(name)
            players_list = players
        elif 'generate_pairs' in request.POST:
            error = validate_players(players)
            if error:
                return render(request, 'christmas/santa.html', {'players': players, 'error': error})

            pairs = generate_pairs(players)
            players_list = []

            return render(request, 'christmas/result.html', {'pairs': pairs})

    return render(request, 'christmas/santa.html', {'players': players})
