import urllib


from flask import Blueprint, json, request


def build_overview_blueprint(ll):
    from liveline import LiveLine

    liveline: LiveLine = ll
    overview = Blueprint('overview', __name__)

    # pylint: disable=W0612
    @overview.route('/')
    def get_overview():
        base_url = request.host_url
        endpoints = {
            'strategies': urllib.parse.urljoin(base_url, '/strategy/'),
            'executions': urllib.parse.urljoin(base_url, '/execution/')
        }
        running = not liveline.paused
        executions = liveline.execution_store.get()
        last_execution_day = sorted([e['day']
                                     for e in executions], reverse=True)
        last_execution_day = last_execution_day[0] if len(last_execution_day) > 0 else ''
        last_executions = [e for e in executions if e['day'] == last_execution_day] 

        # filter out silent executions
        for execution in last_executions:
            execution['executions'] = [e for e in execution['executions'] if len(e['order_placed']) > 0]

        return json.jsonify({
            'running': running,
            'last_executions': last_executions,
            'endpoints': endpoints
        })

    return overview
