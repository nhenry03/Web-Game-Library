from flask import Blueprint, render_template, request, url_for, redirect
import games.games_browsing.service as services
import games.adapters.repository as repo

browse_blueprint = Blueprint('game_bp', __name__)


@browse_blueprint.route('/games', methods=['GET'])
def browse_game_by_id():
    games_per_page = 3
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    game_ids = services.get_games_id(repo.repo_instance)
    games = services.get_games_by_game_id(game_ids[cursor:cursor + games_per_page], repo.repo_instance)

    # Generate urls to display in the prev / next buttons.
    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if cursor > 0:
        prev_game_url = url_for('game_bp.browse_game_by_id', cursor=cursor - games_per_page)
        first_game_url = url_for('game_bp.browse_game_by_id')

    if cursor + games_per_page < len(game_ids):
        next_game_url = url_for('game_bp.browse_game_by_id', cursor=cursor + games_per_page)

        last_cursor = games_per_page * int(len(game_ids) / games_per_page)
        if len(game_ids) % games_per_page == 0:
            last_cursor -= games_per_page
        last_game_url = url_for('game_bp.browse_game_by_id', cursor=last_cursor)

    return render_template('games.html',
                            games=games,
                            first_game_url=first_game_url,
                            last_game_url=last_game_url,
                            prev_game_url=prev_game_url,
                            next_game_url=next_game_url,
                            num_games=len(game_ids),
                            )

@browse_blueprint.route('/games_by_genre', methods=['GET'])
def browse_game_by_genre():
    games_per_page = 3

    genre = request.args.get('genre')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)
    
    game_ids, number_of_games = services.get_games_id_for_genre(genre, repo.repo_instance)

    games = services.get_games_genre_by_id(game_ids[cursor:cursor + games_per_page], repo.repo_instance)

    # Generate urls to display in the prev / next buttons.
    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if cursor > 0:
        prev_game_url = url_for('game_bp.browse_game_by_genre', genre=genre, cursor=cursor - games_per_page)
        first_game_url = url_for('game_bp.browse_game_by_genre', genre=genre)

    if cursor + games_per_page < len(game_ids):
        next_game_url = url_for('game_bp.browse_game_by_genre', genre=genre, cursor=cursor + games_per_page)

        last_cursor = games_per_page * int(len(game_ids) / games_per_page)
        if len(game_ids) % games_per_page == 0:
            last_cursor -= games_per_page
        last_game_url = url_for('game_bp.browse_game_by_genre', genre=genre, cursor=last_cursor)

    return render_template('games.html',
                           genre_name=genre,
                            games=games,
                           first_game_url=first_game_url,
                           last_game_url=last_game_url,
                           prev_game_url=prev_game_url,
                           next_game_url=next_game_url,
                           num_games=number_of_games,
                           )



