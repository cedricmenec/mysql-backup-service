from app import app
from flask import jsonify

from backup.api import api as api_backup


# Blueprints registration
app.register_blueprint(api_backup, url_prefix='/api/backup')


@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


if __name__ == '__main__':
    app.run('0.0.0.0')