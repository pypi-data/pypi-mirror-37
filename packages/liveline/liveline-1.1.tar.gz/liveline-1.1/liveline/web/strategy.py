from flask import Blueprint, json


def build_strategy_blueprint(ll):
    # we have to import LiveLine here because Engine is importing this module,
    # so it will be a circular import if we import LiveLine globally
    from liveline import LiveLine

    liveline: LiveLine = ll
    strategy_bp = Blueprint('strategy', __name__)

    # pylint: disable=W0612
    @strategy_bp.route('/')
    def list_strategies():
        strategies = liveline.get_strategies()
        return json.jsonify(list(strategies.keys()))

    return strategy_bp