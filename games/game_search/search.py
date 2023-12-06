from flask import Blueprint, render_template, request, url_for, redirect
from typing import List, Union
import games.game_search.service as services
import games.adapters.repository as repo
from games.domainmodel.model import Genre
game_search_Blueprint = Blueprint("game_search_bp", __name__)


@game_search_Blueprint.route('/search', methods=['GET', 'POST'])
def show_search():
    search_results = []
    message = None
    unique_publishers = []

    # Use a try-except block to catch any errors during the fetching process
    try:
        all_games = services.get_all_games(repo.repo_instance)
    except:
        all_games = []
        message = "An error occurred while fetching the games."

    try:
        all_genres = services.get_all_genres(repo.repo_instance)
    except:
        all_genres = []
        message = "An error occurred while fetching the games."

    unique_genres = []
    for game in all_games:
        if game.publisher not in unique_publishers:
            unique_publishers.append(game.publisher)

    for genre in all_genres:
        if genre not in unique_genres:
            unique_genres.append(genre)



    if request.method == 'POST':
        query = request.form.get('query', '').lower()
        a_genre = request.form.get('genre', '')
        publisher = request.form.get('publisher', '').lower()
        print(publisher)
        for game in all_games:
            if query and query not in game.title.lower():  # Use dot notation
                continue
            if a_genre and Genre(a_genre) not in game.genres:  # Assume genres are objects with a name attribute
                continue
            if publisher and publisher not in game.publisher.publisher_name.lower():  # Assume publisher is # an object with a name attribute
                continue

            search_results.append(game)

        if not search_results:
            message = 'No games found. (You can click the search without any filters to check all games here.)'

    unique_publishers.sort()
    unique_genres.sort()

    return render_template('search.html', search_results=search_results, unique_genres=unique_genres,
                           unique_publishers=unique_publishers, message=message)
