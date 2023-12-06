import better_profanity
from flask import Blueprint, render_template, redirect, request, url_for, session
from games.Game_Page import services
from games.app import repo
from games.authentication.authentication import login_required
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, AnyOf
from datetime import datetime
from better_profanity import profanity
from games.domainmodel.model import Wishlist, Review

Game_Page_Blueprint = Blueprint("game_page_bp", __name__)


@Game_Page_Blueprint.route("/game/<game_id>", methods=['GET'])
def game_page(game_id):
    if game_id is None or game_id is '':
        return redirect('/games')
    else:
        game = services.get_game(repo.repo_instance, int(game_id))
        genres = ""
        for genre in game.genres:
            genres += genre.genre_name + " "
        publisher = game.publisher.publisher_name
        average = 0
        divider = 0
        if len(game.reviews) == 0:
            reviews = None
        else:
            reviews = []
            for review in game.reviews:
                if isinstance(review, Review):
                    average += review.rating
                    divider += 1
                    average /= divider
                    reviews.append(review)
        return render_template('gameDescription.html',
                               game=game,
                               genres=genres,
                               publisher=publisher,
                               reviews=reviews,
                               average=average)



@Game_Page_Blueprint.route("/game/<game_id>/add_to_wishlist", methods=['GET', 'POST'])
@login_required
def add_to_wishlist(game_id):
    user_name = session['user_name']
    if game_id is None or game_id is '':
        return redirect('/')
    else:
        if user_name is None:
            return redirect('/login')
        else:
            user = repo.repo_instance.get_user(user_name)
            game = services.get_game(repo.repo_instance, int(game_id))
            services.add_wishlist(game, user, repo.repo_instance)
            return redirect('/game/' + str(game_id))



@Game_Page_Blueprint.route("/game/<game_id>/remove_from_wishlist", methods=['GET', 'POST'])
@login_required
def remove_from_wishlist(game_id):
    user_name = session['user_name']
    if game_id is None or game_id is '':
        return redirect('/')
    else:
        if user_name is None:
            return redirect('/login')
        else:
            user = repo.repo_instance.get_user(user_name)
            game = services.get_game(repo.repo_instance, int(game_id))
            services.remove_wishlist(game, user, repo.repo_instance)
            return redirect('/profile?user_name=' + user_name)


