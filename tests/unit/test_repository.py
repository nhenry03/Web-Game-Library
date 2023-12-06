import pytest
import os
from games.adapters.memory_repository import MemoryRepository, read_data
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Review, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def test_memory_repository_add_game():
    repository = MemoryRepository()
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    repository.add_game(game1)
    repository.add_game(game2)
    assert len(repository.get_games()) == 2
    assert repository.get_games() == [game1, game2]
    game3 = Game(3, "Elden Ring")
    repository.add_game(game3)
    assert len(repository.get_games()) == 3
    assert repository.get_games() == [game1, game2, game3]
    game4 = Game(3, "Elden Ring")
    repository.add_game(game4)
    assert len(repository.get_games()) == 4
    assert repository.get_games() == [game1, game2, game3, game3]
    game5 = "Total War: Medieval"
    repository.add_game(game5)
    assert len(repository.get_games()) == 4
    assert repository.get_games() == [game1, game2, game3, game3]


def test_memory_repository_get_games():
    repository = MemoryRepository()
    assert repository.get_games() == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    repository.add_game(game1)
    repository.add_game(game2)
    assert len(repository.get_games()) == 2
    assert repository.get_games() == [game1, game2]
    game3 = Game(3, "Elden Ring")
    repository.add_game(game3)
    assert len(repository.get_games()) == 3
    assert repository.get_games() == [game1, game2, game3]
    game4 = Game(3, "Elden Ring")
    repository.add_game(game4)
    assert len(repository.get_games()) == 4
    assert repository.get_games() == [game1, game2, game3, game3]
    game5 = "Total War: Medieval"
    repository.add_game(game5)
    assert len(repository.get_games()) == 4
    assert repository.get_games() == [game1, game2, game3, game3]
    repository = MemoryRepository()
    assert repository.get_games() == []


def test_memory_repository_get_number_of_games():
    repository = MemoryRepository()
    game1 = Game(1, "Halo 3")
    repository.add_game(game1)
    assert repository.get_number_of_games() == 1
    game2 = Game(2, "MineCraft")
    repository.add_game(game2)
    assert repository.get_number_of_games() == 2
    game3 = Game(3, "Elden Ring")
    repository.add_game(game3)
    game4 = Game(4, "Dark Souls")
    repository.add_game(game4)
    assert repository.get_number_of_games() == 4
    game5 = "Total War: Medieval"
    repository.add_game(game5)
    assert repository.get_number_of_games() == 4
    repository = MemoryRepository()
    assert repository.get_number_of_games() == 0

def test_get_games_genre_by_id():
    repository = MemoryRepository()
    assert repository.get_games_genre_by_id([1]) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    game1.add_genre(Genre("FPS"))
    game2.add_genre(Genre("Survival"))
    repository.add_game(game2)
    repository.add_game(game1)
    assert repository.get_games_genre_by_id([1, 2]) == [game1, game2]


def test_get_games_id_for_genre():
    repository = MemoryRepository()
    assert repository.get_games_id_for_genre("Action") == ([], 0)
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    game3 = Game(3, "BioShock")
    game1.add_genre(Genre("Action"))
    game2.add_genre(Genre("Adventure"))
    game3.add_genre(Genre("Action"))
    repository.add_game(game2)
    repository.add_game(game1)
    assert repository.get_games_id_for_genre("Action") == ([1], 1)
    assert repository.get_games_id_for_genre("Adventure") == ([2], 1)
    repository.add_game(game3)
    assert repository.get_games_id_for_genre("Action") == ([1, 3], 2)


def test_get_genres():
    repository = MemoryRepository()
    assert len(repository.get_genres()) == 24

def test_get_user():
    repository = MemoryRepository()
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")
    repository.add_user(user1)
    repository.add_user(user2)
    assert repository.get_user("user1") == user1
    assert repository.get_user("user2") == user2
    assert repository.get_user("user3") is None

def test_get_review():
    repo = MemoryRepository()
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "Mass Effect")
    repo.add_user(user1)
    repo.add_user(user2)
    assert repo.get_reviews(user1) == []
    assert repo.get_reviews(user2) == []
    repo.add_game(game1)
    repo.add_game(game2)
    review1 = Review(user1, game1, 2, "mid")
    review2 = Review(user2, game2, 2, "meh")
    user1.add_review(review1)
    user2.add_review(review2)
    game1.reviews.append(review1)
    game2.reviews.append(review1)
    repo.add_review(review1, user1)
    assert repo.get_reviews(user1) == [review1]
    repo.add_review(review2, user2)
    assert repo.get_reviews(user2) == [review2]

def test_get_and_add_wishlist():
    repo = MemoryRepository()
    user = User("user1", "password")
    repo.add_user(user)
    assert repo.get_wishlist(user).list_of_games() == []
    game = Game(1, "Halo 3")
    game2 = Game(2, "Mass Effect")
    repo.add_wishlist(game, user)

    assert repo.get_wishlist(user).list_of_games() == [game]
    repo.add_wishlist(game, user)
    assert repo.get_wishlist(user).list_of_games() == [game]
    repo.add_wishlist(game2, user)
    assert repo.get_wishlist(user).list_of_games() == [game, game2]


