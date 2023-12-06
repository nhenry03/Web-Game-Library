import pytest
import os
from games.domainmodel.model import Game, Publisher, User, Review, Wishlist
from games.Game_Page.services import get_game, add_wishlist
from games.adapters.memory_repository import MemoryRepository
from games.games_browsing.service import *
from games.game_search.service import get_genre, get_publisher
from games.app import create_app
from games.review import service
from games.profile.service import *
from utils import get_project_root


TEST_DATA_PATH = get_project_root() / "tests" / "data" / "games.csv"

def test_get_games_id():
    repository = MemoryRepository()
    assert get_games_id(repository) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    repository.add_game(game1)
    repository.add_game(game2)
    assert get_games_id(repository) == [1, 2]

def test_get_games_by_id():
    repository = MemoryRepository()
    assert get_games_by_game_id([1], repository) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    repository.add_game(game1)
    repository.add_game(game2)
    assert get_games_by_game_id([1, 2], repository) == [{'description': None,
                                                              'game_id': 1,
                                                              'genre': [],
                                                              'image_url': None,
                                                              'price': None,
                                                              'release_date': None,
                                                              'title': 'Halo 3'},
                                                             {'description': None,
                                                              'game_id': 2,
                                                              'genre': [],
                                                              'image_url': None,
                                                              'price': None,
                                                              'release_date': None,
                                                              'title': 'MineCraft'}]

def test_get_game():
    repository = MemoryRepository()
    assert get_game(repository, 1) is None
    game1 = Game(1, "Halo 3")
    repository.add_game(game1)
    assert get_game(repository, 1) == game1

def test_game_to_dict():
    game = Game(1, "Halo 3")
    assert game_to_dict(game) == {'game_id': 1,
                                  'title': 'Halo 3',
                                  'image_url': None,
                                  'description': None,
                                  'release_date': None,
                                  'price': None,
                                  'genre': []
                                  }
    genre1 = Genre("FPS")
    genre2 = Genre("Action")
    game.add_genre(genre1)
    game.add_genre(genre2)
    game.description = "The greatest shooter of all time"
    assert game_to_dict(game) == {'game_id': 1,
                                  'title': 'Halo 3',
                                  'image_url': None,
                                  'description': 'The greatest shooter of all time',
                                  'release_date': None,
                                  'price': None,
                                  'genre': [genre1, genre2]
                                  }


def test_get_games_genre_by_id():
    repository = MemoryRepository()
    assert get_games_genre_by_id([1], repository) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    game1.add_genre(Genre("FPS"))
    game2.add_genre(Genre("Survival"))
    repository.add_game(game1)
    repository.add_game(game2)
    assert get_games_genre_by_id([1, 2], repository) == games_dict_to_list([game1, game2])


def test_get_genre():
    repository = MemoryRepository()
    assert get_genre(repository, ["Action"]) == []
    assert get_genre(repository, [2]) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    game1.add_genre(Genre("FPS"))
    game2.add_genre(Genre("Survival"))
    repository.add_game(game1)
    repository.add_game(game2)
    assert get_genre(repository, ["FPS"]) == [game1]
    assert get_genre(repository, ["Survival"]) == [game2]


def test_get_publisher():
    repository = MemoryRepository()
    assert get_publisher(repository, "Activision") == []
    assert get_publisher(repository, 2) == []
    game1 = Game(1, "Halo 3")
    game2 = Game(2, "MineCraft")
    game1.publisher = Publisher("Microsoft")
    game2.publisher = Publisher("Mojang")
    repository.add_game(game1)
    repository.add_game(game2)
    assert get_publisher(repository, "Microsoft") == [game1]
    assert get_publisher(repository, "Mojang") == [game2]

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False  
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_genres(client):
    first_6_games = [b'10 Second Ninja X', b'A Blind Legend', b'A Journey Through Valhalla', b'ANARCHY', b'ARENA 8', b'Ablockalypse']
    response = client.get('/games_by_genre?genre=Action')
    for i in range(len(first_6_games)):
        if i < 3:
            assert first_6_games[i] in response.data
        else:
            assert first_6_games[i] not in response.data
    response = client.get('games_by_genre?genre=Action&cursor=3')
    for i in range(len(first_6_games)):
        if i >= 3:
            assert first_6_games[i] in response.data
        else:
            assert first_6_games[i] not in response.data


def test_get_user():
    user1 = User("user1", "password")
    assert user1.username == "user1"
    assert user1.password == "password"



