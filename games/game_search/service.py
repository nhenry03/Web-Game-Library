import bisect
from typing import List, Union
from games.domainmodel.model import Game, Genre, Publisher
from games.adapters.repository import AbstractRepository, RepositoryException


def get_game(repo: AbstractRepository, game_id: Union[int, str]) -> List[Game]:
    # Ensure game_id is an integer
    try:
        game_id = int(game_id)
    except ValueError:
        return []

    # Use the repository to get the game
    try:
        return repo.get_game_by_id(game_id)
    except RepositoryException:
        return []


def get_genre(repo: AbstractRepository, genre_name: Union[str, List[str]]) -> List[Game]:
    # Ensure genre_name is a list of strings
    if isinstance(genre_name, str):
        genre_name = [genre_name]
    if not all(isinstance(g, str) for g in genre_name):
        return []

    # Handle genres in a different way, using the correct attribute of the Genre class
    try:
        all_games = repo.get_games()
        return [game for game in all_games if any(genre.lower() in map(lambda g: g.genre_name.lower(), game.genres) for genre in genre_name)]
    except RepositoryException:
        return []


def get_publisher(repo: AbstractRepository, publisher_name: str) -> List[Game]:
    # Ensure publisher_name is a string
    if not isinstance(publisher_name, str):
        return []

    # Handle publishers in a different way, using the correct attribute of the Publisher class
    try:
        all_games = repo.get_games()
        return [game for game in all_games if game.publisher.publisher_name.lower() == publisher_name.lower()]
    except RepositoryException:
        return []


def get_all_games(repo: AbstractRepository) -> List[Game]:
    # Use the repository to get all games
    try:
        return repo.get_games()
    except RepositoryException:
        return []


def get_all_genres(repo: AbstractRepository) -> List[Genre]:
    try:
        return repo.get_genres()
    except RepositoryException:
        return []

