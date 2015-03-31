from flask import request, jsonify, Blueprint

from porte import oauth_provider

api_module = Blueprint('api', __name__, url_prefix='/api')

@api_module.route('/me')
@oauth_provider.require_oauth('email')
def me():
    user = request.oauth.user
    return jsonify(username=user.username)
