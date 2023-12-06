from flask import Flask
from games.adapters.memory_repository import MemoryRepository
from games.adapters.database_repository import SqlAlchemyRepository
import os
import games.adapters.repository as repo
from games.adapters import repository_populate
from games.adapters.orm import metadata, map_models_to_table

from .games_browsing import layout
from .Game_Page import game_page
from .game_search import search
from .Genre import genre_page
from .authentication import authentication
from .home import home
from .profile import profile
from .review import review


# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

def create_app(test_config=None):

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    else:
        dir_name = os.path.dirname(os.path.abspath(__file__))
        game_file_name = os.path.join(dir_name, "adapters/data/games.csv")
        data_path = game_file_name

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        data_mode = False
        repository_populate.populate(data_path, repo.repo_instance, data_mode)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_models_to_table()
            repository_populate.populate(data_path, repo.repo_instance, True)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_models_to_table()

    with app.app_context():
        app.register_blueprint(layout.browse_blueprint)
        app.register_blueprint(game_page.Game_Page_Blueprint)
        app.register_blueprint(search.game_search_Blueprint)
        app.register_blueprint(genre_page.genre_blueprint)
        app.register_blueprint(authentication.authentication_blueprint)
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(profile.profile_blueprint)
        app.register_blueprint(review.review_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        @app.teardown_appcontext
        def teardown_request(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
