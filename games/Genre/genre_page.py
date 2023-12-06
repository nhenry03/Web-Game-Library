from flask import Blueprint, render_template
import games.adapters.repository as repo
import games.Genre.services as services


genre_blueprint = Blueprint('genre_bp', __name__)

@genre_blueprint.route('/genres')
def displaying_genre():
    genre_urls = services.get_genre_urls(repo.repo_instance)
    genres = services.get_genres(repo.repo_instance)
    genre_numbers = len(genres)
    return render_template(
        'genres.html',
        genre_numbers=genre_numbers,
        genres=genres,
        genre_urls=genre_urls,
    )