from flask import Blueprint, json


def build_executions_blueprint(ll):
    from liveline import LiveLine

    liveline: LiveLine = ll
    executions = Blueprint('executions', __name__)

    # pylint: disable=W0612
    @executions.route('/')
    def get_all():
        executions = liveline.execution_store.get()
        return json.jsonify(executions)

    return executions