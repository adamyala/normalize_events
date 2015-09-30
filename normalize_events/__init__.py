import config
from flask import Flask, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth
from lib.models import *
from sqlalchemy.sql import select
from lib.feeds.helpers import *
from flask_compress import Compress


app = Flask(__name__, static_url_path="")
Compress(app)
auth = HTTPBasicAuth()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


@auth.get_password
def get_password(username):
    if username == config.USER_NAME:
        return config.PASSWORD
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)


@app.errorhandler(400)
def not_found():
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.route('/v1.0/events', methods=['GET'])
@auth.login_required
def get_events():
    conn = engine.connect()
    query = "SELECT e.id, e.name, e.place, e.date, e.description, e.link, e.address1, e.address2, e.city, e.state, e.zipcode, e.cost, e.created, e.source, string_agg(c.category,',') as category FROM event AS e JOIN eventcategory AS ec ON e.id = ec.event_id JOIN category AS c ON ec.category_id = c.id WHERE e.date >= NOW() GROUP BY 1ORDER BY e.date"
    events = conn.execute(query)
    events = rows_to_dict(events.keys(), events.fetchall())
    events = pretty_events(events)
    return jsonify(events=events), 200


@app.route('/v1.0/events/<int:event_id>', methods=['GET'])
@auth.login_required
def get_event(event_id):
    conn = engine.connect()
    query = "SELECT e.id, e.name, e.place, e.date, e.description, e.link, e.address1, e.address2, e.city, e.state, e.zipcode, e.cost, e.created, e.source, string_agg(c.category,',') as category FROM event AS e JOIN eventcategory AS ec ON e.id = ec.event_id JOIN category AS c ON ec.category_id = c.id WHERE e.date >= NOW() AND e.id = " + str(event_id) + "GROUP BY 1 ORDER BY e.date"
    events = conn.execute(query)
    events = rows_to_dict(events.keys(), events.fetchall())
    if len(events) == 0:
        abort(404)
    events = pretty_events(events)
    return jsonify(events=events), 200


@app.route('/v1.0/eventlogs', methods=['GET'])
@auth.login_required
def get_event_logs():
    conn = engine.connect()
    event_logs = conn.execute(select([eventlog]))
    event_logs = rows_to_dict(event_logs.keys(), event_logs.fetchall())
    if len(event_logs) == 0:
        abort(404)
    return jsonify(event_logs=event_logs), 200

if __name__ == '__main__':
    # app.run(debug = True)
    app.run()
