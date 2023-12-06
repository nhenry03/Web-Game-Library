import abc
from typing import List
from games.domainmodel.model import Game, Review, User, Genre


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message = None):
        print(f'Repository: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def sort_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_wishlist(self, game: Game, user: User):
        raise NotImplementedError

    def get_wishlist(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_id_for_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_genre_by_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review, user: User):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException("Review has no user!")

    @abc.abstractmethod
    def get_games_id(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_game_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, user):
        raise NotImplementedError

    def get_game_reviews(self, game):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_wishlist(self, game: Game, user: User):
        raise NotImplementedError
