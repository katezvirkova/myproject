from django.shortcuts import render, redirect
from datetime import datetime
from random import shuffle

def index(request):
    today = datetime.now()
    is_christmas = today.month == 12 and today.day == 25
    return render(request, 'christmas/index.html', {'is_christmas': is_christmas})

def get_players(request):
    return request.session.get('players', [])

def validate_players(players):
    if len(players) < 2:
        return 'Add at least two players'
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
    players = get_players(request)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name and name not in players:
            players.append(name)
            request.session['players'] = players

    return render(request, 'christmas/santa.html', {'players': players})

def generate_pairs_view(request):
    players = get_players(request)
    error = validate_players(players)

    if error:

        return render(request, 'christmas/santa.html', {'players': players, 'error': error})
    pairs = generate_pairs(players)
    request.session['players'] = []

    return render(request, 'christmas/result.html', {'pairs': pairs})
