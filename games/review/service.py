from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game, Review, User, Wishlist
from games.adapters.repository import AbstractRepository
from flask import redirect

class NonExistentGameException(Exception):
    pass


def add_review(game_id: int, review_text: str, rating:int, user_name: str, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)
    if game is None:
        raise NonExistentGameException
    user = repo.get_user(user_name)
    if user is None:
        return redirect('/login')

    review = Review(user, game, rating, review_text)
    user.add_review(review)
    game.add_review(review)
    repo.add_review(review, user)


def get_game(repo: MemoryRepository, game_id):
    game = repo.get_game_by_id(game_id)
    return game
