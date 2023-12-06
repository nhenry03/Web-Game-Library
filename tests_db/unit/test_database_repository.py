import pytest
import os
from games.adapters.database_repository import SqlAlchemyRepository, SessionContextManager
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Review, Wishlist, Publisher
from tests_db.conftest import session_factory, empty_session, database_engine

def test_add_and_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Messi', '10101010')
    repo.add_user(user)
    repo.add_user(User("Ronaldo", '7777777'))
    user1 = repo.get_user('messi')
    user2 = repo.get_user('ronaldo')
    assert user1 == user
    assert user2 != user
    user3 = repo.get_user("Tom")
    assert user3 is None


def test_add_and_get_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(1, 'Halo')
    publisher = Publisher('Bungie')
    game.price = 2
    game.release_date = 'Nov 28, 1999'
    game.description = 'A pretty good game'
    game.image_url = 'halo.com'
    game.website_url = 'halo.com'
    game.publisher = publisher
    test = repo.get_game_by_id(1)
    assert test is None
    repo.add_game(game)
    test = repo.get_game_by_id(1)
    assert test == game
    game2 = Game(2, "Call of Duty")
    publisher2 = Publisher('Activision')
    game2.price = 2
    game2.release_date = 'Nov 28, 1999'
    game2.description = 'A pretty ok game'
    game2.image_url = 'cod.com'
    game2.website_url = 'cod.com'
    game2.publisher = publisher2
    test2 = repo.get_game_by_id(2)

    assert test2 != game
    assert test2 is None
    repo.add_game(game2)
    test2 = repo.get_game_by_id(2)
    assert test2 == game2
    test3 = repo.get_game_by_id(7)
    assert test3 is None

def test_get_and_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre("FPS")
    assert genre not in repo.get_genres()
    repo.add_genre(genre)
    assert genre in repo.get_genres()
    genre2 = Genre("Survival Horror")
    repo.add_genre(genre2)
    assert genre2 in repo.get_genres() and genre in repo.get_genres()

def test_get_and_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('Tom123', 'password123')
    repo.reset_session()
    game = Game(1, 'Knack')
    game.price = 2
    game.release_date = 'Nov 28, 1999'
    repo.add_game(game)
    review = Review(user, game, 1, 'mid')
    assert repo.get_game_reviews(game) == []
    repo.add_review(review, user)
    assert repo.get_game_reviews(game) == [review]
    user2 = User("Jamesb", 'passwordinit')
    review2 = Review(user2, game, 1, 'trash')
    repo.add_review(review2, user)
    assert repo.get_game_reviews(game) == [review, review2]
