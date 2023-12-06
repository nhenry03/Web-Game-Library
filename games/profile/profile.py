from flask import render_template, Blueprint, request, redirect, url_for, session
import games.profile.service as service
import games.adapters.repository as repo
from games.authentication.authentication import login_required

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_name = request.args.get('user_name')
    user = service.get_user(repo.repo_instance, user_name)
    if user_name is None or user_name == "":
        return redirect(url_for('authentication_bp.login'))
    else:
        review = service.get_reviewed_games(repo.repo_instance, user)
        wishlist = service.get_wishlist_games(repo.repo_instance, user)
        return render_template('profile.html',
                               user=user,
                               review=review,
                               wishlist=wishlist,
                               )

