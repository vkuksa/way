from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from way import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True)
    resources = db.relationship('Resource', backref='author', lazy=True)
    test_result = db.relationship('TestResult', backref='participant', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag = db.Column(db.Integer)

    def __repr__(self):
        return f"Article('{self.title}', '{self.date_added}')"


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag = db.Column(db.Integer)

    def __repr__(self):
        return f"Resource('{self.title}', '{self.type}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag('{self.tag_name}')"


class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    E_id = db.Column(db.Integer, default=-1)
    A_id = db.Column(db.Integer, default=-1)
    C_id = db.Column(db.Integer, default=-1)
    N_id = db.Column(db.Integer, default=-1)
    O_id = db.Column(db.Integer, default=-1)

    @classmethod
    def serialize(cls):
        return {'A': {'score': 6, 'count': 2, 'result': 'neutral'}, 'E': {'score': 6, 'count': 2, 'result': 'neutral'},
         'O': {'score': 3, 'count': 1, 'result': 'neutral'}, 'N': {'score': 3, 'count': 1, 'result': 'neutral'},
         'C': {'score': 3, 'count': 1, 'result': 'neutral'}}

    def to_dict(self):
        result = {}
        for X in ['O', 'C', 'E', 'A', 'N']:
            res = DomainResult.query.get(getattr(self, X + '_id'))
            result = {**result, **res.to_dict()}
        return result

    def get_scores(self):
        result = {}
        for X in ['O', 'C', 'E', 'A', 'N']:
            res = DomainResult.query.get(getattr(self, X + '_id'))
            result = {**result, **res.get_score()}
        return result

    def __repr__(self):
        return f"TestResult('{self.user_id}')"


class DomainResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(1), nullable=False)
    score = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    result = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {self.domain: {'score': self.score, 'count': self.count, 'result': self.result}}

    def get_score(self):
        return {self.domain: {'score': self.score}}

    def __repr__(self):
        return f"TestResult('{self.domain}','{self.score}', '{self.count}', '{self.result}')"
