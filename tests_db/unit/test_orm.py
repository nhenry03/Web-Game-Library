import pytest
from sqlalchemy.exc import IntegrityError
from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist
from tests_db.conftest import empty_session

def insert_user(empty_session, values=None):
    new_name = "hunt123"
    new_password = "Zx123456"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game(empty_session):
    publisher_key = "Curve Games"
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, game_image_url, publisher_name) VALUES'
        "(435790,"
        "'10 Second Ninja X', "
        "0.99, "
        "'Jul 19, 2016', "
        "'xxxx', "
        "'https://cdn.akamai.steamstatic.com/steam/apps/435790/header.jpg?t=1634742090', "
        ":publisher_name)",
        {'publisher_name': publisher_key}
    )
    empty_session.commit()

    # Fetch the primary key of the inserted game and return it
    game_id = empty_session.execute('SELECT game_id FROM games WHERE game_title = "10 Second Ninja X"').fetchone()[0]
    return game_id


def insert_reviews(empty_session):
    user_key = insert_user(empty_session)
    game_key = insert_game(empty_session)
    empty_session.execute(
        'INSERT INTO reviews (user_id, game_id, comment, rating) VALUES'
        '(:user_id, :game_id, "Comment 1", 3)',
        {'user_id': user_key, 'game_id': game_key}
    )
    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]


def insert_wishlist(empty_session):
    user_key = insert_user(empty_session)
    empty_session.execute(
        'INSERT INTO wishlist (user_name) VALUES'
        '(:user_name)',
        {'user_name': user_key}
    )
    row = empty_session.execute('SELECT wishlist_id from wishlist').fetchone()
    return row[0]


def insert_wishlist_game_associations(empty_session, wishlist_key, game_keys):
    stmt = 'INSERT INTO wishlist_game_assoc (wishlist_id, game_id) VALUES (:wishlist_id, :game_id)'
    for game_key in game_keys:
        empty_session.execute(stmt, {'wishlist_id': wishlist_key, 'game_id': game_key})


def insert_game_genre_associations(empty_session, game_key, genre_keys):
    stmt = 'INSERT INTO game_genre (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'game_id': game_key, 'genre_name': genre_key})


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES'
        '("Action"),'
        '("Adventure")'
    )
    rows = list(empty_session.execute('SELECT genre_name from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("hunt123", "Zx123456")
    return user


def maker_game():
    game = Game(435790, "10 Second Ninja X")
    game.price = 0.99
    game.release_date = "Jul 19, 2016"
    game.description = "xxxx"
    game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/435790/header.jpg?t=1634742090"
    game.publisher = Publisher("Curve Games")
    return game


def make_review():
    user = make_user()
    game = maker_game()
    review = Review(user, game, 3, "Comment 1")
    return review


def make_wishlist():
    user = make_user()
    wishlist = Wishlist(user)
    return wishlist


def test_loading_of_users(empty_session):
    users = list()
    users.append(("hunt123", "As19890604"))
    users.append(("hunt234", "Zx123456"))
    insert_users(empty_session, users)

    expected = [
        User("hunt123", "As19890604"),
        User("hunt234", "Zx123456")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("hunt123", "Zx123456")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("hunt123", "As19890604"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("hunt123", "Zx123456")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = maker_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id


def test_loading_of_reviews(empty_session):
    review_key = insert_reviews(empty_session)
    expected_review = make_review()
    fetched_review = empty_session.query(Review).one()

    assert expected_review == fetched_review
    assert review_key == fetched_review.id


def test_loading_of_genres(empty_session):
    genre_keys = insert_genres(empty_session)
    expected_genres = [
        Genre("Action"),
        Genre("Adventure")
    ]
    fetched_genres = empty_session.query(Genre).all()

    assert expected_genres == fetched_genres
    assert genre_keys == tuple(genre.genre_name for genre in fetched_genres)


def test_loading_of_wishlist(empty_session):
    wishlist_key = insert_wishlist(empty_session)
    fetched_wishlist = empty_session.query(Wishlist).one()

    assert wishlist_key == fetched_wishlist.wishlist_id


def test_loading_of_game_genre(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_keys)

    fetched_game = empty_session.query(Game).one()
    fetched_genres = empty_session.query(Genre).all()

    assert fetched_game.genres == fetched_genres


def test_saving_reviews(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    row = empty_session.query(Game).all()
    game = row[0]
    user = empty_session.query(User).filter(User._User__username == "hunt123").one()

    review = Review(user, game, 3, "Comment 1")
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, comment, rating FROM reviews'))
    assert rows == [(user_key, game_key, "Comment 1", 3)]


def test_saving_game(empty_session):
    game = maker_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title FROM games'))
    assert rows == [(435790, "10 Second Ninja X")]


def test_saving_game_genre(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_keys)

    rows = list(empty_session.execute('SELECT game_id, genre_name FROM game_genre'))
    assert rows == [(435790, "Action"), (435790, "Adventure")]


def test_saving_reviewed_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    row = empty_session.query(Game).all()
    game = row[0]
    user = empty_session.query(User).filter(User._User__username == "hunt123").one()

    review = Review(user, game, 3, "Comment 1")
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, comment, rating FROM reviews'))
    assert rows == [(user_key, game_key, "Comment 1", 3)]


def test_saving_wishlist(empty_session):
    wishlist = make_wishlist()
    empty_session.add(wishlist)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name FROM wishlist'))
    assert rows == [("hunt123",)]


def test_saving_wishlist_game_associations(empty_session):
    wishlist_key = insert_wishlist(empty_session)
    game_keys = [insert_game(empty_session)]
    insert_wishlist_game_associations(empty_session, wishlist_key, game_keys)

    rows = list(empty_session.execute('SELECT wishlist_id, game_id FROM wishlist_game_assoc'))
    assert rows == [(wishlist_key, game_keys[0])]




