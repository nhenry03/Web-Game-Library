from sqlalchemy import select, inspect
from games.adapters.orm import metadata
from tests_db.conftest import database_engine

def test_database_populate_inspect_table_names(database_engine):
    # Get all the tables in the database
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genre', 'games', 'genres', 'publishers', 'reviews', 'users', 'wishlist', 'wishlist_game_assoc']

def test_database_populate_select_all_publishers(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # Create a select statement for all columns from the publishers table
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['publisher_name'])

        assert all_publishers[0:4] == ['Activision', 'Beep Games, Inc.', 'Buka Entertainment', 'D3PUBLISHER']


def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # Create a select statement for all columns from the genres table
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])

        assert all_genres[0:4] == ['Action', 'Adventure', 'Casual', 'Indie']


def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        games_tables = select([metadata.tables[name_of_games_table]])
        result = connection.execute(games_tables)

        all_games = []
        for row in result:
            all_games.append(row['game_title'])

        assert all_games[0:4] == ['Xpand Rally', 'Call of Duty® 4: Modern Warfare®', 'Nikopol: Secrets of the Immortals', 'Max Payne']
