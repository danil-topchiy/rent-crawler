from flask import Blueprint, render_template, current_app

blueprint = Blueprint('public', __name__)


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def index(path):
    # TODO: delete and move to nginx
    return render_template('index.html')
