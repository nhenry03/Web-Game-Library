import os
from typing import List
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import Game, User, Review, Wishlist, Genre
from games.adapters.repository import AbstractRepository
import bisect


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__games_index = dict()
        self.__users = list()
        self.__sorted_list = dict()
        self.__id = list()
        self.__reviews = dict()
        self.__wishlists = dict()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            self.__games.append(game)
            self.__games_index[game.game_id] = game
            self.__sorted_list[game.title] = game
            self.__id = [game.game_id for game in self.__games]

    def sort_games(self):
        sorted_list = dict(sorted(self.__sorted_list.items()))
        sorted_list = list(sorted_list.values())
        self.__id = [game.game_id for game in sorted_list]
        sorted_dict = {key: self.__games_index[key] for key in self.__id}
        self.__games_index = sorted_dict
        self.__games = sorted_list

    def get_games(self) -> List[Game]:
        return self.__games

    def add_wishlist(self, game: Game, user: User):
        if user.username not in self.__wishlists.keys():
            self.__wishlists[user.username] = Wishlist(user)
            self.__wishlists[user.username].add_game(game)
        else:
            self.__wishlists[user.username].add_game(game)

    def remove_wishlist(self, game: Game, user: User):
        self.__wishlists[user.username].remove_game(game)

    def get_wishlist(self, user):
        if user.username not in self.__wishlists.keys():
            self.__wishlists[user.username] = Wishlist(user)
        return self.__wishlists[user.username]

    def get_number_of_games(self):
        return len(self.__games)

    def get_game_by_id(self, id) -> List[Game]:
        target_game = Game(game_id=id, game_title=None)
        for game in self.__games:
            if game.game_id == id:
                return game

    def game_index(self, target_game: Game):
        index = self.__id.index(target_game.game_id)
        if index != len(self.__games) and self.__games[index].game_id == target_game.game_id:
            return index
        raise ValueError

    def get_games_genre_by_id(self, id_list):
        existing_id = [id for id in id_list if id in self.__games_index]
        games = [self.__games_index[id] for id in existing_id]
        return games

    def get_games_id_for_genre(self, genre_name: str):
        data = read_data()
        data.read_csv_file()
        genres = [genre for genre in data.dataset_of_genres if genre.genre_name == genre_name]
        game_ids = []
        if genres is not None:
            for game in self.get_games():
                for genre in genres:
                    if genre in game.genres:
                        game_ids.append(game.game_id)
        return game_ids, len(game_ids)

    def get_genres(self):
        data = read_data()
        data.read_csv_file()
        genre_list = []
        for genres in data.dataset_of_genres:
            bisect.insort_left(genre_list, genres)
        return genre_list

    def add_user(self, user: User):
        self.__users.append(user)
    def get_user(self, user_name):
        return next((user for user in self.__users if user.username == user_name), None)

    def add_review(self, review: Review, user: User):
        super().add_review(review, user)
        if user not in self.__reviews.keys():
            self.__reviews[user.username] = [review]
        else:
            self.__reviews[user.username] += [review]

    def get_reviews(self, user) -> [Review]:
        if user in self.__users:
            return user.reviews

    def get_games_id(self):
        return self.__id

    def get_games_by_game_id(self, id_list):
        existing_id = [id for id in id_list if id in self.__games_index]
        games = [self.__games_index[id] for id in existing_id]
        return games

    def add_genre(self, genre: Genre):
        pass

    def add_publisher(self, publisher):
        pass


def read_data():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    game_file_name = os.path.join(dir_name, "data/games.csv")
    data = GameFileCSVReader(game_file_name)
    return data








