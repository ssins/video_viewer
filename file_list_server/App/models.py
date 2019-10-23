from flask_sqlalchemy import SQLAlchemy
import datetime
import json

db = SQLAlchemy()
unknown = 'unknown'


# 自定义基类
class base():
    id = db.Column(db.Integer, primary_key=True)
    update_time = db.Column(db.TIMESTAMP, nullable=False)

# 序列化
class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, base):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (
                            datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

class User(db.Model, base):
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    key = db.Column(db.String(255))

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.user_name

