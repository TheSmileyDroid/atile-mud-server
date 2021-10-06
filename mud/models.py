from atile import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def dict(self):
        return {
            'email': self.email,
            'id': self.id
        }
    
    def __repr__(self) -> str:
        return '<User id={} email={}>'.format(self.id, self.email)


class UserSchema(ma.Schema):
    class Meta():
        fields = ('id','email', 'characters')
    
    characters = ma.Function(lambda obj: list(map( lambda obj: obj.dict(), obj.characters)))

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
        backref=db.backref('characters', lazy=True))

    def dict(self):
        return {
            'name': self.name,
            'id': self.id,
        }

    def __repr__(self) -> str:
        return '<Character name={} id={} user_id={}>'.format(self.name, self.id, self.user_id)

class CharacterSchema(ma.Schema):
    class Meta():
        fields = ('id', 'name', 'user')
    
    user = ma.Function(lambda obj: obj.user.dict())


user_schema = UserSchema()
users_schema = UserSchema(many=True)
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)