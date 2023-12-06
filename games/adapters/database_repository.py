from typing import List
import sqlite3
from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from games.adapters.orm import games_table

from games.domainmodel.model import Game, User, Review, Wishlist, Genre, Publisher
from games.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        with self._session_cm as scm:
            try:
                user = scm.session.query(User).filter(User._User__username == user_name).one()
            except NoResultFound:
                pass
        return user

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_games(self) -> List[Game]:
        with self._session_cm as scm:
            return scm.session.query(Game).order_by(asc(Game._Game__game_title)).all()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_genres(self):
        genres = self._session_cm.session.query(Genre).order_by(asc(Genre._Genre__genre_name)).all()
        return genres

    def add_review(self, review: Review, user: User):
        super().add_review(review, user)
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_reviews(self, user):
        reviews = list()
        with self._session_cm as scm:
            reviews = scm.session.query(Review).filter(Review._Review__user == user).all()
        return reviews
    
    def get_game_reviews(self, game):
        reviews = list()
        with self._session_cm as scm:
            reviews = scm.session.query(Review).filter(Review._Review__game == game).all()
        return reviews

    def add_wishlist(self, game: Game, user: User):
        with self._session_cm as scm:
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist__user == user).all()
            if len(wishlist) == 0:
                wishlist = Wishlist(user)
                scm.session.add(wishlist)
                scm.commit()
                wishlist = [wishlist]
            wishlist[0].add_game(game)
            scm.commit()

    def get_wishlist(self, user):
        with self._session_cm as scm:
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist__user == user).first()
            if wishlist:
                game_in_wishlist = wishlist.list_of_games()
            else:
                game_in_wishlist = []

        return game_in_wishlist

    def remove_wishlist(self, game: Game, user: User):
        with self._session_cm as scm:
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist__user == user).first()
            if wishlist and game in wishlist.list_of_games():
                wishlist.remove_game(game)
                scm.commit()

    def get_games_genre_by_id(self, id) -> List[Game]:
        game = list()
        with self._session_cm as scm:
            for game_id in id:
                game.append(scm.session.query(Game).filter(Game._Game__game_id == game_id).one())
        return game

    def get_game_by_id(self, id) -> List[Game]:
        game = None
        with self._session_cm as scm:
            try:
                game = scm.session.query(Game).filter(Game._Game__game_id == id).one()
            except NoResultFound:
                pass
        return game

    def get_number_of_games(self):
        with self._session_cm as scm:
            return scm.session.query(Game).count()

    def get_games_by_game_id(self, id_list):
        games = list()
        with self._session_cm as scm:
            for n in id_list:
                n = int(n)
                game = scm.session.query(Game).filter(Game._Game__game_id == n).one()
                games.append(game)
        return games

    def get_games_id_for_genre(self, genre_name: str):
        game_ids = list()
        with self._session_cm as scm:
            genre = scm.session.query(Genre).filter(Genre._Genre__genre_name == genre_name).one()
            games = scm.session.query(Game).filter(Game._Game__genres.contains(genre)).all()
            sorted_games = sorted(games, key=lambda game: game.title)
            for game in sorted_games:
                game_ids.append(game.game_id)
        return game_ids, len(game_ids)


    def get_games_id(self):
        game_ids = list()
        sorted_game_ids = self.get_games()
        for game in sorted_game_ids:
            game_ids.append(game.game_id)
        return game_ids

    def sort_games(self):
        pass

    def add_publisher(self, publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

