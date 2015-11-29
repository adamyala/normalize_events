from config import USERS
from datetime import datetime
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from lib.models import engine, event, category, eventcategory, eventlog, StringAgg
from sqlalchemy.sql import select, expression
from lib.feeds.helpers import rows_to_dict, pretty_events
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
    for user in USERS:
        if username == user['USER_NAME']:
            return user['PASSWORD']
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)


@app.errorhandler(400)
def bad_request(detail):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(detail):
    return make_response(jsonify({'error': 'Not Found'}), 404)


def build_select():
    j = event.join(eventcategory).join(category)
    query = select(
        [
            expression.label('id', event.c.id), expression.label('name', event.c.name),
            expression.label('place', event.c.place), expression.label('date', event.c.date),
            expression.label('description', event.c.description), expression.label('link', event.c.link),
            expression.label('address1', event.c.address1), expression.label('address2', event.c.address2),
            expression.label('city', event.c.city), expression.label('state', event.c.state),
            expression.label('zipcode', event.c.zipcode), expression.label('cost', event.c.cost),
            expression.label('source', event.c.source), expression.label('category', StringAgg(category.c.category)),
            expression.label('created', event.c.created),
        ]
    ).select_from(j).group_by(event.c.id)
    return query


@app.route('/v1.0/events', methods=['GET'])
@auth.login_required
def get_events():
    params = request.args.to_dict()
    conn = engine.connect()
    query = build_select()

    if 'event_id' in params:
        query = query.where(event.c.id == params['event_id'])
    if 'startDate' in params:
        query = query.where(event.c.date >= datetime.strptime(params['startDate'], '%Y-%m-%d'))
    if 'endDate' in params:
        query = query.where(event.c.date <= datetime.strptime(params['endDate'], '%Y-%m-%d'))
    if 'createdDateStart' in params:
        query = query.where(event.c.created >= datetime.strptime(params['createdDateStart'], '%Y-%m-%d'))
    if 'createdDateEnd' in params:
        query = query.where(event.c.created <= datetime.strptime(params['createdDateEnd'], '%Y-%m-%d'))
    if 'city' in params:
        query = query.where(event.c.city == params['city'])

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
