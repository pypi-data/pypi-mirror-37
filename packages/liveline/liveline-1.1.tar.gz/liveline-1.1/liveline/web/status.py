from flask import Blueprint, json


def build_status_blueprint(ll):
    from liveline import LiveLine

    liveline: LiveLine = ll
    status = Blueprint('status', __name__)

    # pylint: disable=W0612
    @status.route('/health')
    def health_check():
        return json.jsonify({'health': 'ok'})

    # pylint: disable=W0612
    @status.route('/')
    def status_check():
        return json.jsonify({
            'running': not liveline.paused
        })

    return status