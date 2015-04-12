from flask import session, request, Blueprint, render_template, jsonify, \
    redirect, url_for
from porte.auth.helpers import current_user
from porte.auth.facebook import views as facebook_views
from porte.auth.email import views as email_views


auth_module = Blueprint('auth', __name__, url_prefix='/auth',
                        template_folder='templates')

auth_module.add_url_rule('/email', 'email_login', email_views.email_login)
auth_module.add_url_rule('/email/register', 'email_register',
                         email_views.email_register)

auth_module.add_url_rule('/facebook', 'facebook', facebook_views.index)
auth_module.add_url_rule('/facebook/callback', 'facebook_callback',
                         facebook_views.facebook_callback)


@auth_module.route('/', methods=['GET'])
def home():
    user = current_user()
    urls = {
        'email': url_for('auth.email_register'),
        'facebook': url_for('auth.facebook'),
        'logout': url_for('auth.logout')
    }
    return render_template('auth/index.html',
                           user=user,
                           urls=urls)


@auth_module.route('/success', methods=['GET'])
def success():
    user = current_user()
    if user:
        return jsonify(user.json())
    return redirect(url_for('auth.home'))


@auth_module.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(request.referrer or url_for('auth.home'))
