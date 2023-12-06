from games.adapters.repository import AbstractRepository
from flask import url_for


def get_genre_urls(repo: AbstractRepository):
    genres = repo.get_genres()
    genres_urls = dict()
    for genre_names in genres:
        name = genre_names.genre_name
        genres_urls[name] = url_for('game_bp.browse_game_by_genre', genre=name)
    return genres_urls

def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    return genres
