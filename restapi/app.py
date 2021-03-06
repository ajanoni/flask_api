from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from _datetime import datetime
from restapi import scheduler


app = Flask(__name__)
api = Api(app)


class ContentScheduler(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('datetime', type=lambda s: datetime.strptime(s, scheduler.DATETIME_FORMAT),
                            required=True)
        args = parser.parse_args()

        new_id = scheduler.schedule_content(args['datetime'], args['content'])
        return {'id': new_id}, 202


api.add_resource(ContentScheduler, '/scheduler')

if __name__ == '__main__':
    app.run()
