from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def populate(data_path: str, repo: AbstractRepository, database_mode: bool):
    reader = GameFileCSVReader(data_path)
    reader.read_csv_file()

    for game in reader.dataset_of_games:
        repo.add_game(game)

    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)

    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)

    if database_mode == False:
        repo.sort_games()
