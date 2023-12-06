from flask import Blueprint, render_template, redirect, url_for, session, request
from games.authentication.authentication import login_required
from flask_wtf import FlaskForm
from games.review import service as services
from games.adapters import repository as repo
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf

review_blueprint = Blueprint('review_bp', __name__)
@review_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def write_review():
    game_id = request.args.get('game_id')
    user_name = session['user_name']
    form = ReviewForm()

    if form.validate_on_submit():
        services.add_review(int(game_id), form.review.data, int(form.rating.data), user_name, repo.repo_instance)
        return redirect('/game/' + str(game_id))

    if request.method == 'GET':
        form.game_id.data = game_id

    game = services.get_game(repo.repo_instance, int(game_id))
    genres = ""
    for genre in game.genres:
        genres += genre.genre_name + " "
    publisher = game.publisher.publisher_name
    return render_template(
        'game_reviews.html',
        game=game,
        form=form,
        genres=genres,
        publisher=publisher,
        reviews=game.reviews
    )


class ReviewForm(FlaskForm):
    rating = TextAreaField("Rating from 1-5", [
        DataRequired(),
        AnyOf(['1', '2', '3', '4', '5'], 'Please enter a number between 1 and 5')
    ])
    review = TextAreaField("Leave a review", [
        DataRequired(),
        Length(min=1, message='Please leave a valid review')])
    game_id = HiddenField("Game ID")
    submit = SubmitField("Submit")