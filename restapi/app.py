from flask import Flask
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

        scheduler.schedule_content(args['datetime'], args['content'])
        return None, 202


api.add_resource(ContentScheduler, '/scheduler/new')

if __name__ == '__main__':
    app.run()
