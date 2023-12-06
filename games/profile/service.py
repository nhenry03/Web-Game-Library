from games.domainmodel.model import User
from games.adapters.repository import AbstractRepository


def get_reviewed_games(repo: AbstractRepository, user: User):
    reviewed_games = repo.get_reviews(user)
    return reviewed_games

def get_wishlist_games(repo: AbstractRepository, user: User):
    wishlist_games = repo.get_wishlist(user)
    return wishlist_games

def get_user(repo: AbstractRepository, user_name: str):
    return repo.get_user(user_name)
