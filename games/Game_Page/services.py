from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game, Review, User, Wishlist
from games.adapters.repository import AbstractRepository
from flask import redirect


class NonExistentGameException(Exception):
    pass


def get_game(repo: MemoryRepository, game_id):
    game = repo.get_game_by_id(game_id)
    return game


def add_wishlist(game: Game, user: User, repo: AbstractRepository):
    repo.add_wishlist(game, user)

def remove_wishlist(game, user, repo: AbstractRepository):
    repo.remove_wishlist(game, user)
