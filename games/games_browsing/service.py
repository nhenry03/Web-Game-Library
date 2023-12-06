from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre
from typing import Iterable


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def game_to_dict(game: Game):
    game_dict = {
        'game_id': game.game_id,
        'title': game.title,
        'image_url': game.image_url,
        'description': game.description,
        'release_date': game.release_date,
        'price': game.price,
        'genre': game.genres
    }
    return game_dict


def games_dict_to_list(games: Iterable[Game]):
    return [game_to_dict(game) for game in games]

def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre': genre.genre_name,
        'games': []
    }
    return genre_dict


def get_games_id_for_genre(genre_name: str, repo: AbstractRepository):
    game_ids = repo.get_games_id_for_genre(genre_name)
    return game_ids

def get_games_genre_by_id(id_list, repo: AbstractRepository):
    games = repo.get_games_genre_by_id(id_list)

    games_as_dict = games_dict_to_list(games)
    return games_as_dict


def get_games_id(repo: AbstractRepository):
    game_ids = repo.get_games_id()
    return game_ids


def get_games_by_game_id(id_list, repo: AbstractRepository):
    games = repo.get_games_by_game_id(id_list)

    games_as_dict = games_dict_to_list(games)
    return games_as_dict
